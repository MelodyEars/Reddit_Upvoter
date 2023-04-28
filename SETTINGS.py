from peewee import PostgresqlDatabase
from playhouse.cockroachdb import CockroachDatabase

from Uprove_TG_Bot.restrict import get_or_create_token
from work_fs.chack_info_and_write_to_file import get_or_create_info
from work_fs.PATH import path_near_exefile

mine_project = True

# ____________________________________________________________________ DATABASE
# set up db_tg_bot
if mine_project:
    # # Or, alternatively, specified as part of a connection-string:
    # set_database = {
    #     "username": "doadmin",
    #     'password': 'AVNS_XCxtxUH7rZz8txAxKYO',
    #     'host': 'bots-do-user-11731497-0.b.db.ondigitalocean.com',
    #     'port': '25061',
    #     "database": "storage_bots",
    #     "sslmode": "require",
    #     "sslrootcert": r"C:\Users\Administrator\Documents\ca-certificate.crt"
    # }

    set_database = r'postgresql://doadmin:AVNS_XCxtxUH7rZz8txAxKYO@bots-do-user-11731497-0.b.db.ondigitalocean.com:25061/8-core_start_comp?sslmode=require&sslrootcert=C:\Users\Administrator\Documents\ca-certificate.crt'
    db = CockroachDatabase(set_database)


else:
    set_database = {
                    "user": 'postgres',
                    "password": 'root123',
                    "host": "localhost",
                    "port": 5432,
                    }
    db = PostgresqlDatabase('database', **set_database)

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
# if mine_project:
#     # our bot
#     TOKEN = '5340721195:AAFlnSS4qNyoVF1mfkwmdBrzHzOStr--ThA'
# else:
    # get from file
TOKEN = get_or_create_token()

# _______________________________________________________________________ CHECK BAN
if mine_project:
    commands = ["add", "del"]
else:
    commands = ["del"]
