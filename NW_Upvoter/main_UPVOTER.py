import time
import traceback

from aiogram import types
from loguru import logger

from NW_Upvoter.TG_bot.src.repair_tgBOT import send_telegram_message
from NW_Upvoter.db_tortories_orm.query.bot_accounts import db_update_0_by_id
from NW_Upvoter.handl_info.count_upvoter import adder_count_upvote
from NW_Upvoter.handl_info.link.create_obj_in_db import analizated_link
from base_exception import RanOutAccountsForLinkException, ThisLinkIsNotPostException
from BASE_Reddit.exceptions import PostDeletedException, NotLoadPageException

from NW_Upvoter.db_tortories_orm.query.record import db_delete_record_work_account_with_link
from NW_Upvoter.TG_bot.src.telegram.messages.user_msg import MESSAGES
from NW_Upvoter.reddit_api_selenium import open_browser
from NW_Upvoter.PickUpAccountsForLink import collection_info


async def body_loop(msg, link_obj):
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
        msg = str(MESSAGES['not_enough_bots'])
        logger.error(msg)
        if cookie_db_obj:
            await db_update_0_by_id(cookie_db_obj.id)  # bot engaged

        return "break", msg

    except PostDeletedException:
        await db_delete_record_work_account_with_link(id_work_link_account_obj)
        msg = str(MESSAGES['deleted_post'])
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

        return await body_loop(msg, link_obj)

    return None, msg


@logger.catch
async def start_reddit_work(reddit_link: str, upvote_int: int, message: types.Message):
    # TODO: if tg-user has 2 threads, then he can't start 3 thread
    msg = str(MESSAGES['finish_process'])

    # time
    start = time.time()
    try:
        link_obj = await analizated_link(message, reddit_link, upvote_int)
    except ThisLinkIsNotPostException:
        msg = str(MESSAGES['this_link_is_not_post'])
        await send_telegram_message(message, msg)
        return

    if link_obj:
        upvote_int = adder_count_upvote(upvote_int)

        counter = 0
        while counter < upvote_int:
            start_open_browser = time.time()

            logger.info(f"Upvote count: {counter}")
            condition, msg = await body_loop(msg, link_obj)

            end_open_browser = time.time()
            elapsed_time = end_open_browser - start_open_browser
            logger.info(f"Open browser: {elapsed_time}")

            if condition is not None:
                # terminated send message
                break
            counter += 1
    else:
        msg = str(MESSAGES['post_is_sent'])

    await send_telegram_message(message, msg)
    end = time.time()
    elapsed_time = end - start
    logger.info(f"Program execute: {elapsed_time}")
