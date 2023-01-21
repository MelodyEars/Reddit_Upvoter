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
