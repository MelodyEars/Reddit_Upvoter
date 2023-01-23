import random

import work_fs
from models import Proxy, Cookie, db


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

def get_db_cookie_proxy():
    with db:
        res = random.choice(Cookie.select().where(Cookie.is_work == 0))
        # print(res.proxy.host)
        res.delete()


def reset_all_1_on_0():
    with db:
        Cookie.update(is_work=0).where(Cookie.is_work == 1).execute()


def save_by_id(id_cookie):
    with db:
        Cookie.update(is_work=1).where(Cookie.id == id_cookie).execute()


def delete_by_id(id_cookie):
    with db.atomic():
        proxy_for_save = Proxy.get(Proxy(id_cookie))
        # Save as str to file
        proxy_as_str = f"{proxy_for_save.host}:{proxy_for_save.port}:{proxy_for_save.user}:{proxy_for_save.password}"
        path_filename = work_fs.path_near_exefile("working_proxy_after_ban.txt")
        work_fs.write_line(path_filename, proxy_as_str)
        # delete from tabel
        Cookie.delete().where(Cookie.id == id_cookie).execute()
        Proxy.delete().where(Proxy.id == id_cookie).execute()


if __name__ == '__main__':
    get_db_cookie_proxy()