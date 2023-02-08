from loguru import logger

from handl_info import get_account_file, file_get_proxy
from work_fs import file_exists, path_near_exefile, write_list_to_file
from database import create_db, db_save_proxy_cookie

from .auth_reddit_api_selenium import RedditAuth


def get_cookies(account: dict, proxy_for_api: dict):
    logger.info("auth begin")
    with RedditAuth(proxy_for_api) as api:
        api.goto_login_form()
        api.fill_login_form(**account)
        api.skip_popups()
        cookie_path, proxy_from_api = api.get_path_cookie(account['login'])
        api.DRIVER.close()
    logger.info("write data")

    return cookie_path, proxy_from_api


def check_new_acc():
    if not file_exists(path_near_exefile('database.db')):
        create_db()

    for account in get_account_file():
        # get working proxy
        proxy_for_api, list_proxies, path_proxies_file = file_get_proxy()

        # work_api
        proxy_from_api, cookie_path = get_cookies(proxy_for_api=proxy_for_api, account=account)

        # save to db
        db_save_proxy_cookie(proxy_from_api, cookie_path, account)

        # rewrite file without current proxy
        write_list_to_file(path_proxies_file, list_proxies)