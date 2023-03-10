from multiprocessing import freeze_support

from aiogram.utils import executor
from loguru import logger

from work_fs import path_near_exefile
from TG_bot import dp


async def on_startup(_):
	logger.info("Bot online")


@logger.catch
def run_tg_bot():
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
