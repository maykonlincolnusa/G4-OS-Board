from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    service_name: str = "audit-ledger-service"
    service_port: int = 8000
    environment: str = "development"
    log_level: str = "INFO"

    database_provider: str = "local"
    database_url: str = "postgresql+psycopg://board_user:board_pass@postgres:5432/board_os"
    aws_database_url: str | None = None
    gcp_database_url: str | None = None
    azure_database_url: str | None = None

    redis_url: str = "redis://redis:6379/0"
    sentry_dsn: str | None = None

    def resolved_database_url(self) -> str:
        provider = self.database_provider.lower().strip()
        if provider == "aws" and self.aws_database_url:
            return self.aws_database_url
        if provider == "gcp" and self.gcp_database_url:
            return self.gcp_database_url
        if provider == "azure" and self.azure_database_url:
            return self.azure_database_url
        return self.database_url


@lru_cache
def get_settings() -> Settings:
    return Settings()
