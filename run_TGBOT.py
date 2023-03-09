import asyncio
from multiprocessing import freeze_support

from aiogram.utils import executor
from loguru import logger

from TG_bot.work_PROCESS import on_process_finished
from work_fs import path_near_exefile
from TG_bot import dp


async def on_startup(_):
	# task = asyncio.create_task(on_process_finished())
	# await task
	logger.info("Bot online")


async def task_create():
	# Start the background task to handle process completion notifications
	await asyncio.run(on_process_finished())


@logger.catch
def run_tg_bot():
	asyncio.run(task_create())
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
	freeze_support()

	logger.add(
		path_near_exefile("TgBot.log"),
		format="{time} {level} {message}",
		level="INFO",
		rotation="10 MB",
		compression="zip"
	)
	run_tg_bot()
	# asyncio.run(run_tg_bot())
