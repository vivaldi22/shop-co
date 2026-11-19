"""Хеширование паролей и JWT-токены."""

import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone

import jwt

from .config import ACCESS_TOKEN_EXPIRE_HOURS, JWT_ALGORITHM, SECRET_KEY


def hash_password(password: str) -> str:
    """Пароль никогда не хранят как есть — только хеш с солью (scrypt из стандартной библиотеки)."""
    salt = os.urandom(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return f"{salt.hex()}${digest.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    salt_hex, digest_hex = stored_hash.split("$")
    digest = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt_hex), n=2**14, r=8, p=1)
    return hmac.compare_digest(digest.hex(), digest_hex)


def create_access_token(user_id: int) -> str:
    """Создаёт JWT: внутри id пользователя (sub) и время жизни (exp)."""
    expires = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    return jwt.encode({"sub": str(user_id), "exp": expires}, SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> int:
    """Возвращает id пользователя из токена. Бросает jwt.PyJWTError, если токен плохой или просрочен."""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return int(payload["sub"])
