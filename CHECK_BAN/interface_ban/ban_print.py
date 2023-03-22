from colorama import Fore, Style, Back, init, deinit

from SETTINGS import commands
from database import Cookie, Proxy
from work_fs import clear_cmd, path_near_exefile
from work_fs.color import green_color, cyan_color, blue_color, magenta_color, warning_text



# __________________________________________ COLOR  _______________________________________________
def permanent_ban(text):
	returning_text = Back.RED + Fore.WHITE + str(
		text) + Style.RESET_ALL + Fore.LIGHTRED_EX + " <- permanent ban!" + Style.RESET_ALL

	return returning_text


def opened_account(text):
	returning_text = Back.YELLOW + Fore.WHITE + str(
		text) + Style.RESET_ALL + Fore.RED + " <- already opened!" + Style.RESET_ALL

	return returning_text


def shadow_ban(text):
	returning_text = Back.LIGHTMAGENTA_EX + Fore.WHITE + str(
		text) + Style.RESET_ALL + Fore.LIGHTRED_EX + " <- shadow ban!" + Style.RESET_ALL

	return returning_text


########################### answered user ##########################
def indicate_number(text_what_answer: str):
	print(cyan_color(f"{text_what_answer}?"))
	list_number_cmd = input().split(":")

	try:
		num = int(list_number_cmd[0]) - 1
	except ValueError:
		warning_text("Не ціле число!")
		return indicate_number(text_what_answer)

	if len(list_number_cmd) == 1:
		return num, False

	else:
		command = list_number_cmd[1].replace(" ", "").lower()
		if command in commands:
			return num, command

		else:
			warning_text(f'Команда не схожа на {green_color("del")}')
			return indicate_number(text_what_answer)


def unpack_data(cookie_obj: Cookie):
	db_id = cookie_obj.id
	ban = cookie_obj.ban
	username_acc: str = path_near_exefile(cookie_obj.cookie_path).stem
	proxy: Proxy = cookie_obj.proxy
	info_proxy: str = f"{proxy.host}:{proxy.port}:{proxy.user}:{proxy.password}"

	about_acc = f'id:{db_id} {username_acc} {info_proxy}'
	return ban, about_acc


################################ print ################################
def print_info(count: int, cookie_obj: Cookie, selected_cookie_objs: list):
	ban, about_acc = unpack_data(cookie_obj=cookie_obj)

	if ban is None:  # if ban not exists
		account_print = green_color(about_acc)

	elif ban == "shadow":
		if cookie_obj not in selected_cookie_objs:
			account_print = shadow_ban(about_acc)

		else:
			account_print = opened_account(about_acc)
	else:
		if cookie_obj not in selected_cookie_objs:
			account_print = permanent_ban(about_acc)

		else:
			account_print = opened_account(about_acc)

	print(f"{cyan_color(count)} : {account_print}")


def unpack_info(cookies_objs, selected_cookie_objs: list):
	for count, acc_obj in enumerate(cookies_objs, start=1):
		print_info(count=count, cookie_obj=acc_obj, selected_cookie_objs=selected_cookie_objs)


def user_response(cookies_objs, list_selected_cookie_objs: list):
	clear_cmd()

	init()  # <-color
	print(blue_color("Обери аккаунт, для цього обери цифру."))
	print(magenta_color("del") + cyan_color(' - пропиши через ":" якщо хочеш видалити аккаунт з бд'))
	print('Наприклад: "1:del"')

	unpack_info(cookies_objs, list_selected_cookie_objs)
	is_del_db: bool  # is True then del by number from db
	user_int: int
	user_int, command = indicate_number("Вкажи число: ")

	deinit()  # <-color
	selected_cookie = cookies_objs[user_int]
	list_selected_cookie_objs.append(selected_cookie)

	return selected_cookie, list_selected_cookie_objs, command
