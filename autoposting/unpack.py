
# print url post to txt after execute program

from loguru import logger

from database.autoposting_db.models_posting import JobModel, Photo, Category, LinkSubReddit, Posting
from database.autoposting_db import db_grab_model_obj, db_get_gen_categories, db_get_photos, db_pick_up_reddit_sub, \
	db_get_post_for_posting


def pick_up_link_sub_reddit(jobmodel_obj: JobModel, category_obj: Category, photo_obj: Photo):
	link_sub_objs: list[LinkSubReddit] = db_pick_up_reddit_sub(jobmodel_obj, category_obj, photo_obj)

	for link_sub_obj in link_sub_objs:
		logger.info(link_sub_obj.link_SubReddit)  # __________________ log link
		yield jobmodel_obj, category_obj, photo_obj, link_sub_obj


def pick_up_photos(jobmodel_obj: JobModel, category_obj: Category):
	photos_objs: list[Photo] = db_get_photos(jobmodel_obj, category_obj)

	for photo_obj in photos_objs:
		logger.info(photo_obj.path_photo)  # __________________ log photo
		yield pick_up_link_sub_reddit(jobmodel_obj, category_obj, photo_obj)


def pick_up_category(jobmodel_obj: JobModel):
	category_objs: list[Category] = db_get_gen_categories(jobmodel_obj)

	for category_obj in category_objs:
		logger.info(category_obj.name_category)  # __________________ log category
		yield pick_up_photos(jobmodel_obj, category_obj)


def pick_up_data():
	jobmodels_objs: list[JobModel] = db_grab_model_obj()

	# while list exists from Posting.select()
	for jobmodels_obj in jobmodels_objs:
		logger.info(jobmodels_obj.account.login)  # __________________ log account's login
		yield pick_up_category(jobmodels_obj)


def yield_up_data_from_db():
	for jobmodel_obj, category_obj, photo_obj, link_sub_obj in pick_up_data():
		logger.info("Start collecting data.")
		post_obj: list[Posting] = db_get_post_for_posting(jobmodel_obj, category_obj, photo_obj, link_sub_obj)
		logger.info(post_obj[0].id_jobmodel.model_name)
		logger.info(post_obj[0].id_category.name_category)
		logger.info(post_obj[0].id_link_sub_reddit.link_SubReddit)
		logger.info(post_obj[0].id_photo.path_photo)
		logger.info("Finish collecting data.")
		# TODO delete by id
		# TODO if process then is_work == True and select is_work == False
