import pickle
import time
from pathlib import Path

from work_fs import file_exists


class CookiesBrowser:
    def __init__(self, driver, link_from_file=None, path_cookie=Path, id_work_link_account_obj=None, username=None):
        self.DRIVER = driver
        self.path_cookie = path_cookie
        self.link_from_file = link_from_file
        self.id_work_link_account_obj = id_work_link_account_obj
        self.username = username

    def are_valid(self):
        if file_exists(self.path_cookie):
            near_future = time.time() + 30  # 30s in the future
            with open(self.path_cookie, mode="rb") as f:
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

        with open(self.path_cookie, mode="rb") as f:
            for cookie in pickle.load(f):
                self.DRIVER.execute_cdp_cmd("Network.setCookie", cookie)
            f.close()
            
        self.DRIVER.execute_cdp_cmd("Network.disable", {})

    def save(self):
        with open(self.path_cookie, mode="wb") as f:
            pickle.dump(self.DRIVER.get_cookies(), f)
            f.close()
