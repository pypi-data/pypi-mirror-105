"""Class for python plugin and files structure"""

import sys
import logging
import zipfile
import tempfile
from pathlib import Path
import paramiko

logger = logging.getLogger(__name__)


class PluginStructure:
    """Class for Rundeck python plugin folder structure"""

    def __init__(self, path: str):
        self.path = Path(path).resolve()
        self.root = self.path.parent
        self.plugin = self.path.relative_to(self.root)
        self.name = self.path.name
        self.root_required_files = ["plugin.yaml", "README.md"]

    def __repr__(self):
        return repr(self.name)

    @staticmethod
    def _is_folder(path):
        """Exits is path is not a folder"""
        if not path.is_dir():
            sys.exit("Paramether provided is not a folder.\n")
        print(f"    Path provided {path} is a folder.")

    @staticmethod
    def _has_required_files(path, required_files: list):
        """Exits if required file is missing from file list"""
        items_names = [x.name for x in path.iterdir()]
        if not set(required_files).issubset(items_names):
            print(f"  Folder: {path}")
            print(f"  Items: {items_names}")
            print(f"  Required Items: {required_files}")
            sys.exit("  Folder provided does not contain all required files.")
        print(f"    Folder {path} contains all required files: {required_files}")

    @staticmethod
    def _folder_has_contents_folder(path):
        """Exits if folder does not have contents folder."""
        folders = [x.name for x in path.iterdir() if x.is_dir()]
        if "contents" not in folders:
            sys.exit(
                f"{path} does not contain subfolder 'contents'. It contains {folders}"
            )
        print(f"    Folder {path} contains subfolder named 'contents'.")

    def validate(self):
        """Exits if folder does not have all files required to build a plugin"""
        print("  Validate:")
        self._is_folder(self.path)
        self._has_required_files(self.path, self.root_required_files)
        self._folder_has_contents_folder(self.path)
        # WIP
        # Add resources folder to validation
        # Validate if contents folder has file
        # Validate if YAML is ok
        # Validate if script described in YAML is in contents folder
        # Change zip to only include necessary items (ignore readme, tests)
        # Run plugin tests
        print("  Valid plugin.\n")

    def make_plugin_file(self, destination_dir):
        """ZIPs all content of plugin folder"""
        zip_file_name = self.name + ".zip"
        zip_file_path = destination_dir + "/" + zip_file_name
        zip_file = zipfile.ZipFile(zip_file_path, "w")
        with zip_file:
            for item in self.path.rglob("*"):
                zip_file.write(item, item.relative_to(self.root))
        return zip_file

    @staticmethod
    def _move_file_local(source, destination: str):
        """Moves file in path to destination"""
        target_file = Path(source)
        target_file.replace(f"{destination}/{target_file.name}")

    @staticmethod
    def _move_file_remote(source, destination: str, server, port, credentials):
        """Moves file in path to destination"""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=server,
            port=port,
            username=credentials[0],
            password=credentials[1],
            allow_agent=False,
            look_for_keys=False,
        )
        sftp = ssh.open_sftp()
        sftp.put(source, destination)
        ssh.close()

    def install_local(self, destination_folder):
        """Makes the plugin and moves to Rundeck plugin folder"""
        print(f"  Install {self.path} locally:")
        # WIP
        # Add install plugin requirements if it exists.
        print(f"  Compressing {self.path}")
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_file = self.make_plugin_file(tmpdir)
            print(f"  Zip file created {zip_file.filename}")
            self._move_file_local(zip_file.filename, destination_folder)
            print(f"  Moved {zip_file.filename} to {destination_folder}")

    def install_remote(self, destination, server, username, password):
        """Makes the plugin and moves to Rundeck plugin folder"""
        print(f"  Install {self.path} remote server {server}:")
        # WIP
        # Add install plugin requirements if it exists.
        print(f"    Compressing {self.path}")
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_file = self.make_plugin_file(tmpdir)
            zip_file_name = Path(zip_file.filename).name
            destination_name = f"{destination}{zip_file_name}"
            print(f"    Zip file created {zip_file}")
            print(f"    Moving {zip_file.filename} to {server}:{destination_name}")
            self._move_file_remote(
                zip_file.filename, destination_name, server, 22, (username, password)
            )
            print(f"    Moved {zip_file.filename} to {destination_name}")

    def create(self):
        """Creates a folder with all required files and folders for a valid plugin"""
        print(f"  need to create {self.path}\n")
