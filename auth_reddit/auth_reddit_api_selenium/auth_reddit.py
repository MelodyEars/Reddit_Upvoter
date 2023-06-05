import time
import random

from loguru import logger
from selenium.common import ElementClickInterceptedException

import work_fs

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from BASE_Reddit.BaseReddit import BaseReddit
from Settings_Selenium import BrowserCookie


class RedditAuth(BaseReddit):

    def __init__(self, proxy: dict):

        super(__class__, self).__init__()
        self.proxy = proxy

    def __enter__(self):
        self.DRIVER = self.run_driver(proxy=self.proxy, detection_location=True)
        self.act = ActionChains(self.DRIVER)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.DRIVER.quit()

    def __button_login(self):

        try:
            self.click_element('//header//a[@role="button"]')
        except ElementClickInterceptedException:
            logger.debug("Клік був перехоплений.")
            time.sleep(random.uniform(1, 3))
            self.reset_actions()
            return self.__button_login()

    def goto_login_form(self):
        self.DRIVER.get('https://www.reddit.com/')
        self.wait_load_webpage()

        # self.DRIVER.current_url() <- url

        self.__button_login()  # attend wbpage for log in
        self.accept_all_cookie()

    def fill_login_form(self, login, password):
        if self.switch_iframe_xpath("//iframe[contains(@src, 'https://www.reddit.com/login/')]"):
            self.send_text_by_elem(value='loginUsername', by=By.ID, text_or_key=login)
            self.send_text_by_elem(value='loginPassword', by=By.ID, text_or_key=password)

            self.click_element('//button[contains(text(), "Log In")]')
        else:
            logger.error("Not ok iframe")
            return self.goto_login_form()  # refresh auth reddit

    def skip_popups(self):
        self.wait_load_webpage()
        self.click_element('//button[@aria-label="Close"]', wait=1)
        num = 1
        for i in range(random.randint(1, 5)):
            num = num + i
            self.scroll_to_elem(f'//div[@data-scroller-first]/following-sibling::div[{num}]')

        self.accept_all_cookie()

    def _shadow_ban(self):
        text_or_key = 'am I?'

        # send title
        self.send_text_by_elem(value='//textarea[@placeholder="Title"]', text_or_key=text_or_key)

        # send text(optional)
        self.send_text_by_elem(value='//div[@class="notranslate public-DraftEditor-content"]',
                               text_or_key=" " + text_or_key)

        # press btn post
        self._btn_send_post()

    def create_post(self):
        logger.info("Create post")
        self.DRIVER.get('https://www.reddit.com/r/ShadowBan/')
        self.wait_load_webpage()
        self.btn_close_interest()
        logger.info("Close interest")
        self.subscribing_main_page_sub()
        logger.info("Subscribing main page sub")
        self._btn_create_post()
        logger.info("Click btn create post")
        self._shadow_ban()
        logger.info("Write Shadow ban")

    def get_path_cookie(self, login):
        logger.info("Get path cookie")
        root_folder = work_fs.path_near_exefile()
        path_cookie = work_fs.auto_create(work_fs.path_near_exefile('cookies'), _type='dir') / f'{login}.pkl'
        db_cookie_path = path_cookie.relative_to(root_folder)
        print(db_cookie_path)
        cookie = BrowserCookie(driver=self.DRIVER, path_filename=path_cookie)
        cookie.save()

        return db_cookie_path, self.proxy

    def gen_avatar(self, login):
        logger.debug("Start gen avatar")
        self.DRIVER.get(f'https://www.reddit.com/user/{login}')
        self.wait_load_webpage()
        self.select_interests()

        logger.info("Click btn edit avatar")
        if self.click_element('//h1/following-sibling::button', wait=10):

            logger.info("Click btn randomize")
            self.click_element('//button[contains(text(), "Randomize")]')

            logger.info("Save avatar")
            self.click_element('//button[contains(text(), "Save")]')
