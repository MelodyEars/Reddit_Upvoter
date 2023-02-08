import time

from database import *
from auth_reddit import get_cookies

from .reddit_actions import RedditWork
from .exceptions import NotRefrashPageException, BanAccountException, CookieInvalidException


def delete_account_db(path_cookie, id_cookie, reddit_username):
    logger.error(f'Account "{reddit_username}" banned and delete from data base.')
    db_delete_cookie_by_id(id_cookie)
    path_cookie.unlink()  # delete in folder


def work_with_api_reddit(link_reddit, dict_proxy, path_cookie, reddit_username, id_profile, text_comment=False):
    # open browser
    with RedditWork(link=link_reddit, proxy=dict_proxy, path_cookie=path_cookie) as api_reddit:
        # attends Reddit and check cookie works
        try:
            api_reddit.attend_link()
        except CookieInvalidException:
            api_reddit.DRIVER.close()
            logger.error(f'Cookie аккаунта "{reddit_username}" не работают, нужно перезаписать.')
            account_dict = db_get_account_by_id(id_profile)
            get_cookies(account=account_dict, proxy_for_api=dict_proxy)
            raise CookieInvalidException

        try:
            # put on upvote
            api_reddit.upvote()
        except BanAccountException:
            api_reddit.DRIVER.close()
            return delete_account_db(path_cookie, id_profile, reddit_username)

        except NotRefrashPageException:
            api_reddit.DRIVER.close()
            logger.error(f'Our CDN was unable to reach our servers. Account: "{reddit_username}"')
            return

        # if required to write comments
        if text_comment:
            api_reddit.write_comment(text_comment, reddit_username)

        api_reddit.client_cookie.save()
        logger.info(f'Successfully completed "{reddit_username}"')
        time.sleep(0.5)
        api_reddit.DRIVER.close()
