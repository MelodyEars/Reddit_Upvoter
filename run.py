import random
from multiprocessing import freeze_support

from loguru import logger

from Settings_Selenium import CookiesBrowser
from base_exception import ProxyInvalidException
from interface import user_desired_value, thread_for_api
from database import pick_up_accounts_to_link
from handl_info import file_get_random_comments
from auth_reddit import check_new_acc
from reddit_api_selenium import work_in_browser, run_browser
from work_fs import path_near_exefile


@logger.catch
def main():
    user_thread = thread_for_api()
    try:
        check_new_acc()
    except ProxyInvalidException:
        logger.error("Недостатньо проксі!")

    # interface
    upvote_int, comments_int = user_desired_value()

    list_link_acc = pick_up_accounts_to_link(upvote_int)  # get info
    random.shuffle(list_link_acc)

    # get random comment from txt
    list_comment = file_get_random_comments(comments_int)

    # navigator
    num = user_thread
    next_links = list_link_acc[:num]

    while next_links:
        client_cookies: list[CookiesBrowser] = run_browser(list_link_acc=next_links)
        work_in_browser(client_cookies, list_comment)

        resent_num = num
        num += user_thread
        next_links = list_link_acc[resent_num:num]


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
