import time

from loguru import logger
from selenium.common import ElementClickInterceptedException

from BASE_Reddit.BaseReddit import BaseReddit
from BASE_Reddit.exceptions import CookieInvalidException, PostDeletedException
from Settings_Selenium.SupportSelenium import BrowserCookie


class RedditWork(BaseReddit):
    def __init__(self, path_cookie=str, link=str, proxy=None):
        super(__class__, self).__init__()

        self.client_cookie = BrowserCookie
        self.proxy = proxy
        self.link = link
        self.cookie_path = path_cookie

    def __enter__(self):
        self.DRIVER = self.run_driver(proxy=self.proxy)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.DRIVER.save_screenshot("UpvoterMistake.png")
        self.DRIVER.quit()

    def _deleted_post(self):
        if not self.elem_exists('//div[contains(text(), "Sorry, this post")]', wait=1):
            logger.info("Post prepare!")
            return
        else:
            logger.error("Post deleted!")
            raise PostDeletedException("this post has been remove")

    def attend_link(self):
        # self._activation_window()  # ___________________________________________________________ activation
        logger.info("Check cookie valid!")
        # self.DRIVER.delete_all_cookies()
        self.client_cookie = BrowserCookie(driver=self.DRIVER, path_filename=self.cookie_path)

        if self.client_cookie.are_valid():
            self.client_cookie.preload()
            logger.info("Attend link!")
            self.DRIVER.get(self.link)

        else:
            raise CookieInvalidException("Cookie invalid")

    def _find_popups(self):
        logger.info("Find Popups!")
        # use Reddit in browser
        if self.click_element(value='//a[contains(text(), "Browse Reddit")]', wait=0.2):
            self.wait_load_webpage()

        # THen content 18+
        if self.elem_exists('//h3[contains(text(), "You must be 18+")]', wait=0.2):
            logger.info('You must be 18+')
            self.click_element('//button[contains(text(), "Yes")]')
            self.DRIVER.get(self.link)
            self.wait_load_webpage()

        # when we watch on the first time on the network
        self.select_interests()

        # asks to continue when you visit a site with a post
        self._button_continue()

    def _previously_upvote(self, wait):
        # click button upvote
        if self.click_element(
                value='//div[@data-test-id="post-content"]//button[@data-click-id="upvote" and @aria-pressed="false"]',
                wait=wait):
            logger.info("Відбувся клік по апвоуту!")

            time.sleep(2)
            # check if red button
            if self.elem_exists('//div[@data-test-id="post-content"]//i[contains(@class, "icon icon-upvote_fill ")]',
                                wait=4):
                logger.info("Клік червоний проходимо далі!")
                # success
                return
            else:
                # repeats actions
                logger.error("Клік був, але кнопка апвоуту і досі прозора!")

                return self._previously_upvote(wait)

        else:
            logger.error("Кліку по апвоуту не було!")
            # the upvote has already been made
            if self.elem_exists(
                    value='//div[@data-test-id="post-content"]//button[@data-click-id="upvote" and @aria-pressed="true"]',
                    wait=1):
                logger.info("Upvote exists!")
                return
            else:
                logger.error("Щось пішло не запланом, мабуть з'явились меню вибору інтересів!")
                self.btn_close_interest()
                self._previously_upvote(wait)

    def upvote(self, wait=4):
        try:
            self._baned_account()
            self._find_popups()
            self.btn_close_interest()
            self._deleted_post()
            self._previously_upvote(wait)
            self.subscribing()
        except ElementClickInterceptedException:
            logger.error("ElementClickInterceptedException: Клік був перехоплнний коли ставив upvote!")
            self._find_popups()
            self.upvote(wait=1)
