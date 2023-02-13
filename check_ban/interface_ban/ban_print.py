from pathlib import Path

from colorama import Fore, Style, Back, init, deinit

from database import Cookie
from work_fs import green_color, cyan_color, blue_color, indicate_number, clear_cmd, path_near_exefile


def shadow_ban(text):
	returning_text = Back.RED + Fore.WHITE + str(text) + Style.RESET_ALL + Fore.RED + " <-ban!" + Style.RESET_ALL
	return returning_text


def opened_shadow_ban(text):
	returning_text = Back.YELLOW + Fore.WHITE + str(text) + Style.RESET_ALL + Fore.RED + " <- already opened!" + Style.RESET_ALL
	return returning_text


def print_info(count: int, cookie_obj: Cookie, selected_cookie_objs: list):
	ban = cookie_obj.ban
	cookie_name: str = cookie_obj.cookie_path.split("/")[1]
	if not ban:  # if ban not exists
		account_print = green_color(cookie_name)

	else:
		if cookie_obj not in selected_cookie_objs:
			account_print = shadow_ban(cookie_name)

		else:
			account_print = opened_shadow_ban(cookie_name)

	print(f"{cyan_color(count)} : {account_print}")


def unpack_info(cookies_objs, selected_cookie_objs: list):
	for count, acc_obj in enumerate(cookies_objs, start=1):
		print_info(count=count, cookie_obj=acc_obj, selected_cookie_objs=selected_cookie_objs)


def user_response(cookies_objs, selected_cookie_objs: list):
	clear_cmd()

	init()  # <-color
	print(blue_color("Обери аккаунт"))

	unpack_info(cookies_objs, selected_cookie_objs)
	user_int: int = indicate_number("Вкажи число: ") - 1
	deinit()  # <-color

	cookies_select = cookies_objs[user_int]
	selected_cookie: Path = path_near_exefile(cookies_select)
	selected_cookie_objs.append(cookies_select)

	return selected_cookie, selected_cookie_objs
