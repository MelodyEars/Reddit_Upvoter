import traceback
from multiprocessing import freeze_support

from base_exception import ProxyInvalidException
from interface import user_desired_value, thread_for_api
from database import *
from handl_info import file_get_random_comments, get_user_link_file, check_proxy
from reddit_api_selenium import run_browser
from auth_reddit import check_new_acc


def get_fata_from_db(cookie_obj):

    # get from db account not worked random choice
    path_cookie, dict_proxy, id_account = db_get_cookie_proxy(cookie_obj)

    check_proxy(**dict_proxy)

    return path_cookie, dict_proxy, id_account

def pick_up_accounts_to_link(upvote_int: int):
    dict_link_value = {}

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
                path_cookie, dict_proxy, id_account = get_fata_from_db(cookie_obj)
                # Add info to file
                dict_link_value[link_from_file] = path_cookie, dict_proxy, id_account, id_work_link_account_obj

    return dict_link_value

@logger.catch
def main():
    user_thread = thread_for_api()
    try:
        check_new_acc()
    except ProxyInvalidException:
        logger.error("Недостатньо проксі!")

    # interface
    upvote_int, comments_int = user_desired_value()

    # approves - comment = count for for 2
    remaining_upvote = upvote_int - comments_int

    dict_link_value = pick_up_accounts_to_link(upvote_int)
        # get random comment from txt
        list_comment = file_get_random_comments(comments_int)
        for text_comment in list_comment:
            try:
                logger.info(f'Work with "{reddit_username}"')
                run_browser(link_from_file, dict_proxy, path_cookie, reddit_username, id_account, text_comment)

            except Exception:
                db_delete_record_work_account_with_link(id_work_link_account_obj)
                logger.error(traceback.format_exc())
                continue

        # remaining upvote after comment
        for _ in range(remaining_upvote):
            try:
                logger.info(f'Work with "{reddit_username}"')
                run_browser(link_from_file, dict_proxy, path_cookie, reddit_username, id_account, text_comment)

            except Exception:
                db_delete_record_work_account_with_link(id_work_link_account_obj)
                logger.error(traceback.format_exc())
                continue


if __name__ == '__main__':
    freeze_support()

    logger.add(
        path_near_exefile("base_reddit.log"),
        format="{time} {level} {message}",
        level="INFO",
        rotation="10 MB",
        compression="zip"
    )

    try:
        main()
    finally:
        input("Press Enter:")
