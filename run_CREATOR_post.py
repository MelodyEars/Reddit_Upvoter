from multiprocessing import freeze_support

from loguru import logger

import work_fs as wf

from autoposting import yield_up_data_from_db
from database.autoposting_db import db_reset_is_submit_post_0


@logger.catch
def main():
	db_reset_is_submit_post_0()
	yield_up_data_from_db()


if __name__ == '__main__':
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
