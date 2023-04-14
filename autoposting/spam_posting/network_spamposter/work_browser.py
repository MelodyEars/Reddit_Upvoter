
from auth_reddit.auth_reddit_api_selenium import RedditAuth
from autoposting.network.api import CreatePost


class SpamPosterReddit(CreatePost, RedditAuth):
    def __init__(self, proxy: dict, path_cookie):
        CreatePost.__init__(self, path_cookie, proxy)
        RedditAuth.__init__(self, proxy)

        self.proxy = proxy
        self.cookie_path = None
        self.client_cookie = None

    def __enter__(self):
        self.DRIVER = self.run_driver(proxy=self.proxy, detection_location=True)
        self.DRIVER.get('https://www.reddit.com/')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.DRIVER.quit()
