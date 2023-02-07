from .models import db, Proxy, WorkAccountWithLink, Cookie, RedditLink


def create_db():
    with db:
        db.create_tables([Proxy, WorkAccountWithLink, RedditLink, Cookie]) # , Account,


def create_proxy(proxy):
    with db:
        in_db_proxy = Proxy.create(**proxy)

    return in_db_proxy


def create_cookie(path_cookie, in_db_proxy):
    with db:
        Cookie.create(cookie_path=path_cookie, proxy=in_db_proxy)

