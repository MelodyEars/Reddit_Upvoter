import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from loguru import logger

import markups as nav


TOKEN = "6296457111:AAF-WRfX5OhpJehvd2hTS_3iAmQUB-yH9Yw"

# initalization bot
# bot = Bot(token=os.getenv('TOKEN'))
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# first func with decorator
@dp.message_handler(commands=['start'])  # means event, when anybody sends to tg_bot message
async def command_start(message: types.Message):
	await bot.send_message(message.from_user.id, f"Вітаю, {message.from_user.first_name}", reply_markup=nav.mainMenu)


@dp.message_handler()  # means event, when anybody sends to tg_bot message
async def command_other(message: types.Message):
	print(message.text[2:9])
	if message.text[2:9] == 'Каталог':
		await bot.send_message(message.from_user.id, "Каталог", reply_markup=nav.otherMenu)
	elif message.text == "⬅️ Все спочатку":
		await bot.send_message(message.from_user.id, "⬅️ Все спочатку", reply_markup=nav.mainMenu)
	else:
		await bot.send_message(message.from_user.id, "Інше")

if __name__ == '__main__':

	# command for run tg_bot
	executor.start_polling(dp, skip_updates=True)
	# skip_updates=True need for our bot. When it's not in online, and when it's will be online, sended many error
