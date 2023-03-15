
# print url post to txt after execute program

from loguru import logger

from database.autoposting_db.models_posting import JobModel, Photo, Category, LinkSubReddit, Posting
from database.autoposting_db import db_grab_model_obj, db_get_gen_categories, db_get_photos, db_pick_up_reddit_sub, \
	db_get_post_for_posting, db_delete_executed_post, db_update_photo_is_work_1


def pick_up_link_sub_reddit(jobmodel_obj: JobModel, category_obj: Category, photo_obj: Photo):
	link_sub_objs: list[LinkSubReddit] = db_pick_up_reddit_sub(jobmodel_obj, category_obj, photo_obj)

	for link_sub_obj in link_sub_objs:
		logger.warning('Link Sub')
		logger.info(link_sub_obj.link_SubReddit)  # __________________ log link
		if not link_sub_obj.is_submitted:
			list_post_obj: list[Posting] = db_get_post_for_posting(jobmodel_obj, category_obj, photo_obj, link_sub_obj)

			if list_post_obj:
				post_obj = list_post_obj[0]
				yield post_obj


def pick_up_photos(jobmodel_obj: JobModel, category_obj: Category):
	photos_objs: list[Photo] = db_get_photos(jobmodel_obj, category_obj)

	for photo_obj in photos_objs:
		logger.warning('Photo')
		logger.info(photo_obj.path_photo)  # __________________ log photo
		if not photo_obj.is_submitted:
			for post_obj in pick_up_link_sub_reddit(jobmodel_obj, category_obj, photo_obj):
				if post_obj is not None:
					yield post_obj


def pick_up_category(jobmodel_obj: JobModel):
	category_objs: list[Category] = db_get_gen_categories(jobmodel_obj)

	for category_obj in category_objs:
		logger.warning('Category')
		logger.info(category_obj)  # __________________ log category
		for post_obj in pick_up_photos(jobmodel_obj, category_obj):
			if post_obj is not None:
				yield post_obj


def pick_up_data():
	jobmodels_objs: list[JobModel] = db_grab_model_obj()

	# while list exists from Posting.select()
	for jobmodels_obj in jobmodels_objs:
		logger.warning('Models')
		logger.info(jobmodels_obj.account.login)  # __________________ log account's login
		for post_obj in pick_up_category(jobmodels_obj):
			if post_obj is not None:
				yield post_obj


def yield_up_data_from_db():
	for post_obj in pick_up_data():
		if post_obj is not None:
			logger.info("Start collecting data.")
			db_update_photo_is_work_1(post_obj)
			logger.critical("Виконуюю якісь дії!")
			logger.info("Finish collecting data.")
			db_delete_executed_post(post_obj)
			logger.info("Post did deleted.")

			# TODO if process then is_work == True and select is_work == False
			# TODO join to the sub reddit
