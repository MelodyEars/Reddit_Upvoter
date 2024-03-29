from typing import TypedDict

from SETTINGS import mine_project


if mine_project:
    from .mine_USER_text import *
else:
    from .nochance_user_text import *


class Messages(TypedDict):
    start: str
    help: str
    reddit_link: str
    error_vote_int: str
    upvote_int: str
    # error_comments_int: str
    # comments_int: str
    start_process: str
    finish_process: str
    deleted_post: str
    reset_msg: str
    btn_reset: str
    notif_browser_run: str
    hi_user: str
    btn_run_work: str
    not_enough_bots: str


MESSAGES: Messages = {
    'start': start_message,
    'help': help_message,
    'reddit_link': reddit_link,
    'error_vote_int': error_vote_int,
    'upvote_int': upvote_int,
    # 'error_comments_int': error_comments_int,
    # 'comments_int': comments_int,
    'start_process': start_process,
    'finish_process': finish_process,
    'deleted_post': deleted_post,
    'reset_msg': reset_msg,
    'btn_reset': btn_reset,
    'notif_browser_run': notif_browser_run,
    'hi_user': hi_user,
    'btn_run_work': btn_run_work,
    'not_enough_bots': not_enough_bots
}
