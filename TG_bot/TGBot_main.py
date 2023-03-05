from aiogram.utils import executor

from loguru import logger
from handlers import dp


async def on_startup(_):
	logger.info("Bot online")


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
