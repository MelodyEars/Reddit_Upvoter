import os
import pickle
from urllib.parse import urlparse

import work_fs


class Cookies:
    def __init__(self, driver, path_filename, url):
        self.DRIVER = driver
        self.domain = urlparse(url).netloc
        self.path_filename = work_fs.path_near_exefile(path_filename)

    def exists(self):
        return work_fs.file_exists(self.path_filename)

    def preload(self):
        print(f"preload cookies for {self.domain}")
        self.DRIVER.execute_cdp_cmd("Network.enable", {})
        with open(self.path_filename, mode="rb") as f:
            for cookie in pickle.load(f):
                self.DRIVER.execute_cdp_cmd("Network.setCookie", cookie)
        self.DRIVER.execute_cdp_cmd("Network.disable", {})

    def save(self):
        print(f"save cookies for {self.domain}")
        with open(self.path_filename, mode="wb") as f:
            pickle.dump(self.DRIVER.get_cookies(), f)
