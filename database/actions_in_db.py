import random

from base_exception import RanOutAccountsForLinkException

from .models import WorkAccountWithLink, db, Cookie


def db_exist_record_link_account(link_id, account_id):
    # check if id band with id link
    with db:
        obj: WorkAccountWithLink
        obj, created = WorkAccountWithLink.get_or_create(account=account_id, link=link_id)

    return created, obj.id


def db_reset_work_all_accounts_1_on_0():
    with db:
        Cookie.update(is_selected=0).where(Cookie.is_selected == 1).execute()


def db_get_random_account_with_0() -> Cookie:
    with db:
        try:
            account_obj = random.choice(Cookie.select().where(Cookie.is_selected == 0, Cookie.ban == 0))
        except IndexError:
            raise RanOutAccountsForLinkException

    return account_obj
