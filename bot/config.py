from __future__ import annotations
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class AppSettings(BaseSettings):
    """
    🎯 Ilovaning global konfiguratsiyasi (FastAPI, DB, JWT)
    """

    # =======================
    # 🏛 Asosiy app sozlamalari
    # =======================
    APP_NAME: str = Field(default="University Attendance System")
    APP_ENV: str = Field(default="development")  # development | production | test
    DEBUG: bool = Field(default=True)
    API_V1_PREFIX: str = Field(default="/api/v1")
    TIMEZONE: str = Field(default="Asia/Tashkent")

    # =======================
    # 🤖 Telegram Bot sozlamalari
    # =======================
    BOT_TOKEN: str = Field(default="YOUR_BOT_TOKEN_HERE")

    # =======================
    # 🗄 Ma’lumotlar bazasi (PostgreSQL)
    # =======================
    DB_USER: str = Field(default="turnikeuser")
    DB_PASSWORD: str = Field(default="StrongSecurePass123!")
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5436)
    DB_NAME: str = Field(default="turnikedb")

    @property
    def DATABASE_URL(self) -> str:
        """Async SQLAlchemy uchun to‘liq DSN."""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        """Sync versiya (Alembic migratsiyalari uchun)"""
        return self.DATABASE_URL.replace("+asyncpg", "")

    # =======================
    # 🔐 JWT / Authentication
    # =======================
    JWT_SECRET_KEY: str = Field(default="change_this_super_secret_key")
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(default=43200)

    # =======================
    # 🧩 Validatorlar
    # =======================
    @field_validator("APP_ENV")
    @classmethod
    def validate_env(cls, v: str) -> str:
        allowed = {"development", "production", "test"}
        if v not in allowed:
            raise ValueError(f"APP_ENV must be one of: {', '.join(allowed)}")
        return v

    @field_validator("DB_HOST")
    @classmethod
    def validate_db_host(cls, v: str) -> str:
        if not v:
            raise ValueError("DB_HOST cannot be empty")
        return v

    # =======================
    # ⚙️ Model config
    # =======================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    """Caching orqali konfiguratsiyani tezkor olish."""
    return AppSettings()
