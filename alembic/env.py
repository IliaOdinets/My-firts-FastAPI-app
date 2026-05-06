# alembic/env.py
import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# 🔑 1. Добавляем корень проекта в sys.path, чтобы работали импорты
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# 🔑 2. Импортируем Base и ВСЕ модели. Без этого Alembic не увидит таблицы!
from db.base import Base
from models.note import Note  # pyright: ignore[reportUnusedImport] # Явный импорт регистрирует модель в Base.metadata
from models.user import User

# Alembic Config object
config = context.config

# Настройка логирования (берёт из alembic.ini)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 🔑 3. Передаём метаданные моделей в Alembic
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в offline-режиме (без подключения к БД)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection): # type: ignore
    """Внутренняя функция для применения миграций к синхронному соединению."""
    context.configure(connection=connection, target_metadata=target_metadata) # type: ignore
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Асинхронный запуск миграций."""
    # Пытаемся взять URL из pydantic-settings (.env)
    try:
        from core.config import settings
        db_url = settings.DATABASE_URL
    except Exception:
        # Фоллбэк на alembic.ini, если core.config недоступен
        db_url = config.get_main_option("sqlalchemy.url")

    connectable = async_engine_from_config(
        {"sqlalchemy.url": db_url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # Для CLI-миграций пул не нужен
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations) # type: ignore

    await connectable.dispose()


def run_migrations_online() -> None:
    """Запуск миграций в online-режиме (с подключением к БД)."""
    asyncio.run(run_async_migrations())


# === ТОЧКА ВХОДА ===
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()