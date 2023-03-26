import time

from loguru import logger

from .network import run_browser
from .unpack import get_name_model


def post_every_3_hours():
	while True:
		start_time = time.time()  # get the start time of the program
		logger.warning(f"Start time {start_time}")

		for jobmodel_obj in get_name_model():
			run_browser(jobmodel_obj)

		end_time = time.time()  # get the end time of the program
		logger.warning(f"End time {end_time}")

		running_time = end_time - start_time  # calculate the program's running time
		logger.info(f"The program's running time {running_time}")

		if running_time < 10800:  # if the program runs less than 3 hours
			time.sleep(10800 - running_time)  # sleep for the remaining time

		# the program will start again after 3 hours due to the while loop

