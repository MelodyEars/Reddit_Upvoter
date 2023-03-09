import asyncio
from multiprocessing import freeze_support

from loguru import logger

from TG_bot.work_PROCESS import on_process_finished
from work_fs import path_near_exefile
from TG_bot import dp


async def on_startup(_):
	logger.info("Bot online")


@logger.catch
async def run_tg_bot():
	asyncio.create_task(on_process_finished())
	await dp.start_polling(skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
	freeze_support()

	logger.add(
		path_near_exefile("TgBot.log"),
		format="{time} {level} {message}",
		level="INFO",
		rotation="10 MB",
		compression="zip"
	)

	asyncio.run(run_tg_bot())
