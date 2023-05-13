import time
import traceback

from aiogram import types
from loguru import logger

from NW_Upvoter.TG_bot.src.repair_tgBOT import send_telegram_message
from NW_Upvoter.db_tortories_orm.models import RedditLink
from NW_Upvoter.db_tortories_orm.query.bot_accounts import db_update_0_by_id
from NW_Upvoter.db_tortories_orm.query.link import db_get_or_create_link_obj
from base_exception import RanOutAccountsForLinkException
from BASE_Reddit.exceptions import PostDeletedException, NotLoadPageException

from NW_Upvoter.db_tortories_orm.query.record import db_delete_record_work_account_with_link
from NW_Upvoter.TG_bot.src.telegram.messages.user_msg import MESSAGES
from NW_Upvoter.reddit_api_selenium import open_browser
from NW_Upvoter.PickUpAccountsForLink import collection_info


async def body_loop(sub, msg, link_obj):
    reddit_link = link_obj.link
    id_work_link_account_obj = None
    cookie_db_obj = None


    try:
        logger.warning(f'Підбираю інформацію для "{reddit_link}"')
        id_work_link_account_obj, dict_for_browser, cookie_db_obj = await collection_info(link_obj)
        logger.warning(f'''Відкриваю браузер для "{reddit_link}" і "{dict_for_browser["reddit_username"]}"''')

        await open_browser(dict_for_browser)  # , comment=comment)
        await db_update_0_by_id(cookie_db_obj.id)  # bot engaged

    except RanOutAccountsForLinkException:
        msg = str(MESSAGES['not_enough_bots']) + str(sub)
        logger.error(msg)
        if cookie_db_obj:
            await db_update_0_by_id(cookie_db_obj.id)  # bot engaged

        return "break", msg

    except PostDeletedException:
        await db_delete_record_work_account_with_link(id_work_link_account_obj)
        msg = str(MESSAGES['deleted_post']) + str(sub)
        logger.error(msg)

        if cookie_db_obj:
            await db_update_0_by_id(cookie_db_obj.id)  # bot engaged

        return "break", msg

    except NotLoadPageException:
        logger.error("Not load page in Reddit, start new account")
        await db_delete_record_work_account_with_link(id_work_link_account_obj)

        if cookie_db_obj:
            await db_update_0_by_id(cookie_db_obj.id)  # bot engaged

    except Exception:
        await db_delete_record_work_account_with_link(id_work_link_account_obj)
        logger.error(traceback.format_exc())

        if cookie_db_obj:
            await db_update_0_by_id(cookie_db_obj.id)  # bot engaged

        return await body_loop(sub, msg, link_obj)

    return None, msg


@logger.catch
async def start_reddit_work(reddit_link: str, upvote_int: int, message: types.Message):  # comments_int: int
    # time
    start = time.time()

    # info
    sub = "/".join(reddit_link.split("/")[3:5])
    msg = str(MESSAGES['finish_process']) + " " + str(sub)
    who_posted = message.from_user.username

    # db get link
    link_obj: RedditLink = await db_get_or_create_link_obj(reddit_link, who_posted, sub, upvote_int)

    counter = 0
    while counter < upvote_int:
        logger.info(f"Upvote count: {counter}")
        condition, msg = await body_loop(sub, msg, link_obj)

        if condition is not None:
            # terminated send message
            break
        counter += 1

    await send_telegram_message(message, msg)
    end = time.time()
    elapsed_time = end - start
    logger.info(f"Program execute: {elapsed_time}")
