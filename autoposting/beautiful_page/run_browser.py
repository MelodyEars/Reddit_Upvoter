import time
import traceback
from pathlib import Path

from loguru import logger
from selenium.common import UnexpectedAlertPresentException

from BASE_Reddit.exceptions import CookieInvalidException

from auth_reddit import get_cookies

from database import JobModel, Account, Posting
from database.autoposting_db import db_add_url_to_upvoter, db_get_list_post_obj_sort_by_date, \
	db_SUBLINK_reset_is_submitted, db_PHOTO_reset_is_submitted, db_add_date_post, db_del_post_banned_sub

from work_fs.PATH import path_near_exefile, move_file_or_dir

from autoposting.beautiful_page.unpack import yield_up_data_from_db, if_enough_post
from autoposting.beautiful_page.handl_obj import get_info_from_obj, get_info_about_photo
from autoposting.network.execeptions_autoposting import WaitRequestToSubredditException, WaitingPostingException, \
	NotTrustedMembersException, SubredditWasBannedException

from autoposting.network.api import CreatePost


def cookie_refresh(jobmodel_obj: JobModel, proxy_for_api: dict, model_cookie_path: Path):
	logger.error(f'Cookie "{jobmodel_obj.model_name}" invalid.')

	account: Account = jobmodel_obj.account
	account_dict = {
		"login": account.login,
		"password": account.password,
	}

	# model_cookie_path.unlink()
	cookie_path, _ = get_cookies(account=account_dict, proxy_for_api=proxy_for_api)
	old_path: Path = path_near_exefile(cookie_path)
	move_file_or_dir(old_path, model_cookie_path)

	logger.info("Refrash browser!")
	return run_browser(jobmodel_obj, model_cookie_path, proxy_for_api)


def delete_post(BROWSER: CreatePost, jobmodel_obj: JobModel):
	logger.info("get last post.")
	# get all model's posts
	list_post_obj = list(db_get_list_post_obj_sort_by_date(jobmodel_obj))

	if list_post_obj:
		# get last post_obj
		older_post_obj: Posting = list_post_obj.pop()
		logger.info(f"Older post: {older_post_obj.id_url.url}, {older_post_obj.date_posted}")
		print(older_post_obj.date_posted)
		logger.info("del last post by date in browser.")
		BROWSER.delete_last_post(older_post_obj.id_url.url)  # add by post_obj.url
		logger.info("deleted last post by date in browser.")

		# db update photo and subreddit link 1->0
		db_SUBLINK_reset_is_submitted(older_post_obj.id_link_sub_reddit.id)
		db_PHOTO_reset_is_submitted(older_post_obj.id_photo.id)

	else:
		# if not exists records in db this means it's model new,
		# then need delete all on the reddit profile's page
		logger.info("Delete all profile's posts.")
		BROWSER.delete_all_posts()


def run_browser(jobmodel_obj: JobModel, cookie_path=None, proxy_for_api=None):
	if cookie_path is None:
		cookie_path, proxy_for_api = get_info_from_obj(jobmodel_obj)

	logger.critical(cookie_path)

	logger.info('Run browser!')
	with CreatePost(path_cookie=cookie_path, proxy=proxy_for_api) as BROWSER:
		logger.info('Check cookie!')
		try:
			BROWSER.check_cookie()
		except CookieInvalidException:
			BROWSER.DRIVER.quit()
			return cookie_refresh(jobmodel_obj, proxy_for_api, cookie_path)

		# delete post by date in browser and db
		delete_post(BROWSER, jobmodel_obj)
		logger.info("Finish delete post")

		for post_obj in yield_up_data_from_db(jobmodel_obj):  # get obj where url == None
			try:
				# get info about post
				path_photo, title, link_sub_reddit = get_info_about_photo(post_obj)

				if path_photo:  # return path_photo NOne if file not exists in folder and delete all post in db
					# _________________________  Imgur ______________________________
					logger.info("Upload photo on Imgur and get url.")
					BROWSER.upload_video(path_photo)

					photo_url = BROWSER.grub_link()

					# ___________________________  Reddit  ____________________________
					logger.info("Creating post")
					BROWSER.create_post(title, photo_url, link_sub_reddit)

					reddit_post_url = BROWSER.get_post_url()

					# _______________________________  to db  ____________________
					db_add_url_to_upvoter(post_obj, reddit_post_url)
					db_add_date_post(post_obj.id)  # date posted
					# adder_list(path_near_exefile("Post_url.txt"), reddit_post_url)

			except WaitingPostingException:
				logger.error('Reddit give you a break < 1hour')
				# without continue because this post is posted
				break

			except NotTrustedMembersException:
				logger.error("NotTrustedMembersException -> This community only allows trusted members to post here.")
				db_del_post_banned_sub(link_sub_reddit)

			except SubredditWasBannedException:
				logger.error("SubredditWasBannedException -> This subreddit was banned due to being unmoderated.")
				db_del_post_banned_sub(link_sub_reddit)

			except WaitRequestToSubredditException:
				logger.error("WaitRequestToSubredditException -> Wait for offer posting from subreddit.")

			except UnexpectedAlertPresentException:
				logger.error('UnexpectedAlertPresentException -> refresh browser')
				# BROWSER.close_alert(link_sub_reddit)
				return run_browser(jobmodel_obj, cookie_path, proxy_for_api)

			except Exception:
				logger.error(traceback.format_exc())

		BROWSER.client_cookie.save()
		BROWSER.DRIVER.quit()
		logger.warning("Close browser!")


def autoposting(jobmodel_obj: JobModel):
	if_enough_post(jobmodel_obj)
	start_time = time.time()  # get the start time of the program
	logger.warning(f"Start time {start_time}")

	run_browser(jobmodel_obj)

	end_time = time.time()  # get the end time of the program
	logger.warning(f"End time {end_time}")

	running_time = end_time - start_time  # calculate the program's running time
	logger.info(f"The program's running time {running_time}")

	if running_time < 900:  # if the program runs less than 3 hours
		time_sleep = 900 - running_time
		time.sleep(time_sleep)  # sleep for the remaining time

	# the program will start again every 10 minutes due to the while loop

