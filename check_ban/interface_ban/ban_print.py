from pathlib import Path

from colorama import Fore, Style, Back, init, deinit

from work_fs import green_color, cyan_color, blue_color, indicate_number, clear_cmd


def shadow_ban(text):
	returning_text = Back.RED + Fore.WHITE + str(text) + Style.RESET_ALL + Fore.RED + " <-ban!" + Style.RESET_ALL
	return returning_text


def opened_shadow_ban(text):
	returning_text = Back.YELLOW + Fore.WHITE + str(text) + Style.RESET_ALL + Fore.RED + " <- already opened!" + Style.RESET_ALL
	return returning_text


def print_info(count: int, path_cookies: Path, ban: bool, list_selected_acc: list):
	if not ban:  # if ban not exists
		account_print = green_color(path_cookies.stem)

	else:
		if path_cookies not in list_selected_acc:
			account_print = shadow_ban(path_cookies.stem)

		else:
			account_print = opened_shadow_ban(path_cookies.stem)

	print(f"{cyan_color(count)} : {account_print}")


def unpack_info(list_acc_cond: list, list_selected_acc: list):
	for count, info in enumerate(list_acc_cond, start=1):
		print_info(count=count, path_cookies=info[0], ban=info[1], list_selected_acc=list_selected_acc)


def user_response(list_acc_cond: list, list_selected_acc: list):
	clear_cmd()

	init()  # <-color
	print(blue_color("Обери аккаунт"))
	unpack_info(list_acc_cond, list_selected_acc)
	user_int: int = indicate_number("Вкажи число: ") - 1
	deinit()  # <-color
	# TODO replace list_selected_acc on second value in list_acc_cond
	selected_cookie: Path = list_acc_cond[user_int][0]
	list_selected_acc.append(selected_cookie)

	return selected_cookie, list_selected_acc
