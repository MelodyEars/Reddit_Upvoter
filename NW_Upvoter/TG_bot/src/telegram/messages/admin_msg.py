from typing import TypedDict

from SETTINGS import mine_project


if mine_project:
    from .mine_ADMIN_text import *
else:
    from .nochance_Admin_text import *


class Messages(TypedDict):
    deleted_user: str
    user_denied: str
    added_user: str
    has_access: str
    has_many_user: str
    cmd_admin: str
    send_username: str


admin_MESSAGES: Messages = {
    'deleted_user': deleted_user,
    'user_denied': user_denied,
    'added_user': added_user,
    'has_access': has_access,
    'has_many_user': has_many_user,
    'cmd_admin': cmd_admin,
    'send_username': send_username
}