"""Подключение к базе данных (SQLite через SQLAlchemy)."""

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import DATABASE_URL

# check_same_thread=False нужен SQLite, потому что FastAPI работает в нескольких потоках
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    """Базовый класс для всех таблиц."""


def get_db() -> Iterator[Session]:
    """Зависимость FastAPI: выдаёт сессию БД на время запроса и закрывает её."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
