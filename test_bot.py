import asyncio
import time
import multiprocessing as mp
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from loguru import logger

TOKEN = "6296457111:AAF-WRfX5OhpJehvd2hTS_3iAmQUB-yH9Yw"
CHAT_ID = "487950394"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
processes = {}

async def on_process_finished(chat_id, process_name):
    processes.pop(chat_id)
    message = f"Process '{process_name}' has finished"
    await bot.send_message(chat_id, message)

@dp.message_handler(commands=['start_process'])
async def start_process(message: types.Message):
    chat_id = message.chat.id
    process_name = message.text.split()[-1]

    if chat_id in processes:
        await message.reply("You have already started a process")
        return
    logger.info('start_process')
    process = mp.Process(target=long_task, args=(chat_id, process_name))
    process.start()
    processes[chat_id] = process

    await message.reply(f"Process '{process_name}' has started")

def long_task(chat_id, process_name):
    # Simulating a long-running task
    for i in range(5):
        time.sleep(1)
        print(f"{process_name} is running...")

    asyncio.run(on_process_finished(chat_id, process_name))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
