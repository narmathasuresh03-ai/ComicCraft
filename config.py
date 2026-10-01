from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.5-flash-lite"
    app_name: str = "ComicCraft"

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()