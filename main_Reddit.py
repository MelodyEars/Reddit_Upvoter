import traceback
from multiprocessing import freeze_support

from base_exception import ProxyInvalidException
from interface import user_desired_value
from database import *
from handl_info import file_get_random_comments, get_user_link_file, check_proxy
from reddit_api_selenium import run_browser
from auth_reddit import check_new_acc


def pick_up_account_to_link(link_from_file):

    count = db_get_number_of_records_account()
    link_id = db_get_link_id(link_from_file)

    for _ in range(count):
        account_obj = db_get_random_account_with_0()
        outcome_created, created_id_work_link_account_obj = db_exist_record_link_account(link_id=link_id,
                                                                                         account_id=account_obj.id)
        db_save_1_by_id(id_cookie=account_obj.id)  # update record in the db about this acc selected

        if outcome_created:  # if create record return TRUE
            return link_id, account_obj, created_id_work_link_account_obj
        else:
            continue
    else:
        # This exception will be earlier in db_get_random_account_with_0
        raise RanOutAccountsForLinkException


def body_loop(reddit_link: str, comment: str):

    link_id, account_obj, created_id_work_link_account_obj = pick_up_account_to_link(reddit_link)
    # get from db account not worked random choice
    path_cookie, dict_proxy, id_account = db_get_cookie_proxy(account_obj)

    check_proxy(**dict_proxy)

    reddit_username = path_cookie.stem  # Path to str

    logger.info(f'Work with "{reddit_username}"')
    run_browser(link_reddit=reddit_link,
                dict_proxy=dict_proxy,
                path_cookie=path_cookie,
                reddit_username=reddit_username,
                id_profile=id_account,
                text_comment=comment)

    return created_id_work_link_account_obj


def main_Reddit(reddit_link: str, upvote_int: int, comments_int: int):

    id_work_link_account_obj = WorkAccountWithLink

    # get random comment from txt
    list_comments = file_get_random_comments(comments_int)

    for text_comment in range(upvote_int):
        comment = str

        try:
            comment = list_comments.pop()
        except IndexError:
            pass

        try:
            id_work_link_account_obj = body_loop(reddit_link=reddit_link, comment=comment)
        except Exception:
            db_delete_record_work_account_with_link(id_work_link_account_obj)
            logger.error(traceback.format_exc())
            continue
