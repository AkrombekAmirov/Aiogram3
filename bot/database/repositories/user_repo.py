from typing import Optional, Tuple
from bot.database.DatabaseService.repositories import BaseRepository
from bot.database.models.user import User


class UserRepository(BaseRepository[User]):
    """
    User modeli uchun maxsus repository.
    BaseRepository'dagi barcha standart metodlarni (create, update, list, delete_soft) meros qilib oladi.
    Bu yerda faqat User'ga xos bo'lgan maxsus biznes mantiqlar yoziladi.
    """

    def __init__(self, db=None):
        # BaseRepository ga o'zimizning User modelimizni tanitib qo'yamiz
        super().__init__(model=User, db=db)

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Telegram ID bo'yicha foydalanuvchini topish."""
        users = await self.list(filters={"telegram_id": telegram_id}, limit=1)
        return users[0] if users else None

    async def get_or_create(self, telegram_id: int, defaults: dict) -> Tuple[User, bool]:
        """
        Juda foydali metod: Telegram'dan xabar kelganda foydalanuvchini qidiradi,
        agar bazada bo'lmasa, uni yangi ro'yxatdan o'tkazadi.

        Qaytaradi: (User obyekti, Yaratildimi? (True/False))
        """
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            # Agar foydalanuvchi ismini o'zgartirgan bo'lsa, bazani yangilab qo'yish mantiqini shu yerga qo'shish mumkin
            return user, False

        # Foydalanuvchi topilmadi, demak yangi yaratamiz
        new_user = User(telegram_id=telegram_id, **defaults)
        created_user = await self.create(new_user)
        return created_user, True

    async def update_language(self, telegram_id: int, language_code: str) -> Optional[User]:
        """Foydalanuvchining tilini tezkor o'zgartirish."""
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            return await self.update_fields(user.id, {"language_code": language_code})
        return None

    async def block_user(self, telegram_id: int) -> bool:
        """Foydalanuvchi botni bloklaganda (is_active = False) holatiga o'tkazish."""
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            await self.update_fields(user.id, {"is_active": False})
            return True
        return False