import asyncio

from loguru import logger

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from SETTINGS import tuple_admins_id

from .messages import MESSAGES
from .markups import mainMenu, returnMain
from .utils import RunBotStates
from .create import bot, dp
from .work_PROCESS import run_process_and_reply_after


@dp.message_handler(commands="start")
async def start(message: types.Message):
	logger.info("Start")
	await message.reply(MESSAGES['start'])
	await bot.send_message(message.from_user.id, f"Вітаю, {message.from_user.first_name}", reply_markup=mainMenu)


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
	await RunBotStates.reddit_link.set()
	await message.reply(MESSAGES['reddit_link'])


# catch up user's link answer
@dp.message_handler(state=RunBotStates.reddit_link)
async def answer_link(message: types.Message, state: FSMContext):
	logger.info('answering for link')
	await RunBotStates.next()
	await state.update_data(reddit_link=message.text)

	await message.reply(MESSAGES['upvote_int'])


@dp.message_handler(lambda message: not message.text.isdigit(), state=RunBotStates.upvote_int)
async def vote_invalid(message: types.Message):
	""" Caught up error if upvote_int not integer """
	return await message.reply(MESSAGES['error_vote_int'])


# catch user's upvote integer
@dp.message_handler(lambda message: message.text.isdigit(), state=RunBotStates.upvote_int)
async def answer_vote(message: types.Message, state: FSMContext):
	logger.info("How much upvote")
	# await state.update_data(upvote_int=int(message.text))
	async with state.proxy() as data:  # save result to dict FSM state
		data['upvote_int'] = int(message.text)

	await RunBotStates.next()
	await message.reply(MESSAGES['comments_int'])


@dp.message_handler(lambda message: not message.text.isdigit(), state=RunBotStates.comments_int)
async def comment_invalid(message: types.Message):
	""" Caught up error if comments_int not integer """
	return await message.reply(MESSAGES['error_comments_int'])


# catch user's upvote integer
@dp.message_handler(lambda message: message.text.isdigit(), state=RunBotStates.comments_int)
async def answer_comment(message: types.Message, state: FSMContext):
	async with state.proxy() as data:  # save result to dict FSM state
		logger.info("comments?")
		data['comments_int'] = int(message.text)  # write data

		message_for_finish = await message.reply(MESSAGES['start_process'])

		logger.info("Process starting")
		runner_process = asyncio.create_task(run_process_and_reply_after(message_for_finish, data))

	await state.finish()

	await message.reply(f'Браузер запустився для опрацювання вашого посилання {data["reddit_link"]}.', reply_markup=mainMenu)
	await runner_process
