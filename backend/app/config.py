"""Настройки приложения. Для учебного стенда хватает значений по умолчанию."""

import os
from pathlib import Path

# Корень проекта (папка clothes-shop)
BASE_DIR = Path(__file__).resolve().parent.parent

# Файл базы данных SQLite — создаётся сам при первом запуске.
# Хотите чистую базу — удалите shop.db и перезапустите сервер.
DATABASE_URL = f"sqlite:///{BASE_DIR / 'shop.db'}"

# Ключ подписи токенов. В настоящем проекте его берут из переменной окружения.
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me-in-production-0123456789")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

STATIC_DIR = BASE_DIR / "static"
