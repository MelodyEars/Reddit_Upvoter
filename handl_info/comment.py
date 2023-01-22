import random

import work_fs as wf


def get_comments():
    path_comment = wf.path_near_exefile("comments.txt")
    str_file_content = wf.get_str_file(path_to_file=path_comment)

    # split by ###
    content = str_file_content.split("###")
    return content


def get_random_comments() -> str:
    comments = get_comments()
    return random.choice(comments)


if __name__ == '__main__':
    print(get_random_comments())
