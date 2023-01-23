import random

import work_fs as wf


def get_comments() -> list:
    path_comment = wf.path_near_exefile("comments.txt")
    str_file_content = wf.get_str_file(path_to_file=path_comment)

    # split by ###
    content = str_file_content.split("###")
    return content


def get_random_comments(count=int) -> list:
    # get count and random return count list
    comments = get_comments()
    selects_comments = random.choices(comments, k=int(count))

    return selects_comments


if __name__ == '__main__':
    print(get_random_comments())
