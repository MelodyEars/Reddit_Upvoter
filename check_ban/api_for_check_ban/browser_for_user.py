from pathlib import Path

from reddit_api_selenium import RedditWork
from database import db_get_proxy_by_cookies


def for_user_open_browser(path_cookie: Path) -> None:
	url = f"https://www.reddit.com/user/{path_cookie.stem}"
	dict_proxy, id_account = db_get_proxy_by_cookies(f"cookies/{path_cookie.name}")

	with RedditWork(link=url, proxy=dict_proxy, path_cookie=path_cookie) as api_reddit:
		api_reddit.attend_link()
		input("Press Enter, если работа с браузером окончена: ")
		api_reddit.client_cookie.save()
		api_reddit.DRIVER.quit()
