import asyncio
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from loguru import logger
from requests import ReadTimeout
from urllib3.exceptions import ProtocolError

from database import db_get_account_by_id
from database.vote_tg_bot.models import Cookie

from auth_reddit import get_cookies

from .reddit_actions import RedditWork
from BASE_Reddit.exceptions import NotRefrashPageException, BanAccountException, CookieInvalidException


async def open_browser(dict_for_browser):
    with ProcessPoolExecutor() as executor:
        try:
            await asyncio.wait_for(asyncio.get_running_loop().run_in_executor(executor, handling_api, dict_for_browser), timeout=180)
        except asyncio.TimeoutError:
            logger.info("Timeout occurred. Restarting process...")
            return await open_browser(dict_for_browser)


def handling_api(dict_for_browser):
    try:
        return work_api(**dict_for_browser)
    except (ConnectionResetError, ProtocolError, TimeoutError, ReadTimeout) as e:
        logger.critical(f'{type(e).__name__} in output.py')
        return handling_api(dict_for_browser)


def work_api(link_reddit: str, dict_proxy: dict[str], path_cookie: Path, reddit_username: str, id_cookie: Cookie.id):
    while True:
        with RedditWork(link=link_reddit, proxy=dict_proxy, path_cookie=path_cookie) as api_reddit:
            try:
                api_reddit.attend_link()
            except CookieInvalidException:
                logger.error(f'Cookie аккаунта "{reddit_username}" не работают, нужно перезаписать.')
                account_dict = db_get_account_by_id(id_cookie)
                get_cookies(account=account_dict, proxy_for_api=dict_proxy)
                continue

            try:
                logger.info("Put on upvote!")
                api_reddit.upvote()
                logger.info("Upvote stay on.")

            except BanAccountException:
                logger.info(f'Ban: "{reddit_username}"')

            except NotRefrashPageException:
                logger.info(f'Our CDN was unable to reach our servers. Account: "{reddit_username}"')

            logger.info("Save cookie!")
            api_reddit.client_cookie.save()
            logger.info(f'Successfully completed "{reddit_username}"')
            break
