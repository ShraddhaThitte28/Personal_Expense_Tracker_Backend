from logging.config import fileConfig

from alembic import context

from app.database import Base, engine
from app import models  # noqa: F401  # register User and Expense on Base.metadata

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    raise RuntimeError(
        "Offline Alembic migrations are disabled. Use online mode so the "
        "existing .env configuration is reused without putting a database URL "
        "in alembic.ini."
    )


def run_migrations_online() -> None:
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
