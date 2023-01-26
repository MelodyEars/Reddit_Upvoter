from multiprocessing import freeze_support
from loguru import logger

from interface import user_desired_value
from db_lib import db_get_cookie_proxy, db_reset_all_1_on_0, db_save_1_by_id, db_delete_by_id
from reddit_api_selenium import RedditWork
from reddit_api_selenium.exceptions import NotRefrashPageException, BanAccountException, CookieInvalidException
from handl_info import file_get_random_comments, check_proxy


def delete_account_db(path_cookie, id_profile, reddit_username):
    logger.error(f'Account "{reddit_username}" banned and delete from data base.')
    db_delete_by_id(id_profile)
    path_cookie.unlink()  # delete in folder


def get_attr():
    # get from db account not worked random choice
    path_cookie, dict_proxy, id_profile = db_get_cookie_proxy()
    reddit_username = path_cookie.stem  # Path to str
    return path_cookie, dict_proxy, id_profile, reddit_username

def work_with_api(link_reddit, dict_proxy, path_cookie, reddit_username, id_profile, text_comment):
    # approves and comment on the Reddit
    with RedditWork(link=link_reddit, proxy=dict_proxy, path_cookie=path_cookie) as api_reddit:
        # attends Reddit and check cookie works
        try:
            api_reddit.attend_link()
        except CookieInvalidException:
            logger.error(f'Cookie аккаунта "{reddit_username}" не работают, нужно перезаписать.')
            # db rewrite 1 is worked profile
            return db_save_1_by_id(id_profile)

        # Handling error and close popups
        try:
            api_reddit.prepare_reddit()
        except BanAccountException:
            return delete_account_db(path_cookie, id_profile, reddit_username)
        except NotRefrashPageException:
            logger.error(f'Our CDN was unable to reach our servers. Account: "{reddit_username}"')
            # db rewrite 1 is worked profile
            return db_save_1_by_id(id_profile)

        # put on upvote
        api_reddit.upvote()

        # if required to write comments
        if text_comment:
            api_reddit.write_comment(text_comment, reddit_username)

        api_reddit.client_cookie.save()
        # db rewrite 1 is worked profile
        db_save_1_by_id(id_profile)

        logger.info(f'Successfully completed "{reddit_username}"')


def body_loop(link_reddit, text_comment=str):
    path_cookie, dict_proxy, id_profile, reddit_username = get_attr()
    if check_proxy(**dict_proxy):
        logger.info(f'Work with "{reddit_username}"')
        work_with_api(link_reddit, dict_proxy, path_cookie, reddit_username, id_profile, text_comment)
    else:
        db_save_1_by_id(id_profile)
        logger.error(f"Proxy Invalid: {reddit_username} прокси не работает.")


@logger.catch
def main():
    # interface
    link_reddit, upvote_int, comments_int = user_desired_value()
    # 4 approves - comment = count for for 2
    remaining_upvote = upvote_int - comments_int

    # db
    # reset all data in the worked_is
    db_reset_all_1_on_0()
    # get random comment from txt
    list_comment = file_get_random_comments(comments_int)

    # for list random comment
    for text_comment in list_comment:
        body_loop(link_reddit, text_comment=text_comment)

    # remaining upvote after comment
    for _ in range(remaining_upvote):
        body_loop(link_reddit)


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
