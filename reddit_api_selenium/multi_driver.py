import time
import traceback
from pathlib import Path
from typing import List, Tuple, Type, Any

import undetected_chromedriver as uc
from loguru import logger

from auth_reddit import get_cookies
from database import db_get_account_by_id, Cookie, db_delete_record_work_account_with_link, WorkAccountWithLink

from Settings_Selenium import driver_run, CookiesBrowser


def reddit_run(link_from_file: str, path_cookie: Path, dict_proxy: dict, id_cookie: Cookie.id, id_work_link_account_obj: WorkAccountWithLink.id):
	driver: uc.Chrome = driver_run(proxy=dict_proxy)
	username = path_cookie.stem
	client_cookie = CookiesBrowser(driver, link_from_file, path_cookie, id_work_link_account_obj, username)

	if client_cookie.are_valid():
		client_cookie.preload()
		driver.get('https://www.reddit.com/')
	else:
		logger.error(f'Cookie акаунта "{username}" не працюють, перезаписую!')
		account_dict = db_get_account_by_id(id_cookie)
		client_cookie = get_cookies(driver=driver, account=account_dict, client_cookie=client_cookie)
		logger.info(f'Cookie аккаунта "{username}" перезаписані.')

	return client_cookie


def run_browser(list_link_acc: list) -> list[CookiesBrowser]:
	client_cookies = []

	for tuple_obj in list_link_acc:
		# unpack info
		*_, id_work_link_account_obj = tuple_obj
		client_cookie = CookiesBrowser

		try:
			client_cookie = reddit_run(*tuple_obj)
		except Exception:
			logger.error(traceback.format_exc())
			db_delete_record_work_account_with_link(id_work_link_account_obj)

		client_cookies.append(client_cookie)

	return client_cookies
