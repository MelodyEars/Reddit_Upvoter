from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Text, Command
# from aiogram import F
from NW_Upvoter.TG_bot.setup import user_router
from NW_Upvoter.TG_bot.src.telegram.buttons.user_btn import main_btn, cancel_btn
from NW_Upvoter.TG_bot.src.telegram.handlers.fsm_h.start_new_proc import RunBotStates
from NW_Upvoter.TG_bot.src.telegram.messages.user_msg import MESSAGES


@user_router.message(Command(commands='start'))
async def start(message: Message):
    # await message.answer(MESSAGES['start'])
    await message.reply(MESSAGES['hi_user'] + message.from_user.first_name, reply_markup=main_btn)


@user_router.message(Command(commands='start'))
async def helper(message: Message):
    await message.reply(MESSAGES['help'])


@user_router.message(Text(text=MESSAGES['btn_run_work'], ignore_case=True))
async def starter(message: Message, state: FSMContext):
    await message.answer(MESSAGES['btn_run_work'],)  # navigation
    # await RunBotStates.link.set()
    await state.set_state(RunBotStates.reddit_link)
    await message.reply(MESSAGES['reddit_link'], reply_markup=cancel_btn)
