from base_exception import RedditException


class WaitRequestToSubredditException(RedditException):
	"""When wait for offer posting from sub"""


class WaitingPostingException(RedditException):
	"""Reddit give you a break <1hour"""


class NotTrustedMembersException(RedditException):
	"""This community only allows trusted members to post here"""
