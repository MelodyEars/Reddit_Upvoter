import random

import work_fs
from .models import Proxy, Cookie, db


def create_db():
    with db:
        db.create_tables([Proxy, Cookie])


def save_proxy(proxy):
    with db:
        in_db_proxy = Proxy.create(**proxy)

    return in_db_proxy


def save_cookie(path_cookie, in_db_proxy):
    with db:
        Cookie.create(cookie_path=path_cookie, proxy=in_db_proxy)


####################### for this project #################

def db_get_random_obj_with_0():
    with db:
        random_account = random.choice(Cookie.select().where(Cookie.is_work == 0))
        return random_account


def db_reset_all_1_on_0():
    with db:
        Cookie.update(is_work=0).where(Cookie.is_work == 1).execute()


def db_save_1_by_id(id_cookie):
    with db:
        Cookie.update(is_work=1).where(Cookie.id == id_cookie).execute()


def db_delete_by_id(id_cookie):
    with db.atomic():
        proxy_for_save = Proxy.get(Proxy(id_cookie))
        # Save as str to file
        proxy_as_str = f"{proxy_for_save.host}:{proxy_for_save.port}:{proxy_for_save.user}:{proxy_for_save.password}"
        path_filename = work_fs.path_near_exefile("working_proxy_after_ban.txt")
        work_fs.write_line(path_filename, proxy_as_str)
        # delete from tabel
        Cookie.delete().where(Cookie.id == id_cookie).execute()
        Proxy.delete().where(Proxy.id == id_cookie).execute()


def db_get_cookie_proxy():
    db_obj = db_get_random_obj_with_0()

    dict_proxy = {
        "host": db_obj.proxy.host,
        "port": db_obj.proxy.port,
        "user": db_obj.proxy.user,
        "password": db_obj.proxy.password,
    }

    path_cookie = db_obj.cookie_path
    id_profile = db_obj.id

    return path_cookie, dict_proxy, id_profile
