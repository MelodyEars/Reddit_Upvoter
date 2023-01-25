import random

import work_fs as wf


def get_comments() -> list:
    path_comment = wf.path_near_exefile("comments.txt")
    str_file_content = wf.get_str_file(path_to_file=path_comment)

    # split by ###
    content = str_file_content.split("###")
    return content


def file_get_random_comments(count=int) -> list:
    # get count and random return count list
    comments = get_comments()

    select_comments = []

    while len(select_comments) < count:
        selection = random.choice(comments)
        # selection = selection.replace("\n", "")
        selection = selection.strip()
        if selection not in select_comments:
            select_comments.append(selection)

    print(select_comments)

    return select_comments
