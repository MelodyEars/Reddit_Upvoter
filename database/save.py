from work_fs import write_line

from .models import Cookie, db
from .create import create_proxy, create_cookie


def db_save_proxy_cookie(proxy_from_api, cookie_path):
    with db:
        if len(Cookie.select().where(Cookie.cookie_path == cookie_path)) == 0:
            proxy_in_db = create_proxy(proxy_from_api)
            create_cookie(cookie_path, proxy_in_db)
        else:
            write_line("proxies.txt", ":".join((proxy_from_api['host'], proxy_from_api['port'],
                                                proxy_from_api['user'], proxy_from_api['password'])))


def db_save_1_by_id(id_account):
    with db:
        Cookie.update(is_selected=1).where(Cookie.id == id_account).execute()


