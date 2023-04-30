import asyncio

from NW_Upvoter.db_tortories_orm.db_connect import connect_to_db
from NW_Upvoter.db_tortories_orm.models import Cookie


# ________________________________________ GET BOT ACCOUNTS ________________________________________
async def get_bot_accounts() -> list[Cookie]
    """Get all accounts from database via Tortoise ORM."""
    cookies_db_objs = await Cookie.filter(is_selected=False, ban__isnull=True)
    return cookies_db_objs


async def db_work():
    await connect_to_db()
    result = await get_bot_accounts()
    print(result)


if __name__ == '__main__':
    asyncio.run(db_work())

