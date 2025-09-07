from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pydantic import EmailStr, SecretStr


class Settings(BaseSettings):
    ENVIRONMENT: str = 'development'
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: SecretStr
    MAIL_FROM: EmailStr
    MAIL_FROM_NAME: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
