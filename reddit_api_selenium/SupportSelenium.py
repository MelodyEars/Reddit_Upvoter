import pickle
from urllib.parse import urlparse

from work_fs import file_exists, path_near_exefile


class Cookies:
    def __init__(self, driver, path_filename, url):
        self.DRIVER = driver
        self.domain = urlparse(url).netloc
        self.path_filename = path_near_exefile(fr"{path_filename}")
        print(path_filename)
        print(self.path_filename)

    def exists(self):
        return file_exists(self.path_filename)

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

'//div[contains(text(), "Incorrect username or password")]'