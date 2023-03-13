from itertools import product
from pathlib import Path
from typing import Generator, List, Any

from loguru import logger

from database import JobModel
from work_fs import get_list_file, path_near_exefile
from database.autoposting_db import db_grab_model_obj


# _________________________________ gen path to info ________________________________
# def get_list_cookie_path():
# 	logger.info("generation list cookies path")
# 	list_model_obj = db_grab_model_obj()
# 	# gen_cookie_path = (path_near_exefile(model_obj.cookie_path) for model_obj in list_model_obj)
#
# 	# return gen_cookie_path, list_model_obj
# 	return list_model_obj


def gen_grub_category():
	logger.info("get category")

	list_model_objs: list[JobModel]
	# gen_cookie_path: Generator[Path, Any, None]

	# gen_cookie_path, list_model_obj = get_gen_list_cookie_path()
	list_model_objs = db_grab_model_obj()

	for jobmodel_obj in list_model_objs:
		root_folder_model = path_near_exefile(jobmodel_obj.root_folder)

		# get all folder in root model folder
		gen_model_category = (file for file in root_folder_model.iterdir() if file.is_dir())

		yield jobmodel_obj, gen_model_category


# ___________________________________ take data ______________________________________
def gives_gen_list_photo(category_folder: Path) -> Generator[Path, None, None]:
	path_photo_model = category_folder / "Photo"
	gen_photo = (file for file in path_photo_model.iterdir())
	return gen_photo


def gives_list_sub_reddit(category_folder: Path) -> list[str]:
	path_to_txt = category_folder / "sub_reddit.txt"
	list_sub_reddit = get_list_file(path_to_txt)

	return list_sub_reddit


def get_unique_combinations(path_category: Path) -> list[tuple[Path, str]]:
	list_photo: Generator[Path] = gives_gen_list_photo(path_category)
	list_sub_reddit: list[str] = gives_list_sub_reddit(path_category)

	# get unique combinations via itertools.product
	combinations = list(product(list_photo, list_sub_reddit))
	unique_combinations = list(set(combinations))

	return unique_combinations
