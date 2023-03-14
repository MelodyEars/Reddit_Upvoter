from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def one_btn(text: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            # KeyboardButton(text='Поїхали!🚀')
            [KeyboardButton(text=text)]
        ], resize_keyboard=True
    )


main_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Поїхали!🚀')]
    ], resize_keyboard=True
)


cancel_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='⬅️ Все спочатку')]
    ], resize_keyboard=True
)