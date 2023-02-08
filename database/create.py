from .models import db, Proxy, WorkAccountWithLink, Cookie, RedditLink, Account


def create_db():
    with db:
        db.create_tables([Proxy, WorkAccountWithLink, RedditLink, Cookie, Account])


def create_proxy(proxy: dict):
    with db:
        in_db_proxy = Proxy.create(**proxy)

    return in_db_proxy


def create_cookie(path_cookie, proxy_obj: Proxy, account_obj: Account):
    with db:
        Cookie.create(cookie_path=path_cookie, proxy=proxy_obj, account=account_obj)


def create_account(account: dict):
    with db:
        account_obj = Account.create(**account)

    return account_obj
