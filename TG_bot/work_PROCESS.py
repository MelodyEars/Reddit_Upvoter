from multiprocessing import Queue, Process

from main_Reddit import start_reddit_work

from .handlers import bot

queue = Queue()


async def on_process_finished():
    chat_id, message_id, proces_message = queue.get()  # очікуємо на сигнал з черги
    """When process finish send edit message for process"""
    await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=proces_message
    )


async def start_process(data: dict, chat_id, message_id):
    Process(
        target=start_reddit_work, args=(data['link'], data['vote_int'], data['comments_int'], queue, chat_id, message_id)
    ).start()
