import asyncio
import time
from multiprocessing import Process, Queue
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = 'BOT TOKEN HERE'
chat_id = 'CHAT ID HERE'
queue = Queue()


async def on_process_finished():
    while True:
        process, result = queue.get()
        text = f"Process {process.pid} finished with result {result}"
        bot = Bot(token=TOKEN)
        await bot.send_message(chat_id, text)


async def run_command(cmd):
    start_time = time.time()
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await process.communicate()
    elapsed_time = time.time() - start_time

    return_code = process.returncode
    return stdout.decode(), stderr.decode(), elapsed_time, return_code


async def start_process(cmd):
    loop = asyncio.get_event_loop()
    task = loop.create_task(run_command(cmd))
    queue.put_nowait((await asyncio.ensure_future(task), task.result()))


async def on_startup(dp):
    asyncio.create_task(on_process_finished())


if __name__ == '__main__':
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)
    dp.register_message_handler(start_process, commands="run")

    executor.start_polling(dp, on_startup=on_startup)
