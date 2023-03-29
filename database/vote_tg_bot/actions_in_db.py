import time

from loguru import logger

from .models import WorkAccountWithLink, db, Cookie

# from SETTINGS import mine_project


def db_exist_record_link_account(link_id, cookie_id):
    # check if id band with id link
    with db:
        obj: WorkAccountWithLink
        created: bool
        obj, created = WorkAccountWithLink.get_or_create(cookie=cookie_id, link=link_id)

    return created, obj.id


# def db_reset_work_all_accounts_1_on_0():
#     with db:
#         Cookie.update(is_selected=0).where(Cookie.is_selected == 1).execute()


def db_get_random_account_with_0() -> list[Cookie]:
    with db:
        cookies_db_objs = Cookie.select().where((Cookie.is_selected == False) & (Cookie.ban.is_null(True)))

        # if mine_project:
        #
        #  compare list selected models and cookies_db_objs then return,
        #  but this method work if remove method delete after add model

    return cookies_db_objs


def db_ban_add(DICT_ACC_BAN: dict):
    with db.atomic():
        for acc_path_cookie, ban_cond in DICT_ACC_BAN.items():
            # without ban
            logger.info(ban_cond)
            Cookie.update(ban=ban_cond).where(Cookie.cookie_path == acc_path_cookie).execute()

        time.sleep(3)
