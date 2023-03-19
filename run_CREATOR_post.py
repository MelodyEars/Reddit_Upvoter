from multiprocessing import freeze_support

from loguru import logger

import work_fs as wf
from autoposting.api_run import work_browser
from autoposting.unpack import get_name_model

from database.autoposting_db import db_reset_is_submit_post_0


@logger.catch
def main():
	db_reset_is_submit_post_0()
	for jobmodel_obj in get_name_model():
		work_browser(jobmodel_obj)


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
		