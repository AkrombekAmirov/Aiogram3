from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

# Sizning custom DB servisingizni import qilamiz
from bot.database.DatabaseService.base import DatabaseService


class DatabaseMiddleware(BaseMiddleware):
    """
    Har bir kelgan Update uchun DatabaseService obyektini yaratib,
    handlerlarga 'db' kaliti orqali uzatadi.
    """

    def __init__(self) -> None:
        # Singlton sifatida bitta DB engine ishlatilishi uchun
        # asosiydan olinadi. Har bir so'rovda yangi session ochiladi.
        self.db_service = DatabaseService()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        # Handlerlar argument sifatida db=DatabaseService() ni qabul qila oladi
        data["db"] = self.db_service

        # Handlerni ishga tushirish
        return await handler(event, data)