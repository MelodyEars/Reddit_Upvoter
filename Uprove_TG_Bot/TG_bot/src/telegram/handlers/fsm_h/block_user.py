from aiogram.types import Message
# from setup import admin_router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# from src.database.query.block_user import unblock_user, block_user
# from src.database.tables import AllowedUser

from Uprove_TG_Bot.TG_bot.setup import admin_router
from database.vote_tg_bot.db_tg_bot.tables import AllowedUser

blocked_users = []


class DeleteUser(StatesGroup):
    username = State()


class AddUser(StatesGroup):
    username = State()


@admin_router.message(DeleteUser.username)
async def block(message: Message, state: FSMContext):
    user = AllowedUser.get_or_none(username=message.text)
    if user:
        user.delete_instance()
        await message.reply(f"Юзер *{message.text}* видален 🦉",
                            parse_mode='MARKDOWN')
    else:
        await message.reply("Такого юзера не існує 🙉")

    await state.clear()


@admin_router.message(AddUser.username)
async def unblock(message: Message, state: FSMContext):
    user, created = AllowedUser.get_or_create(username=message.text)
    if created:
        await message.reply(f"Юзеру *{message.text}* наданий доступ до бота 👑",
                            parse_mode='MARKDOWN')
    else:
        await message.reply("Юзер вже має доступ 🙉")

    await state.clear()
