from contextlib import contextmanager
from pathlib import Path

from loguru import logger

from Uprove_TG_Bot.reddit_api_selenium.exceptions import CookieInvalidException
from auth_reddit import get_cookies
from database import JobModel, Account

from .network import CreatePost
from .handl_obj import get_info_from_obj


def getter_cookie(jobmodel_obj: JobModel, proxy: dict):
	account: Account = jobmodel_obj.account
	account_dict = {
		"login": account.login,
		"password": account.password,
	}

	get_cookies(account=account_dict, proxy_for_api=proxy)

	return connect_api(jobmodel_obj)


# ________________________ open browser _______________________
@contextmanager
def connect_api(jobmodel_obj: JobModel):
	path_cookie, proxy = get_info_from_obj(jobmodel_obj)
	logger.info('Run browser!')
	with CreatePost(path_cookie=path_cookie, proxy=proxy) as api:
		logger.info('Check cookie!')
		try:
			api.check_cookie()
		except CookieInvalidException:
			api.DRIVER.quit()
			logger.error(f'Cookie "{jobmodel_obj.model_name}" invalid.')
			# return getter_cookie(jobmodel_obj, path_cookie)

	logger.info('Return instance!')
	try:
		yield api
	finally:
		logger.warning("Close browser!")
		api.client_cookie.save()
		api.DRIVER.quit()


def delete_all_posts(api: CreatePost):
	logger.info("Delete all profile's posts.")
	api.attend_profile_page()

	# delete all profile's posts
	return api.delete_all_posts()


	# _________________________  Imgur ______________________________
def get_url_imgur_img(path_photo: str, api: CreatePost):
	logger.info("Upload photo on Imgur and get url.")
	api.upload_video(path_photo)

	return api.grub_link()


	# ___________________________  Reddit  ____________________________
def reddit_create_post(photo_url: str, title: str, link_sub_reddit: str, api: CreatePost):
	logger.info("Creating post")
	api.create_post(title, photo_url, link_sub_reddit)

	return api.get_post_url()


# def completed_session(api: CreatePost):
#
# 	if api is not None:
# 		logger.warning("Close browser!")
# 		api.client_cookie.save()
# 		api.DRIVER.quit()
