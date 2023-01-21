"""
This file cans:
    - work with pathlib,
    - hidden file and directory
    - auto create if not exists file or dir

"""

import os
import sys
import subprocess
import time
import zipfile

from pathlib import Path


def file_exists(path_to_file) -> bool:
    """Check file exists by path"""
    path = Path(path_to_file)

    if path.is_file():
        return True
    else:
        return False


def dir_exists(path_to_dir) -> bool:
    """Check directory exists by path"""
    path = Path(path_to_dir)

    if path.is_dir():
        return True
    else:
        return False


def path_near_exefile(filename=""):
    """
    create=visible :create folder or file is visible for users
    create=hidden :create folder or file is hidden for users

    return path to file near executable file
    """

    if getattr(sys, 'frozen', False):
        path = Path(sys.executable).parent / filename

    # get path from this file
    else:
        path = Path(__file__).parent.parent / filename

    return path


def auto_create(path, _type, hidden=False):
    """
    @_type=file
    @_type=dir
    """

    if _type == "file":

        if not file_exists(path):
            open(path, "a+", encoding="utf8", errors="ignore").close()

            if hidden:
                subprocess.call("attrib +h " + str(path))

    elif _type == "dir":
        if not dir_exists(path):
            os.makedirs(path)

            if hidden:
                subprocess.call("attrib +h " + str(path))

    else:
        raise Exception(f"Invalid flag _type='{_type}'")

    return path


def unziping(path_to_zipfile=Path, unzip_path=Path):
    downloads_path = path_to_zipfile.parent

    with zipfile.ZipFile(path_to_zipfile, 'r') as zip_ref:
        for content in zip_ref.namelist():
            data = zip_ref.read(content, downloads_path)
            myfile_path = unzip_path
            myfile_path.write_bytes(data)

    # delete zip
    path_to_zipfile.unlink()


def wait_download(filepath):
    while not filepath.is_file():
        time.sleep(1)

    return filepath