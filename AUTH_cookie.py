from multiprocessing import freeze_support

from loguru import logger

from SETTINGS import mine_project
from Uprove_TG_Bot.restrict import check_access
from auth_reddit import check_new_acc
from work_fs import path_near_exefile, auto_create


@logger.catch
def main():
    if mine_project:
        check_new_acc()
    else:
        if check_access():
            check_new_acc()
        else:
            logger.error("Доступ запрещен проверте подписку.")


if __name__ == '__main__':
    freeze_support()

    logger.add(
        auto_create(path_near_exefile("logs"), _type="dir") / "GetCookie.log",
        format="{time} {level} {message}",
        level="INFO",
        rotation="10 MB",
        compression="zip"
    )

    main()

