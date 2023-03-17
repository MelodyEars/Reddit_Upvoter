from pathlib import Path

from work_fs import path_near_exefile
from database import Posting, JobModel, LinkSubReddit


def get_info_from_obj(jobmodel_obj: JobModel):
	path_cookie = path_near_exefile(jobmodel_obj.cookie_path)

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

	return path_photo, title, link_sub_reddit
