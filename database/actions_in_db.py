from playhouse.postgres_ext import fn
from .models import WorkAccountWithLink, db, Cookie


def db_exist_record_link_account(link_id, account_id):
    # check if id band with id link
    with db:
        obj: WorkAccountWithLink
        created: bool
        obj, created = WorkAccountWithLink.get_or_create(account=account_id, link=link_id)

    return created, obj.id


def db_reset_work_all_accounts_1_on_0():
    with db:
        Cookie.update(is_selected=0).where(Cookie.is_selected == 1).execute()


def db_get_random_account_with_0() -> list[Cookie]:
    with db:
        cookies_db_objs = Cookie.select().where((Cookie.is_selected == 0) & (fn.is_null(Cookie.ban)) & (Cookie.cookie_path != "cookies/kirillorlovmae.pkl"))

    return cookies_db_objs


def db_ban_add(DICT_ACC_BAN: dict):
    with db.atomic():
        for acc_path_cookie, ban_cond in DICT_ACC_BAN.items():
            if ban_cond is not None:
                Cookie.update(ban=ban_cond).where(Cookie.cookie_path == acc_path_cookie).execute()
            else:
                # without ban
                Cookie.update(ban=None).where(Cookie.cookie_path == acc_path_cookie).execute()
