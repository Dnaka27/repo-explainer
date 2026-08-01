from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_ENV_FILE, extra="ignore")

    gemini_api_key: str
    gemini_model: str = "gemini-flash-latest"
    gemini_timeout_seconds: int = 60

    github_token: str = ""

    max_files_to_analyze: int = 20
    max_file_size_bytes: int = 50_000
    max_total_prompt_bytes: int = 400_000

    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()
