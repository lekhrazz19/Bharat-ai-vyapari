from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_BASE_URL: str = "http://localhost:8000"
    PUBLIC_FILE_BASE_URL: str = "http://localhost:8000/files"

    TELEGRAM_BOT_TOKEN: str = ""
    ADMIN_TELEGRAM_CHAT_ID: str = ""
    ALLOWED_TELEGRAM_USER_IDS: str = ""

    OPENROUTER_API_KEY: str = ""
    OPENROUTER_DEFAULT_MODEL: str = "google/gemini-2.5-flash"
    OPENROUTER_FALLBACK_MODEL: str = "google/gemini-2.5-flash"

    SERPER_API_KEY: str = ""

    BASEROW_API_TOKEN: str = ""
    BASEROW_TABLE_ID: str = ""
    BASEROW_API_URL: str = "https://api.baserow.io/api"
    BASEROW_PROPOSAL_ID_FIELD: str = "proposal_id"

    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASS: str = ""
    SMTP_FROM: str = ""

    STORAGE_MODE: str = "local"
    LOCAL_STORAGE_DIR: str = "storage/pdf"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
