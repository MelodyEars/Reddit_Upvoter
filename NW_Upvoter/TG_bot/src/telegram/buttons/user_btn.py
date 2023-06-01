from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from NW_Upvoter.TG_bot.src.telegram.messages.user_msg import MESSAGES


def one_btn(text: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            # KeyboardButton(text='Поїхали!🚀')
            [KeyboardButton(text=text)]
        ], resize_keyboard=True
    )


main_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=MESSAGES['btn_run_work'])]
    ], resize_keyboard=True
)


cancel_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=MESSAGES['btn_reset'])]
    ], resize_keyboard=True
)
