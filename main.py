from multiprocessing import freeze_support
from loguru import logger

from interface import user_desired_value
from db_lib import *

from handl_info import file_get_random_comments, get_link_id
from reddit_api_selenium import work_with_api_reddit


def body_loop(link_reddit, text_comment):
    # get from db account not worked random choice
    path_cookie, dict_proxy, id_account = db_get_cookie_proxy()
    reddit_username = path_cookie.stem  # Path to str

    logger.info(f'Work with "{reddit_username}"')
    work_with_api_reddit(link_reddit, dict_proxy, path_cookie, reddit_username, id_account, text_comment)


def pick_up_account_to_link(link_id):
    count = db_number_of_records_account()
    for _ in range(count):
        created, obj_id = db_exist_record_link_account()
        if not created: # if create record return TRUE
            return created
        else:
            continue

    return None


@logger.catch
def main():
    # interface
    upvote_int, comments_int = user_desired_value()
    # approves - comment = count for for 2
    remaining_upvote = upvote_int - comments_int
    for link_id in get_link_id():
        db_reset_all_1_on_0()
        # get random comment from txt
        list_comment = file_get_random_comments(comments_int)

        # for list random comment
        for text_comment in list_comment:
            body_loop(link_reddit, text_comment=text_comment)

        # remaining upvote after comment
        for _ in range(remaining_upvote):
            body_loop(text_comment=False)

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
