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
    start_process: str
    finish_process: str
    deleted_post: str
    reset_msg: str
    btn_reset: str
    notif_browser_run: str
    hi_user: str
    btn_run_work: str
    not_enough_bots: str
    process_wrong: str
    error_vote_int_2: str
    post_is_sent: str
    this_link_is_not_post: str


MESSAGES: Messages = {
    'start': start_message,
    'help': help_message,
    'reddit_link': reddit_link,
    'error_vote_int': error_vote_int,
    'upvote_int': upvote_int,
    'start_process': start_process,
    'finish_process': finish_process,
    'deleted_post': deleted_post,
    'reset_msg': reset_msg,
    'btn_reset': btn_reset,
    'notif_browser_run': notif_browser_run,
    'hi_user': hi_user,
    'btn_run_work': btn_run_work,
    'not_enough_bots': not_enough_bots,
    'process_wrong': process_wrong,
    'error_vote_int_2': error_vote_int_2,
    "post_is_sent": post_is_sent,
    "this_link_is_not_post": this_link_is_not_post,
}
