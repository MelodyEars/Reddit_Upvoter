from pathlib import Path

from .models_posting import autoposting_db, Posting, JobModel, Category, LinkSubReddit, Photo, UrlPost


# ----------------------- create -------------------------
def create_table_posting():
	with autoposting_db:
		autoposting_db.create_tables([Posting, Photo, LinkSubReddit, Category, UrlPost])


def db_add_record_post(jobmodel_obj: JobModel, name_category: str, photo_path: Path, link_sub_reddit: str):
	with autoposting_db.atomic():
		link_obj, _ = LinkSubReddit.get_or_create(link_SubReddit=link_sub_reddit)
		photo_obj, _ = Photo.get_or_create(path_photo=photo_path)
		category_obj, _ = Category.get_or_create(name_category=name_category)

		_, created = Posting.get_or_create(
			id_jobmodel=jobmodel_obj, id_link_sub_reddit=link_obj, id_photo=photo_obj, id_category=category_obj
		)
		return created


# ------------------------- get --------------------------
def db_grab_model_obj() -> list[JobModel]:
	with autoposting_db.connection_context():
		query = JobModel.select()
		return list(query)
