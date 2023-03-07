from multiprocessing import freeze_support

from loguru import logger

from auth_reddit import check_new_acc
from work_fs import path_near_exefile

if __name__ == '__main__':
    freeze_support()

    logger.add(
        path_near_exefile("GetCookie.log"),
        format="{time} {level} {message}",
        level="INFO",
        rotation="10 MB",
        compression="zip"
    )

    check_new_acc()
