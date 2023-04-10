import concurrent.futures

from database import JobModel
from database.autoposting_db import db_grab_model_obj
from autoposting.beautiful_page.run_browser import autoposting


def do_autoposter():
	jobmodels_objs: list[JobModel] = db_grab_model_obj()

	while True:
		with concurrent.futures.ThreadPoolExecutor() as executor:
			# запускаємо функцію process_item паралельно для кожного елемента в списку
			futures = [executor.submit(autoposting, jobmodel_obj) for jobmodel_obj in jobmodels_objs]

			# очікуємо завершення всіх функцій
			for future in concurrent.futures.as_completed(futures):
				result = future.result()
