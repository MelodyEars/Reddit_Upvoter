from aiogram.types import Message
# from setup import admin_router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from SETTINGS import mine_project
# from src.database.query.block_user import unblock_user, block_user
# from src.database.tables import AllowedUser

from NW_Upvoter.TG_bot.setup import admin_router
from NW_Upvoter.TG_bot.src.database.tables import AllowedUser
from NW_Upvoter.TG_bot.src.telegram.messages.admin_msg import admin_MESSAGES

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
        await message.reply(f"{message.text} " + admin_MESSAGES['deleted_user'],
                            parse_mode='MARKDOWN')
    else:
        await message.reply(admin_MESSAGES['user_denied'])

    await state.clear()


if mine_project:
    @admin_router.message(AddUser.username)
    async def unblock(message: Message, state: FSMContext):
        user, created = AllowedUser.get_or_create(username=message.text)

        if created:
            await message.reply(f"{message.text}" + admin_MESSAGES['added_user'],
                                parse_mode='MARKDOWN')
        else:
            await message.reply(admin_MESSAGES['has_access'])
        await state.clear()

else:
    @admin_router.message(AddUser.username)
    async def unblock(message: Message, state: FSMContext):
        added_users = AllowedUser.select()
        if len(added_users) <= 3:
            user, created = AllowedUser.get_or_create(username=message.text)

            if created:
                await message.reply(f"{message.text}" + admin_MESSAGES['added_user'],
                                    parse_mode='MARKDOWN')
            else:
                await message.reply(admin_MESSAGES['has_access'])
        else:
            await message.reply(admin_MESSAGES['has_many_user'])

        await state.clear()
