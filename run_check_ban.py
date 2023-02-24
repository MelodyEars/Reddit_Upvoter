from multiprocessing import freeze_support

from check_ban.api_for_check_ban import check_ban
from check_ban.interface_ban import user_response, thread_for_api, if_need_check
from check_ban.api_for_check_ban import for_user_open_browser
from database import *


def delete_account_db(cookie_obj: Cookie):
    db_delete_cookie_by_id(cookie_obj.id)
    path_cookie = path_near_exefile(cookie_obj.cookie_path)
    path_cookie.unlink()  # delete in folder
    logger.error(f'{path_cookie.stem} був видалений з бд.')


@logger.catch
def main():
    list_selected_cookie_objs = []

    answer = if_need_check()
    if answer:  # print interface
        count_page = thread_for_api()
        list_path_cookies = list(path_near_exefile("cookies").glob("*"))
        DICT_ACC_BAN = check_ban(list_path_cookies, count_page)  # api playwright
        db_ban_add(DICT_ACC_BAN)  # update db

    cookies_objs = list(db_get_cookie_objs())

    while cookies_objs:
        selected_cookie, list_selected_cookie_objs, is_del_db = user_response(cookies_objs, list_selected_cookie_objs)
        if not is_del_db:
            for_user_open_browser(selected_cookie)
        else:
            delete_account_db(selected_cookie)


if __name__ == '__main__':
    freeze_support()

    logger.add(
        "check_ban.log",
        format="{time} {level} {message}",
        level="DEBUG",
        rotation="10 MB",
        compression="zip"
    )

    try:
        main()
    finally:
        input("Press Enter:")
