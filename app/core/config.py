# app/core/config.py
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "Records API"
    APP_VERSION: str = "1.0.0"
    APP_DEBUG: bool = False

    APP_CORS_ORIGINS: str = "*"  # CSV или "*"
    DATABASE_URL: str
    FTS_DICTIONARY: str = "russian"

    # Pydantic v2 settings config
    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

settings = Settings()
