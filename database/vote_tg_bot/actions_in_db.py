from peewee import DoesNotExist

from SETTINGS import mine_project
from .models import WorkAccountWithLink, db, Cookie


def db_exist_record_link_account(link_id, cookie_id) -> (bool, WorkAccountWithLink):
    # check if id band with id link
    if mine_project:
        with db:
            obj: WorkAccountWithLink
            try:
                obj = WorkAccountWithLink.get(cookie=cookie_id, link=link_id)
                created = False
            except DoesNotExist:
                obj = WorkAccountWithLink.create(cookie=cookie_id, link=link_id)
                created = True
    else:
        with db:
            obj: WorkAccountWithLink
            created: bool
            obj, created = WorkAccountWithLink.get_or_create(cookie=cookie_id, link=link_id)

    # заменить запросом в бд если записи такой еще нет берем и делаем, делать вьіборку из записей у которьіх нет связей в бд с сьілкой
    return created, obj


def db_get_random_account_with_0() -> list[Cookie]:
    with db:
        cookies_db_objs = Cookie.select().where((Cookie.is_selected == False) & (Cookie.ban.is_null(True)))

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
    if mine_project:
        with db.transaction():
            for i in range(0, len(cookies_to_update), 1000):
                Cookie.bulk_update(cookies_to_update[i:i + 1000], fields=['ban'])
    else:
        with db.atomic():
            for i in range(0, len(cookies_to_update), 1000):
                Cookie.bulk_update(cookies_to_update[i:i + 1000], fields=['ban'])

