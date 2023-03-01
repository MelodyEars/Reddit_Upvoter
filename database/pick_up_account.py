import random
import traceback

from loguru import logger

from database import db_get_cookie_objs, db_get_link_id, Cookie, db_exist_record_link_account, db_get_cookie_proxy, \
    db_delete_record_work_account_with_link, WorkAccountWithLink
from handl_info.get_links import get_user_link_file


def pick_up_accounts_to_link(upvote_int: int):

    list_link_acc = []

    for link_from_file in get_user_link_file():
        list_cookies_objs: list = db_get_cookie_objs()
        random.shuffle(list_cookies_objs)

        link_id = db_get_link_id(link_from_file)

        for _ in range(upvote_int):
            id_work_link_account_obj = WorkAccountWithLink

            try:
                cookie_obj: Cookie = list_cookies_objs.pop()

                outcome_created, id_work_link_account_obj = db_exist_record_link_account(
                    link_id=link_id, account_id=cookie_obj.id
                )

                if outcome_created:  # if create record return TRUE
                    working_proxy, path_cookie, dict_proxy, id_cookie = db_get_cookie_proxy(cookie_obj)

                    if working_proxy:
                        # Add info to file
                        list_link_acc.append(
                            (link_from_file, path_cookie, dict_proxy, id_cookie, id_work_link_account_obj)
                        )

            except IndexError:
                break

            except Exception:
                logger.error(traceback.format_exc())
                list_link_acc.pop(-1)
                db_delete_record_work_account_with_link(id_work_link_account_obj)
                continue

    return list_link_acc
