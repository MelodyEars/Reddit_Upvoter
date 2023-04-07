from Uprove_TG_Bot.restrict import get_or_create_token
from work_fs.chack_info_and_write_to_file import get_or_create_info
from work_fs.PATH import path_near_exefile

mine_project = True

# ____________________________________________________________________ DATABASE
# set up db_tg_bot
set_database = {
                "user": 'postgres',
                "password": 'root123',
                "host": "localhost",
                "port": 5432,
                }

# ______________________________________________________________________ TG BOT
if mine_project:
    admins_id = [487950394, ]
else:
    # get from file
    admins_id = [
        int(admin_id) for admin_id in get_or_create_info("Введи свой telegram id", path_near_exefile("admin_id.txt"))
    ]
    # admins_id = [487950394, 6238496977]

# token for telegram bot
if mine_project:
    # our bot
    TOKEN = '5340721195:AAFlnSS4qNyoVF1mfkwmdBrzHzOStr--ThA'
else:
    # get from file
    TOKEN = get_or_create_token()
# _______________________________________________________________________ CHECK BAN
if mine_project:
    commands = ["add", "del"]
else:
    commands = ["del"]
