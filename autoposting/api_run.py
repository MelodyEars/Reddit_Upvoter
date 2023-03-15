from database import JobModel
from .network import CreatePost

from .handl_obj import get_info_from_obj

api: CreatePost = None


# ________________________ open browser _______________________
def connect_api(id_jobmodel: JobModel):
	path_cookie, proxy = get_info_from_obj(id_jobmodel)
	with CreatePost(path_cookie=path_cookie, proxy=proxy) as api:
		api.check_cookie()
		return api


def delete_all_posts():
	api.attend_profile_page()

	# delete all profile's posts
	api.delete_all_posts()


	# _________________________  Imgur ______________________________
def get_url_imgur_img(path_photo: str):
	api.upload_video(path_photo)
	return api.grub_link()


	# ___________________________  Reddit  ____________________________
def reddit_create_post(photo_url: str, title: str, link_sub_reddit: str):
	api.create_post(title, photo_url, link_sub_reddit)

	return api.get_post_url()


def completed_session():
	if api is not None:
		api.client_cookie.save()
		api.DRIVER.quit()
