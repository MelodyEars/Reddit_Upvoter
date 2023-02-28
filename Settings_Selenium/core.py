import traceback

import undetected_chromedriver as uc
from loguru import logger

from Settings_Selenium import ProxyExtension, CookiesBrowser
from database import db_delete_record_work_account_with_link
from reddit_api_selenium import RedditWork

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


def get_reddit_api(list_reddit_api: list[RedditWork]):
	for reddit_api in list_reddit_api:
		if reddit_api.client_cookie.is_work:
			try:
				yield reddit_api
			except Exception:
				db_delete_record_work_account_with_link(reddit_api.client_cookie.id_work_link_account_obj)
				logger.error(traceback.format_exc())
				reddit_api.client_cookie.is_work = False


def close_all_browser(cl_cookies: list[CookiesBrowser]):
	for cl_cookie in cl_cookies:
		cl_cookie.save()
		cl_cookie.DRIVER.quit()
		logger.info(f"Закінчив працювати з {cl_cookie.username}")
