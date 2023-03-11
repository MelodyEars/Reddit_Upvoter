import time
from pathlib import Path

from loguru import logger
from urllib3.exceptions import ProtocolError

from database import db_get_account_by_id
from database.vote_tg_bot.models import Cookie

from auth_reddit import get_cookies

from .reddit_actions import RedditWork
from .exceptions import NotRefrashPageException, BanAccountException, CookieInvalidException


def work_api(link_reddit: str, dict_proxy: dict[str], path_cookie: Path, reddit_username: str,
                 id_cookie: Cookie.id, comment: str):

    with RedditWork(link=link_reddit, proxy=dict_proxy, path_cookie=path_cookie) as api_reddit:

        # attends Reddit and check cookie works
        try:
            api_reddit.attend_link()
        except CookieInvalidException:
            api_reddit.DRIVER.quit()
            logger.error(f'Cookie аккаунта "{reddit_username}" не работают, нужно перезаписать.')
            account_dict = db_get_account_by_id(id_cookie)
            get_cookies(account=account_dict, proxy_for_api=dict_proxy)
            api_reddit.attend_link()

        try:
            # put on upvote
            api_reddit.upvote()

            # follow model or join to community
            api_reddit.subscribing()

        except BanAccountException:
            logger.info(f'Ban: "{reddit_username}"')

        except NotRefrashPageException:
            logger.info(f'Our CDN was unable to reach our servers. Account: "{reddit_username}"')

        # if required to write comments
        if len(comment) != 0:
            api_reddit.write_comment(comment, reddit_username)

        api_reddit.client_cookie.save()
        logger.info(f'Successfully completed "{reddit_username}"')
        time.sleep(0.2)
        api_reddit.DRIVER.quit()


def open_browser(link_reddit: str, dict_proxy: dict[str], path_cookie: Path, reddit_username: str,
                 id_cookie: Cookie.id, comment: str):
    try:
        work_api(link_reddit, dict_proxy, path_cookie, reddit_username, id_cookie, comment)
    except ConnectionResetError:
        logger.critical('ConnectionResetError')
        work_api(link_reddit, dict_proxy, path_cookie, reddit_username, id_cookie, comment)
    except ProtocolError:
        logger.critical('ProtocolError')
        work_api(link_reddit, dict_proxy, path_cookie, reddit_username, id_cookie, comment)
    except ConnectionRefusedError:
        logger.critical('ConnectionRefusedError')
        work_api(link_reddit, dict_proxy, path_cookie, reddit_username, id_cookie, comment)

