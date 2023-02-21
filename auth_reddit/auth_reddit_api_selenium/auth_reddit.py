import time
import random

import work_fs

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from Settings_Selenium import BaseClass, Cookies


class RedditAuth(BaseClass):

    def __init__(self, proxy: dict):

        super(__class__, self).__init__()
        self.proxy = proxy

    def __enter__(self):
        self.DRIVER = self._driver(proxy=self.proxy)
        self.act = ActionChains(self.DRIVER)
        self.DRIVER.get('https://www.reddit.com/')
        self.DRIVER.reconnect(0.3)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.DRIVER.quit()

    def goto_login_form(self):
        self.elem_exists("//body")
        # self.DRIVER.current_url() <- url

        self.click_element('//header//a[@role="button"]')  # attend wbpage for log in

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

    def get_path_cookie(self, login):
        path_cookie = work_fs.auto_create(work_fs.path_near_exefile('cookies'), _type='dir') / f'{login}.pkl'
        cookie = Cookies(driver=self.DRIVER, path_filename=path_cookie)
        cookie.save()

        db_cookie_path = f"cookies/{login}.pkl"
        return db_cookie_path, self.proxy


