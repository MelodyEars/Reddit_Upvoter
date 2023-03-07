
help_message = f'''Для того щоб використовувати бота натисніть кнопку "Поїхали!🚀" на панелі.
                    Якщо ви вже почали роботу, але зробили десь помилку, то для того, щоб повернутись на початок натисніть "⬅️ Все спочатку".
                    Дайте відповіді на всі запитання і Reddit бот почне працювати.'''

start_message = 'Вітаю! Цей бот потрібен для накрутки апвоутів та написання коментарів у Reddit.\n' + help_message

answer_link = "Надішли посилання на пост Reddit."
vote_int = "Введіть кількість upvote."
error_vote_int = "Помилка! Ваша відповідь не є цілим числом./Введіть кількість upvote.(тільки ціле число)"
comments_int = "Кількість коментарів (якщо потрібно)"
error_comments_int = "Помилка! Ваша відповідь не є цілим числом./Кількість коментарів (якщо потрібно).(тільки ціле число)"


MESSAGES = {
    'start': start_message,
    # 'help': help_message,
    'link': answer_link,
    'error_vote_int': error_vote_int,
    'vote_int': vote_int,
    'error_comments_int': error_comments_int,
    'comments_int': comments_int,
}
