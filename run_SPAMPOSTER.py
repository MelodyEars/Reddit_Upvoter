from loguru import logger

from Uprove_TG_Bot.handl_info import get_account_file, file_get_proxy
from autoposting.spam_posting.run_browser import activate_spam_poster
from work_fs.PATH import auto_create, path_near_exefile


@logger.catch
def main():
    proxy_for_api: dict[str: str]

    account: dict[str: str] = list(get_account_file(delete_from_file=True))[0]
    proxy_for_api, _, _ = file_get_proxy()

    activate_spam_poster(account, proxy_for_api)


if __name__ == '__main__':
    logger.add(
        auto_create(path_near_exefile("logs"), _type="dir") / "planning_post.log",
        format="{time} {level} {message}",
        level="INFO",
        rotation="10 MB",
        compression="zip"
    )

    try:
        main()
    finally:
        input("Press Enter:")
