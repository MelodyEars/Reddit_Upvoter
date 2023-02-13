from colorama import init, deinit
from work_fs import data_confirmation


def if_need_check():
	init()  # <-color
	if data_confirmation("Перевіряти аккаунти (запуск брузера)"):
		necessary = True
	else:
		necessary = False
	deinit()  # <-color

	return necessary
