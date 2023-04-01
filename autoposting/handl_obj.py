from pathlib import Path

from loguru import logger

from database.autoposting_db import db_delete_executed_post
from work_fs import path_near_exefile, file_exists
from database import Posting, JobModel, LinkSubReddit


def get_info_from_obj(jobmodel_obj: JobModel) -> tuple[Path, dict[str:str]]:
	path_cookie: Path = path_near_exefile(jobmodel_obj.cookie_path)

	proxy = {
		"host": jobmodel_obj.proxy.host,
		"port": jobmodel_obj.proxy.port,
		"user": jobmodel_obj.proxy.user,
		"password": jobmodel_obj.proxy.password
	}

	return path_cookie, proxy


def get_info_about_photo(post_obj: Posting):
	path_photo: Path = path_near_exefile(post_obj.id_photo.path_photo)
	title: str = post_obj.id_photo.title
	link_sub_reddit: LinkSubReddit = post_obj.id_link_sub_reddit.link_SubReddit
	if file_exists(path_photo):
		return path_photo, title, link_sub_reddit

	else:
		logger.error(f"This photo not exists {path_photo}")
		logger.info("Post will delete from db.")
		db_delete_executed_post(post_obj)
		logger.info("Post did deleted from db.")
		return None, None, None
