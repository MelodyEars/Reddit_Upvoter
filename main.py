from multiprocessing import freeze_support
from loguru import logger

from interface import user_deasire_data
from db_lib import db_get_cookie_proxy, db_reset_all_1_on_0, db_save_1_by_id, db_delete_by_id, \
    db_print_cookie_info, db_get_cookie_by_id
from reddit_api_selenium import RedditWork
from handl_info import file_get_random_comments

'https://www.reddit.com/r/drawing/comments/101dlrm/this_got_removed_for_being_nsfw_so_here_is_day/'
'Looks amazing!!!'
'https://www.reddit.com/r/ffxiv/comments/10hf1e1/nsfw/'
"This is Geralt, but what is the name of the elf? Are there ero-content with her?"
'https://www.reddit.com/r/PornMemes/comments/10exyyz/eat_fresh/'
"It's so deep!"


def body_loop(link_reddit, text_comment=str):
    # get from db account not worked random choice
    path_cookie, dict_proxy, id_profile = db_get_cookie_proxy()
    # approves and comment on the Reddit
    with RedditWork(link=link_reddit, proxy=dict_proxy, path_cookie=path_cookie) as api_reddit:
        api_reddit.attend_link()
        if not api_reddit.baned_account():
            api_reddit.prepare_reddit()
            api_reddit.upvote()
            if text_comment:
                api_reddit.write_comment(text_comment)
            api_reddit.client_cookie.save()
        else:
            logger.error("Your account banned and delete from data base.")
            db_print_cookie_info(id_profile)
            db_delete_by_id(id_profile)
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
        body_loop(list_comment)


if __name__ == '__main__':
    freeze_support()

    logger.add(
        "base_reddit.log",
        format="{time} {level} {message}",
        level="ERROR",
        rotation="10 MB",
        compression="zip"
    )

    # comment split ###
    # TODO "get cookies" replase " ", ""
    # write readme when file band name

    main()
    