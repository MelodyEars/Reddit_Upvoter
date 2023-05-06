from NW_Upvoter.db_tortories_orm.models import Cookie, Proxy, Account
from work_fs import path_near_exefile


def unpack_cooke_obj(cookie_db_obj: Cookie):
    proxy_obj: Proxy = cookie_db_obj.proxy
    account_obj: Account = cookie_db_obj.account

    dict_proxy: dict[str, Cookie] = {
        "host": proxy_obj.host,
        "port": proxy_obj.port,
        "user": proxy_obj.user,
        "password": proxy_obj.password,
    }

    log_pswd = {
        "login": account_obj.login,
        "password": account_obj.password
    }

    path_cookie = path_near_exefile(cookie_db_obj.cookie_path)

    return path_cookie, dict_proxy, log_pswd
