import time
import traceback

from loguru import logger

from Uprove_TG_Bot.TG_bot.src.telegram.messages.user_msg import MESSAGES
from BASE_Reddit.exceptions import PostDeletedException
from database.vote_tg_bot.models import WorkAccountWithLink
# from database.vote_tg_bot.delete import db_delete_record_work_account_with_link

from base_exception import RanOutAccountsForLinkException
from Uprove_TG_Bot.reddit_api_selenium import open_browser
from Uprove_TG_Bot.PickUpAccountsForLink import collection_info
from work_fs import path_near_exefile, auto_create


def body_loop(reddit_link, sub, work_link_account_obj, msg, LIST_PID_BROWSERS):
    try:
        logger.warning(f'Підбираю інформацію для "{reddit_link}"')
        work_link_account_obj, dict_for_browser = collection_info(reddit_link=reddit_link)

        logger.warning(f'''Відкриваю браузер для "{reddit_link}" і "{dict_for_browser["reddit_username"]}"''')
        dict_for_browser['LIST_PID_BROWSERS'] = LIST_PID_BROWSERS
        open_browser(**dict_for_browser)  # , comment=comment)

    except RanOutAccountsForLinkException:
        msg = str(MESSAGES['not_enough_bots']) + str(sub)
        logger.error(msg)
        return "break", msg

    except PostDeletedException:
        msg = str(MESSAGES['deleted_post']) + str(sub)
        logger.error(msg)
        return "break", msg

    except Exception:
        work_link_account_obj.delete_instance()
        # db_delete_record_work_account_with_link(work_link_account_obj)
        logger.error(traceback.format_exc())
        return body_loop(reddit_link, sub, work_link_account_obj, msg, LIST_PID_BROWSERS)

    return None, msg


@logger.catch
def start_reddit_work(reddit_link: str, upvote_int: int, LIST_PID_BROWSERS):  # comments_int: int
    sub = reddit_link.split("/")[4]
    msg = str(MESSAGES['finish_process']) + " " + str(sub)

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
        condition, msg = body_loop(reddit_link, sub, id_work_link_account_obj, msg, LIST_PID_BROWSERS)
        if condition == "break":
            break

    end = time.time()
    elapsed_time = end - start
    logger.info(f"Program execute: {elapsed_time}")
    return msg
