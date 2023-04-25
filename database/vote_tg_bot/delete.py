from SETTINGS import mine_project
from .models import db, WorkAccountWithLink, Proxy, Cookie, Account


def db_delete_record_work_account_with_link(obj_record: WorkAccountWithLink):
    # obj.id if needed to delete when exception exists
    # with db:
    obj_record.delete_instance()


def db_delete_cookie_by_id(cookie_obj: Cookie):
    if mine_project:
        with db:
            WorkAccountWithLink.delete().where(WorkAccountWithLink.cookie == cookie_obj.id).execute()

            # delete from
            cookie_obj.delete_instance()
            Proxy.delete_by_id(cookie_obj.id)
            Account.delete_by_id(cookie_obj.id)
    else:
        with db.atomic():
            # delete all by index from account
            WorkAccountWithLink.delete().where(WorkAccountWithLink.cookie == cookie_obj.id).execute()

            # delete from
            cookie_obj.delete_instance()
            Proxy.delete_by_id(cookie_obj.id)
            Account.delete_by_id(cookie_obj.id)


