from aiogram.dispatcher.filters.state import State, StatesGroup


class RunBotStates(StatesGroup):

    reddit_link = State()
    upvote_int = State()
    comments_int = State()

