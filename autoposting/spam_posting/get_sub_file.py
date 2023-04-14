from pathlib import Path

from work_fs.PATH import file_exists, path_near_exefile
from work_fs.read_file import get_list_file
from work_fs.write_to_file import write_line


def gen_list_sub():
    path_to_file: Path = path_near_exefile("list_sub.txt")

    if file_exists(path_to_file):
        while list_sub := get_list_file(path_to_file):
            sub = list_sub.pop()
            yield sub
            write_line(path_to_file, list_sub)

    else:
        raise Exception("Not found 'list_sub.txt")
