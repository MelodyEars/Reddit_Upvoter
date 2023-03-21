from base_exception import RedditException


class WaitRequestToSubredditException(RedditException):
	"""When wait for offer posting from sub"""


class WaitingPostingException(RedditException):
	"""Reddit give you a break <1hour"""
