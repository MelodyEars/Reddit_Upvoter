import asyncio
from multiprocessing import Process

from aiogram import types
from loguru import logger

from main_Reddit import start_reddit_work

from .messages import MESSAGES


async def run_process_and_reply_after(message: types.Message, data):
    logger.info("runner process")

    reddit_link = data['reddit_link']
    upvote_int = data['upvote_int']
    comments_int = data['comments_int']

    proc = Process(target=start_reddit_work, args=(reddit_link, upvote_int, comments_int))
    proc.start()

    while proc.is_alive():
        await asyncio.sleep(1)

    await message.reply(MESSAGES['finish_process'])
