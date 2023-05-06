import asyncio

from NW_Upvoter.db_tortories_orm.db_connect import db_connection_required
from NW_Upvoter.db_tortories_orm.models import Cookie
from NW_Upvoter.db_tortories_orm.query.link import db_get_or_create_link_obj


@db_connection_required
async def get_unlinked_cookies(link_obj) -> list[Cookie]:
    # Запит на отримання cookies, які не мають зв'язку з link_obj в таблиці WorkAccountWithLink
    cookies = await Cookie.filter(is_selected=False, ban__isnull=True).prefetch_related("proxy", "work_accounts")

    unlinked_cookies = [
        cookie for cookie in cookies
        if not any(wa.link_id == link_obj.id for wa in cookie.work_accounts)
    ]

    return unlinked_cookies


async def main():
    url = 'https://www.reddit.com/r/DadWouldBeProud/comments/138yk77/this_gift_is_ready_to_unpack/?utm_source=share&utm_medium=web2x&context=3'
    link_obj = await db_get_or_create_link_obj(url)

    unlinked_cookies = await get_unlinked_cookies(link_obj)
    print(len(unlinked_cookies))


if __name__ == '__main__':
    asyncio.run(main())


# TODO screenshot this site
# 'https://kipling.com.au/product/art-m-jessica-large-tote/KI47786JB.html'

# from SETTINGS import db
# from database import Cookie
#
# with db:
#     cookies_db_objs = Cookie.select().where((Cookie.is_selected == False) & (Cookie.ban.is_null(True)))
#     print(len(cookies_db_objs))
#     for cookie_obj in cookies_db_objs:
#         print(cookie_obj.account.login)
#         # Cookie.update(is_selected=0).where(Cookie.id == cookie_obj.id).execute()
#


# базу данньіх
# 1 тг бот ник уникальньій ключ
# оплата и когда автоматически отключать
#  приход и расход кто сколько получил чколько на что тратиться (прокси и сервера)


