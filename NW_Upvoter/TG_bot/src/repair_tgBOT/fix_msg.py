import asyncio

from aiogram.exceptions import TelegramNetworkError


async def send_telegram_message(message, text_msg, retries=3):
    for attempt in range(retries):
        try:
            # Ваш код для надсилання повідомлення через Telegram
            await message.reply(text_msg)
            break
        except TelegramNetworkError:
            if attempt < retries - 1:
                await asyncio.sleep(5)  # Затримка перед повторною спробою
                continue
            else:
                raise Exception("Can't send message")
