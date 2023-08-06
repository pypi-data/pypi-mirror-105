"""Utils to help with API calls."""
import logging
from functools import partial
from json.decoder import JSONDecodeError
from typing import Dict, Any

import click
import requests
import sqlalchemy
import yaml
from sqlalchemy.engine import Engine

logger = logging.getLogger("server_api")

echo_red = partial(click.secho, fg="red", bold=True)
echo_green = partial(click.secho, fg="green", bold=True)


def load_yaml_into_dict(file_path: str) -> Dict[Any, Any]:
    """
    This loads yaml files into a dictionary to be used in API calls.
    """
    with open(file_path, "r") as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.FullLoader)


def check_response(response: requests.Response) -> requests.Response:
    """
    Check that a response has valid JSON.
    """

    try:
        response.json()
    except JSONDecodeError as json_error:
        logger.error(response.status_code)
        logger.error(response.text)
        raise json_error
    else:
        return response


def get_db_engine(connection_string: str) -> Engine:
    """
    Use SQLAlchemy to create a DB engine.
    """
    try:
        engine = sqlalchemy.create_engine(connection_string)
    except Exception as err:
        echo_red("Failed to create engine!")
        raise SystemExit(err)

    try:
        with engine.begin() as connection:
            connection.execute("SELECT 1")
    except Exception as err:
        echo_red(f"Database connection failed with engine:\n{engine}!")
        raise SystemExit(err)
    return engine


def write_manifest(file_name: str, manifest: Dict):
    """
    Write a Python dict out to a yaml file.
    """
    with open(file_name, "w") as manifest_file:
        yaml.dump(manifest, manifest_file, sort_keys=False, indent=2)
