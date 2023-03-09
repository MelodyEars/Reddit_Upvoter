import asyncio
from multiprocessing import Queue, Process

from loguru import logger

from main_Reddit import start_reddit_work

from .create import user_queues
from .handlers import bot


# Background task to handle process completion notifications
async def on_process_finished():
    while True:
        # Check if there are any finished processes in the queues
        for message_for_finish, queue in user_queues.items():
            if not queue.empty():
                # Get the message from the queue and send it to the user
                message_for_finish, proces_message = queue.get()
                message_id = message_for_finish.message_id
                chat_id = message_for_finish.chat.id

                """When process finish send edit message for process"""
                await bot.edit_message_text(
                    chat_id=chat_id, message_id=message_id, text=proces_message
                )

        # Sleep for a short time to avoid consuming too much CPU
        await asyncio.sleep(0.1)


async def start_process(data: dict, message_for_finish):

    if message_for_finish not in user_queues:
        logger.info(message_for_finish)
        user_queues[message_for_finish] = Queue()

        Process(
            target=start_reddit_work,
            args=(data['link'], data['vote_int'], data['comments_int'],
                  message_for_finish, user_queues[message_for_finish])
        ).start()
