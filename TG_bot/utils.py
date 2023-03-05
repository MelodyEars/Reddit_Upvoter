from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.utils.helper import ListItem, Helper, HelperMode


class RunBotStates(StatesGroup):
    # mode = HelperMode.snake_case

    link = State()
    vote_int = State()
    comments_int = State()

