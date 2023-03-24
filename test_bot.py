import re

from loguru import logger

from work_fs.PATH import path_near_exefile, move_file_or_dir
from work_fs.read_file import get_list_file
from work_fs.write_to_file import write_list_to_file


def name_in_file():
    path_file_names = path_near_exefile("name_photo.txt")
    list_names = get_list_file(path_file_names)

    while list_names:
        list_names = get_list_file(path_file_names)
        name = list_names.pop()
        new_filename = re.sub(r'[<>:"/\\|?*]', '', name)
        yield new_filename + ".jpg"
        write_list_to_file(path_file_names, list_names)
    else:
        raise Exception("Немає імен для фото, перевірь name_photo.txt")


def gen_photo_paths():
    photos_paths = path_near_exefile("Photo")
    list_paths_photo = [old_path for old_path in photos_paths.iterdir()]
    return list_paths_photo


def main():
    list_paths_photo = gen_photo_paths()
    for count, name in enumerate(name_in_file()):
        logger.info(name)
        old_path = list_paths_photo[count]
        new_path = old_path.parent / name
        logger.info(new_path)
        move_file_or_dir(old_path, new_path)


if __name__ == '__main__':
    logger.info("Start")
    main()
    logger.info("Finish")
