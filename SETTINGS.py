
mine_project = True
# token for telegram bot

# if mine_project:
    # our bot
TOKEN = '5340721195:AAFlnSS4qNyoVF1mfkwmdBrzHzOStr--ThA'
# else:
#     TOKEN = "6296457111:AAF-WRfX5OhpJehvd2hTS_3iAmQUB-yH9Yw"


# set up db_tg_bot
set_database = {
                "user": 'postgres',
                "password": 'root123',
                "host": "localhost",
                "port": 5432,
                }
if mine_project:
    admins_id = [487950394, ]
else:
    admins_id = [487950394, 6238496977]
