from typing import NamedTuple

from loguru import logger

from aiogram import types
from aiogram.fsm.state import State, StatesGroup

from NW_Upvoter.main_UPVOTER import start_reddit_work


class RunBotStates(StatesGroup):
    reddit_link = State()
    upvote_int = State()


class StructData(NamedTuple):
    reddit_link: str
    upvote_int: int


async def run_process_and_reply_after(message: types.Message, data: StructData):
    logger.info("runner process")

    reddit_link = data.reddit_link
    upvote_int = data.upvote_int
    await start_reddit_work(reddit_link, upvote_int, message)
    # with ProcessPoolExecutor(max_workers=2) as executor:
    #     q = await asyncio.get_running_loop().run_in_executor(executor, start_reddit_work, reddit_link, upvote_int)
    #
    # if q:
    #     await message.reply(q)
    #     return

# async def run_process_and_reply_after(message: types.Message, data: StructData):
#     logger.info("runner process")
#
#     reddit_link = data.reddit_link
#     upvote_int = data.upvote_int
#
#     with ProcessPoolExecutor(max_workers=2) as executor:
#         try:
#             q = await asyncio.wait_for(asyncio.get_running_loop().run_in_executor(executor, start_reddit_work, reddit_link, upvote_int), timeout=180)
#         except asyncio.TimeoutError:
#             logger.info("Timeout occurred. Restarting process...")
#             return await run_process_and_reply_after(message, data) # Рекурсивно перезапускає функцію, якщо вона завершилася через timeout
#
#     if q:
#         await message.reply(q)
#         return

# TODO 1 create link to db before body loop,
#  how many upvote need to put on.
# in this func await 3 minutes and if the one thread more then,kill process
