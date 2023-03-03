import random

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def emoji_car() -> str:
	auto = ["🚙", "🏎️", "🚘", "🚗"]
	return random.choice(auto)


def emoji_catalog() -> str:
	list_catalog = ["📑", "📄", "📜", "📃", "📒", "📓", "📙", "📘", "📗", "📕", "📔"]
	return random.choice(list_catalog)


# ________________________________________additional options of button____________________
btn_returnMain = KeyboardButton("⬅️ Все спочатку")


# ---------------------- Main menu -----------------------------
btn_catalog = KeyboardButton('📖 Каталог ' + emoji_car())
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_catalog)


# _______________________ NExt level button ____________________________
buttons = [btn_returnMain]
models = sorted(("Tesla", "Volkswagen", "Toyota", "Audi", "Honda", "Hyundai", "Pego", "LOL",
                 "ldskflsd", "s;flsdfl;", "csdfsdfsdf", "sfsafcasd", "sadasda", "asdsadasd"
                 "Fior", "lsbgkfxd;lbx", ";gjsdf;gl,"))

for model in models:
	btn_example = KeyboardButton(model)
	buttons.append(btn_example)

otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)
