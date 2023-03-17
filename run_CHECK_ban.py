from multiprocessing import freeze_support

from loguru import logger

from CHECK_BAN.api_for_check_ban import check_ban
from CHECK_BAN.interface_ban import user_response, thread_for_api, if_need_check
from CHECK_BAN.api_for_check_ban import for_user_open_browser
from CHECK_BAN.ADD_new_model import create_model
from CHECK_BAN.DELETE import delete_account
from database import db_ban_add
from database.vote_tg_bot.get import db_get_cookie_objs

from work_fs import path_near_exefile, auto_create


@logger.catch
def main():
    list_selected_cookie_objs = []

    answer = if_need_check()
    if answer:  # print interface
        count_page = thread_for_api()  # interface
        list_path_cookies = list(path_near_exefile("cookies").glob("*"))  # in folder
        DICT_ACC_BAN = check_ban(list_path_cookies, count_page)  # api playwright
        db_ban_add(DICT_ACC_BAN)  # update db

    cookies_objs = list(db_get_cookie_objs())

    while cookies_objs:
        selected_cookie_obj, list_selected_cookie_objs, command = user_response(cookies_objs, list_selected_cookie_objs)

        # --------------------------------------- del ----------------------------------------
        if command == "del":
            logger.info("Selected account deleting.")
            delete_account(selected_cookie_obj)

        # +++++++++++++++++++++++++++++++++++++++ add +++++++++++++++++++++++++++++++++++++++++
        elif command == "add":
            logger.info("Your account preparing.")
            create_model(selected_cookie_obj)
            delete_account(selected_cookie_obj)

        # ======================================= open ========================================
        else:
            for_user_open_browser(selected_cookie_obj)


if __name__ == '__main__':
    freeze_support()
    logger.add(
        auto_create(path_near_exefile("logs"), _type="dir") / "CHECK_BAN.log",
        format="{time} {level} {message}",
        level="INFO",
        rotation="10 MB",
        compression="zip"
    )

    try:
        main()
    finally:
        input("Press Enter:")
