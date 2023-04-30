from random import shuffle

from NW_Upvoter.db_tortories_orm.models import RedditLink, Cookie
from NW_Upvoter.db_tortories_orm.quiery.bot_accounts import get_bot_accounts
from NW_Upvoter.db_tortories_orm.quiery.link import db_get_or_create_link_obj
from base_exception import RanOutAccountsForLinkException

from Uprove_TG_Bot.handl_info import check_proxy

from database.vote_tg_bot.actions_in_db import db_exist_record_link_account
from database.vote_tg_bot.get import db_get_cookie_proxy


async def pick_up_account_to_link(link_from_file):
	link_obj: RedditLink = await db_get_or_create_link_obj(link_from_file)

	cookies_db_objs: list[Cookie] = get_bot_accounts()
	shuffle(cookies_db_objs)

	for cookie_db_obj in cookies_db_objs:
		outcome_created, work_link_account_obj = db_exist_record_link_account(
			link_id=link_obj, cookie_id=cookie_db_obj.id
		)

		if not outcome_created:  # if create record return TRUE
			# db_save_1_by_id(cookie_db_obj.id)  # bot engaged
			return link_obj, cookie_db_obj, work_link_account_obj

	else:
		# This exception will be earlier in db_get_random_account_with_0
		raise RanOutAccountsForLinkException


async def collection_info(reddit_link: str):
	link_id, account_obj, work_link_account_obj = await pick_up_account_to_link(reddit_link)
	# get from db account not worked random choice
	path_cookie, dict_proxy, id_account = await db_get_cookie_proxy(account_obj)

	check_proxy(**dict_proxy)

	reddit_username = path_cookie.stem  # Path to str

	dict_for_browser = {
		"link_reddit": reddit_link,
		"dict_proxy": dict_proxy,
		"path_cookie": path_cookie,
		"reddit_username": reddit_username,
		"id_cookie": id_account,
	}

	return work_link_account_obj, dict_for_browser
