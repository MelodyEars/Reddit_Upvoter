import asyncio

from multiprocessing import freeze_support

from loguru import logger

from aiogram import Bot
from aiohttp import web
from aiogram.webhook.aiohttp_server import (
	SimpleRequestHandler,
	setup_application,
)
from tortoise import Tortoise

import work_fs as wf
from NW_Upvoter.TG_bot.setup import dp, bot
from NW_Upvoter.TG_bot.src.database.tables import create_tables_user_tg
from NW_Upvoter.TG_bot.src.telegram.middleware.admin_only import AdminOnly
from NW_Upvoter.TG_bot.src.telegram.middleware.check_users import CheckUser
from NW_Upvoter.TG_bot.src.telegram.handlers.admin_handlers import admin_router
from NW_Upvoter.TG_bot.src.telegram.handlers.user_handlers import user_router
from NW_Upvoter.db_tortories_orm.query.bot_accounts import db_update_0_all


async def _start():
	admin_router.message.middleware(AdminOnly())
	user_router.message.middleware(CheckUser())
	dp.include_router(admin_router)
	dp.include_router(user_router)
	await dp.start_polling(bot)


def start_simple():
	logger.info("Telegram bot started")
	asyncio.run(_start())


async def on_startup(bot: Bot, base_url: str):
	await db_update_0_all()
	await bot.set_webhook(f"{base_url}")


async def on_shutdown(bot: Bot, base_url: str):
	await Tortoise.close_connections()
	await bot.delete_webhook()


def start_webhook():
	# dp["base_url"] = ngrok_url
	dp.startup.register(on_startup)
	dp.shutdown.register(on_shutdown)
	dp.include_router(admin_router)

	app = web.Application()
	app["bot"] = bot
	SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path='')
	setup_application(app, dp, bot=bot)
	web.run_app(app, host="0.0.0.0", port=5000)


def run_tg_bot():
	try:
		create_tables_user_tg()
		start_simple()  # run without webhook
	# #start_webhook()  # run tg bot
	except KeyboardInterrupt:
		logger.info("Bot stopped by admin")


@logger.catch
def main():
	run_tg_bot()


if __name__ == '__main__':
	freeze_support()
	logger.add(
		wf.auto_create(wf.path_near_exefile("logs"), _type="dir") / "TgBot.log",
		format="{time} {level} {message}",
		level="INFO",
		rotation="10 MB",
		compression="zip"
	)

	main()
