
from loguru import logger

import work_fs as wf
from PostPlanning.data_generation import registration_to_db
from database.autoposting_db import create_table_posting, db_add_record_post


@logger.catch
def main():
	logger.info("start")

	create_table_posting()

	for data in registration_to_db():
		logger.info(data)  # ____________________ log
		if db_add_record_post(*data):
			logger.warning("Created new record!")
		else:
			logger.warning("This records exists!")
		logger.info("to next data")

	logger.info("finish")


if __name__ == '__main__':

	logger.add(
		wf.auto_create(wf.path_near_exefile("logs"), _type="dir") / "planning_post.log",
		format="{time} {level} {message}",
		level="INFO",
		rotation="10 MB",
		compression="zip"
	)
	try:
		main()
	finally:
		input("Press Enter:")
