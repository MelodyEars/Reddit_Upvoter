from pathlib import Path

from loguru import logger

from BASE_Reddit.exceptions import CookieInvalidException

from auth_reddit import get_cookies

from database import JobModel, Account
from database.autoposting_db import db_write_url

from work_fs.PATH import path_near_exefile, move_file_or_dir
from work_fs.write_to_file import write_line

from . import yield_up_data_from_db

from .network import CreatePost
from .handl_obj import get_info_from_obj, get_info_about_photo
from .network.execeptions_autoposting import WaitRequestToSubredditException, WaitingPostingException


def getter_cookie(jobmodel_obj: JobModel, proxy_for_api: dict, model_cookie_path: Path):
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
	return work_browser(jobmodel_obj, model_cookie_path, proxy_for_api)


def work_browser(jobmodel_obj: JobModel, cookie_path=None, proxy_for_api=None):
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
			return getter_cookie(jobmodel_obj, proxy_for_api, cookie_path)

		logger.info("Delete all profile's posts.")
		BROWSER.delete_all_posts()

		for post_obj in yield_up_data_from_db(jobmodel_obj):
			try:
				# get info about post
				path_photo, title, link_sub_reddit = get_info_about_photo(post_obj)

				# _________________________  Imgur ______________________________
				logger.info("Upload photo on Imgur and get url.")
				BROWSER.upload_video(path_photo)

				photo_url = BROWSER.grub_link()

				# ___________________________  Reddit  ____________________________
				logger.info("Creating post")
				BROWSER.create_post(title, photo_url, link_sub_reddit)

				reddit_post_url = BROWSER.get_post_url()

				# _______________________________  to db  ____________________
				db_write_url(reddit_post_url)
				write_line(path_near_exefile("Post_url.txt"), reddit_post_url)

			except WaitRequestToSubredditException:
				logger.error("WaitRequestToSubredditException -> Wait for offer posting from subreddit.")
			except WaitingPostingException:
				logger.error('Reddit give you a break < 1hour')

		BROWSER.client_cookie.save()
		BROWSER.DRIVER.quit()
		logger.warning("Close browser!")


