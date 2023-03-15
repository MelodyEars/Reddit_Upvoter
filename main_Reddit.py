import time
import traceback

from loguru import logger

from database.vote_tg_bot.models import WorkAccountWithLink
from database.vote_tg_bot.delete import db_delete_record_work_account_with_link

from base_exception import RanOutAccountsForLinkException
from Uprove_TG_Bot.handl_info import file_get_random_comments
from Uprove_TG_Bot.reddit_api_selenium import open_browser
from Uprove_TG_Bot.PickUpAccountsForLink import collection_info
from work_fs import path_near_exefile, auto_create


@logger.catch
def start_reddit_work(reddit_link: str, upvote_int: int, comments_int: int):
    logger.add(
        auto_create(path_near_exefile("logs"), _type="dir") / "BaseReddit.log",
        format="{time} {level} {message}",
        level="INFO",
        rotation="10 MB",
        compression="zip"
    )

    start = time.time()

    id_work_link_account_obj = WorkAccountWithLink

    # get random comment from txt
    list_comments = file_get_random_comments(comments_int)

    for text_comment in range(upvote_int):
        comment = ""

        if list_comments:
            comment = list_comments.pop()

        try:
            logger.info(f'Підбираю інформацію для "{reddit_link}"')
            id_work_link_account_obj, dict_for_browser = collection_info(reddit_link=reddit_link)

            logger.info(f'''Відкриваю браузер для "{reddit_link}" і "{dict_for_browser["reddit_username"]}"''')
            open_browser(**dict_for_browser, comment=comment)

        except RanOutAccountsForLinkException:
            logger.error("Недостатньо акаунтів, щоб продовжувати робити апвоути.")
            break

        except Exception:
            db_delete_record_work_account_with_link(id_work_link_account_obj)
            logger.error(traceback.format_exc())

    end = time.time()
    elapsed_time = end - start
    logger.info(f"Program execute: {elapsed_time}")
