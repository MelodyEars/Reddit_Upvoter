from pathlib import Path

from colorama import deinit, init

from .PATH import file_exists
from .color import cyan_color

from work_fs.read_file import get_list_file


# def get_token_from_file(filepath: Path):
#     with open(str(filepath), encoding="utf-8") as file:
#         return file.read()


def get_or_create_info(text_what_get: str, filepath: Path):
    if file_exists(filepath):
        return get_list_file(filepath)

    else:
        init()
        info_to_file = input(cyan_color(text_what_get + ":"))
        deinit()

        with open(str(filepath), "w", encoding="utf-8") as file:
            file.write(info_to_file)

        return info_to_file
