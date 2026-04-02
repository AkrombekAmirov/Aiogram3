from aiogram import Router, types
from aiogram.filters import CommandStart
from bot.database.repositories.user_repo import UserRepository
from bot.database.connection import async_session

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: types.Message):
    async with async_session() as session:
        repo = UserRepository(session)
        user = await repo.get_or_create(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username
        )

    await message.answer(f"Xush kelibsiz, {user.full_name}!")
