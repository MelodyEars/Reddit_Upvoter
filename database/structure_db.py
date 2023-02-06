import random

from work_fs import write_line, path_near_exefile

from base_exception import RanOutAccountsForLinkException

from .models import Proxy, RedditLink, Cookie, WorkAccountWithLink, Account, db


def create_db():
    with db:
        db.create_tables([Proxy, WorkAccountWithLink, Cookie, RedditLink, Account])


def create_proxy(proxy):
    with db:
        in_db_proxy = Proxy.create(**proxy)

    return in_db_proxy


def create_cookie(path_cookie, in_db_proxy):
    with db:
        Cookie.create(cookie_path=path_cookie, proxy=in_db_proxy)


def db_save_proxy_cookie(proxy_from_api, cookie_path):
    if len(Cookie.select().where(Cookie.cookie_path == cookie_path)) == 0:
        proxy_in_db = create_proxy(proxy_from_api)
        create_cookie(cookie_path, proxy_in_db)
    else:
        write_line("proxies.txt", ":".join((proxy_from_api['host'], proxy_from_api['port'],
                                            proxy_from_api['user'], proxy_from_api['password'])))


def db_get_link_id(link_from_file) -> RedditLink:
    # this func work in handl_info->get_links
    # get list id by list text
    with db:
        link_obj = RedditLink.get_or_create(link=link_from_file)[0]

    return link_obj


def db_text_link_by_id(link_id) -> str:
    # get link by id
    with db:
        link_obj = RedditLink.get_by_id(link_id)

    return link_obj.link


def db_exist_record_link_account(link_id, account_id):
    # check if id band with id link
    with db:
        obj: WorkAccountWithLink
        obj, created = WorkAccountWithLink.get_or_create(account=account_id, link=link_id)

    return created, obj.id


def db_delete_record_work_account_with_link(id_record):
    # obj.id if needed to delete when exception exists
    with db:
        WorkAccountWithLink.delete_by_id(id_record)


def db_delete_accounts_by_id(id_account):
    with db.atomic():
        proxy_for_save = Proxy.get_by_id(id_account)
        # Save as str to file
        proxy_as_str = f"{proxy_for_save.host}:{proxy_for_save.port}:{proxy_for_save.user}:{proxy_for_save.password}"
        path_filename = path_near_exefile("working_proxy_after_ban.txt")
        write_line(path_filename, proxy_as_str)

        # delete all by index from account
        WorkAccountWithLink.delete().where(WorkAccountWithLink.account == id_account)

        # delete from tabel
        Cookie.delete_by_id(id_account)
        Proxy.delete_by_id(id_account)


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


def db_number_of_records_account() -> int:
    with db:
        return len(Cookie.select())


def db_reset_work_all_accounts_1_on_0():
    with db:
        Cookie.update(is_selected=0).where(Cookie.is_selected == 1).execute()


def db_get_random_account_with_0() -> Cookie:
    with db:
        try:
            account_obj = random.choice(Cookie.select().where(Cookie.is_selected == 0))
        except IndexError:
            raise RanOutAccountsForLinkException
    return account_obj


def db_save_1_by_id(id_account):
    with db:
        Cookie.update(is_selected=1).where(Cookie.id == id_account).execute()


def get_proxy_by_cookies(path_cookie):
    acc_obj: Cookie = Cookie.get(cookie_path=path_cookie)
    path_cookie, dict_proxy, id_account = db_get_cookie_proxy(account_obj=acc_obj)

    return dict_proxy, id_account


__all__ = [
    "create_db",
    "db_save_proxy_cookie",
    "db_get_link_id",
    "db_text_link_by_id",
    "db_exist_record_link_account",
    "db_delete_record_work_account_with_link",
    "db_delete_accounts_by_id",
    "db_get_cookie_proxy",
    "db_number_of_records_account",
    "db_reset_work_all_accounts_1_on_0",
    "db_get_random_account_with_0",
    "db_get_random_account_with_0",
    "db_save_1_by_id",
    "get_proxy_by_cookies"
]
