from .models import db, Proxy, WorkAccountWithLink, Cookie, RedditLink, Account


def create_db() -> None:
    with db:
        db.create_tables([Proxy, WorkAccountWithLink, RedditLink, Cookie, Account])


def create_proxy(host, port, user, password):
    with db:
        in_db_proxy: Proxy = Proxy.create(host=host, port=port, user=user, password=password)

    return in_db_proxy


def create_cookie(path_cookie, proxy_obj: Proxy, account_obj: Account):
    with db:
        Cookie.create(cookie_path=path_cookie, proxy=proxy_obj, account=account_obj)


def create_account(login, password):
    with db:
        account_obj: Account = Account.create(login=login, password=password)

    return account_obj
