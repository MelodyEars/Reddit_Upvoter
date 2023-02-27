from pathlib import Path

import undetected_chromedriver as uc
from loguru import logger

from Settings_Selenium import CookiesBrowser, ProxyExtension
from auth_reddit import get_cookies
from database import db_get_account_by_id, Cookie
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


def reddit_run(cookie_path: Path, id_profile: Cookie, dict_proxy: dict):
	driver: uc.Chrome = driver_run(proxy=dict_proxy)
	client_cookie = CookiesBrowser(driver=driver, path_filename=cookie_path)

	if client_cookie.are_valid():
		client_cookie.preload()
		driver.get('https://www.reddit.com/')
		driver.reconnect()
	else:
		logger.error(f'Cookie акаунта "{cookie_path.stem}" не працюють, перезаписую!')
		account_dict = db_get_account_by_id(id_profile)
		client_cookie = get_cookies(driver=driver, account=account_dict)
		logger.info(f'Cookie аккаунта "{cookie_path.stem}" перезаписані.')

	return client_cookie


def run_browser(thread):
	drivers = []
	for _ in range(thread):
		drivers.append(driver_run())

	return drivers


def get_browser(drivers):
	for driver in drivers:
		try:
			yield driver
		finally:
			driver.quit()
