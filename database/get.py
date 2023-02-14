from work_fs import path_near_exefile
from .models import RedditLink, db, Cookie, Account


def db_get_link_id(link_from_file) -> RedditLink:
    # this func work in handl_info->get_links
    # get list id by list text
    with db:
        link_obj = RedditLink.get_or_create(link=link_from_file)[0]

    return link_obj


def db_get_text_link_by_id(link_id) -> str:
    # get link by id
    with db:
        link_obj = RedditLink.get_by_id(link_id)

    return link_obj.link


def db_get_cookie_proxy(account_obj):

    dict_proxy: dict[str, Cookie] = {
        "host": account_obj.proxy.host,
        "port": account_obj.proxy.port,
        "user": account_obj.proxy.user,
        "password": account_obj.proxy.password,
    }

    path_cookie = path_near_exefile(account_obj.cookie_path)
    id_account = account_obj.id

    return path_cookie, dict_proxy, id_account


def db_get_number_of_records_account() -> int:
    with db:
        return len(Cookie.select())


def db_get_account_by_id(id_cookies) -> Account:
    acc_obj: Account = Account.get_by_id(id_cookies)
    return acc_obj


def db_get_cookie_objs() -> list:
    with db:
        return Cookie.select().order_by(Cookie.cookie_path)
