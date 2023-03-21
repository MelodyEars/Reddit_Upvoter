import pickle
import time

from work_fs import file_exists


class BrowserCookie:
    def __init__(self, driver, path_filename):
        self.DRIVER = driver
        self.path_filename = path_filename

    def are_valid(self):
        if file_exists(self.path_filename):
            near_future = time.time() + 30  # 30s in the future
            with open(self.path_filename, mode="rb") as f:
                # check all are still valid in near_future
                try:
                    exists = all(expiry >= near_future
                                 for cookie in pickle.load(f)
                                 if (expiry := cookie.get("expiry"))
                                 )
                except EOFError:
                    exists = False
                return exists
        return False

    def preload(self):
        self.DRIVER.execute_cdp_cmd("Network.enable", {})

        with open(self.path_filename, mode="rb") as f:
            for cookie in pickle.load(f):
                self.DRIVER.execute_cdp_cmd("Network.setCookie", cookie)
            f.close()
            
        self.DRIVER.execute_cdp_cmd("Network.disable", {})

    def save(self):
        with open(self.path_filename, mode="wb") as f:
            pickle.dump(self.DRIVER.get_cookies(), f)
            f.close()
