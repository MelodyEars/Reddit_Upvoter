from pathlib import Path

from reddit_api_selenium import RedditWork
from database import db_get_cookie_proxy, Cookie


def for_user_open_browser(cookie_obj: Cookie) -> None:

	path_cookie, dict_proxy, id_account = db_get_cookie_proxy(cookie_obj)
	url = f"https://www.reddit.com/user/{path_cookie.stem}"

	with RedditWork(link=url, proxy=dict_proxy, path_cookie=path_cookie) as api_reddit:
		api_reddit.attend_link()
		input("Press Enter, если работа с браузером окончена: ")
		api_reddit.client_cookie.save()
		api_reddit.DRIVER.quit()
