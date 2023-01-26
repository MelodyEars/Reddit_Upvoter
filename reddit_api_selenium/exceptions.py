class RedditException(Exception):
    """Generic exception that all other YouTube errors are children of."""

    def __init__(self, *args):
        self.message = args[0] if args else None
        super().__init__(self.message)

    def __str__(self):
        return f'RedditAPI -> {self.message}'


class NotRefrashPageException(RedditException):
    """Our CDN was unable to reach our servers"""


class BanAccountException(RedditException):
    """Your account banned"""


class CookieInvalidException(RedditException):
    """Cookie invalid"""
