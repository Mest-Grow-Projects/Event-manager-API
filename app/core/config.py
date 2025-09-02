from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os

class Settings(BaseSettings):
    ENVIRONMENT: str = 'development'
    DATABASE_URL: str
    SECRETE_KEY: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            '.env'
        ), env_file_encoding='utf-8'
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
