from work_fs import get_list_file, path_near_exefile
from db_lib import db_get_link_id


def get_user_link_file():
    list_links = get_list_file(path_near_exefile('LinkList.txt'))

    for link in list_links:
        link = link.replace(" ", "")

        yield link


def get_link_id():
    for link_file in get_user_link_file():
        link_id = db_get_link_id(link_file)
        yield link_id
