from loguru import logger

from db_lib import *

from .reddit_actions import RedditWork
from .exceptions import NotRefrashPageException, BanAccountException, CookieInvalidException


def delete_account_db(path_cookie, id_account, reddit_username):
    logger.error(f'Account "{reddit_username}" banned and delete from data base.')
    db_delete_accounts_by_id(id_account)
    path_cookie.unlink()  # delete in folder


def work_with_api_reddit(link_reddit, dict_proxy, path_cookie, reddit_username, id_profile, text_comment=False):
    # open browser
    with RedditWork(link=link_reddit, proxy=dict_proxy, path_cookie=path_cookie) as api_reddit:
        # attends Reddit and check cookie works
        try:
            api_reddit.attend_link()
        except CookieInvalidException:
            logger.error(f'Cookie аккаунта "{reddit_username}" не работают, нужно перезаписать.')

        try:
            # put on upvote
            api_reddit.upvote()
        except BanAccountException:
            return delete_account_db(path_cookie, id_profile, reddit_username)
        except NotRefrashPageException:
            logger.error(f'Our CDN was unable to reach our servers. Account: "{reddit_username}"')

        # if required to write comments
        if text_comment:
            api_reddit.write_comment(text_comment, reddit_username)

        api_reddit.client_cookie.save()
        #
        # # close browser
        # api_reddit.DRIVER.quit()

        logger.info(f'Successfully completed "{reddit_username}"')
