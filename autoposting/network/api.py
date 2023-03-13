import time
from pathlib import Path

from selenium.webdriver.common.by import By

from Settings_Selenium import BaseClass, Cookies
from Uprove_TG_Bot.reddit_api_selenium.exceptions import CookieInvalidException


class CreatePost(BaseClass):
    """Get link photo from Imgure passes to Reddit Post(create post on a sub-network)"""
    def __init__(self, path_cookie: Path, link_sub_reddit: str, proxy=None):

        super(__class__, self).__init__()
        self.link_sub_reddit = link_sub_reddit
        self.client_cookie = Cookies
        self.proxy = proxy
        self.cookie_path = path_cookie

    def __enter__(self):
        self.DRIVER = self.run_driver(proxy=self.proxy)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.DRIVER.save_screenshot("CreatePost.png")

        self.DRIVER.quit()

    def check_cookie(self):

        # self.DRIVER.delete_all_cookies()
        self.client_cookie = Cookies(driver=self.DRIVER, path_filename=self.cookie_path)

        if self.client_cookie.are_valid():
            self.client_cookie.preload()
            self.DRIVER.reconnect()
        else:
            raise CookieInvalidException("Cookie invalid")

    # ==================================  IMGUR  ============================
    def upload_video(self, path_photo: str):
        self.DRIVER.get('https://imgur.com/upload')

        self.elem_exists('file-input', by=By.ID, return_xpath=True).send_keys(path_photo)

    def grub_link(self) -> str:
        photo_elem = self.elem_exists('//div[@class="PostContent-imageWrapper-rounded"]/img', return_xpath=True)
        photo_url = photo_elem.get_attribute('href')

        return photo_url

    # ==================================  REDDIT  ============================
    def attend_profile_page(self):
        profile_url = f"https://www.reddit.com/user/{self.cookie_path.stem}"
        self.DRIVER.get(profile_url)

    def create_post(self, title, image_url):
        # attend sub
        self.DRIVER.get(self.link_sub_reddit)

        # _________________________ nav ________________________
        self.click_element('//button[@aria-label="Create Post"]')  # click on the +
        self.click_element('//button[contains(text(), "Link")]')  # select button link

        # write title
        self.send_text_by_elem('//textarea[@placeholder="Title"]', title)

        # send url
        self.send_text_by_elem('//textarea[@placeholder="Url"]', image_url)

        # press button Post
        if self.click_element('//button[contains(text(), "Post") and @role="button"]'):
            return

        else:
            input("Неможу запостити обери елемент чому? Та клацни Ентер.")
            # TODO select Flair and waiting 15 minutes

    def get_post_url(self) -> str:
        # _____________________________ post _________________________________
        url = self.DRIVER.current_url

        # go on account's main page
        self.click_element('email-collection-tooltip-id', by=By.ID)  # profile menu

        # click button profile
        self.click_element('//a[./span[contains(text(), "Profile")]]')

        # ________________________________ main page ______________________________
        # on main page press button 'Insights'
        self.click_element('//button[./span[contains(text(), "Insights")]]')

        # while statistic is not hidden
        while not self.elem_exists("//div[contains(text(), 'Total Views')]"):
            time.sleep(1)

        return url

    def delete_all_posts(self):
        while self.click_element('//button[@aria-label="more options"]', wait=1):
            self.click_element('//button[./span[contains(text(), "delete")]]')
            time.sleep(5)

