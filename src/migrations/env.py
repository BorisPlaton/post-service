import asyncio
from logging.config import fileConfig

from punq import Container
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from settings.config.database import DatabaseSettings
from settings.module import SettingsModule
from shared.database.sqlalchemy.base import Base
from shared.module_setup.bootstrap import ModulesConfig
from domain.user.model import *
from domain.post.model import *


module_bootstrap = ModulesConfig(
    container=Container(),
    modules=(
        SettingsModule(),
    ),
)
module_bootstrap.setup()

config = context.config
config.set_main_option(
    'sqlalchemy.url',
    module_bootstrap.container.resolve(DatabaseSettings).db_url,
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
