"""This module handles the logic required for non-direct API commands."""
import os
from functools import reduce
from typing import Any, Dict, List, Tuple, Set

from fides.cli.utils import pretty_echo
from fides.core import api as _api
from .utils import load_yaml_into_dict, echo_green


def union_manifests(manifests: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
    """
    Combine all of the manifests into a single dictionary,
    appending object values with the same keys.
    """

    key_lists: List[List[str]] = [list(manifest.keys()) for manifest in manifests]
    key_set: Set[str] = set(reduce(lambda x, y: [*x, *y], key_lists))

    unioned_dict: Dict[str, List] = {}
    for manifest in manifests:
        for key in key_set:
            if key in manifest.keys() and key in unioned_dict.keys():
                unioned_dict[key] += manifest[key]
            elif key in manifest.keys():
                unioned_dict[key] = manifest[key]
    return unioned_dict


def ingest_manifests(manifests_dir: str) -> Dict[str, List[Dict]]:
    """
    Ingest all of the manifests available in a directory and concatenate
    them into a single object.
    """
    manifest_list = [
        manifests_dir + "/" + file
        for file in os.listdir(manifests_dir)
        if "." in file and file.split(".")[1] in ["yml", "yaml"]
    ]
    loaded_manifests = [load_yaml_into_dict(file) for file in manifest_list]
    unioned_manifests = union_manifests(loaded_manifests)
    return unioned_manifests


def get_server_key_pairs(server_object_list: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Get a list of all of the objects of a certain type from the server.
    """
    server_object_key_pairs = {
        _object["fidesKey"]: _object["id"] for _object in server_object_list
    }
    return server_object_key_pairs


def check_create_or_update(
    manifest_object_list: List[Dict[str, Any]], server_object_key_pairs: Dict[str, str]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Check if each object exists in the object_list. If it exists,
    put it in a queue for updating, otherwise put it in a queue for creation.
    """

    update_list = []
    create_list = []
    for _object in manifest_object_list:
        object_key = _object["fidesKey"]
        if object_key in server_object_key_pairs.keys():
            server_object_id = server_object_key_pairs[object_key]
            update_list.append(
                {"server_object_id": server_object_id, "object": _object}
            )
        else:
            create_list.append(_object)
    return create_list, update_list


def apply(url: str, manifests_dir: str):
    """
    Compose functions to apply file changes to the server.
    """

    manifests = ingest_manifests(manifests_dir)

    create_or_update_exclude = ["system", "version"]
    filtered_manifests = {
        key: value
        for key, value in manifests.items()
        if key not in create_or_update_exclude
    }

    for object_type, manifest_object_list in filtered_manifests.items():
        server_object_list = _api.show(url, object_type).json()["data"]
        server_object_key_pairs = get_server_key_pairs(server_object_list)
        create_list, update_list = check_create_or_update(
            manifest_object_list, server_object_key_pairs
        )
        for _object in create_list:
            _api.create(url, object_type, _object)
            echo_green(
                "Created {} object with fidesKey: {}".format(
                    object_type, _object["fidesKey"]
                ),
            )
        for _object in update_list:
            _api.update(
                url=url,
                object_type=object_type,
                object_id=_object["server_object_id"],
                object_manifest=_object["object"],
            )
            echo_green(
                "Updated {} object with fidesKey: {} and ID: {}".format(
                    object_type,
                    _object["object"]["fidesKey"],
                    _object["server_object_id"],
                ),
            )


def rate(url: str, manifests_dir: str, policy_id: str, system_key: str):
    """
    Rate a system against a specific policy without side-effects.
    """

    system_manifests = ingest_manifests(manifests_dir)["system"]
    object_url = _api.generate_object_url(url, "system")

    for system in system_manifests:
        rating_response = _api.rate(object_url, policy_id, system)
        print(rating_response.text)
        rating_data = rating_response.json()["data"]
        echo_green(
            f"Rated system with fidesKey: {system['fidesKey']} against Policy ID: {policy_id}",
        )
        if rating_response["status"] != "PASS":
            pretty_echo(rating_data, "red")
        else:
            pretty_echo(rating_data, "green")


def validate():
    """
    Validate that a system file is able to be created.
    """
