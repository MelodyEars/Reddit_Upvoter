import time
import traceback
from pathlib import Path
from typing import List, Tuple, Type, Any

import undetected_chromedriver as uc
from loguru import logger

from Settings_Selenium import CookiesBrowser, ProxyExtension
from auth_reddit import get_cookies
from database import db_get_account_by_id, Cookie, db_delete_record_work_account_with_link, WorkAccountWithLink

executable_path = None


def set_new_download_path(driver: uc.Chrome, download_path):
	# Defines auto download and download PATH
	params = {
		"behavior": "allow",
		"downloadPath": download_path
	}
	driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

	return driver


def driver_run(profile=None, browser_executable_path=executable_path, user_data_dir=None, download_path="default", proxy=None) -> uc.Chrome:
	your_options = {}

	options = uc.ChromeOptions()
	options.add_argument("""--disable-dev-shm-usage --disable-setuid-sandbox --disable-software-rasterizer 
	--disable-notifications --disable-renderer-backgrounding --disable-backgrounding-occluded-windows
	""")  # 2 arg in  the end need for working on the backgrounding

	if proxy is not None:
		# proxy = ("64.32.16.8", 8080, "username", "password")  # your proxy with auth, this one is obviously fake
		# pass  host, port, user, password
		proxy_extension = ProxyExtension(**proxy)
		options.add_argument(f"--load-extension={proxy_extension.directory}")

	# if user_data_dir is not None:
	#     your_options["user_data_dir"] = user_data_dir
	#
	# elif profile is not None:
	#     # match on windows 10
	#     options.add_argument(fr"--user-data-dir={os.environ['USERPROFILE']}\AppData\Local\Google\Chrome\User Data")
	#     options.add_argument(f"--profile-directory={profile}")

	your_options["options"] = options
	your_options["browser_executable_path"] = browser_executable_path

	# if not profile or user_data_dir == incognito
	driver = uc.Chrome(**your_options)

	driver.maximize_window()
	# action = EnhancedActionChains(driver)

	# if you need download to your folder
	if download_path == "default":
		return driver

	else:
		return set_new_download_path(driver, download_path)


def reddit_run(link_from_file: str, path_cookie: Path, dict_proxy: dict, id_cookie: Cookie.id, id_work_link_account_obj: WorkAccountWithLink.id):
	driver: uc.Chrome = driver_run(proxy=dict_proxy)
	username = path_cookie.stem
	client_cookie = CookiesBrowser(driver, link_from_file, path_cookie, id_work_link_account_obj, username)

	if client_cookie.are_valid():
		client_cookie.preload()
		driver.get('https://www.reddit.com/')
		driver.reconnect()
		time.sleep(3)
		link_sub_reddit = "/".join(link_from_file.split("/")[:6])
		driver.get(link_sub_reddit)
		time.sleep(3)

	else:
		logger.error(f'Cookie акаунта "{username}" не працюють, перезаписую!')
		account_dict = db_get_account_by_id(id_cookie)
		client_cookie = get_cookies(driver=driver, account=account_dict)
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
			client_cookie.DRIVER.quit()
			db_delete_record_work_account_with_link(id_work_link_account_obj)
			logger.error(traceback.format_exc())

		client_cookies.append(client_cookie)

	return client_cookies
