import asyncio

from typing import NamedTuple
from multiprocessing import Process

from loguru import logger

from aiogram import types
from aiogram.fsm.state import State, StatesGroup

from Uprove_TG_Bot.TG_bot.src.telegram.messages.user_msg import MESSAGES
from main_Reddit import start_reddit_work


# from .messages import MESSAGES
class RunBotStates(StatesGroup):
    reddit_link = State()
    upvote_int = State()
    comments_int = State()


class StructData(NamedTuple):
    reddit_link: str
    upvote_int: int
    comments_int: int


async def run_process_and_reply_after(message: types.Message, data: StructData):
    logger.info("runner process")

    reddit_link = data.reddit_link
    upvote_int = data.upvote_int
    comments_int = data.comments_int

    proc = Process(target=start_reddit_work, args=(reddit_link, upvote_int, comments_int))
    proc.start()

    while proc.is_alive():
        await asyncio.sleep(1)

    await message.reply(MESSAGES['finish_process'])
