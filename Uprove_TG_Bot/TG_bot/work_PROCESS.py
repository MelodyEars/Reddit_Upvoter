import asyncio

from typing import NamedTuple
from concurrent.futures import ProcessPoolExecutor

from loguru import logger

from aiogram import types
from aiogram.fsm.state import State, StatesGroup


from Uprove_TG_Bot.main_Reddit import start_reddit_work  # MESSAGE_IN_TG


class RunBotStates(StatesGroup):
    reddit_link = State()
    upvote_int = State()
    # comments_int = State()


class StructData(NamedTuple):
    reddit_link: str
    upvote_int: int


async def run_process_and_reply_after(message: types.Message, data: StructData):
    logger.info("runner process")

    reddit_link = data.reddit_link
    upvote_int = data.upvote_int

    with ProcessPoolExecutor() as executor:
        msg = await asyncio.get_running_loop().run_in_executor(executor, start_reddit_work, reddit_link, upvote_int)

    if msg:
        await message.reply(msg)
        return
