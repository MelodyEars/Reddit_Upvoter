from colorama import init, deinit
from work_fs import clear_cmd

from .user_requests import get_user_count_approves, get_user_count_comments


def user_desired_value():
    init()
    clear_cmd()
    approves_int = get_user_count_approves()
    clear_cmd()
    comments_int = get_user_count_comments()
    deinit()

    return approves_int, comments_int
