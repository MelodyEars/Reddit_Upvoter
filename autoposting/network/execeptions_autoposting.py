from base_exception import RedditException


class SubredditWasBannedException(RedditException):
    """This subreddit was banned due to being unmoderated."""
