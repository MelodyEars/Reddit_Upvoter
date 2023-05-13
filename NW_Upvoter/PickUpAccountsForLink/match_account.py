from random import shuffle

from loguru import logger

from NW_Upvoter.db_tortories_orm.models import RedditLink
from NW_Upvoter.db_tortories_orm.query.bot_accounts import get_unlinked_cookies, db_save_1_by_id
from NW_Upvoter.db_tortories_orm.query.record import db_exist_record_link_account
from NW_Upvoter.handl_info import check_proxy
from NW_Upvoter.handl_info.cookie import unpack_cooke_obj

from base_exception import RanOutAccountsForLinkException


async def pick_up_account_to_link(link_obj):
	"""Pick up account to link"""
	# cookies_db_objs: list[Cookie] = await get_bot_accounts()
	cookies_db_objs = await get_unlinked_cookies(link_obj)
	shuffle(cookies_db_objs)

	for cookie_db_obj in cookies_db_objs:
		outcome_created, work_link_account_obj = await db_exist_record_link_account(
			link_obj=link_obj,
			cookie_obj=cookie_db_obj
		)

		if outcome_created:  # if create record return TRUE
			logger.info("Find account for link")
			await db_save_1_by_id(cookie_db_obj.id)  # bot engaged
			return cookie_db_obj, work_link_account_obj
		else:
			logger.info("Search account for link continue")

	else:
		# This exception will be earlier in db_get_random_account_with_0
		raise RanOutAccountsForLinkException


async def collection_info(link_obj: RedditLink):
	"""Collection info for link"""
	reddit_link = link_obj.link

	logger.info(f"Start collection info for link: {reddit_link}")
	cookie_db_obj, work_link_account_obj = await pick_up_account_to_link(link_obj)
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

	return work_link_account_obj, dict_for_browser, cookie_db_obj
