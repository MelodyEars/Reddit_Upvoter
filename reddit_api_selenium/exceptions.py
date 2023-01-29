from base_exception import RedditException


class NotRefrashPageException(RedditException):
    """Our CDN was unable to reach our servers"""


class BanAccountException(RedditException):
    """Your account banned"""


class CookieInvalidException(RedditException):
    """Cookie invalid"""
