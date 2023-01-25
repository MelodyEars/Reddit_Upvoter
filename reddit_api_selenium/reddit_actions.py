import time

from selenium.webdriver.common.by import By

from .SupportSelenium import Cookies
from .selenium_driver import BaseClass


class RedditWork(BaseClass):
    def __init__(self, path_cookie=str, link=str, proxy=None):

        super(__class__, self).__init__()
        self.client_cookie = None
        self.proxy = proxy
        self.link = link
        self.cookie_path = path_cookie

    def __enter__(self):
        self.DRIVER = self._driver(proxy=self.proxy)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.DRIVER.save_screenshot("picture_mistake.png")

        self.DRIVER.quit()

    def attend_link(self):
        # self.DRIVER.delete_all_cookies()
        self.client_cookie = Cookies(driver=self.DRIVER, path_filename=self.cookie_path)

        if self.client_cookie.are_valid():
            self.client_cookie.preload()
            self.DRIVER.get(self.link)
            self.DRIVER.reconnect()
            return True
        else:
            return False

    def baned_account(self):
        if self.xpath_exists(value='//a[contains(@href, "https://www.reddithelp.com/")]', wait=1):
            return True
        else:
            return False

    def prepare_reddit(self):
        self.xpath_exists(value='body', by=By.TAG_NAME)
        # use Reddit in browser
        self.click_element(value='//a[contains(text(), "Browse Reddit")]', wait=0.1, move_to=True)

        # self.xpath_exists(value='body', by=By.TAG_NAME)
        # THen content 18+
        if self.xpath_exists('//h3[contains(text(), "You must be 18+")]', wait=0.1):
            # access
            self.click_element('//button[contains(text(), "Yes")]', move_to=True)

        # self.xpath_exists(value='body', by=By.TAG_NAME)
        # asks to continue when you visit a site with a post
        self.click_element('//button[contains(text(), "Continue")]', wait=0.1, move_to=True)

        return not self.baned_account()

    def upvote(self):
        self.reset_actions()
        # post
        # self.xpath_exists(by=By.ID, value="post-content")
        # upvote
        if self.click_element(
                value='//div[@data-test-id="post-content"]//button[@data-click-id="upvote" and @aria-pressed="false"]',
                wait=4, move_to=True):

            time.sleep(2)
            # wait for
            if self.xpath_exists('//div[@data-test-id="post-content"]//i[contains(@class, "icon icon-upvote_fill ")]',
                                 wait=4):
                # success
                return
            else:
                return self.upvote()
        else:
            # account's click exists
            return

    def write_comment(self, text_comment, reddit_username):
        self.send_text_by_elem(value='//div[@class="notranslate public-DraftEditor-content"]',
                               text_or_key=text_comment)
        # send comment
        self.click_element('//button[contains(text(), "Comment")]', move_to=True)

        if self.xpath_exists(f'//a[contains(text(), "{reddit_username}") and @data-testid="comment_author_link"]',
                             wait=10):
            # success
            return

        else:
            return self.write_comment(text_comment, reddit_username)
