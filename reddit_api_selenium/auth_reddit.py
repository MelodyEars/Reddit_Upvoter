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

    def __init__(self, cookie, link=str, proxy=None):

        super(__class__, self).__init__()
        self.proxy = proxy
        self.link = link

    def __enter__(self):
        self.DRIVER = self._driver(proxy=self.proxy)
        self.act = ActionChains(self.DRIVER)
        self.DRIVER.get(self.link)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.DRIVER.quit()


# TODO not close browse, most better solve driver.delete_all_cookies() and create new profile coookie the new profile
# driver.execute_cdp_cmd("Network.clearBrowserCache", {})
# driver.execute_cdp_cmd("Network.clearBrowserCookies", {})

# clear all
# driver.execute_script('document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section:nth-child(9) > settings-privacy-page").shadowRoot.querySelector("settings-clear-browsing-data-dialog").shadowRoot.querySelector("#clearBrowsingDataConfirm").click()')