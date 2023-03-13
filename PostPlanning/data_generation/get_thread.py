from pathlib import Path

from loguru import logger

from .info_from_folder import gen_grub_category, get_unique_combinations


def registration_to_db():
	logger.info("search info ")
	for jobmodel_obj, list_category in gen_grub_category():
		for path_category in list_category:
			name_category = path_category.name
			# get unique_combinations from model's photos and sub network for posting
			unique_combinations: list[tuple[Path, str]] = get_unique_combinations(path_category)

			# recording to db
			for photo_path, link_sub_reddit in unique_combinations:
				photo_path = photo_path.relative_to(photo_path.parent.parent.parent.parent.parent)

				yield jobmodel_obj, name_category, photo_path, link_sub_reddit

