from multiprocessing import freeze_support
from loguru import logger

from base_exception import RanOutAccountsForLinkException
from interface import user_desired_value
from db_lib import *
from handl_info import file_get_random_comments, get_user_link_file
from reddit_api_selenium import work_with_api_reddit


def pick_up_account_to_link(link_from_file):

    count = db_number_of_records_account()
    link_id = db_get_link_id(link_from_file)

    for _ in range(count):
        account_obj = db_get_random_account_with_0()
        outcome_created, created_id_work_link_account_obj = db_exist_record_link_account(link_id=link_id, account_id=account_obj.id)

        if outcome_created:  # if create record return TRUE
            return link_id, account_obj, created_id_work_link_account_obj

        else:
            db_save_1_by_id(id_account=account_obj.id)

    else:
        # This exception will be earlier in db_get_random_account_with_0
        raise RanOutAccountsForLinkException


def body_loop(link_from_file, text_comment):
    link_id, account_obj, created_id_work_link_account_obj = pick_up_account_to_link(link_from_file)

    try:
        # get from db account not worked random choice
        path_cookie, dict_proxy, id_account = db_get_cookie_proxy(account_obj)
        reddit_username = path_cookie.stem  # Path to str

        logger.info(f'Work with "{reddit_username}"')
        work_with_api_reddit(link_from_file, dict_proxy, path_cookie, reddit_username, id_account, text_comment)

    except Exception as ex:
        db_delete_record_work_account_with_link(created_id_work_link_account_obj)
        raise ex


@logger.catch
def main():
    # interface
    upvote_int, comments_int = user_desired_value()

    # approves - comment = count for for 2
    remaining_upvote = upvote_int - comments_int

    for link_from_file in get_user_link_file():
        db_reset_work_all_accounts_1_on_0()

        # get random comment from txt
        list_comment = file_get_random_comments(comments_int)

        # for list random comment
        try:
            for text_comment in list_comment:
                body_loop(link_from_file=link_from_file, text_comment=text_comment)

            # remaining upvote after comment
            for _ in range(remaining_upvote):
                body_loop(link_from_file=link_from_file, text_comment=False)

        except RanOutAccountsForLinkException:
            continue
        # if create and exists exception delete record from db


if __name__ == '__main__':
    freeze_support()

    logger.add(
        "base_reddit.log",
        format="{time} {level} {message}",
        level="ERROR",
        rotation="10 MB",
        compression="zip"
    )
    try:
        main()
    finally:
        print("Press Enter: ")
