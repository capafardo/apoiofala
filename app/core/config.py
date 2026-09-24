"""
Configurações da aplicação CAA-Lab.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Configurações globais carregadas de variáveis de ambiente ou .env."""

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "CAA-Lab"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"
    DEBUG: bool = False

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    SECRET_KEY: str = "caa-lab-default-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas

    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'data' / 'caa_lab.db'}"

    DEFAULT_LANGUAGE: str = "pt-BR"
    DEFAULT_VOICE_RATE: float = 1.0
    TTS_OFFLINE_MODE: bool = False

    DATA_DIR: Path = BASE_DIR / "data"
    ASSETS_DIR: Path = BASE_DIR / "assets"
    STATIC_DIR: Path = BASE_DIR / "app" / "static"
    TEMPLATES_DIR: Path = BASE_DIR / "app" / "templates"


settings = Settings()
