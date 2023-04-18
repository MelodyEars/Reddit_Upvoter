import asyncio
from multiprocessing import Manager, Process

from typing import NamedTuple
from concurrent.futures import ProcessPoolExecutor

import psutil
from loguru import logger

from aiogram import types
from aiogram.fsm.state import State, StatesGroup

from SWITCHer_window import call_auto_focus
from main_Reddit import start_reddit_work # MESSAGE_IN_TG

import time

from pywinauto import Application

# import time
from pathlib import Path
# from threading import Thread

from loguru import logger
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
        reddit_username: str, id_cookie: Cookie.id, LIST_PID_BROWSERS
):  # comment: str):

    with RedditWork(link=link_reddit, proxy=dict_proxy, path_cookie=path_cookie) as api_reddit:
        # ______________________________________________________________________________ run window focus
        browser_pid = api_reddit.DRIVER.browser_pid
        LIST_PID_BROWSERS.append(browser_pid)  # append browser's pid which handling in switcher_window

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
                 id_cookie: Cookie.id, LIST_PID_BROWSERS):  # , comment: str):
    try:
        return work_api(link_reddit, dict_proxy, path_cookie, reddit_username, id_cookie, LIST_PID_BROWSERS)
    except ConnectionResetError:
        logger.critical('ConnectionResetError output.py')
        return work_api(link_reddit, dict_proxy, path_cookie, reddit_username, id_cookie, LIST_PID_BROWSERS)
    except ProtocolError:
        logger.critical('ProtocolError output.py')
        return work_api(link_reddit, dict_proxy, path_cookie, reddit_username, id_cookie, LIST_PID_BROWSERS)
    except TimeoutError:
        logger.critical('TimeoutError output.py')
        return getter_cookie(link_reddit, dict_proxy, path_cookie, reddit_username, id_cookie, LIST_PID_BROWSERS)

# Process 2
def call_auto_focus(LIST_PID_BROWSERS):
    while len(LIST_PID_BROWSERS) != 0:  # wait start process
        print("wait more window")
        time.sleep(5)

    while LIST_PID_BROWSERS:
        # if len(LIST_PID_BROWSERS) != 1:
        for browser_pid in LIST_PID_BROWSERS:
            try:
                print(f"Select: {browser_pid}")
                app = Application().connect(process=browser_pid)
                main_window = app.top_window()

                main_window.set_focus()
                time.sleep(5)
            except RuntimeError:
                print(f"Delete: {browser_pid}")
                LIST_PID_BROWSERS.remove(browser_pid)
        # else:
        #     time.sleep(5)

class RunBotStates(StatesGroup):
    reddit_link = State()
    upvote_int = State()
    # comments_int = State()


class StructData(NamedTuple):
    reddit_link: str
    upvote_int: int

class AutofocusManager:
    def __init__(self):
        self.process = None

    def start_autofocus(self, LIST_PID_BROWSERS):
        if self.process is not None and self.process.is_alive():
            print("Process running")
            return

        self.process = Process(target=call_auto_focus, args=(LIST_PID_BROWSERS,))
        self.process.start()


async def run_process_and_reply_after(message: types.Message, data: StructData):
    logger.info("runner process")

    reddit_link = data.reddit_link
    upvote_int = data.upvote_int
    autofocus_manager = AutofocusManager()

    with Manager() as manager:
        LIST_PID_BROWSERS = manager.list()
        autofocus_manager.start_autofocus(LIST_PID_BROWSERS)

        with ProcessPoolExecutor() as executor:
            q = await asyncio.get_running_loop().run_in_executor(
                executor, start_reddit_work, reddit_link, upvote_int, LIST_PID_BROWSERS
            )

    if q:
        await message.reply(q)
