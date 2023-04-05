import time
import traceback
from queue import Queue

from loguru import logger

from Uprove_TG_Bot.TG_bot.src.telegram.messages.user_msg import MESSAGES
from BASE_Reddit.exceptions import PostDeletedException
from database.vote_tg_bot.models import WorkAccountWithLink
from database.vote_tg_bot.delete import db_delete_record_work_account_with_link

from base_exception import RanOutAccountsForLinkException
# from Uprove_TG_Bot.handl_info import file_get_random_comments
from Uprove_TG_Bot.reddit_api_selenium import open_browser
from Uprove_TG_Bot.PickUpAccountsForLink import collection_info
from work_fs import path_near_exefile, auto_create


@logger.catch
def start_reddit_work(reddit_link: str, upvote_int: int, q: Queue):  # comments_int: int
    sub = reddit_link.split("/")[4]
    msg = MESSAGES['finish_process'] + " " + sub

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
    # list_comments = file_get_random_comments(comments_int)

    for _ in range(upvote_int):
        # comment = ""
        #
        # if list_comments:
        #     comment = list_comments.pop()

        try:
            logger.warning(f'Підбираю інформацію для "{reddit_link}"')
            id_work_link_account_obj, dict_for_browser = collection_info(reddit_link=reddit_link)

            logger.warning(f'''Відкриваю браузер для "{reddit_link}" і "{dict_for_browser["reddit_username"]}"''')
            open_browser(**dict_for_browser)  # , comment=comment)

        except RanOutAccountsForLinkException:
            msg = MESSAGES['not_enough_bots'] + sub
            logger.error(msg)
            break

        except PostDeletedException:
            msg = MESSAGES['deleted_post'] + sub
            logger.error(msg)
            break

        except Exception:
            db_delete_record_work_account_with_link(id_work_link_account_obj)
            logger.error(traceback.format_exc())

    end = time.time()
    elapsed_time = end - start
    logger.info(f"Program execute: {elapsed_time}")
    q.put(msg)
