from loguru import logger

from database import db_ban_add
from database.vote_tg_bot.get import db_get_cookie_objs
from work_fs import path_near_exefile

from .api_for_check_ban import check_ban
from .interface_ban import user_response, if_need_action
from .api_for_check_ban import for_user_open_browser
from .ADD_new_model import create_model
from .DELETE import delete_account


def access_to_account():
    """Base action with account."""
    list_selected_cookie_objs = []
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


def check_acc_ban():

    answer = if_need_action()
    if answer:  # print interface
        # count_page = thread_for_api()  # interface.
        list_path_cookies = list(path_near_exefile("cookies").glob("*"))  # in folder
        DICT_ACC_BAN = check_ban(list_path_cookies)  # api playwright
        db_ban_add(DICT_ACC_BAN)  # update db
