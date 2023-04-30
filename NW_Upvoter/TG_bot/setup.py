from aiogram import Dispatcher, Bot, Router
# from dotenv import load_dotenv
# import os
# from pathlib import Path
from work_fs.PATH import path_near_exefile
from SETTINGS import TOKEN
# load_dotenv()
# TOKEN = os.getenv("TOKEN_BOT")
# TOKEN = '5697563320:AAGmc7f5nW0GNZEdqWz-aLWgCkTplXHxYu4'

bot = Bot(TOKEN)
dp = Dispatcher()

# create routes

admin_router = Router()
user_router = Router()
# common_router = Router()

ROOT_DIR = path_near_exefile()
