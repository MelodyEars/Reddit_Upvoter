import random

from loguru import logger

from database import db_get_cookie_objs, db_get_link_id, Cookie, db_exist_record_link_account, db_get_cookie_proxy
from work_fs import path_near_exefile, get_list_file, write_list_to_file

from .get_links import get_user_link_file


def get_account_file():
    path_account_file = path_near_exefile('accounts.txt')

    while list_accounts := get_list_file(path_account_file):
        account_line = list_accounts.pop()
        list_line_content = account_line.replace(" ", "").split(':')

        logger.info(list_line_content)
        account = {
            'login': list_line_content[0],
            'password': list_line_content[1]
        }

        try:
            yield account
        finally:
            write_list_to_file(path_account_file, list_accounts)


def pick_up_accounts_to_link(upvote_int: int):
    list_link_acc = []

    for link_from_file in get_user_link_file():
        list_cookies_objs: list = db_get_cookie_objs()
        random.shuffle(list_cookies_objs)

        link_id = db_get_link_id(link_from_file)

        for _ in range(upvote_int):
            try:
                cookie_obj: Cookie = list_cookies_objs.pop()
            except IndexError:
                break

            outcome_created, id_work_link_account_obj = db_exist_record_link_account(
                link_id=link_id, account_id=cookie_obj.id
            )

            if outcome_created:  # if create record return TRUE
                path_cookie, dict_proxy, id_cookie = db_get_cookie_proxy(cookie_obj)

                # Add info to file
                list_link_acc.append((link_from_file, path_cookie, dict_proxy, id_cookie, id_work_link_account_obj))

    return list_link_acc
