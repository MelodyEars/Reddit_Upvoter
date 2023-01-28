import random

import work_fs
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


def db_delete_accounts_by_id(id_cookie):
    with db.atomic():
        proxy_for_save = Proxy.get_by_id(id_cookie)
        # Save as str to file
        proxy_as_str = f"{proxy_for_save.host}:{proxy_for_save.port}:{proxy_for_save.user}:{proxy_for_save.password}"
        path_filename = work_fs.path_near_exefile("working_proxy_after_ban.txt")
        work_fs.write_line(path_filename, proxy_as_str)

        # TODO delete all by index from account

        # delete from tabel
        Account.delete_by_id(id_cookie)
        Proxy.delete_by_id(id_cookie)


def db_get_cookie_proxy():
    with db:
        account_obj = random.choice(Account.select())

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


def db_reset_all_1_on_0():
    with db:
        Account.update(is_work=0).where(Account.is_selected == 1).execute()

