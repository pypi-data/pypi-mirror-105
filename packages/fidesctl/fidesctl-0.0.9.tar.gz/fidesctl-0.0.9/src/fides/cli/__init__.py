"""Contains all of the commands for the Fides CLI."""
import json

import click
from click.decorators import version_option

from fides.core import api as _api
from fides.core import commands as _commands
from fides.core import generate_dataset as _generate_dataset

from .utils import (
    url_option,
    manifest_option,
    id_argument,
    object_type_argument,
    handle_response,
)

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(prog_name="fides-cli")
def cli():
    """
    The Fides CLI for managing Fides systems.
    """


####################
### Generic Commands
####################
@cli.command()
@url_option
@object_type_argument
@manifest_option
def create(url: str, object_type: str, manifest: str):
    """
    Create a new object.
    """
    parsed_manifest = json.loads(manifest)
    handle_response(_api.create(url, object_type, parsed_manifest))


@cli.command()
@url_option
@object_type_argument
@id_argument
def delete(url: str, object_type: str, object_id: str):
    """
    Delete an object.
    """
    handle_response(_api.delete(url, object_type, object_id))


@cli.command()
@url_option
@object_type_argument
@id_argument
def get(url: str, object_type: str, object_id: str):
    """
    Get an object by its id.
    """
    handle_response(_api.get(url, object_type, object_id))


@cli.command()
@url_option
@object_type_argument
def show(url: str, object_type: str):
    """
    List all of the exiting objects of a certain type.
    """
    handle_response(_api.show(url, object_type))


@cli.command()
@url_option
@manifest_option
@object_type_argument
@id_argument
def update(url: str, object_type: str, object_id: str, manifest: str):
    """
    Update an existing object.
    """
    parsed_manifest = json.loads(manifest)
    handle_response(_api.update(url, object_type, object_id, parsed_manifest))


#########
### Special Commands
#########
@cli.command()
@url_option
@click.argument("manifest_dir", type=click.Path())
def apply(url: str, manifest_dir: str):
    """
    Update the state of database to match the state of the
    applied files.

    Args:

        manifest_dir (str): A path to a directory that contains only Fides manifest files.
    """
    _commands.apply(url, manifest_dir)


@cli.command()
@url_option
def audit_log(url):
    """
    Show the full audit-log.
    """
    _api.show(url, "audit_log")


@cli.command()
@url_option
def connect(url: str):
    """
    Ping the Server.
    """
    click.secho(f"Pinging {url}...", fg="green")
    _api.connect(url)
    click.secho("Connection Successful!", fg="green")


@cli.command()
@click.argument("connection_string", type=str)
@click.argument("output_filename", type=str)
def generate_dataset(connection_string, output_filename):
    """
    Generates a dataset manifest from a database.

    Args:

        connection_string (str): A SQLAlchemy-compatible connection string

        output_filename (str): A path to where the manifest will be written
    """
    _generate_dataset.generate_dataset(connection_string, output_filename)


@cli.command()
@url_option
@click.argument("manifest_dir", type=click.Path())
@click.argument("policy_id", type=str)
@click.argument("system_key", type=str, default="")
def rate(url: str, manifest_dir: str, policy_id: str, system_key: str):
    """
    Rate a system for approval or denial without formally creating it.

    Requires a path to a manifest as well as a Policy ID for rating
    and optionally a specific fidesKey to rate a particular system.
    """
    _commands.rate(url, manifest_dir, policy_id, system_key)


@cli.command()
@url_option
@click.argument("manifest_dir", type=click.Path())
def validate(url: str, manifest_dir: str):
    """
    Test a system's validity without submitting it.
    """
    _commands.validate()
