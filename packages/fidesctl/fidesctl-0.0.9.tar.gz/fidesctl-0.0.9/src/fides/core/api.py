"""Logic to make calling the API smoother across different modules."""
import json
from typing import Dict, Any

import requests

from .utils import load_yaml_into_dict


def generate_request_headers() -> Dict[str, Any]:
    """
    Generate the headers for a request.
    """
    return {"Content-Type": "application/json", "user-id": "1"}


def generate_object_url(
    url: str, object_type: str = "", object_id: str = "", version: str = "v1"
):
    """
    Generate an object's URL using a base url, the object type and a version.
    """
    return f"{url}/{version}/{object_type}/{object_id}"


def get(url: str, object_type: str, object_id: str) -> requests.Response:
    """
    Get a specific object by its id.
    """
    object_url = generate_object_url(url, object_type, object_id)
    headers = generate_request_headers()
    return requests.get(object_url, headers=headers)


def create(
    url: str, object_type: str, object_manifest: Dict[str, Any]
) -> requests.Response:
    """
    Create a new object.
    """
    payload = json.dumps(object_manifest)
    object_url = generate_object_url(url, object_type)
    headers = generate_request_headers()
    return requests.post(object_url, headers=headers, data=payload)


def connect(url: str):
    """
    Pings the Server on the base url to make sure its available.
    """
    return requests.get(url)


def delete(url: str, object_type: str, object_id: str) -> requests.Response:
    """
    Delete an object by its id.
    """
    object_url = generate_object_url(url, object_type, object_id)
    headers = generate_request_headers()
    return requests.delete(object_url, headers=headers)


def show(url: str, object_type: str) -> requests.Response:
    """
    Get a list of all of the existing objects of a certain type.
    """
    object_url = generate_object_url(url, object_type)
    headers = generate_request_headers()
    return requests.get(object_url, headers=headers)


def update(
    url: str, object_type: str, object_id: str, object_manifest: Dict[str, Any]
) -> requests.Response:
    """
    Update an existing object.
    """
    object_url = generate_object_url(url, object_type, object_id)
    payload = json.dumps(object_manifest)
    headers = generate_request_headers()
    return requests.post(object_url, headers=headers, data=payload)


def rate(url: str, object_id: str, object_manifest: str) -> requests.Response:
    """
    Submit a system(s) for rating.
    """
    url = f"{url}rate/{object_id}"
    payload = json.dumps(object_manifest)
    headers = generate_request_headers()
    return requests.post(url, headers=headers, data=payload)


def validate(url: str, manifest_path: str) -> requests.Response:
    """
    Validate that a system manifest is valid.
    """
    manifest = load_yaml_into_dict(manifest_path)
    payload = json.dumps(manifest)
    headers = generate_request_headers()
    url = f"{url}/validateForCreate"
    return requests.post(url, headers=headers, data=payload)
