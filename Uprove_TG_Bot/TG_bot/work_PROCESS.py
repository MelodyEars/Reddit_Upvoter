import queue
import asyncio
from threading import Thread

from typing import NamedTuple
# from multiprocessing import Process

from loguru import logger

from aiogram import types
from aiogram.fsm.state import State, StatesGroup

# from Uprove_TG_Bot.TG_bot.setup import bot
# from Uprove_TG_Bot.TG_bot.src.telegram.messages.user_msg import MESSAGES
from main_Reddit import start_reddit_work # MESSAGE_IN_TG


class RunBotStates(StatesGroup):
    reddit_link = State()
    upvote_int = State()
    # comments_int = State()


class StructData(NamedTuple):
    reddit_link: str
    upvote_int: int
    # comments_int: int


async def run_process_and_reply_after(message: types.Message, data: StructData):
    logger.info("runner process")
    # chat_id = message.chat.id
    # message.from_user.id
    # MESSAGE_IN_TG[chat_id] = False
    reddit_link = data.reddit_link
    upvote_int = data.upvote_int
    # comments_int = data.comments_int

    q = queue.Queue()

    thread = Thread(target=start_reddit_work, args=(reddit_link, upvote_int, q))  # , comments_int
    thread.start()

    while thread.is_alive():
        await asyncio.sleep(5)

    msg = q.get()

    if msg:
        # await bot.send_message(message.from_user.id, msg)
        await message.reply(msg)
        return

