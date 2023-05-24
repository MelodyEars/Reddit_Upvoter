# from random import shuffle

from base_exception import RanOutAccountsForLinkException
from Uprove_TG_Bot.handl_info import check_proxy
# from database import db_save_1_by_id

from database.vote_tg_bot.actions_in_db import db_get_random_account_with_0, db_exist_record_link_account
from database.vote_tg_bot.get import db_get_link_id, db_get_cookie_proxy


def pick_up_account_to_link(link_from_file):
	link_id = db_get_link_id(link_from_file)

	cookies_db_objs = list(db_get_random_account_with_0())
	# shuffle(cookies_db_objs)

	for cookie_db_obj in cookies_db_objs:
		outcome_created, work_link_account_obj = db_exist_record_link_account(
			link_id=link_id, cookie_id=cookie_db_obj.id
		)

		if outcome_created:  # if create record return TRUE
			# db_save_1_by_id(cookie_db_obj.id)  # bot engaged
			return link_id, cookie_db_obj, work_link_account_obj

	else:
		# This exception will be earlier in db_get_random_account_with_0
		raise RanOutAccountsForLinkException


def collection_info(reddit_link: str):
	link_id, account_obj, work_link_account_obj = pick_up_account_to_link(reddit_link)
	# get from db account not worked random choice
	path_cookie, dict_proxy, log_pswd = db_get_cookie_proxy(account_obj)

	check_proxy(**dict_proxy)

	reddit_username = path_cookie.stem  # Path to str

	dict_for_browser = {
		"link_reddit": reddit_link,
		"dict_proxy": dict_proxy,
		"path_cookie": path_cookie,
		"reddit_username": reddit_username,
		"log_pswd": log_pswd,
	}

	return work_link_account_obj, dict_for_browser
