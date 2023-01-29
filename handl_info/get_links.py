from work_fs import get_list_file, path_near_exefile


def get_user_link_file():
    list_links = get_list_file(path_near_exefile('LinkList.txt'))

    for link in list_links:
        link = link.replace(" ", "")

        yield link

