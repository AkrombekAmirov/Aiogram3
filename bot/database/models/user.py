import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, Column
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    # Asosiy ID (Baza uchun UUID ishlatish eng to'g'ri yo'l, xavfsiz va kengayuvchan)
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)

    # Telegram ma'lumotlari
    # BigInteger ishlatilishi shart, chunki Telegram ID lar int32 chegarasidan oshib ketgan
    telegram_id: int = Field(sa_column=Column(BigInteger, unique=True, index=True, nullable=False))
    username: Optional[str] = Field(default=None)
    full_name: str
    language_code: Optional[str] = Field(default="uz")

    # Statuslar
    is_active: bool = Field(default=True, description="Foydalanuvchi botdan foydalanyaptimi (bloklamaganmi)")
    is_admin: bool = Field(default=False, description="Bot administratori ekanligini bildiradi")

    # Soft delete (BaseRepository dagi delete_soft() funksiyasi uchun muhim)
    is_deleted: bool = Field(default=False, index=True)

    # Audit vaqtlar
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Xohishga ko'ra qo'shimcha maydonlar (masalan: telefon raqam, balans)
    # phone_number: Optional[str] = Field(default=None)
    # balance: float = Field(default=0.0)

    class Config:
        arbitrary_types_allowed = True