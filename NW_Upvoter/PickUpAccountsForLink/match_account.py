import asyncio

from random import shuffle

from loguru import logger

from NW_Upvoter.db_tortories_orm.models import RedditLink, Cookie
from NW_Upvoter.db_tortories_orm.query.bot_accounts import get_bot_accounts, get_unlinked_cookies
from NW_Upvoter.db_tortories_orm.query.link import db_get_or_create_link_obj
from NW_Upvoter.db_tortories_orm.query.record import db_exist_record_link_account
from NW_Upvoter.handl_info import check_proxy
from NW_Upvoter.handl_info.cookie import unpack_cooke_obj

from base_exception import RanOutAccountsForLinkException


async def pick_up_account_to_link(link_from_file):
	link_obj: RedditLink = await db_get_or_create_link_obj(link_from_file)
	logger.info(f"Link obj: {link_obj}")
	# cookies_db_objs: list[Cookie] = await get_bot_accounts()
	cookies_db_objs = await get_unlinked_cookies(link_obj)
	shuffle(cookies_db_objs)

	for cookie_db_obj in cookies_db_objs:
		outcome_created, work_link_account_obj = await db_exist_record_link_account(
			link_obj=link_obj,
			cookie_obj=cookie_db_obj
		)

		if outcome_created:  # if create record return TRUE
			# db_save_1_by_id(cookie_db_obj.id)  # bot engaged
			logger.info("Find account for link")
			return link_obj, cookie_db_obj, work_link_account_obj
		else:
			logger.info("Search account for link continue")

	else:
		# This exception will be earlier in db_get_random_account_with_0
		raise RanOutAccountsForLinkException


async def collection_info(reddit_link: str):
	logger.info(f"Start collection info for link: {reddit_link}")
	link_id, cookie_db_obj, work_link_account_obj = await pick_up_account_to_link(reddit_link)
	logger.info(f"Collection info for link: {reddit_link} - OK")
	# get from db account not worked random choice
	path_cookie, dict_proxy, log_pswd = unpack_cooke_obj(cookie_db_obj)

	# Check connect to proxy
	logger.info(f"Check connect to proxy: {dict_proxy}")
	await check_proxy(**dict_proxy)
	logger.info(f"Check connect to proxy: {dict_proxy} - OK")
	reddit_username = path_cookie.stem  # Path to str

	dict_for_browser = {
		"link_reddit": reddit_link,
		"dict_proxy": dict_proxy,
		"path_cookie": path_cookie,
		"reddit_username": reddit_username,
		"log_pswd": log_pswd,
	}

	return work_link_account_obj, dict_for_browser


if __name__ == '__main__':
	asyncio.run(collection_info('https://www.reddit.com/r/OnlyCurvyGW/comments/133x9i3/im_new_here_but_i_know_how_to_make_it_hot/'))
