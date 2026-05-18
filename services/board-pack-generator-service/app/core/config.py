from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    service_name: str = "board-pack-generator-service"
    service_port: int = 8000
    environment: str = "development"
    log_level: str = "INFO"
    database_url: str = "postgresql+psycopg://board_user:board_pass@postgres:5432/board_os"
    redis_url: str = "redis://redis:6379/0"
    sentry_dsn: str | None = None
    jwt_secret: str = "change-me"


@lru_cache
def get_settings() -> Settings:
    return Settings()

