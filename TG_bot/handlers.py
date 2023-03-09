from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from loguru import logger

from SETTINGS import tuple_admins_id

from .messages import MESSAGES
from .markups import mainMenu, returnMain
from .utils import RunBotStates
from .create import bot, dp
from .work_PROCESS import start_process, on_process_finished


@dp.message_handler(commands="start")
async def start(message: types.Message):
	logger.info("Start")
	if message.from_user.id in tuple_admins_id:
		await message.reply(MESSAGES['start'])
		await bot.send_message(message.from_user.id, f"Вітаю, {message.from_user.first_name}", reply_markup=mainMenu)

	# else:
		# await bot.send_message(message.from_user.id, "Ви не зареєстровані, зверніться до https://t.me/no_chance_o")
		# raise Exception("Хтось зайшов не зареєстрований ")


@dp.message_handler(commands='help')
async def helper(message: types.Message):
	logger.info("help")
	await message.reply(MESSAGES['help'])


@dp.message_handler(state='*', commands='reset')
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
	# async with state.proxy() as data:  # save result to dict FSM state
	# 	data['link'] = message.text
	await RunBotStates.next()
	await state.update_data(link=message.text)

	await message.reply(MESSAGES['vote_int'])


@dp.message_handler(lambda message: not message.text.isdigit(), state=RunBotStates.vote_int)
async def vote_invalid(message: types.Message):
	""" Caught up error if vote_int not integer """
	return await message.reply(MESSAGES['error_vote_int'])


# catch user's upvote integer
@dp.message_handler(lambda message: message.text.isdigit(), state=RunBotStates.vote_int)
async def answer_vote(message: types.Message, state: FSMContext):
	# if message.text.isdigit():
	logger.info("How much upvote")
	# await state.update_data(vote_int=int(message.text))
	async with state.proxy() as data:  # save result to dict FSM state
		data['vote_int'] = int(message.text)

	await RunBotStates.next()
	await message.reply(MESSAGES['comments_int'])
	# else:
	# 	return await message.reply(MESSAGES['error_vote_int'])


@dp.message_handler(lambda message: not message.text.isdigit(), state=RunBotStates.comments_int)
async def comment_invalid(message: types.Message):
	""" Caught up error if comments_int not integer """
	return await message.reply(MESSAGES['error_comments_int'])


# catch user's upvote integer
@dp.message_handler(lambda message: message.text.isdigit(), state=RunBotStates.comments_int)
async def answer_comment(message: types.Message, state: FSMContext):
	# if message.text.isdigit():
	async with state.proxy() as data:  # save result to dict FSM state
		logger.info("comments?")
		data['comments_int'] = int(message.text)  # write data

		# send message for edited when process finish work
		message_for_finish = await bot.send_message(chat_id=message.chat.id, text=MESSAGES['start_process'])

		logger.info("Process starting")
		await start_process(data=data, message_for_finish=message_for_finish)
		logger.info(f"Process did started on the {data['link']}")
		await on_process_finished()

	await state.finish()

	await message.reply(f'Браузер запустився для опрацювання вашого посилання {data["link"]}.', reply_markup=mainMenu)

	# else:
	# 	return await message.reply(MESSAGES['error_comments_int'])
