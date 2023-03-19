import random
import time

from loguru import logger
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By

from Settings_Selenium import Cookies
from .exceptions import NotRefrashPageException, BanAccountException, CookieInvalidException, PostDeletedException
from Settings_Selenium import BaseClass


class RedditWork(BaseClass):
    def __init__(self, path_cookie=str, link=str, proxy=None):

        super(__class__, self).__init__()
        self.client_cookie = Cookies
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
        if not self.elem_exists('//div[contains(text(), "Sorry, this post has been remove")]', wait=1):
            logger.error("Post prepare!")
            return
        else:
            logger.error("Post deleted!")
            raise PostDeletedException("this post has been remove")

    def attend_link(self):
        logger.info("Check cookie valid!")
        # self.DRIVER.delete_all_cookies()
        self.client_cookie = Cookies(driver=self.DRIVER, path_filename=self.cookie_path)

        if self.client_cookie.are_valid():
            self.client_cookie.preload()
            logger.info("Attend link!")
            self.DRIVER.get(self.link)
            self.DRIVER.reconnect()
        else:
            raise CookieInvalidException("Cookie invalid")

    def _baned_account(self):
        logger.info("Check if account banned.")
        self._wait_load_webpage()
        if not self.elem_exists(value='//a[contains(@href, "https://www.reddithelp.com/")]', wait=0.3):
            return

        else:
            raise BanAccountException("Your account banned")

    def _error_cdn_to_server(self):
        logger.info("Loading webpage!")
        if self.elem_exists(value='body', by=By.TAG_NAME, wait=60):
            self.click_element(value='//section/form/button[contains(text(), "Accept all")]', wait=0.3)
            if self.elem_exists('//*[contains(text(), "Our CDN was unable to reach our servers")]', wait=0.1):
                return True
            else:
                return False
        else:
            logger.warning("Сторінка не завантажилась, беру наступну задачу.")
            return True

    def _wait_load_webpage(self):
        logger.info("Wait load page!")
        if not self._error_cdn_to_server():
            return
        else:
            self.refrash_page()
            if not self._error_cdn_to_server():
                return
            else:
                raise NotRefrashPageException("Our CDN was unable to reach our servers")

    def _button_continue(self):
        logger.info('Press button "continue"')
        # asks to continue when you visit a site with a post
        if self.click_element('//button[contains(text(), "Continue")]', wait=0.2):
            self._wait_load_webpage()

    def _select_communities(self):
        self.elem_exists('//button[contains(text(), "Select All")]')
        count_communities = len(self.DRIVER.find_elements(By.XPATH, '//button[contains(text(), "Select All")]'))

        for _ in range(random.randint(1, count_communities)):
            communities_button = f'//button[contains(text(), "Select All")]'
            self.click_element(value=communities_button, scroll_to=True, wait=1)

        self._button_continue()
        self._wait_load_webpage()

    def _select_interests(self):
        logger.info("Select interests!")
        if self.elem_exists('//div[@role="dialog" and @aria-modal="true"]', wait=0.2):
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
        logger.info("Find Popups!")
        # use Reddit in browser
        if self.click_element(value='//a[contains(text(), "Browse Reddit")]', wait=0.2):
            self._wait_load_webpage()

        # THen content 18+
        if self.elem_exists('//h3[contains(text(), "You must be 18+")]', wait=0.2):
            logger.info('You must be 18+')
            self.click_element('//button[contains(text(), "Yes")]')
            self._wait_load_webpage()

        # when we watch on the first time on the network
        self._select_interests()

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
                return self.upvote()

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
                self._find_popups()
                self._previously_upvote(wait)

    def upvote(self, wait=4):
        try:
            self._baned_account()
            self._deleted_post()
            # self.scroll_to_elem('//button[contains(text(), "Comment")]')
            self._previously_upvote(wait)
        except ElementClickInterceptedException:
            logger.error("ElementClickInterceptedException: Клік був перехоплнний коли ставив upvote!")
            self._find_popups()
            self.upvote(wait=1)

    def write_comment(self, text_comment, reddit_username):

        if not self.elem_exists(
                value=f'//a[contains(text(), "{reddit_username}") and @data-testid="comment_author_link"]', wait=2):

            self.stealth_send_text(value='//div[@class="notranslate public-DraftEditor-content"]',
                                   text_or_key=str(text_comment),
                                   scroll_to=True)

            if not self.elem_exists("""//*[contains(text(),
            "Looks like you've been doing that a lot. Take a break for 2 minutes before trying again.")]""", wait=1):
                # send comment
                self.click_element('//button[contains(text(), "Comment")]', move_to=True)
                time.sleep(5)

                # check username's comment exists
                if self.elem_exists(
                        f'//a[contains(text(), "{reddit_username}") and @data-testid="comment_author_link"]', wait=10):
                    # success
                    return
                else:
                    logger.warning("Виникла помилка при написанні коментаря! =(")
                #     if self.elem_exists('//*[contains("Something went wrong")]'):
                #         logger.warning('З\'явлось алерт при написанні коментаря "Something went wrong"')
                #         return
                #     else:
                #         return self.write_comment(text_comment, reddit_username)

    ####################################### subscribe ###################################
    def _previously_subscribing(self):
        # while not exists button
        if self.elem_exists('//button[contains(@id, "subscribe-button") and contains(text(), "Join")]', wait=1):
            wait = 10
            # while not self.elem_exists('''//button[descendant::span[contains(text(), "Joined")]
            # or descendant::span[contains(text(), "Leave")]]''', wait=wait):
            while not self.click_element(
                    '//button[contains(@id, "subscribe-button") and contains(text(), "Join")]',
                    wait=wait):

                time.sleep(2)
                wait = 1
                self.DRIVER.refresh()
                self.DRIVER.reconnect()
                logger.debug("Чекаємо підписки!")
            else:
                logger.debug("Підписка оформлена!!!")
        # elif self.elem_exists('//button[contains(text(), "Follow")]', wait=1):
        #     wait = 0.1
        #     while not self.elem_exists('//button[contains(text(), "Unfollow")]', wait=wait):
        #         self.click_element('//button[contains(text(), "Follow")]', wait=1)
        #         wait = 10
        #         time.sleep(2)
        #     else:
        #         logger.debug("Підписка оформлена")
        else:
            logger.debug("Підписки не було зроблено. Можливо вона вже оформлена.")

    def subscribing(self):
        try:
            self._previously_subscribing()
        except ElementClickInterceptedException:
            self.subscribing()
