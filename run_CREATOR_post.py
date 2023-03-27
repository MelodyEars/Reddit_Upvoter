
from multiprocessing import freeze_support

from loguru import logger

import work_fs as wf
from CHECK_BAN.interface_ban import if_need_action
from autoposting import post_every_3_hours


@logger.catch
def main():
	post_every_3_hours()


if __name__ == '__main__':
	# IF_RUN_FIRST = if_need_action("Видяляти?")

	freeze_support()

	logger.add(
		wf.auto_create(wf.path_near_exefile("logs"), _type="dir") / "CreatePOST.log",
		format="{time} {level} {message}",
		level="INFO",
		rotation="10 MB",
		compression="zip"
	)
	try:
		main()
	finally:
		input("Press Enter:")
		