import time

from database import *
from auth_reddit import get_cookies

from .reddit_actions import RedditWork
from .exceptions import NotRefrashPageException, BanAccountException, CookieInvalidException


def work_with_api_reddit(api_reddit, dict_proxy, reddit_username, id_profile, text_comment):
    # attends Reddit and check cookie works
    try:
        api_reddit.attend_link()
    except CookieInvalidException:
        api_reddit.DRIVER.quit()
        logger.error(f'Cookie аккаунта "{reddit_username}" не работают, нужно перезаписать.')
        account_dict = db_get_account_by_id(id_profile)
        get_cookies(account=account_dict, proxy_for_api=dict_proxy)
        api_reddit.attend_link()

    try:
        # put on upvote
        api_reddit.upvote()

        # follow model or join to community
        api_reddit.subscribing()

    except BanAccountException:
        logger.trace(f'Ban: "{reddit_username}"')

    except NotRefrashPageException:
        logger.trace(f'Our CDN was unable to reach our servers. Account: "{reddit_username}"')

    # if required to write comments
    if text_comment:
        api_reddit.write_comment(text_comment, reddit_username)

    api_reddit.client_cookie.save()
    logger.info(f'Successfully completed "{reddit_username}"')
    time.sleep(0.2)
    api_reddit.DRIVER.quit()


def run_browser(link_reddit, dict_proxy, path_cookie, reddit_username, id_profile, text_comment=False):
    # open browser
    with RedditWork(link=link_reddit, proxy=dict_proxy, path_cookie=path_cookie) as api_reddit:
        work_with_api_reddit(api_reddit, dict_proxy, reddit_username, id_profile, text_comment)
