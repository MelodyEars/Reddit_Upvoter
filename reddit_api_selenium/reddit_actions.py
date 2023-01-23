from selenium.webdriver.common.by import By

from .SupportSelenium import Cookies
from .selenium_driver import BaseClass


class RedditWork(BaseClass):
    def __init__(self, path_cookie=str, link=str, proxy=None):

        super(__class__, self).__init__()
        self.client_cookie = None
        self.proxy = proxy
        self.link = link
        self.cookie_path = path_cookie

    def __enter__(self):
        self.DRIVER = self._driver(proxy=self.proxy)
        
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.DRIVER.quit()

    def attend_link(self):
        self.client_cookie = Cookies(driver=self.DRIVER, url=self.link, path_filename=self.cookie_path)
        self.client_cookie.preload()
        self.DRIVER.get(self.link)
        self.DRIVER.reconnect()

    def popups_pass(self):
        # popups
        self.xpath_exists(value='body', by=By.TAG_NAME)
        # THen content 18+
        input("Content 18+:")
        # asks to continue when you visit a site with a post
        self.click_element('//button[contains(text(), "Continue")]', wait=0.5, move_to=True)

    def upvote(self):
        # post
        self.xpath_exists(by=By.ID, value="post-content")
        # upvote
        if self.click_element('//button[@data-click-id="upvote" and @aria-pressed="false"]', wait=10):
            # wait for
            if self.xpath_exists('//div[@data-test-id="post-content"]//i[contains(@class, "icon icon-upvote_fill ")]',
                                 wait=4):
                # success
                return
            else:
                self.reset_actions()
                return self.upvote()
        else:
            # account's click exists
            return

    def write_comment(self, text_comment):
        self.send_text_by_elem(value='//div[@class="notranslate public-DraftEditor-content"]',
                               text_or_key=text_comment,
                               scroll_to=True)
        # send comment
        self.click_element('//button[contains(text(), "Comment")]', move_to=True)

        # wait 2 before, then click button send
        if self.xpath_exists('//span[contains(text(), "1 new comment")]', wait=4):
            # success
            return

        else:
            self.reset_actions()
            return self.write_comment(text_comment)
