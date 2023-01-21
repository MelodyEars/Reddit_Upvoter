'https://www.reddit.com/'
import pickle
import time
import random

from selenium.webdriver import ActionChains

import work_fs
from .selenium_driver import BaseClass

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException, StaleElementReferenceException


class RedditAuth(BaseClass):
    """
    :profile = "Profile num" to be your Chrome "User Data"
    :browser_executable_path = (default path to Chrome) path to executable browser
    :user_data_dir = path copy your "User Data" with your only one profile (the most correct and safe way)
    """

    def __init__(self, proxy=None):

        super(__class__, self).__init__()
        self.proxy = proxy

    def __enter__(self):
        self.DRIVER = self._driver(proxy=self.proxy)
        self.act = ActionChains(self.DRIVER)
        self.DRIVER.get('https://www.reddit.com/')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.DRIVER.quit()

    def goto_login_form(self):
        self.xpath_exists("//body")
        # alert notifications "Block"
        self.click_element('//header//a[@role="button"]')  # attend wbpage for log in
        # go to iframe
        self.switch_iframe_xpath('//iframe[contains(@src, "https://www.reddit.com/login/")]')

    def fill_login_form(self, login, password):
        self.send_text_by_elem(value='loginUsername', text_or_key=login, by=By.ID)
        self.send_text_by_elem(value='loginPassword', by=By.ID, text_or_key=password)

        self.click_element('//button[contains(text(), "Log In")]')

    def skip_popups(self):
        self.xpath_exists('//body')
        self.click_element('//button[@aria-label="Close"]', wait=3)
        num = 1
        for i in range(random.randint(1, 3)):
            num = num + i
            self.scroll_to_elem(f'//div[@data-scroller-first]/following-sibling::div[{num}]')

        time.sleep(random.uniform(1, 3))

    def get_path_cookie(self, login):
        path_cookie = work_fs.auto_create(work_fs.path_near_exefile('cookies'), _type='dir') / f'{login}.pkl'
        self.save_cookie(path_cookie)

        db_cookie_path = f"cookies/{login}.pkl"
        return db_cookie_path, self.proxy


