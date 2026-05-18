from __future__ import annotations

import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def _resolve_database_url() -> str:
    provider = os.getenv("DATABASE_PROVIDER", "local").lower().strip()
    default_url = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))

    if provider == "aws" and os.getenv("AWS_DATABASE_URL"):
        return os.getenv("AWS_DATABASE_URL")  # type: ignore[return-value]
    if provider == "gcp" and os.getenv("GCP_DATABASE_URL"):
        return os.getenv("GCP_DATABASE_URL")  # type: ignore[return-value]
    if provider == "azure" and os.getenv("AZURE_DATABASE_URL"):
        return os.getenv("AZURE_DATABASE_URL")  # type: ignore[return-value]
    return default_url


def run_migrations_offline() -> None:
    url = _resolve_database_url()
    context.configure(url=url, literal_binds=True, dialect_opts={"paramstyle": "named"})

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    section = config.get_section(config.config_ini_section, {})
    section["sqlalchemy.url"] = _resolve_database_url()

    connectable = engine_from_config(section, prefix="sqlalchemy.", poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
