from colorama import init, deinit
from work_fs import data_confirmation


def if_need_action(text="Перевіряти аккаунти (запуск брузера)"):
	init()  # <-color
	if data_confirmation(text):
		necessary = True
	else:
		necessary = False
	deinit()  # <-color

	return necessary
