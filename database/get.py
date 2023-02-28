from handl_info import check_proxy
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


def db_get_cookie_proxy(cookie_obj: Cookie):

    dict_proxy: dict[str, Cookie] = {
        "host": cookie_obj.proxy.host,
        "port": cookie_obj.proxy.port,
        "user": cookie_obj.proxy.user,
        "password": cookie_obj.proxy.password,
    }
    check_proxy(**dict_proxy)

    path_cookie = path_near_exefile(cookie_obj.cookie_path)
    id_account = cookie_obj.id

    return path_cookie, dict_proxy, id_account


def db_get_account_by_id(id_cookies: Cookie) -> dict:
    acc_obj: Account = Account.get_by_id(id_cookies)

    account_dict = {
        "login": acc_obj.login,
        "password": acc_obj.password
    }
    return account_dict


def db_get_cookie_objs() -> list:
    with db:
        return list(Cookie.select())
