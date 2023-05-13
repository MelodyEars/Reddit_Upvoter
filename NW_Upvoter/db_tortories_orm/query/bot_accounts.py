
from NW_Upvoter.db_tortories_orm.db_connect import db_connection_required
from NW_Upvoter.db_tortories_orm.models import Cookie
from tortoise.transactions import in_transaction


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


# ________________________________________ UPDATE BOT ACCOUNTS ________________________________________
@db_connection_required
async def db_save_1_by_id(id_cookie):
    async with in_transaction():
        await Cookie.filter(id=id_cookie).update(is_selected=1)


@db_connection_required
async def db_update_0_by_id(id_cookie):
    async with in_transaction():
        await Cookie.filter(id=id_cookie).update(is_selected=0)

@db_connection_required
async def db_update_0_all():
    async with in_transaction():
        await Cookie.all().update(is_selected=0)
