""" This file work with Selenium """
import time
import random

import requests
import undetected_chromedriver as uc
from loguru import logger
from requests import JSONDecodeError
from requests.exceptions import ProxyError

from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, \
    ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from base_exception import ProxyInvalidException
from .SeleniumExtension import EnhancedActionChains, ProxyExtension


executable_path = None  # default chrome


def geolocation(loc_value_JSON: str):
    data = loc_value_JSON.split(",")
    latitude = float(data[0])
    longitude = float(data[1])

    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['locationContextEnabled'] = True
    capabilities['locationContextDefaultZoomLevel'] = 13
    capabilities['locationContextEnabled'] = True
    capabilities['locationContextMaxDistance'] = 10000
    capabilities['locationContextGeoLocation'] = {'latitude': latitude, 'longitude': longitude}

    return capabilities


def proxy_data(proxy: dict):
    proxies = {"http": f"http://{proxy['user']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"}
    url = "http://ipinfo.io/json"

    try:
        resp = requests.get(url, proxies=proxies, timeout=10)

    except ProxyError:
        logger.error(f"Щось з проксі {proxy['user']}:{proxy['password']}:{proxy['host']}:{proxy['port']}!")
        raise ProxyInvalidException("ProxyError: Invalid proxy ")
    logger.info(resp)
    return resp


class BaseClass:

    def __init__(self):
        self.action = None
        self.DRIVER = uc.Chrome

    def __set_new_download_path(self, download_path):
        # Defines auto download and download PATH
        params = {
            "behavior": "allow",
            "downloadPath": download_path
        }
        self.DRIVER.execute_cdp_cmd("Page.setDownloadBehavior", params)

        return self.DRIVER

    def run_driver(self, browser_executable_path=executable_path, user_data_dir=None,
                   download_path="default", proxy=None, headless=False, detection_location=True):

        resp = None

        your_options = {}
        options = uc.ChromeOptions()

        options.add_argument("""
        --lang=en-US
        --disable-dev-shm-usage
        --disable-setuid-sandbox
        --disable-software-rasterizer
        --disable-popup-blocking
        --disable-notifications
        --disable-renderer-backgrounding
        --disable-backgrounding-occluded-windows
        """)  # 2 arg in  the end need for working on the backgrounding

        if proxy is not None:
            # proxy = ("64.32.16.8", 8080, "username", "password")  # your proxy with auth, this one is obviously fake
            # pass  host, port, user, password
            proxy_extension = ProxyExtension(**proxy)
            options.add_argument(f"--load-extension={proxy_extension.directory}")
            resp = proxy_data(proxy)

            # ____________________________ location _______________________________
            if detection_location:
                try:
                    capabilities = geolocation(resp.json()['loc'])
                    your_options['desired_capabilities'] = capabilities
                except JSONDecodeError:
                    raise Exception("Щось не так з проксі. Було залучено останній з файлу 'proxies.txt'")
        # if user_data_dir is not None:
        #     your_options["user_data_dir"] = user_data_dir
        #
        # elif profile is not None:
        #     # match on windows 10
        #     options.add_argument(fr"--user-data-dir={os.environ['USERPROFILE']}\AppData\Local\Google\Chrome\User Data")
        #     options.add_argument(f"--profile-directory={profile}")

        your_options["headless"] = headless
        your_options["options"] = options
        your_options["browser_executable_path"] = browser_executable_path

        # if not profile or user_data_dir == incognito
        self.DRIVER = uc.Chrome(**your_options)

        self.DRIVER.maximize_window()
        self.action = EnhancedActionChains(self.DRIVER)

        # __________________________________ timezone _________________________________
        if proxy is not None:
            tz_params = {'timezoneId': resp.json()['timezone']}
            self.DRIVER.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)

        # if you need download to your folder
        if download_path == "default":
            return self.DRIVER

        else:
            return self.__set_new_download_path(download_path)

    def elem_exists(self, value, by=By.XPATH, wait=30, return_xpath=False, scroll_to=False):
        try:
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
            take_xpath = WebDriverWait(self.DRIVER,
                                       wait,
                                       ignored_exceptions=ignored_exceptions
                                       ).until(EC.presence_of_element_located((by, value)))

            if scroll_to:
                self.DRIVER.execute_script("arguments[0].scrollIntoView();", take_xpath)
                time.sleep(random.uniform(.5, 1))

            if not return_xpath:
                exist = True
            else:
                # retrurn
                return take_xpath

        except TimeoutException:
            exist = False

        return exist

    def _intercepted_click(self, elem_for_click):
        try:
            elem_for_click.click()
        except ElementClickInterceptedException:
            time.sleep(.5)
            self._intercepted_click(elem_for_click)

    def click_element(
            self, value, by=By.XPATH, wait=60, move_to=True, scroll_to=False, intercepted_click=False
    ) -> bool:

        if scroll_to:
            self.elem_exists(value=value, by=by, wait=wait, scroll_to=True)

        try:
            elem_for_click = WebDriverWait(self.DRIVER, wait).until(EC.element_to_be_clickable((by, value)))
        except TimeoutException:
            return False

        if move_to:
            self.mouse_move_to(elem_for_click)
            time.sleep(random.uniform(0.3, 0.7))

        if intercepted_click:
            self._intercepted_click(elem_for_click)
        else:
            elem_for_click.click()

        return True

    def send_text_by_elem(self, value, text_or_key, by=By.XPATH, scroll_to=False, wait=60):

        if self.click_element(value, by=by, scroll_to=scroll_to, wait=wait, move_to=True):
            research_xpath = self.DRIVER.find_element(by, value=value)

            research_xpath.clear()
            research_xpath.send_keys(text_or_key)

        else:
            input(f"No found or no be clickable {value}")

    def refrash_page(self):
        """if you have "Not Found data" call this function"""
        self.DRIVER.refresh()
        self.DRIVER.reconnect(.5)

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
        web_elem = self.elem_exists(value, return_xpath=True)
        self.DRIVER.execute_script("arguments[0].scrollIntoView();", web_elem)

    def stealth_send_text(self, value, text_or_key, by=By.XPATH, scroll_to=False, wait=60):
        if self.click_element(value, by=by, scroll_to=scroll_to, wait=wait):
            self.action.send_keys_1by1(text_or_key).perform()

    def reset_actions(self):
        self.action.reset_actions()

    def close_alert(self, url, wait=0.3):
        self.DRIVER.execute_script(f"location='{url}'; alert();")
        self.DRIVER.switch_to.alert.accept()
        self.DRIVER.reconnect(wait)
