from work_fs import write_line, path_near_exefile

from .models import db, WorkAccountWithLink, Proxy, Cookie


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
