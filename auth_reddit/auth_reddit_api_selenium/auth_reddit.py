
import time
import random
import undetected_chromedriver as uc

from loguru import logger
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By

import work_fs

from Settings_Selenium import BaseClass, CookiesBrowser


class RedditAuth(BaseClass):

    def __init__(self, driver: uc.Chrome, client_cookie: CookiesBrowser | None):

        super(__class__, self).__init__()
        self.DRIVER = driver
        self.client_cookie = client_cookie

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            if self.client_cookie:
                self.client_cookie.is_work = False
                self.DRIVER.save_screenshot(f"Error_GetCookie_{self.client_cookie.username}.png")
            else:
                self.DRIVER.save_screenshot("Error_GetCookie.png")

    def __reddit_main_page(self):
        self.DRIVER.get('https://www.reddit.com/')
        self.DRIVER.reconnect(0.3)

    def __button_login(self):
        try:
            self.click_element('//header//a[@role="button"]')
        except ElementClickInterceptedException:
            logger.debug("Клік був перехоплений.")
            time.sleep(random.uniform(1, 3))
            self.reset_actions()
            return self.__button_login()

    def goto_login_form(self):
        self.__reddit_main_page()
        self.elem_exists("//body")
        # self.DRIVER.current_url() <- url

        self.__button_login()  # attend wbpage for log in

        # go to iframe
        self.switch_iframe_xpath('//iframe[contains(@src, "https://www.reddit.com/login/")]')

    def fill_login_form(self, login, password):
        self.send_text_by_elem(value='loginUsername', text_or_key=login, by=By.ID)
        self.send_text_by_elem(value='loginPassword', by=By.ID, text_or_key=password)

        self.click_element('//button[contains(text(), "Log In")]')

    def skip_popups(self):
        self.elem_exists('//body')
        self.click_element('//button[@aria-label="Close"]', wait=3)
        num = 1
        for i in range(random.randint(1, 3)):
            num = num + i
            self.scroll_to_elem(f'//div[@data-scroller-first]/following-sibling::div[{num}]')

        time.sleep(random.uniform(1, 3))

    def get_path_cookie(self, login, client_cookie: CookiesBrowser | None):
        path_cookie = work_fs.auto_create(work_fs.path_near_exefile('cookies'), _type='dir') / f'{login}.pkl'

        if client_cookie is None:
            self.client_cookie = CookiesBrowser(driver=self.DRIVER, path_cookie=path_cookie)

        else:
            self.client_cookie = CookiesBrowser(**client_cookie.__dict__)

        return self.client_cookie
