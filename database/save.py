from loguru import logger
from work_fs import write_line

from .models import Cookie, db
from .create import create_proxy, create_cookie, create_account


def db_save_proxy_cookie(proxy_from_api: dict, cookie_path: str, account: dict):
    with db:
        if len(Cookie.select().where(Cookie.cookie_path == cookie_path)) == 0:
            account_in_db = create_account(**account)
            proxy_in_db = create_proxy(**proxy_from_api)
            create_cookie(cookie_path, proxy_in_db, account_in_db)
        else:
            logger.error(f"""This account already exists in the data base.
                        (proxy rewrite in file, account: "{account}" del from list)""")


def db_save_1_by_id(id_cookie):
    with db:
        Cookie.update(is_selected=1).where(Cookie.id == id_cookie).execute()


