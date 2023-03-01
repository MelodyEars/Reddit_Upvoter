import traceback

from loguru import logger

from Settings_Selenium import CookiesBrowser, get_reddit_api, close_all_browser
from database import db_delete_record_work_account_with_link

from .reddit_actions import RedditWork
from .exceptions import NotRefrashPageException, BanAccountException


def create_api_cls(client_cookies: list[CookiesBrowser], list_comment: list[str]):
    list_reddit_api = []
    for cl_cookie in client_cookies:
        try:
            if list_comment:
                comment: str = list_comment.pop()
                with RedditWork(cl_cookie, comment=comment) as api_reddit:
                    list_reddit_api.append(api_reddit)
                    logger.info(f'Взято на облік "{cl_cookie.username}"')

            else:
                with RedditWork(cl_cookie) as api_reddit:
                    list_reddit_api.append(api_reddit)
                    logger.info(f'Взято на облік "{cl_cookie.username}"')
        except Exception:
            logger.error(traceback.format_exc())
            db_delete_record_work_account_with_link(cl_cookie.id_work_link_account_obj)
            cl_cookie.is_work = False

    return list_reddit_api


def vote_api(list_reddit_api: list[RedditWork]):
    for reddit_api in get_reddit_api(list_reddit_api):
        # put on upvote
        try:
            reddit_api.upvote()

        except BanAccountException:
            logger.debug(f'Ban: "{reddit_api.client_cookie.username}"')
            reddit_api.client_cookie.is_work = False
            db_delete_record_work_account_with_link(reddit_api.client_cookie.id_work_link_account_obj)

        except NotRefrashPageException:
            logger.debug(f'Our CDN was unable to reach our servers. Account: "{reddit_api.client_cookie.username}"')
            reddit_api.client_cookie.is_work = False
            db_delete_record_work_account_with_link(reddit_api.client_cookie.id_work_link_account_obj)


def subscribing_api(list_reddit_api: list[RedditWork]):
    for reddit_api in get_reddit_api(list_reddit_api):
        # follow model or join to community
        reddit_api.subscribing()


def comment_api(list_reddit_api: list[RedditWork]):
    for reddit_api in get_reddit_api(list_reddit_api):
        # if required to write comments
        if reddit_api.write_comment():
            continue
        else:
            break


def work_in_browser(client_cookies: list[CookiesBrowser], list_comment: list[str]):
    list_reddit_api = create_api_cls(client_cookies, list_comment)

    [api.attend_link() for api in get_reddit_api(list_reddit_api)]  # attend post link
    vote_api(list_reddit_api)  # put on upvote
    subscribing_api(list_reddit_api)  # subscribe on a sub
    comment_api(list_reddit_api)  # if need writes comment

    close_all_browser(client_cookies)
