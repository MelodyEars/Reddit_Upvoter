
import time
import random

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains

from .SupportSelenium import Cookies
from .selenium_driver import BaseClass


class RedditWork(BaseClass):
    def __init__(self, path_cookie=str, link=str, proxy=None):

        super(__class__, self).__init__()
        self.proxy = proxy
        self.link = link
        self.cookie_path = path_cookie

    def __enter__(self):
        self.DRIVER = self._driver(proxy=self.proxy)

        self.client_cookie = Cookies(driver=self.DRIVER, url=self.link, path_filename=self.cookie_path)
        self.client_cookie.preload()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client_cookie.save()
        self.DRIVER.quit()

    def popups_pass(self):
        # popups
        self.xpath_exists(value='body', by=By.TAG_NAME)
        # THen content 18+
        input("Content 18+:")
        # asks to continue when you visit a site with a post
        self.click_element('//button[contains(text(), "Continue")]', wait=0.5, move_to=True)

    def upvote(self):
        # post
        self.xpath_exists(by=By.ID, value="post-content")
        # upvote
        self.click_element('//button[@data-click-id="upvote" and @aria-pressed="false"]', )
        # wait for
        if self.xpath_exists('//div[@data-test-id="post-content"]//i[contains(@class, "icon icon-upvote_fill ")]',
                             wait=3):
            return
        else:
            return self.upvote()

    def send_comment(self, text_comment):
        '//div[@class="notranslate public-DraftEditor-content"]'
        # send comment
        '//button[contains(text(), "Comment")]'
        # wait 2 before, then click button send
        '//span[contains(text(), "1 new comment")]'

