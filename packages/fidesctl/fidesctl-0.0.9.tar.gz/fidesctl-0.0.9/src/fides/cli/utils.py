"""Contains reusable utils for the CLI commands."""
import json
import os
from typing import Dict, Any

import click
import requests

# A mapping of object names to their Endpoints
ENDPOINT_DICT = {
    "data-category": "data-category",
    "data-qualifier": "data-qualifier",
    "dataset": "dataset",
    "data-subject-category": "data-subject-category",
    "data-use": "data-use",
    "organization": "organization",
    "policy": "policy",
    "policy-rule": "policy-rule",
    "registry": "registry",
    "system": "system",
    "user": "user",
}
ENDPOINT_LIST = [value for key, value in ENDPOINT_DICT.items()]


def pretty_echo(dict_object: Dict[Any, Any], color: str = "white") -> None:
    """
    Given a dict-like object and a color, pretty click echo it.
    """
    click.secho(json.dumps(dict_object, indent=2), fg=color)


def handle_response(response: requests.Response) -> requests.Response:
    """viewable CLI response"""
    if response.status_code == 200:
        pretty_echo(response.json(), "green")
    else:
        pretty_echo(response.json(), "red")
    return response


def url_option(command):
    """
    Apply the url option.
    """
    command = click.option(
        "--url",
        "-u",
        "url",
        default=lambda: os.getenv("FIDES_SERVER_URL", ""),
        help="URL of the Fides Server",
    )(command)
    return command


def object_type_argument(command):
    """
    Apply the object_type option.
    """
    command = click.argument(
        "object_type", type=click.Choice(ENDPOINT_LIST, case_sensitive=False)
    )(command)
    return command


def manifest_option(command):
    """
    Apply the manifest option.
    """
    command = click.option(
        "--manifest",
        "-m",
        "manifest",
        required=True,
        type=click.Path(exists=True),
        help="Path to the manifest file",
    )(command)
    return command


def id_argument(command):
    """
    Apply the id argument.
    """
    command = click.argument(
        "object_id",
        type=str,
    )(command)
    return command
