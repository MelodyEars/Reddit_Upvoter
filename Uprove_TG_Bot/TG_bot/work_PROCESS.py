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


class RunBotStates(StatesGroup):
    reddit_link = State()
    upvote_int = State()
    # comments_int = State()


class StructData(NamedTuple):
    reddit_link: str
    upvote_int: int


# PID_PROCESS_AUTOFOCUS = None
#
#
# def run_process_autofocus(LIST_PID_BROWSERS):
#     global PID_PROCESS_AUTOFOCUS
#
#     if PID_PROCESS_AUTOFOCUS is not None:
#         if psutil.pid_exists(PID_PROCESS_AUTOFOCUS):
#             p = psutil.Process(PID_PROCESS_AUTOFOCUS)
#             if p.status() == psutil.STATUS_RUNNING:
#                 print("Process runing")
#                 return
#
#     autofocus_process = Process(target=call_auto_focus, args=(LIST_PID_BROWSERS, ))
#     PID_PROCESS_AUTOFOCUS = autofocus_process.pid
#     autofocus_process.start()
#
#
# async def run_process_and_reply_after(message: types.Message, data: StructData):
#     logger.info("runner process")
#
#     reddit_link = data.reddit_link
#     upvote_int = data.upvote_int
#     with Manager() as manager:
#         LIST_PID_BROWSERS = manager.list()
#         run_process_autofocus(LIST_PID_BROWSERS)
#
#         with ProcessPoolExecutor() as executor:
#             q = await asyncio.get_running_loop().run_in_executor(executor, start_reddit_work, reddit_link, upvote_int, LIST_PID_BROWSERS)
#
#     if q:
#         # await bot.send_message(message.from_user.id, q)
#         await message.reply(q)
#         return

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
