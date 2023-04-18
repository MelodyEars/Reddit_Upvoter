from loguru import logger
from peewee import fn

from .models import WorkAccountWithLink, db, Cookie

# from SETTINGS import mine_project


def db_exist_record_link_account(link_id, cookie_id):
    # check if id band with id link
    with db:
        obj: WorkAccountWithLink
        created: bool
        obj, created = WorkAccountWithLink.get_or_create(cookie=cookie_id, link=link_id)
    # заменить запросом в бд если записи такой еще нет берем и делаем, делать вьіборку из записей у которьіх нет связей в бд с сьілкой
    return created, obj


# def db_reset_work_all_accounts_1_on_0():
#     with db:
#         Cookie.update(is_selected=0).where(Cookie.is_selected == 1).execute()


def db_get_random_account_with_0() -> list[Cookie]:
    with db:
        cookies_db_objs = Cookie.select().where((Cookie.is_selected == False) & (Cookie.ban.is_null(True)))

        # if mine_project:
        #
        #  compare list selected models and cookies_db_objs then return,
        #  but this method work if remove method delete after add model

    return cookies_db_objs


def db_ban_add(DICT_ACC_BAN: dict):
    # Створіть список об'єктів Cookie, які потрібно оновити
    cookies_to_update = []

    for acc_path_cookie, ban_cond in DICT_ACC_BAN.items():
        cookie = Cookie.get_or_none(Cookie.cookie_path == acc_path_cookie)
        if cookie:
            cookie.ban = ban_cond
            cookies_to_update.append(cookie)

    # Виконати оновлення списку об'єктів за допомогою bulk_update
    with db.atomic():
        for i in range(0, len(cookies_to_update), 1000):
            Cookie.bulk_update(cookies_to_update[i:i + 1000], fields=['ban'])

