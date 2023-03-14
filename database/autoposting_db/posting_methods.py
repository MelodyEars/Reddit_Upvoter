from .models_posting import autoposting_db, Posting, JobModel, Category, LinkSubReddit, Photo, UrlPost


# _______________________________ get __________________________________
def db_get_gen_categories(jobmodel_obj: JobModel) -> list[Posting.id_category]:
	with autoposting_db:
		post_objs = Posting.select().where(
			Posting.id_jobmodel == jobmodel_obj
		)

	category_objs = [post.id_category for post in post_objs]
	return category_objs


def db_get_photos(jobmodel_obj: JobModel, category_obj: Category) -> list[Photo]:
	with autoposting_db:
		post_objs: list[Posting] = (
			Posting
			.select()
			.where((Posting.id_jobmodel == jobmodel_obj) & (Posting.id_category == category_obj))
			.distinct()
		)

	photos_objs = [post.id_photo for post in post_objs]
	return photos_objs


def db_pick_up_reddit_sub(jobmodel_obj: JobModel, category_obj: Category, photo_obj: Photo):
	with autoposting_db:
		post_objs: list[Posting] = (
			Posting
			.select()
			.where(
				(Posting.id_jobmodel == jobmodel_obj) &
				(Posting.id_category == category_obj) &
				(Posting.id_photo == photo_obj)
			)
			.distinct()
		)

	link_sub_objs = [post.id_link_sub_reddit for post in post_objs]
	return link_sub_objs


def db_get_post_for_posting(
		jobmodel_obj: JobModel, category_obj: Category, photo_obj: Photo, link_sub_obj: LinkSubReddit
) -> list[Posting]:
	with autoposting_db:
		post_obj: list[Posting] = (
			Posting
			.select()
			.where(
				(Posting.id_jobmodel == jobmodel_obj) &
				(Posting.id_category == category_obj) &
				(Posting.id_photo == photo_obj) &
				(Posting.id_link_sub_reddit == link_sub_obj)
			)
		)

	return post_obj


# ___________________________________________  DELETE  _________________________________________
def delete_post_by_id(post_id: Posting.id):
	with autoposting_db:
		Posting.delete_by_id(post_id)
