from multiprocessing import Process

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loguru import logger

from TG_bot.messages import MESSAGES
from TG_bot.markups import mainMenu, returnMain
from TG_bot.utils import RunBotStates
from TG_bot.config import bot, dp
from main_Reddit import main_Reddit


@dp.message_handler(commands="start")
async def start(message: types.Message):
	logger.info("Start")
	# if exists_user(message.from_user.id):
	await message.reply(MESSAGES['start'])
	await bot.send_message(message.from_user.id, f"Вітаю, {message.from_user.first_name}", reply_markup=mainMenu)
	# else:
	# 	await bot.send_message(message.from_user.id, "Ви не зареєстровані, зверніться до https://t.me/no_chance_o")
	#   raise Exception("Хтось зайшов не зареєстрований ")


@dp.message_handler(commands='help')
async def helper(message: types.Message):
	logger.info("help")
	await message.reply(MESSAGES['help'])


@dp.message_handler(state='*', commands='⬅️ Все спочатку')
@dp.message_handler(Text(equals='⬅️ Все спочатку', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
	logger.info("reseting Fms '⬅️ Все спочатку'")
	current_state = await state.get_state()
	if current_state is None:
		return

	# Cancel state and inform user about it
	await state.finish()

	# And remove keyboard (just in case)
	await message.reply('Cancelled.', reply_markup=mainMenu)


@dp.message_handler(Text(equals='Поїхали!🚀', ignore_case=True), state='*')
async def starter(message: types.Message):
	logger.info('Поїхали!🚀')
	await bot.send_message(message.from_user.id, "Поїхали!🚀", reply_markup=returnMain)  # navigation
	await RunBotStates.link.set()
	await message.reply(MESSAGES['link'])


# catch up user's link answer
@dp.message_handler(state=RunBotStates.link)
async def answer_link(message: types.Message, state: FSMContext):
	logger.info('answering for link')
	async with state.proxy() as data:  # save result to dict FSM state
		data['link'] = message.text

	await RunBotStates.next()
	await message.reply(MESSAGES['vote_int'])


# catch user's upvote integer
@dp.message_handler(state=RunBotStates.vote_int)
async def answer_vote(message: types.Message, state: FSMContext):
	logger.info("How much upvote")
	async with state.proxy() as data:  # save result to dict FSM state
		data['vote_int'] = message.text

	await RunBotStates.next()
	await message.reply(MESSAGES['comments_int'])


# catch user's upvote integer
@dp.message_handler(state=RunBotStates.comments_int)
async def answer_comment(message: types.Message, state: FSMContext):
	async with state.proxy() as data:  # save result to dict FSM state
		logger.info("comments?")
		data['comments_int'] = message.text

	async with state.proxy() as data:  # save result to dict FSM state
		logger.info("Process starting")
		Process(target=main_Reddit, args=(data['link'], data['vote_int'], data['comments_int'],)).start()
		logger.info(f"Process did started on the {data['link']}")

	await state.finish()

	await message.reply(f'Браузер запустився для опрауювання вашого посилання {data["link"]}.', reply_markup=mainMenu)
