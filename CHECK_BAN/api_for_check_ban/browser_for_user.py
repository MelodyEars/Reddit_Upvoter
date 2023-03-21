import time

from loguru import logger
from selenium.common import NoSuchWindowException

from BASE_Reddit.exceptions import CookieInvalidException
from auth_reddit import get_cookies
from Uprove_TG_Bot.reddit_api_selenium import RedditWork
from database import db_get_cookie_proxy, Cookie, db_get_account_by_id


def getter_cookie(dict_proxy, url, path_cookie, name_account, id_account):
	logger.error(f'Cookie аккаунта "{name_account}" не работают, нужно перезаписать.')
	account_dict = db_get_account_by_id(id_account)
	get_cookies(account=account_dict, proxy_for_api=dict_proxy)
	return work_api(url, dict_proxy, path_cookie, name_account, id_account)


def work_api(url, dict_proxy, path_cookie, name_account, id_account):
	with RedditWork(link=url, proxy=dict_proxy, path_cookie=path_cookie) as api_reddit:
		try:
			api_reddit.attend_link()

			input("Press Enter, если работа с браузером окончена: ")
			api_reddit.client_cookie.save()
			api_reddit.DRIVER.quit()

		except CookieInvalidException:
			api_reddit.DRIVER.quit()
			return getter_cookie(dict_proxy, url, path_cookie, name_account, id_account)

		except NoSuchWindowException:
			logger.warning("Cookie не збереглись. Краще буде закривати браузер через консоль натиснувши ENTER.")
			time.sleep(3)


def for_user_open_browser(cookie_obj: Cookie):
	path_cookie, dict_proxy, id_account = db_get_cookie_proxy(cookie_obj)
	name_account = path_cookie.stem
	url = f"https://www.reddit.com/user/{name_account}"
	return work_api(url, dict_proxy, path_cookie, name_account, id_account)

