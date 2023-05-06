import time
import traceback

from aiogram import types
from loguru import logger

from NW_Upvoter.TG_bot.src.repair_tgBOT import send_telegram_message
from base_exception import RanOutAccountsForLinkException
from BASE_Reddit.exceptions import PostDeletedException, NotLoadPageException
from work_fs import path_near_exefile, auto_create

from NW_Upvoter.db_tortories_orm.query.record import db_delete_record_work_account_with_link
from NW_Upvoter.TG_bot.src.telegram.messages.user_msg import MESSAGES
from NW_Upvoter.reddit_api_selenium import open_browser
from NW_Upvoter.PickUpAccountsForLink import collection_info


async def body_loop(reddit_link, sub, work_link_account_obj, msg):
    try:
        logger.warning(f'Підбираю інформацію для "{reddit_link}"')
        work_link_account_obj, dict_for_browser = await collection_info(reddit_link=reddit_link)
        logger.warning(f'''Відкриваю браузер для "{reddit_link}" і "{dict_for_browser["reddit_username"]}"''')

        await open_browser(dict_for_browser)  # , comment=comment)

    except RanOutAccountsForLinkException:
        msg = str(MESSAGES['not_enough_bots']) + str(sub)
        logger.error(msg)
        return "break", msg

    except PostDeletedException:
        await db_delete_record_work_account_with_link(work_link_account_obj)
        msg = str(MESSAGES['deleted_post']) + str(sub)
        logger.error(msg)
        return "break", msg

    except NotLoadPageException:
        logger.error("Not load page in Reddit, start new account")
        await db_delete_record_work_account_with_link(work_link_account_obj)

    except Exception:
        await db_delete_record_work_account_with_link(work_link_account_obj)
        logger.error(traceback.format_exc())
        return await body_loop(reddit_link, sub, work_link_account_obj, msg)

    return None, msg


@logger.catch
async def start_reddit_work(reddit_link: str, upvote_int: int, message: types.Message):  # comments_int: int
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
    id_work_link_account_obj = None

    counter = 0
    while counter < upvote_int:
        condition, msg = await body_loop(reddit_link, sub, id_work_link_account_obj, msg)
        if condition is not None:
            break
        counter += 1
        print(counter)

    await send_telegram_message(message, msg)
    end = time.time()
    elapsed_time = end - start
    logger.info(f"Program execute: {elapsed_time}")
