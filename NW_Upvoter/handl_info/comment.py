import random
from pathlib import Path
from typing import Type

import work_fs as wf


def get_comments() -> list:
    path_comment: Path = wf.path_near_exefile("comments.txt")
    str_file_content = wf.get_str_file(path_to_file=path_comment)

    # split by ###
    content: list = str_file_content.split("###")
    return content


def file_get_random_comments(count: int) -> Type[list] | list[str] | list:
    if count == 0:
        return []
    else:
        # get count and random return count list
        list_comments = get_comments()
        random.shuffle(list_comments)

        if count != len(list_comments):
            select_comments = [list_comments.pop().strip() for _ in range(count)]
        else:
            select_comments = list_comments

        return select_comments

