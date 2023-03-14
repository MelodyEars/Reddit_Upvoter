from multiprocessing import freeze_support

from loguru import logger

from autoposting import yield_up_data_from_db


@logger.catch
def main():
	yield_up_data_from_db()


if __name__ == '__main__':
	freeze_support()

	logger.add(
		"CreatePOST.log",
		format="{time} {level} {message}",
		level="INFO",
		rotation="10 MB",
		compression="zip"
	)

	main()
