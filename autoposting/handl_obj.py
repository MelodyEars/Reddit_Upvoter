from pathlib import Path

from work_fs import path_near_exefile
from database import Posting, JobModel, LinkSubReddit


def get_info_from_obj(id_jobmodel: JobModel):
	path_cookie = path_near_exefile(id_jobmodel.cookie_path)

	proxy = {
		"host": id_jobmodel.proxy.host,
		"port": id_jobmodel.proxy.port,
		"user": id_jobmodel.proxy.user,
		"password": id_jobmodel.proxy.password
	}

	return path_cookie, proxy


def get_info_about_photo(post_obj: Posting):
	path_photo: Path = path_near_exefile(post_obj.id_photo.path_photo)
	title: str = path_photo.stem
	link_sub_reddit: LinkSubReddit = post_obj.id_link_sub_reddit.link_SubReddit

	return path_photo, title, link_sub_reddit
