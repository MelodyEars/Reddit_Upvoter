from multiprocessing import freeze_support

from loguru import logger
from CHECK_BAN import controller
from SETTINGS import mine_project
from access_bot.restrict import check_access
from work_fs import path_near_exefile, auto_create


@logger.catch
def main():
    if mine_project:
        controller()

    else:
        if check_access():
            controller()
        else:
            logger.error("Доступ запрещен проверте подписку.")


if __name__ == '__main__':
    freeze_support()
    logger.add(
        auto_create(path_near_exefile("logs"), _type="dir") / "CHECK_BAN.log",
        format="{time} {level} {message}",
        level="INFO",
        rotation="10 MB",
        compression="zip"
    )

    try:
        main()
    finally:
        input("Press Enter:")
