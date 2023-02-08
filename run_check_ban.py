from multiprocessing import freeze_support

from loguru import logger
from selenium.common import NoSuchWindowException

from check_ban.api_for_check_ban import check_ban
from work_fs import path_near_exefile
from check_ban.interface_ban import user_response, thread_for_api
from check_ban.api_for_check_ban import for_user_open_browser


@logger.catch
def main():
	count_page = thread_for_api()
	LIST_SELECTED_ACC = []
	path_cookies = list(path_near_exefile("cookies").glob("*"))
	path_cookies.sort()
	list_path_ban = check_ban(path_cookies, count_page)

	while list_path_ban:
		path_selected_cookie, LIST_SELECTED_ACC = user_response(list_path_ban, LIST_SELECTED_ACC)
		try:
			for_user_open_browser(path_selected_cookie)
		except NoSuchWindowException:
			continue


if __name__ == '__main__':
	freeze_support()

	logger.add(
		"check_ban.log",
		format="{time} {level} {message}",
		level="ERROR",
		rotation="10 MB",
		compression="zip"
	)

	try:
		main()
	finally:
		input("Press Enter:")
