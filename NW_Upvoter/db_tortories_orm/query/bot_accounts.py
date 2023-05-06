import asyncio

from NW_Upvoter.db_tortories_orm.db_connect import connect_to_db, db_connection_required
from NW_Upvoter.db_tortories_orm.models import Cookie


# ________________________________________ GET BOT ACCOUNTS ________________________________________
@db_connection_required
async def get_bot_accounts() -> list[Cookie]:
    """Get all accounts from database via Tortoise ORM."""
    cookies_db_objs = await Cookie.filter(is_selected=False, ban__isnull=True).prefetch_related("proxy")
    return cookies_db_objs


@db_connection_required
async def get_unlinked_cookies(link_obj) -> list[Cookie]:
    # Запит на отримання cookies, які не мають зв'язку з link_obj в таблиці WorkAccountWithLink
    cookies = await Cookie.filter(is_selected=False,
                                  ban__isnull=True).prefetch_related("proxy",  "work_accounts", "account")

    unlinked_cookies = [cookie for cookie in cookies if
                        not any(wa.link_id == link_obj.id for wa in cookie.work_accounts)]

    return unlinked_cookies


# async def db_work():
#     await connect_to_db()
#     result = await get_bot_accounts()
#     for cookie_db_obj in result:
#         print(cookie_db_obj.proxy.host)
#
#
# if __name__ == '__main__':
#     asyncio.run(db_work())
