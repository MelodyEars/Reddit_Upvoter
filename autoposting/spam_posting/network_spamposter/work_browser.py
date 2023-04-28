
from auth_reddit.auth_reddit_api_selenium import RedditAuth
from autoposting.network.api import CreatePost


class SuppoetSpamPoster(CreatePost, RedditAuth):
    pass


class SpamPosterReddit(SuppoetSpamPoster):
    def __init__(self, proxy: dict):
        super().__init__(proxy)
        self.proxy = proxy

    def __enter__(self):
        self.DRIVER = self.run_driver(proxy=self.proxy, detection_location=True)
        self.DRIVER.get('https://www.reddit.com/')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.DRIVER.quit()

    def create_post(self, title, image_url, link_sub_reddit):
        CreatePost.create_post(self, title, image_url, link_sub_reddit)