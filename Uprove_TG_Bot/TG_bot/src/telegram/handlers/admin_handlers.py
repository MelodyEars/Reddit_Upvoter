from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from Uprove_TG_Bot.TG_bot.setup import admin_router
# from database.vote_tg_bot.db_tg_bot import AllowedUser
from Uprove_TG_Bot.TG_bot.src.telegram.handlers.fsm_h.block_user import DeleteUser, AddUser
from Uprove_TG_Bot.TG_bot.src.telegram.messages.admin_msg import admin_MESSAGES
from database.vote_tg_bot.db_tg_bot.tables import AllowedUser


@admin_router.message(Command(commands='admin'))
async def test(message: Message):
    await message.answer(admin_MESSAGES['cmd_admin'])


@admin_router.message(Command(commands='delete_user'))
async def test(message: Message, state: FSMContext):
    await message.answer(admin_MESSAGES['send_username'])
    await state.set_state(DeleteUser.username)


@admin_router.message(Command(commands='add_user'))
async def test(message: Message, state: FSMContext):
    await message.answer(admin_MESSAGES['send_username'])
    await state.set_state(AddUser.username)


@admin_router.message(Command(commands='all_users'))
async def test(message: Message, state: FSMContext):
    users_msg = [f'`{user.username}`' for user in AllowedUser.select()]
    await message.answer('\n'.join(users_msg), parse_mode='MARKDOWN')
