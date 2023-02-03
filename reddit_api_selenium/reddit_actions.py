import random
import time

from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By

from Settings_Selenium import Cookies
from .exceptions import NotRefrashPageException, BanAccountException, CookieInvalidException
from Settings_Selenium import BaseClass


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
        else:
            raise CookieInvalidException("Cookie invalid")

    def _baned_account(self):
        self._wait_load_webpage()
        if not self.xpath_exists(value='//a[contains(@href, "https://www.reddithelp.com/")]', wait=1):
            return

        else:
            raise BanAccountException("Your account banned")

    def _error_cdn_to_server(self):
        self.xpath_exists(value='body', by=By.TAG_NAME, wait=500)
        self.click_element(value='//section/form/button[contains(text(), "Accept all")]', wait=0.3)
        if self.xpath_exists('//*[contains(text(), "Our CDN was unable to reach our servers")]', wait=0.1):
            return True
        else:
            return False

    def _wait_load_webpage(self):
        if not self._error_cdn_to_server():
            return
        else:
            self.refrash_page()
            if not self._error_cdn_to_server():
                return
            else:
                raise NotRefrashPageException("Our CDN was unable to reach our servers")

    def _button_continue(self):
        # asks to continue when you visit a site with a post
        if self.click_element('//button[contains(text(), "Continue")]', wait=0.2):
            self._wait_load_webpage()

    def _select_communities(self):
        self.xpath_exists('//button[contains(text(), "Select All")]')
        count_communities = len(self.DRIVER.find_elements(By.XPATH, '//button[contains(text(), "Select All")]'))

        for _ in range(random.randint(1, count_communities)):
            communities_button = f'//button[contains(text(), "Select All")]'
            self.click_element(value=communities_button, scroll_to=True, wait=1)

        self._button_continue()
        self._wait_load_webpage()

    def _select_interests(self):
        if self.xpath_exists('//div[@role="dialog" and @aria-modal="true"]', wait=0.2):
            num = 0
            for _ in range(random.randint(3, 5)):
                num_selected = random.randint(1, 3)
                num += num_selected
                interest_button = f'//div[@role="dialog"]//button[@role="button"][{num}]'
                self.click_element(value=interest_button, scroll_to=True, wait=1)

            self._button_continue()

            # watch element not fill color
            self._wait_load_webpage()

            return self._select_communities()

    def _find_popups(self):
        # use Reddit in browser
        if self.click_element(value='//a[contains(text(), "Browse Reddit")]', wait=0.2):
            self._wait_load_webpage()

        # THen content 18+
        if self.xpath_exists('//h3[contains(text(), "You must be 18+")]', wait=0.2):
            self.click_element('//button[contains(text(), "Yes")]')
            self._wait_load_webpage()

        # when we watch on the first time on the reddit
        self._select_interests()

        # asks to continue when you visit a site with a post
        self._button_continue()

    def _previously_upvote(self, wait=4):
        # upvote
        if self.click_element(
                value='//div[@data-test-id="post-content"]//button[@data-click-id="upvote" and @aria-pressed="false"]',
                wait=wait, move_to=True):

            time.sleep(5)
            # wait for
            if self.xpath_exists('//div[@data-test-id="post-content"]//i[contains(@class, "icon icon-upvote_fill ")]',
                                 wait=4):
                # success
                return
            else:
                # repeats actions
                return self.upvote()
        else:
            # the upvote has already been made
            if self.xpath_exists(
                    value='//div[@data-test-id="post-content"]//button[@data-click-id="upvote" and @aria-pressed="true"]',
                    wait=1):
                return
            else:
                self._find_popups()
                self._previously_upvote()

    def upvote(self):
        try:
            self._baned_account()
            self._previously_upvote()
        except ElementClickInterceptedException:
            self._find_popups()
            self._previously_upvote(wait=120)

    def write_comment(self, text_comment, reddit_username):

        if not self.xpath_exists(
                value=f'//a[contains(text(), "{reddit_username}") and @data-testid="comment_author_link"]',
                wait=2):

            self.stealth_send_text(value='//div[@class="notranslate public-DraftEditor-content"]',
                                   text_or_key=str(text_comment),
                                   scroll_to=True)

            # send comment
            self.click_element('//button[contains(text(), "Comment")]', move_to=True)
            time.sleep(5)

            # check username's comment exists
            if self.xpath_exists(
                    f'//a[contains(text(), "{reddit_username}") and @data-testid="comment_author_link"]', wait=10):
                # success
                return
            else:
                return self.write_comment(text_comment, reddit_username)

