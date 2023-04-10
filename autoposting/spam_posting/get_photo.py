from pathlib import Path

from work_fs.PATH import path_near_exefile, dir_exists


def get_photo():
    path_photo: Path
    title: str

    if dir_exists(path_near_exefile("photo")):
        path_photo = list(path_near_exefile("photo").iterdir())[0]
        title = path_photo.stem
        return path_photo, title

    else:
        raise Exception("Please add folder 'photo'")
