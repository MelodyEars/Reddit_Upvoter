from base_exception import RedditException


class NotRefrashPageException(RedditException):
    """Our CDN was unable to reach our servers"""


class BanAccountException(RedditException):
    """Your account banned"""


class CookieInvalidException(RedditException):
    """Cookie invalid"""


class ElementNotClickException(RedditException):
    """Expected tuple or str"""


class PostDeletedException(RedditException):
    """if exists this message 'Sorry, this post has been remove'"""
