from pathlib import Path

from work_fs import auto_create, path_near_exefile, write_line
from work_fs.PATH import move_file_or_dir

from .SUB_dict import sub_reddit_catalog_dict


def move_cookie(data_path: Path, old_path_cookie: str):

	old_path: Path = path_near_exefile(old_path_cookie)
	new_path: Path = auto_create(data_path, _type="dir") / old_path.name
	move_file_or_dir(old_path, new_path)

	new_path_to_db = new_path.relative_to(new_path.parent.parent)

	return new_path_to_db


def gen_catalog_sub(category: Path):
	name_sub = category.name
	list_sub = sub_reddit_catalog_dict[name_sub]

	write_line(category / "sub_reddit.txt", list_sub)


def generation_category(data_path: Path):
	# create Path categories folder
	path_categories = (data_path / topik for topik, _ in sub_reddit_catalog_dict.items())

	# content in folder
	for category_path in path_categories:
		auto_create(category_path / "Photo", _type="dir")
		gen_catalog_sub(category_path)


def prepare_folder(model_name: str):
	lib_path: Path = auto_create(path_near_exefile("Library"), _type="dir")
	data_path = auto_create(lib_path / model_name, _type="dir")

	generation_category(data_path)

	return data_path
