"""
 read json
 convert file to list line
"""

import json


def read_json(filename):
    """get items from json"""
    with open(filename, 'r', encoding='UTF-8') as file:
        dates = json.loads(file.read())

    return dates


def getter_file_list(filename) -> list:
    """
    Get list from file by path.
    """

    with open(filename, "r", encoding="utf8", errors='ignore') as file:
        list_from_file = [line.strip() for line in file.readlines() if line != "\n"]

    return list_from_file
