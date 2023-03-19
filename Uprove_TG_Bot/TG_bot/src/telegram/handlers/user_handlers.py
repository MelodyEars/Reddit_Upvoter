from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Text, Command
# from aiogram import F
from Uprove_TG_Bot.TG_bot.setup import user_router
from Uprove_TG_Bot.TG_bot.src.telegram.buttons.user_btn import main_btn, cancel_btn
from Uprove_TG_Bot.TG_bot.src.telegram.handlers.fsm_h.start_new_proc import RunBotStates
from Uprove_TG_Bot.TG_bot.src.telegram.messages.user_msg import MESSAGES


@user_router.message(Command(commands='start'))
async def start(message: Message):
    # await message.answer(MESSAGES['start'])
    await message.reply(f"Вітаю, {message.from_user.first_name}",
                        reply_markup=main_btn)


@user_router.message(Command(commands='start'))
async def helper(message: Message):
    await message.reply(MESSAGES['help'])


@user_router.message(Text(text='Поїхали!🚀', ignore_case=True))
async def starter(message: Message, state: FSMContext):
    await message.answer("Поїхали!🚀",)  # navigation
    # await RunBotStates.link.set()
    await state.set_state(RunBotStates.reddit_link)
    await message.reply(MESSAGES['reddit_link'], reply_markup=cancel_btn)
