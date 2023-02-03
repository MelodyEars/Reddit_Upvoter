from multiprocessing import freeze_support

from loguru import logger

from reddit_api_selenium import RedditAuth
from handl_info import get_account, get_proxy
from work_fs import file_exists, path_near_exefile, write_list_to_file
from database import create_db, db_save_proxy_cookie


@logger.catch
def main():
    if not file_exists(path_near_exefile('database.db')):
        create_db()

    for account in get_account():
        proxy_for_api, list_proxies, path_proxy_file = get_proxy()
        logger.info("auth begin")
        with RedditAuth(proxy_for_api) as api:
            api.goto_login_form()
            api.fill_login_form(**account)
            api.skip_popups()
            cookie_path, proxy_from_api = api.get_path_cookie(account['login'])
            api.DRIVER.close()
        logger.info("write data")
        db_save_proxy_cookie(proxy_from_api, cookie_path)

        # rewrite file without current proxy
        write_list_to_file(path_proxy_file, list_proxies)


if __name__ == '__main__':
    freeze_support()

    logger.add("reddit_auth.log",
               format="{time} {level} {message}",
               level="ERROR",
               rotation="10 MB",
               compression="zip")
    try:
        main()
    finally:
        input("Press Enter: ")

        