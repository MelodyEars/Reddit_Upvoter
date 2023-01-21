"""
This file makes requests to user.
"""

from .color import blue_color, green_color, warning_text


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
        warning_text(f"Потрібно обрати yes or no")
        return data_confirmation(massage)
