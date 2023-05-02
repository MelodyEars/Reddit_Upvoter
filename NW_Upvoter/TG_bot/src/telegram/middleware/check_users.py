from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

from NW_Upvoter.TG_bot.src.database.tables import AllowedUser


class CheckUser(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        allowed_users = [user.username for user in AllowedUser.select()]
        if event.from_user.username in allowed_users:
            return await handler(event, data)
