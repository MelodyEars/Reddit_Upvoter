
from .models import db, WorkAccountWithLink, Proxy, Cookie, Account


def db_delete_record_work_account_with_link(id_record):
    # obj.id if needed to delete when exception exists
    with db:
        WorkAccountWithLink.delete_by_id(id_record)


def db_delete_cookie_by_id(id_cookie):
    with db.atomic():
        # delete all by index from account
        WorkAccountWithLink.delete().where(WorkAccountWithLink.cookie == id_cookie)

        # delete from tabel
        Cookie.delete_by_id(id_cookie)
        Proxy.delete_by_id(id_cookie)
        Account.delete_by_id(id_cookie)
