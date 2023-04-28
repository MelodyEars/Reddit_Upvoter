import time

from .get_photo import get_photo
from .get_sub_file import gen_list_sub
from .network_spamposter.work_browser import SpamPosterReddit


def get_link_photo(api: SpamPosterReddit):
    path_photo, title = get_photo()

    api.upload_photo_imgur(path_photo)
    image_url = api.grub_link()

    return image_url, title


def activate_spam_poster(account: dict[str, str], proxy_for_api: dict[str: str]):
    with SpamPosterReddit(proxy=proxy_for_api) as api:
        # ________________________________________________________________ auth

        api.goto_login_form()
        api.fill_login_form(account["login"], account["password"])
        image_url, title = get_link_photo(api)
        # ________________________________________________________________ Imgur

        for link_sub_reddit in gen_list_sub():
            try:
                api.create_post(title, image_url, link_sub_reddit)
                url_post = api.get_post_url()
                print(url_post)
            except Exception:
                continue

            time.sleep(900)

        api.DRIVER.quit()


