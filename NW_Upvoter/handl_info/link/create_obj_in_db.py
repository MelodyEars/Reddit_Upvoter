import re

from loguru import logger

from NW_Upvoter.db_tortories_orm.query.link import db_get_or_create_link_obj
from NW_Upvoter.handl_info import get_reveddit_link
from base_exception import ThisLinkIsNotPostException


def match_pattern_reddit_url(url):
    pattern = r'^https://www\.reddit\.com/r/[\w-]+/comments/[\w-]+/.*'
    if re.match(pattern, url):
        return True
    else:
        return False


async def analizated_link(message, reddit_link, upvote_int):
    sub = "/".join(reddit_link.split("/")[3:5])
    who_posted = message.from_user.username

    if match_pattern_reddit_url(reddit_link):
        reveddit_url = await get_reveddit_link(reddit_link)
        logger.info(f"reveddit_url: {reveddit_url}")
        link_obj, created = await db_get_or_create_link_obj(reddit_link, who_posted, sub, upvote_int, reveddit_url)

        if created:
            return link_obj

        else:
            return None

    else:
        raise ThisLinkIsNotPostException("This link is not post")

