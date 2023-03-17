from multiprocessing import freeze_support

from loguru import logger

import work_fs as wf

from database import JobModel
from database.autoposting_db import db_reset_is_submit_post_0

from autoposting import yield_up_data_from_db
from autoposting.api_run import connect_api, delete_all_posts, get_url_imgur_img, reddit_create_post
from autoposting.handl_obj import get_info_about_photo

api = None


@logger.catch
def main():
	global api
	current_model = None

	db_reset_is_submit_post_0()

	for post_obj in yield_up_data_from_db():
		# get info about post
		model_name = post_obj.id_jobmodel.account.login
		path_photo, title, link_sub_reddit = get_info_about_photo(post_obj)

		if not current_model == model_name:
			# if new model then open browser else work old browser
			current_model = model_name
			jobmodel_obj: JobModel = post_obj.id_jobmodel
			# completed_session(api)  # close current browser
			with connect_api(jobmodel_obj) as api:  # open new browser
				delete_all_posts(api)  # delete all post in model's account on Reddit

		# every iteration work in old browser
		photo_url = get_url_imgur_img(post_obj, api)  # upload photo imgur

		reddit_create_post(photo_url, title, link_sub_reddit, api)


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
