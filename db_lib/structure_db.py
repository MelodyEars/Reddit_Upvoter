import random

import work_fs

from base_exception import RanOutAccountsForLinkException

from .models import Proxy, RedditLink, Account, WorkAccountWithLink, db


def db_get_link_id(link_from_file):
    # this func work in handl_info->get_links
    # get list id by list text
    with db:
        link_obj = RedditLink.get_or_create(link=link_from_file)[0]

    return link_obj


def db_text_link_by_id(link_id):
    # get link by id
    with db:
        link_obj = RedditLink.get_by_id(link_id)

    return link_obj.link


def db_exist_record_link_account(link_id, account_id):
    # check if id band with id link
    with db:
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
        path_filename = work_fs.path_near_exefile("working_proxy_after_ban.txt")
        work_fs.write_line(path_filename, proxy_as_str)

        # delete all by index from account
        WorkAccountWithLink.delete().where(WorkAccountWithLink.account == id_account)

        # delete from tabel
        Account.delete_by_id(id_account)
        Proxy.delete_by_id(id_account)


def db_get_cookie_proxy(account_obj):

    dict_proxy = {
        "host": account_obj.proxy.host,
        "port": account_obj.proxy.port,
        "user": account_obj.proxy.user,
        "password": account_obj.proxy.password,
    }

    path_cookie = work_fs.path_near_exefile(account_obj.cookie_path)
    id_account = account_obj.id

    return path_cookie, dict_proxy, id_account


def db_number_of_records_account():
    with db:
        return len(Account.select())


def db_reset_work_all_accounts_1_on_0():
    with db:
        Account.update(is_selected=0).where(Account.is_selected == 1).execute()


def db_get_random_account_with_0() -> Account:
    with db:
        try:
            account_obj = random.choice(Account.select().where(Account.is_selected == 0))
        except IndexError:
            raise RanOutAccountsForLinkException
    return account_obj


def db_save_1_by_id(id_account):
    with db:
        Account.update(is_selected=1).where(Account.id == id_account).execute()
