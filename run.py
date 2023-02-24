from multiprocessing import freeze_support

from base_exception import ProxyInvalidException
from interface import user_desired_value
from database import *
from handl_info import file_get_random_comments, get_user_link_file, check_proxy
from reddit_api_selenium import work_with_api_reddit
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


def body_loop(link_from_file, text_comment):

    link_id, account_obj, created_id_work_link_account_obj = pick_up_account_to_link(link_from_file)
    # get from db account not worked random choice
    path_cookie, dict_proxy, id_account = db_get_cookie_proxy(account_obj)

    check_proxy(**dict_proxy)
    reddit_username = path_cookie.stem  # Path to str

    logger.info(f'Work with "{reddit_username}"')
    work_with_api_reddit(link_from_file, dict_proxy, path_cookie, reddit_username, id_account, text_comment)

    return created_id_work_link_account_obj


@logger.catch
def main():
    try:
        check_new_acc()
    except ProxyInvalidException:
        logger.error("Недостатньо проксі!")

    # interface
    upvote_int, comments_int = user_desired_value()

    # approves - comment = count for for 2
    remaining_upvote = upvote_int - comments_int

    for link_from_file in get_user_link_file():
        id_work_link_account_obj = WorkAccountWithLink
        db_reset_work_all_accounts_1_on_0()

        # get random comment from txt
        list_comment = file_get_random_comments(comments_int)
        for text_comment in list_comment:
            try:
                id_work_link_account_obj = body_loop(link_from_file=link_from_file, text_comment=text_comment)
            except Exception as ex:
                db_delete_record_work_account_with_link(id_work_link_account_obj)
                logger.critical(ex)
                continue

        # remaining upvote after comment
        for _ in range(remaining_upvote):
            try:
                id_work_link_account_obj = body_loop(link_from_file=link_from_file, text_comment=False)
            except Exception as ex:
                db_delete_record_work_account_with_link(id_work_link_account_obj)
                logger.critical(ex)
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

