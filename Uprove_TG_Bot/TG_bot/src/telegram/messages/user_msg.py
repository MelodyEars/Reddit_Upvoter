from typing import TypedDict

help_message = f'''Для того щоб використовувати бота натисніть кнопку "Поїхали!🚀" на панелі.
                    Якщо ви вже почали роботу, але зробили десь помилку, то для того, щоб повернутись на початок натисніть "⬅️ Все спочатку".
                    Дайте відповіді на всі запитання і Reddit бот почне працювати.'''

start_message = 'Вітаю! Цей бот потрібен для накрутки апвоутів та написання коментарів у Reddit.\n' + help_message

# ___________________________________ FMS State _______________________________________________ #
reddit_link = "Надішли посилання на пост Reddit."

upvote_int = "Введіть кількість upvote."
error_vote_int = "Помилка! Ваша відповідь не є цілим числом./Введіть кількість upvote.(тільки ціле число)"

# comments_int = "Кількість коментарів (якщо потрібно)"
error_comments_int = "Помилка! Ваша відповідь не є цілим числом./Кількість коментарів (якщо потрібно).(тільки ціле число)"

# ___________________________ message for notification about finsh process ______________________ #
start_process = "Виконую..."
finish_process = "Зробив!"

# ___________________________ deleted post______________________________
deleted_post = 'Пост був видалений!\n або \n Недостатньо акаунтів, щоб продовжувати робити апвоути.'


class Messages(TypedDict):
    start: str
    help: str
    reddit_link: str
    error_vote_int: str
    upvote_int: str
    error_comments_int: str
    # comments_int: str
    start_process: str
    finish_process: str
    deleted_post: str


MESSAGES: Messages = {
    'start': start_message,
    'help': help_message,
    'reddit_link': reddit_link,
    'error_vote_int': error_vote_int,
    'upvote_int': upvote_int,
    'error_comments_int': error_comments_int,
    # 'comments_int': comments_int,
    'start_process': start_process,
    'finish_process': finish_process,
    'deleted_post': deleted_post,
}
