from peewee import DoesNotExist

from SETTINGS import mine_project
from work_fs import path_near_exefile
from .models import RedditLink, db, Cookie, Account


def db_get_link_id(link_from_file) -> RedditLink:
    # this func work in handl_info->get_links
    # get list id by list text
    link_obj: RedditLink
    if mine_project:
        with db:
            try:
                link_obj = RedditLink.get(link=link_from_file)
            except DoesNotExist:
                link_obj = RedditLink.create(link=link_from_file)
    else:
        with db:
            link_obj, created = RedditLink.get_or_create(link=link_from_file)

    return link_obj


def db_get_text_link_by_id(link_id) -> str:
    # get link by id
    with db:
        link_obj = RedditLink.get_by_id(link_id)

    return link_obj.link


def db_get_cookie_proxy(cookie_db_obj: Cookie):
    proxy_obj = cookie_db_obj.proxy
    account_obj = cookie_db_obj.account

    dict_proxy: dict[str, Cookie] = {
        "host": proxy_obj.host,
        "port": proxy_obj.port,
        "user": proxy_obj.user,
        "password": proxy_obj.password,
    }

    log_pswd = {
        "login": account_obj.login,
        "password": account_obj.password,
    }

    path_cookie = path_near_exefile(cookie_db_obj.cookie_path)

    return path_cookie, dict_proxy, log_pswd


def db_get_account_by_id(id_cookies) -> dict:
    acc_obj: Account = Account.get_by_id(id_cookies)

    account_dict = {
        "login": acc_obj.login,
        "password": acc_obj.password
    }
    return account_dict


def db_get_cookie_objs() -> list[Cookie]:
    with db:
        return Cookie.select().order_by(Cookie.id)

