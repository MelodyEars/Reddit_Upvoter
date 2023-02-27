from loguru import logger
from selenium.common import NoSuchWindowException

from auth_reddit import get_cookies
from reddit_api_selenium import RedditWork
from database import db_get_cookie_proxy, Cookie, db_get_account_by_id
from reddit_api_selenium.exceptions import CookieInvalidException


def getter_cookie(account_dict, dict_proxy, url, path_cookie, name_account, id_account):
	get_cookies(account=account_dict, proxy_for_api=dict_proxy)
	return work_api(url, dict_proxy, path_cookie, name_account, id_account)


def work_api(url, dict_proxy, path_cookie, name_account, id_account):
	with RedditWork(link=url, proxy=dict_proxy, path_cookie=path_cookie) as api_reddit:
		try:
			api_reddit.attend_link()

		except CookieInvalidException:
			api_reddit.DRIVER.quit()
			logger.error(f'Cookie аккаунта "{name_account}" не работают, нужно перезаписать.')
			account_dict = db_get_account_by_id(id_account)
			return getter_cookie(account_dict, dict_proxy, url, path_cookie, name_account, id_account)

		except NoSuchWindowException:
			pass

		finally:
			input("Press Enter, если работа с браузером окончена: ")
			api_reddit.client_cookie.save()
			api_reddit.DRIVER.quit()


def for_user_open_browser(cookie_obj: Cookie) -> None:

	path_cookie, dict_proxy, id_account = db_get_cookie_proxy(cookie_obj)
	name_account = path_cookie.stem
	url = f"https://www.reddit.com/user/{name_account}"
	return work_api(url, dict_proxy, path_cookie, name_account, id_account)

