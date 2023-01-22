import os
import pickle
from urllib.parse import urlparse


class Cookies:
    def __init__(self, driver, url):
        self.driver = driver
        self.domain = urlparse(url).netloc
        self.filename = f"{self.domain}.cookies.pickle"

    def exists(self):
        return os.path.exists(self.filename)

    def preload(self):
        print(f"preload cookies for {self.domain}")
        self.driver.execute_cdp_cmd("Network.enable", {})
        with open(self.filename, mode="rb") as f:
            for cookie in pickle.load(f):
                self.driver.execute_cdp_cmd("Network.setCookie", cookie)
        self.driver.execute_cdp_cmd("Network.disable", {})

    def save(self):
        print(f"save cookies for {self.domain}")
        with open(self.filename, mode="wb") as f:
            pickle.dump(self.driver.get_cookies(), f)
