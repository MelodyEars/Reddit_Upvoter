from .models_posting import autoposting_db, Posting, JobModel, Category, LinkSubReddit, Photo, UrlPost


# _______________________________ get __________________________________
def db_get_gen_categories(jobmodel_obj: JobModel) -> list[Posting.id_category]:
	with autoposting_db:
		category_objs = Posting.select(Posting.id_category).where(Posting.id_jobmodel == jobmodel_obj)
	return category_objs


def db_get_photos(jobmodel_obj: JobModel, category_obj: Category) -> list[Photo]:
	with autoposting_db:
		photos_objs = (
			Posting
			.select(Posting.id_photo)
			.where((Posting.id_jobmodel == jobmodel_obj) & (Posting.id_category == category_obj))
			.distinct()
			.execute()
		)

	return photos_objs


def db_pick_up_reddit_sub(jobmodel_obj: JobModel, category_obj: Category, photo_obj: Photo):
	with autoposting_db:
		link_sub_objs = (
			Posting
			.select(Posting.id_link_sub_reddit)
			.where(
				(Posting.id_jobmodel == jobmodel_obj) &
				(Posting.id_category == category_obj) &
				(Posting.id_photo == photo_obj)
			)
			.distinct()
			.execute()
		)

	return link_sub_objs


def db_get_post_for_posting(
		jobmodel_obj: JobModel, category_obj: Category, photo_obj: Photo, link_sub_obj: LinkSubReddit
) -> list[Posting]:
	with autoposting_db:
		post_obj = (
			Posting
			.select()
			.where(
				(Posting.id_jobmodel == jobmodel_obj) &
				(Posting.id_category == category_obj) &
				(Posting.id_photo == photo_obj) &
				(Posting.id_link_sub_reddit == link_sub_obj)
			)
			.execute()
		)

	return post_obj
