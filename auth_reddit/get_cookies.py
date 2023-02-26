import undetected_chromedriver as uc
from loguru import logger

from Settings_Selenium import CookiesBrowser
from handl_info import get_account_file, file_get_proxy
from work_fs import file_exists, path_near_exefile, write_list_to_file
from database import create_db, db_save_proxy_cookie

from .auth_reddit_api_selenium import RedditAuth


def get_cookies(driver: uc.Chrome, account: dict):
    logger.info("auth begin")

    with RedditAuth(driver) as api:
        api.goto_login_form()
        api.fill_login_form(**account)
        api.skip_popups()
        cookie: CookiesBrowser = api.get_path_cookie(account['login'])
    logger.info("write data")

    return cookie


def check_new_acc():
    if not file_exists(path_near_exefile('database.db')):
        create_db()

    for account in get_account_file():
        # get working proxy
        proxy_for_api, list_proxies, path_proxies_file = file_get_proxy()

        # work_api
        # get_cookies(driver=, account=account)
        cookie_path = f"cookies/{account['login']}.pkl"

        # save to db
        db_save_proxy_cookie(proxy_from_api=proxy_for_api, cookie_path=cookie_path, account=account)

        # rewrite file without current proxy
        write_list_to_file(path_proxies_file, list_proxies)
