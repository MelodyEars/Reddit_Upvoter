import os

import work_fs as wf


def get_user_link():
    print(wf.light_green_color("Ссылка на пост:"))
    post_link = input()
    return post_link


def get_user_count(what_answering=str):
    # need pass "апрувов" "комментариев"
    wf.clear_cmd()

    count_profile = len(os.listdir(str(wf.path_near_exefile('cookies'))))
    print(wf.light_green_color(f"Доступно аккаунтов {count_profile}"))

    answer = wf.indicate_number(f"Сколько {what_answering} нужно")  # input

    if answer <= count_profile:
        if wf.data_confirmation(f"Устраивает ли вас колличиство {what_answering} {wf.green_color(answer)}"):
            # exit from this func, if user answers YES
            return answer

        # if user's answer NO return self func
    else:
        wf.warning_text("Ождается, что будет указано меньше ровно колличиству аккаунтов!")

    return get_user_count()
