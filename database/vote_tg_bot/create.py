from SETTINGS import mine_project
from .models import db, Proxy, Cookie, Account


def create_db() -> None:
    with db:
        db.create_tables([Proxy, Cookie, Account])


def create_proxy(host, port, user, password):
    if mine_project:
        with db.transaction():
            in_db_proxy: Proxy = Proxy.create(host=host, port=port, user=user, password=password)
    else:
        with db:
            in_db_proxy: Proxy = Proxy.create(host=host, port=port, user=user, password=password)

    return in_db_proxy


def create_cookie(path_cookie, proxy_obj: Proxy, account_obj: Account):
    if mine_project:
        with db.transaction():
            Cookie.create(cookie_path=path_cookie, proxy=proxy_obj, account=account_obj)
    else:
        with db:
            Cookie.create(cookie_path=path_cookie, proxy=proxy_obj, account=account_obj)


def create_account(login, password):
    if mine_project:
        with db.transaction():
            account_obj: Account = Account.create(login=login, password=password)

    else:
        with db:
            account_obj: Account = Account.create(login=login, password=password)

    return account_obj
