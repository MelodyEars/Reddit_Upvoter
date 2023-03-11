from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# ________________________________________additional options of button____________________
btn_returnMain = KeyboardButton("⬅️ Все спочатку")
returnMain = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_returnMain)

# ---------------------- Main menu -----------------------------
btn_catalog = KeyboardButton('Поїхали!🚀')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_catalog)

