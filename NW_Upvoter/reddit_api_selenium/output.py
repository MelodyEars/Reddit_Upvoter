# import time
from pathlib import Path
# from threading import Thread

from loguru import logger
from requests import ReadTimeout
from urllib3.exceptions import ProtocolError

from database import db_get_account_by_id
from database.vote_tg_bot.models import Cookie

from auth_reddit import get_cookies

from .reddit_actions import RedditWork
from BASE_Reddit.exceptions import NotRefrashPageException, BanAccountException, CookieInvalidException


def getter_cookie(link_reddit, dict_proxy, path_cookie, reddit_username, id_cookie):
    logger.error(f'Cookie аккаунта "{reddit_username}" не работают, нужно перезаписать.')
    account_dict = db_get_account_by_id(id_cookie)
    get_cookies(account=account_dict, proxy_for_api=dict_proxy)

    return work_api(link_reddit, dict_proxy, path_cookie, reddit_username, id_cookie)


def work_api(
        link_reddit: str, dict_proxy: dict[str], path_cookie: Path,
        reddit_username: str, id_cookie: Cookie.id,
):  # comment: str):

    with RedditWork(link=link_reddit, proxy=dict_proxy, path_cookie=path_cookie) as api_reddit:
        # ______________________________________________________________________________ go to link
        # attends Reddit and check cookie works
        try:
            api_reddit.attend_link()
        except CookieInvalidException:
            api_reddit.DRIVER.quit()
            return getter_cookie(link_reddit, dict_proxy, path_cookie, reddit_username, id_cookie)

        # ______________________________________________________________________________ upvote
        try:
            logger.info("Put on upvote!")
            # put on upvote
            api_reddit.upvote()
            logger.info("Upvote stay on.")

        except BanAccountException:
            logger.info(f'Ban: "{reddit_username}"')

        except NotRefrashPageException:
            logger.info(f'Our CDN was unable to reach our servers. Account: "{reddit_username}"')

        # ______________________________________________________________________________ save
        logger.info("Save cookie!")
        api_reddit.client_cookie.save()
        logger.info(f'Successfully completed "{reddit_username}"')
        api_reddit.DRIVER.quit()


def open_browser(link_reddit: str, dict_proxy: dict[str], path_cookie: Path, reddit_username: str,
                 id_cookie: Cookie.id, ):  # , comment: str):
    try:
        return work_api(link_reddit, dict_proxy, path_cookie, reddit_username, id_cookie, )
    except ConnectionResetError:
        logger.critical('ConnectionResetError output.py')
        return work_api(link_reddit, dict_proxy, path_cookie, reddit_username, id_cookie, )
    except ProtocolError:
        logger.critical('ProtocolError output.py')
        return work_api(link_reddit, dict_proxy, path_cookie, reddit_username, id_cookie, )
    except TimeoutError:
        logger.critical('TimeoutError output.py')
        return work_api(link_reddit, dict_proxy, path_cookie, reddit_username, id_cookie, )
        # return getter_cookie(link_reddit, dict_proxy, path_cookie, reddit_username, id_cookie, )
    except ReadTimeout:
        logger.critical('ReadTimeout output.py')
        return work_api(link_reddit, dict_proxy, path_cookie, reddit_username, id_cookie, )

