from NW_Upvoter.db_tortories_orm.models import Cookie
from work_fs import path_near_exefile


def unpack_cooke_obj(cookie_db_obj: Cookie):
    dict_proxy: dict[str, Cookie] = {
        "host": cookie_db_obj.proxy.host,
        "port": cookie_db_obj.proxy.port,
        "user": cookie_db_obj.proxy.user,
        "password": cookie_db_obj.proxy.password,
    }

    path_cookie = path_near_exefile(cookie_db_obj.cookie_path)
    id_account = cookie_db_obj.id

    return path_cookie, dict_proxy, id_account
