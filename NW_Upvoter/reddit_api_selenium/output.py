import asyncio
from concurrent.futures import ProcessPoolExecutor
from http.client import RemoteDisconnected
from pathlib import Path

from loguru import logger
from requests import ReadTimeout
from urllib3.exceptions import ProtocolError

from auth_reddit import get_cookies

from .reddit_actions import RedditWork
from BASE_Reddit.exceptions import NotRefrashPageException, BanAccountException, CookieInvalidException


# TODO close browser via pid or driver quit
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
    except (ConnectionResetError, ProtocolError, TimeoutError, ReadTimeout,
            ConnectionError, RemoteDisconnected) as e:
        logger.critical(f'{type(e).__name__} in output.py')
        return handling_api(dict_for_browser)


def work_api(link_reddit: str, dict_proxy: dict, path_cookie: Path, reddit_username: str, log_pswd: dict):
    while True:
        with RedditWork(link=link_reddit, proxy=dict_proxy, path_cookie=path_cookie) as api_reddit:
            try:
                api_reddit.attend_link()
            except CookieInvalidException:
                api_reddit.DRIVER.quit()
                logger.error(f'Cookie аккаунта "{reddit_username}" не работают, нужно перезаписать.')
                get_cookies(account=log_pswd, proxy_for_api=dict_proxy)
                continue

            try:
                logger.info("Put on upvote!")
                api_reddit.upvote()
                logger.info("Upvote stay on.")

            except BanAccountException:
                api_reddit.client_cookie.save()
                api_reddit.DRIVER.quit()
                raise BanAccountException(f'Ban: "{reddit_username}"')

            except NotRefrashPageException:
                api_reddit.client_cookie.save()
                api_reddit.DRIVER.quit()
                raise NotRefrashPageException(f'Not refresh page: "{reddit_username}"')

            logger.info("Save cookie!")
            api_reddit.client_cookie.save()
            logger.info(f'Successfully completed "{reddit_username}"')
            api_reddit.DRIVER.quit()
            break
