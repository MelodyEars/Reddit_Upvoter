import time
from pathlib import Path

import undetected_chromedriver as uc
from loguru import logger
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By

from BASE_Reddit.BaseReddit import BaseReddit
from Settings_Selenium import BrowserCookie
from BASE_Reddit.exceptions import CookieInvalidException
from autoposting.network.execeptions_autoposting import WaitRequestToSubredditException, WaitingPostingException, \
    NotTrustedMembersException, SubredditWasBannedException


class CreatePost(BaseReddit):
    """Get link photo from Imgure passes to Reddit Post(create post on a sub-network)"""
    def __init__(self, path_cookie: Path, proxy=None):
        super(__class__, self).__init__()
        self.client_cookie = BrowserCookie
        self.proxy = proxy
        self.cookie_path = path_cookie

    def __enter__(self):
        self.DRIVER: uc.Chrome = self.run_driver(proxy=self.proxy)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.DRIVER.save_screenshot("CreatePost.png")

        self.DRIVER.quit()

    def check_cookie(self):
        # self.DRIVER.delete_all_cookies()
        self.client_cookie = BrowserCookie(driver=self.DRIVER, path_filename=self.cookie_path)

        if self.client_cookie.are_valid():
            self.client_cookie.preload()
        else:
            raise CookieInvalidException("Cookie invalid")

    # ==================================  IMGUR  ============================
    def upload_video(self, path_photo: str):
        self.DRIVER.get('https://imgur.com/upload')

        self.elem_exists('file-input', by=By.ID, return_xpath=True).send_keys(str(path_photo))

    def grub_link(self) -> str:
        photo_elem = self.elem_exists('//img[contains(@src, "https://i.imgur.com/")]', return_xpath=True)
        photo_url = photo_elem.get_attribute('src')
        print(photo_url)

        return photo_url

    # ==================================  REDDIT  ============================
    def _attend_profile_page(self):
        profile_url = f"https://www.reddit.com/user/{self.cookie_path.stem}"
        self.DRIVER.get(profile_url)
        self.wait_load_webpage()

    def delete_all_posts(self):
        """DELETE all posts while exists elem"""
        self._attend_profile_page()
        # '//div[@data-scroller-first=""]/following-sibling::div//img[@alt="Post image"]'
        # '//div[@data-scroller-first=""]//img[@alt="Post image"]'
        while self.elem_exists('//div[@data-scroller-first]', wait=1, scroll_to=True):
            self.click_element('//div[@data-scroller-first]//button[@aria-label="more options"]',
                               wait=1, intercepted_click=True)  # click ...(options)
            self.click_element('//button[./span[contains(text(), "delete")]]', wait=5)  # select Delete
            time.sleep(1)
            self.click_element('//section/footer/button[contains(text(), "Delete post")]', wait=5)  # confirm delete
            time.sleep(2)

    def delete_last_post(self, url: str):
        self.DRIVER.get(url)
        self.wait_load_webpage()
        self.btn_close_interest()
        # self.scroll_to_elem('//div[./div[./a[@target="_blank"]/img]]')
        self.scroll_to_elem('//button[contains(text(), "Community options")]')
        if self.click_element('//button[@aria-label="more options"]',
                           wait=1, intercepted_click=True):  # click ...(options)

            self.click_element('//button[./span[contains(text(), "delete")]]', wait=5)  # select Delete
            time.sleep(1)
            self.click_element('//section/footer/button[contains(text(), "Delete post")]', wait=5)  # confirm delete
            time.sleep(2)
        else:
            raise Exception("Not scroll to delete last elem")

    def _btn_create_post(self):
        try:
            self.click_element('//button[@aria-label="Create Post"]')  # click on the +
        except ElementClickInterceptedException:
            logger.error("ElementClickInterceptedException: create post")
            self.btn_close_interest()
            self._btn_create_post()

    def _btn_send_post(self):
        if self.click_element('//button[contains(text(), "Post") and @role="button"]', wait=2):
            time.sleep(1)
            if self.click_element('//footer/button[contains(text(), "Save Draft")]', wait=0.2):
                return self._btn_send_post()

            elif self.elem_exists('//*[contains(text(), "This community only allows trusted members to post here")]',
                                  wait=0.2):
                raise NotTrustedMembersException('This community only allows trusted members to post here')

            elif self.elem_exists(
                    '''//*[contains(text(), "Looks like you've been doing that a lot. Take a break for")]''',
                    wait=0.2
            ):
                # waiting 15 minutes
                # "Looks like you've been doing that a lot. Take a break for 9 minutes before trying again."
                # "Looks like you've been doing that a lot. Take a break for 44 seconds before trying again."
                text_from_el: str = self.elem_exists(
                    '''//*[contains(text(), "Looks like you've been doing that a lot. Take a break for")]''',
                    return_xpath=True
                ).text
                post_timeout = text_from_el.split(" ")[-5:-3]
                if post_timeout[1] == "minutes":
                    timeout: int = int(post_timeout[0]) * 60 + 60
                elif post_timeout[1][:-1] == "second":
                    timeout: int = int(post_timeout[0]) + 30
                else:
                    raise WaitingPostingException('Reddit give you a break < 1hour')
                logger.info(f"Pause before post: {timeout}")
                time.sleep(timeout)  # break
                return self._btn_send_post()

            elif self.elem_exists('//span[contains(text(), "Your post must contain post flair.")]', wait=0.2):
                # select Flair
                self.click_element('//button[@aria-label="Add flair"]')  # btn Flair
                self.click_element('//div[@aria-label="flair_picker"]/div')  # checkbox select first topik
                self.click_element('//button[contains(text(), "Apply")]')  # btn apply
                return self._btn_send_post()

            elif self.elem_exists('//button[contains(text(), "Send Request")]', wait=0.2):
                raise WaitRequestToSubredditException("Wait for offer posting from subreddit.")

            else:
                logger.info("Button 'POST'")
                return
        else:
            input("Неможу запостити обери елемент чому? Та клацни Ентер.")

    def _btn_subscribe(self, wait=1):
        while not self.elem_exists('//span[contains(text(), "Joined")]', wait=wait):
            self.click_element('//button[contains(text(), "Join")]', wait=wait, intercepted_click=True)
            time.sleep(1)
            self.DRIVER.refresh()
            self.wait_load_webpage()

    def create_post(self, title, image_url, link_sub_reddit):
        # attend sub
        self.DRIVER.get(link_sub_reddit)
        self.wait_load_webpage()
        self.btn_close_interest()

        if self.elem_exists('//*[contains(text(), "This subreddit was banned")]', wait=0.2):
            raise SubredditWasBannedException("This subreddit was banned due to being unmoderated.")

        self.btn_close_interest()

        # _________________________ nav ________________________
        self._btn_subscribe()
        self._btn_create_post()
        self.wait_load_webpage()

        if self.elem_exists('//span[contains(text(), "Your request to ")]', wait=0.2):
            raise WaitRequestToSubredditException("Requests sent!")

        # if  sent request to sub for posting
        if not self.click_element('//button[contains(text(), "Link")]'):  # select button link
            self.create_post(title, image_url, link_sub_reddit)

        # write title
        self.send_text_by_elem('//textarea[@placeholder="Title"]', title)

        # send url
        self.send_text_by_elem('//textarea[@placeholder="Url"]', image_url)

        # press button Post
        return self._btn_send_post()

    def get_post_url(self) -> str:
        # _____________________________ post _________________________________
        self.wait_load_webpage()
        url = self.DRIVER.current_url

        logger.info(url)
        return url
