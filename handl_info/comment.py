import random
from typing import List, Any

import work_fs as wf


def get_comments() -> list:
    path_comment = wf.path_near_exefile("comments.txt")
    str_file_content = wf.get_str_file(path_to_file=path_comment)

    # split by ###
    content = str_file_content.split("###")
    return content


def file_get_random_comments(count=int) -> None | list[Any] | list:
    if count == 0:
        return
    else:
        # get count and random return count list
        list_comments = get_comments()

        select_comments = []
        if count != len(list_comments):
            for _ in range(count):
                num = random.randint(0, len(list_comments))
                comment = list_comments.pop(num)
                select_comments.append(comment)
        else:
            select_comments = list_comments

        print(select_comments)

        return select_comments

