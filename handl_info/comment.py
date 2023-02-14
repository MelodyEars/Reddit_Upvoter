import random
from pathlib import Path
from typing import Any, Type

import work_fs as wf


def get_comments() -> list:
    path_comment: Path = wf.path_near_exefile("comments.txt")
    str_file_content = wf.get_str_file(path_to_file=path_comment)

    # split by ###
    content: list = str_file_content.split("###")
    return content


def file_get_random_comments(count=int) -> Type[list] | list[Any] | list:
    if count == 0:
        return []
    else:
        # get count and random return count list
        list_comments = get_comments()

        select_comments = []
        length_list_comment = len(list_comments)

        if count != length_list_comment:
            for _ in range(count):
                num = random.randint(0, length_list_comment - 1)
                comment: str = list_comments.pop(num)
                upd_comment = comment.replace('\n', '')
                select_comments.append(upd_comment)
        else:
            select_comments = list_comments

        return select_comments

