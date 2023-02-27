from colorama import init, deinit

from work_fs import indicate_number


def thread_for_api():
	init()
	user_thread = indicate_number("В скільки потоків працювати")
	deinit()
	return user_thread
