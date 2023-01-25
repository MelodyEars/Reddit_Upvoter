from multiprocessing import freeze_support
from loguru import logger

from interface import user_deasire_data
from db_lib import db_get_cookie_proxy, db_reset_all_1_on_0, db_save_1_by_id, db_delete_by_id, db_get_cookie_by_id
from reddit_api_selenium import RedditWork
from handl_info import file_get_random_comments


def body_loop(link_reddit, text_comment=str):
    # get from db account not worked random choice
    path_cookie, dict_proxy, id_profile = db_get_cookie_proxy()
    reddit_username = path_cookie.stem

    logger.info(f"Work with {reddit_username}")

    # approves and comment on the Reddit
    with RedditWork(link=link_reddit, proxy=dict_proxy, path_cookie=path_cookie) as api_reddit:
        if api_reddit.attend_link():
            if api_reddit.prepare_reddit():
                api_reddit.upvote()

                if text_comment:
                    api_reddit.write_comment(text_comment, reddit_username)

                api_reddit.client_cookie.save()

            else:
                logger.error(f"Account {reddit_username} banned and delete from data base.")

                db_delete_by_id(id_profile)
                path_cookie.unlink()  # delete in folder
                #
                # api_reddit.DRIVER.delete_all_cookies()
                api_reddit.DRIVER.quit()
                return
        else:

            logger.error(f"Cookie аккаунта {reddit_username} не работают, нужно перезаписать.")

        api_reddit.DRIVER.quit()

    # db rewrite 1 is worked profile
    db_save_1_by_id(id_profile)
    logger.info(f"Successfully {db_get_cookie_by_id(id_profile).cookie_path}")


@logger.catch
def main():
    # interface
    link_reddit, upvote_int, comments_int = user_deasire_data()
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
