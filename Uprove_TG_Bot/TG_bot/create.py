from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from SETTINGS import TOKEN


# initalization bot
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Queue for notifying users about process completion
# user_queues = {}
