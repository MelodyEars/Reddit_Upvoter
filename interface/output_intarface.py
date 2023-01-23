from colorama import init, deinit
from work_fs import clear_cmd

from .user_requests import get_user_count_approves, get_user_count_comments, get_user_link


def user_deasire_data():
    init()
    link_reddit = get_user_link()
    clear_cmd()
    approves_int = get_user_count_approves()
    clear_cmd()
    comments_int = get_user_count_comments()
    deinit()

    return link_reddit, approves_int, comments_int
