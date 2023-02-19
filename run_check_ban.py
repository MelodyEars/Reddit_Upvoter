from multiprocessing import freeze_support

from selenium.common import NoSuchWindowException

from check_ban.api_for_check_ban import check_ban
from check_ban.interface_ban import user_response, thread_for_api, if_need_check
from check_ban.api_for_check_ban import for_user_open_browser
from database import *


def delete_account_db(cookie_obj: Cookie):
    db_delete_cookie_by_id(cookie_obj.id)
    path_cookie = path_near_exefile(cookie_obj.cookie_path)
    path_cookie.unlink()  # delete in folder
    logger.error(f'{path_cookie.stem} був видалений з бд.')


@logger.catch
def main():
	selected_cookie_objs = []
	answer = if_need_check()
	if answer:  # print interface
		count_page = thread_for_api()
		path_cookies = sorted(path_near_exefile("cookies").glob("*"))
		list_acc_ban = check_ban(path_cookies, count_page)  # api playwright
		db_ban_add(list_acc_ban)  # update db

	cookies_objs = list(db_get_cookie_objs())

	while cookies_objs:
		selected_cookie, selected_cookie_objs, is_del_db = user_response(cookies_objs, selected_cookie_objs)
		if not is_del_db:
			try:
				for_user_open_browser(selected_cookie)
			except NoSuchWindowException:
				continue
		else:
			pass


if __name__ == '__main__':
	freeze_support()

	logger.add(
		"check_ban.log",
		format="{time} {level} {message}",
		level="DEBUG",
		rotation="10 MB",
		compression="zip"
	)

	try:
		main()
	finally:
		input("Press Enter:")
