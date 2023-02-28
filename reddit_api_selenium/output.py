import time

from Settings_Selenium import CookiesBrowser
from database import *

from .reddit_actions import RedditWork
from .exceptions import NotRefrashPageException, BanAccountException, CookieInvalidException


def work_with_api_reddit(client_cookie: CookiesBrowser, text_comment=False):
    with RedditWork(client_cookie) as api_reddit:
        try:
            # put on upvote
            api_reddit.upvote()

            # follow model or join to community
            api_reddit.subscribing()

        except BanAccountException:
            logger.trace(f'Ban: "{client_cookie.username}"')

        except NotRefrashPageException:
            logger.trace(f'Our CDN was unable to reach our servers. Account: "{client_cookie.username}"')

        # if required to write comments
        if text_comment:
            api_reddit.write_comment(text_comment)

        api_reddit.client_cookie.save()
        logger.info(f'Successfully completed "{client_cookie.username}"')
        time.sleep(0.2)
        api_reddit.DRIVER.quit()
