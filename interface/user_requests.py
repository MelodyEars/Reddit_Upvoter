import os

import work_fs as wf
from handl_info import get_comments


def get_user_link():
    print(wf.light_green_color("Ссылка на пост:"))
    post_link = input()
    return post_link


def get_user_count_approves(what_answering="апрувов"):

    available_profile = len(os.listdir(str(wf.path_near_exefile('cookies'))))
    print(wf.light_green_color(f"Доступно аккаунтов {available_profile}"))

    answer = wf.indicate_number(f"Сколько {what_answering} нужно")  # input

    if answer <= available_profile:
        if wf.data_confirmation(f"Устраивает ли вас колличиство {what_answering} {wf.green_color(answer)}"):
            # exit from this func, if user answers YES
            return answer

        # if user's answer NO return self func
    else:
        wf.warning_text("Ождается, что будет указано меньше ровно колличиству аккаунтов!")

    return get_user_count_approves()


def get_user_count_comments():
    comments_available = len(get_comments())
    print(wf.light_green_color(f"Доступно комментариев {comments_available}"))
    count_comments = get_user_count_approves("комментариев")

    if count_comments <= comments_available:
        return count_comments

    else:
        wf.warning_text("Привышено количество комментариев")
        return get_user_count_comments()
