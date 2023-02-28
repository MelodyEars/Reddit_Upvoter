import traceback
from multiprocessing import freeze_support

from Settings_Selenium import CookiesBrowser, run_browser
from base_exception import ProxyInvalidException
from interface import user_desired_value, thread_for_api
from database import *
from handl_info import file_get_random_comments, get_user_link_file
from auth_reddit import check_new_acc
from reddit_api_selenium.output import work_with_api_reddit


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


def body_loop(client_cookies: list[CookiesBrowser], list_comment: list[str]):
    for cl_cookie in client_cookies:
        logger.info(f'Work with "{cl_cookie.username}"')

        try:
            if list_comment:
                comment: str = list_comment.pop()
                work_with_api_reddit(cl_cookie, comment)
            else:
                work_with_api_reddit(cl_cookie)

        except Exception:
            db_delete_record_work_account_with_link(cl_cookie.id_work_link_account_obj)
            logger.error(traceback.format_exc())
            continue


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
    # remaining_upvote = upvote_int - comments_int. it's no longer needed, because body loop get
    # get list comment while not end then it gets integer number remaining upvote

    list_link_acc = pick_up_accounts_to_link(upvote_int)  # get info

    # get random comment from txt
    list_comment = file_get_random_comments(comments_int)

    # navigator
    num = user_thread
    next_links = list_link_acc[:num]

    while next_links:
        client_cookies: list[CookiesBrowser] = run_browser(list_link_acc=next_links)
        body_loop(client_cookies, list_comment)

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
