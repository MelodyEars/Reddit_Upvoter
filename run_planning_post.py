from loguru import logger

from PostPlanning.data_generation import registration_to_db
from database.autoposting_db import create_table_posting, db_add_record_post


@logger.catch
def main():
	logger.info("start")

	create_table_posting()

	for data in registration_to_db():
		logger.info(data)  # ____________________ log
		db_add_record_post(*data)
		logger.info("to next data")

	logger.info("finish")


if __name__ == '__main__':

	logger.add(
		"planning_post.log",
		format="{time} {level} {message}",
		level="INFO",
		rotation="10 MB",
		compression="zip"
	)

	main()
