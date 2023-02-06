"""
This file makes requests to user.
"""

from .color import blue_color, green_color, warning_text, cyan_color


def data_confirmation(massage) -> bool:
    yes = ["y", "yes", ""]
    no = ["n", "no"]

    print(blue_color(massage + green_color("?[Y/n]")))
    answer = input().replace(" ", "").lower()
    if answer in yes:
        return True

    elif answer in no:
        return False

    else:
        warning_text(f"Выбери yes or no")
        return data_confirmation(massage)


def indicate_number(text_what_answer: str):
    print(cyan_color(f"{text_what_answer}?"))
    try:
        number = int(input())
        return number
    except ValueError:
        warning_text("Нужно указать целочисленный тип")

    return indicate_number(text_what_answer)
