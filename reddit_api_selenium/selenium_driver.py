""" This file work with Selenium """
import os
import pickle
import time
import random

import undetected_chromedriver as uc

from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .SeleniumExtension import EnhancedActionChains, ProxyExtension


class BaseClass:

    def __init__(self):
        self.DRIVER = uc.Chrome

    def __set_new_download_path(self, download_path):

        # Defines autodownload and download PATH
        params = {
            "behavior": "allow",
            "downloadPath": download_path
        }
        self.DRIVER.execute_cdp_cmd("Page.setDownloadBehavior", params)

        return self.DRIVER

    def _driver(self, profile=None,
                browser_executable_path=None,
                user_data_dir=None,
                download_path="default",
                proxy=None
                ):

        your_options = {}
        options = uc.ChromeOptions()

        if proxy is not None:

            print("execute proxy")
            # proxy = ("64.32.16.8", 8080, "username", "password")  # your proxy with auth, this one is obviously fake
            # pass  host, port, user, password
            proxy_extension = ProxyExtension(**proxy)
            options.add_argument(f"--load-extension={proxy_extension.directory}")

        # need for working on the backgrounding
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-backgrounding-occluded-windows")

        if user_data_dir is not None:
            your_options["user_data_dir"] = user_data_dir

        elif profile is not None:
            # match on windows 10
            options.add_argument(fr"--user-data-dir={os.environ['USERPROFILE']}\AppData\Local\Google\Chrome\User Data")
            options.add_argument(f"--profile-directory={profile}")

        your_options["options"] = options
        your_options["browser_executable_path"] = browser_executable_path

        # if not profile or user_data_dir == incognito
        self.DRIVER = uc.Chrome(**your_options)

        self.DRIVER.maximize_window()
        self.action = EnhancedActionChains(self.DRIVER)


        # if you need download to your folder
        if download_path == "default":
            return self.DRIVER

        else:
            return self.__set_new_download_path(download_path)

    def xpath_exists(self, value, by=By.XPATH, wait=30, return_xpath=False):
        try:
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
            take_xpath = WebDriverWait(self.DRIVER,
                                       wait,
                                       ignored_exceptions=ignored_exceptions
                                       ).until(EC.presence_of_element_located((by, value)))

            if not return_xpath:
                exist = True
            else:
                # retrurn
                return take_xpath

        except TimeoutException:
            exist = False

        return exist

    def click_element(self, value, by=By.XPATH, wait=60, move_to=True, scroll_to=False):

        try:
            elem_for_click = WebDriverWait(self.DRIVER, wait).until(EC.element_to_be_clickable((by, value)))

            if scroll_to:
                self.scroll_to_elem(value)
                time.sleep(random.uniform(.5, 1))

            if move_to:
                self.mouse_move_to(elem_for_click)
                time.sleep(random.uniform(.5, 1))

            elem_for_click.click()
            return True
        except TimeoutException:
            return False

    def send_text_by_elem(self, value, text_or_key, by=By.XPATH, scroll_to=False, wait=60):

        if self.click_element(value, by=by, scroll_to=scroll_to, wait=wait):
            research_xpath = self.DRIVER.find_element(by, value=value)

            research_xpath.clear()
            research_xpath.send_keys(text_or_key)

        else:
            input(f"No found or no be clickable {value}")

    def refrash_page(self):
        """if you have "Not Found data" call this function"""
        time.sleep(5 * random.uniform(.2, .58))
        self.DRIVER.refresh()
        self.DRIVER.reconnect(random.uniform(2, 5.8))

    def switch_iframe_xpath(self, value, by=By.XPATH, wait=60):
        try:
            WebDriverWait(self.DRIVER, wait).until(
                EC.frame_to_be_available_and_switch_to_it((by, value)))
            return True
        except TimeoutException:
            return False

    def come_back_iframe(self):
        self.DRIVER.switch_to.parent_frame()

    def mouse_move_to(self, element):
        # perform the operation
        self.action.move_to_element(element).pause(1).perform()

    def scroll_to_elem(self, value):
        web_elem = self.xpath_exists(value, return_xpath=True)
        self.DRIVER.execute_script("arguments[0].scrollIntoView();", web_elem)

    def stealth_send_text(self, value, text_or_key, by=By.XPATH, scroll_to=False, wait=60):
        if self.click_element(value, by=by, scroll_to=scroll_to, wait=wait):
            self.action.send_keys_1by1("See how I type like a normal human being...").perform()

    def save_cookie(self, path_cookie):
        pickle.dump(self.DRIVER.get_cookies(), open(path_cookie, "wb"))

    def load_cookie(self, path_cookie):
        cookies = pickle.load(open(path_cookie, "rb"))

        for cookie in cookies:
            self.DRIVER.add_cookie(cookie)
