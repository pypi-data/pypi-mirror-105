"""Rundeckpy CLI."""
import logging
from pathlib import Path
import click
from .rd_plugin import PluginStructure

logger = logging.getLogger(__name__)
# pylint: disable=too-many-arguments

@click.group()
def cli() -> None:
    """RundeckPy version 0.2  """


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--all",
    "all_plugins",
    is_flag=True,
    help="Path is a folder with multiple plugin folders. Validate all.",
)
def validate(path, all_plugins) -> None:
    """Validate plugin in a given path"""
    print("Plugin Validation:\n")
    if all_plugins:
        folders = Path(path).glob("*")
        folder_names = [x.name for x in folders if x.is_dir()]
        for folder in folder_names:
            print(folder)
            try:
                plugin = PluginStructure(f"{path}/{folder}")
                plugin.validate()
            except SystemExit as error:
                print(error)
            print("")
    else:
        plugin = PluginStructure(path)
        plugin.validate()
    print("")


@cli.group()
def install() -> None:
    """Install plugin from a given path."""


@install.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--all",
    "all_plugins",
    is_flag=True,
    help="Path is a folder with multiple plugin folders. Install all.",
)
@click.option(
    "--libext-path",
    "libext_path",
    default="",
    help="Path for Rundeck plugins folder libext (including /libext)",
)
def local(path, all_plugins, libext_path) -> None:
    """Install plugin from a given path in local file system"""
    rd_plugins = Path("/home/rundeck/libext")
    if Path("/var/lib/rundeck/libext").is_dir():
        rd_plugins = Path("/var/lib/rundeck/libext")
    if libext_path:
        rd_plugins = Path(libext_path)
    if all_plugins:
        folders = Path(path).glob("*")
        folder_names = [x.name for x in folders if x.is_dir()]
        for folder in folder_names:
            print(path + folder)
            try:
                plugin = PluginStructure(f"{path}/{folder}")
                plugin.validate()
                plugin.install_local(rd_plugins)
            except SystemExit as error:
                print(error)
        print("")
    else:
        plugin = PluginStructure(path)
        plugin.validate()
        plugin.install_local(rd_plugins)


@install.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--all",
    "all_plugins",
    is_flag=True,
    help="Path is a folder with multiple plugin folders. Install all.",
)
@click.option(
    "--libext-path",
    "libext_path",
    default="",
    help="Path for Rundeck plugins folder libext (including /libext)",
)
@click.option("--server")
@click.option("--user", prompt=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=False)
def remote(path, all_plugins, server, libext_path, user, password) -> None:
    """Install plugin from a given path in a remote server"""
    if all_plugins:
        folders = Path(path).glob("*")
        folder_names = [x.name for x in folders if x.is_dir()]
        for folder in folder_names:
            print(path + folder)
            try:
                plugin = PluginStructure(f"{path}/{folder}")
                plugin.validate()
                plugin.install_remote(libext_path, server, user, password)
            except SystemExit as error:
                print(error)
            print("")
    else:
        plugin = PluginStructure(path)
        plugin.validate()
        plugin.install_remote(libext_path, server, user, password)
