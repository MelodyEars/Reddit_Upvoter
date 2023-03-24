"""
 read json
 convert file to list line
"""

import json
from work_fs.PATH.work_with_path import file_exists


def read_json(filename):
    """get items from json"""
    with open(filename, 'r', encoding='UTF-8') as file:
        dates = json.loads(file.read())

    return dates


def get_list_file(path_to_file) -> list[str]:
    """
    Get list from file by path.
    """
    if file_exists(path_to_file):
        with open(path_to_file, "r", encoding="utf8", errors='ignore') as file:
            list_from_file = [line.strip() for line in file.readlines() if line != "\n"]

        return list_from_file
    else:
        raise Exception(f'Not found {path_to_file}')


def get_str_file(path_to_file) -> str:
    if file_exists(path_to_file):
        with open(path_to_file, "r", encoding="utf8",) as file:
            content = file.read()

        return content
    else:
        raise Exception(f'Not found {path_to_file}')
