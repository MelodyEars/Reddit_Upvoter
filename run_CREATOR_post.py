from multiprocessing import freeze_support

from loguru import logger

import work_fs as wf
from autoposting.api_run import work_browser
from autoposting.unpack import get_name_model

from database.autoposting_db import db_reset_is_submit_post_0


@logger.catch
def main():
	import time

	while True:
		start_time = time.time()  # get the start time of the program
		logger.warning(f"Start time {start_time}")
		db_reset_is_submit_post_0()
		for jobmodel_obj in get_name_model():
			work_browser(jobmodel_obj)

		end_time = time.time()  # get the end time of the program
		logger.warning(f"End time {end_time}")

		running_time = end_time - start_time  # calculate the program's running time
		logger.info(f"The program's running time {running_time}")

		if running_time < 10800:  # if the program runs less than 3 hours
			time.sleep(10800 - running_time)  # sleep for the remaining time

		# the program will start again after 3 hours due to the while loop


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
		