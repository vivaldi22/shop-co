"""Таблицы базы данных: пользователи, товары, корзина."""

from sqlalchemy import Float, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def pack_list(items: list[str]) -> str:
    """['red', 'blue'] -> ',red,blue,'. Так списки (цвета, размеры) хранятся в одной колонке,
    а фильтр по ним — обычный LIKE '%,red,%'. Для учебного проекта этого достаточно."""
    return "," + ",".join(items) + ","


def unpack_list(value: str) -> list[str]:
    """',red,blue,' -> ['red', 'blue']"""
    return [item for item in value.split(",") if item]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(255))  # сам пароль не хранится


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    image: Mapped[str] = mapped_column(String(500))
    alt: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50), index=True)  # T-shirts, Shorts, Shirts, Hoodie, Jeans
    dress_style: Mapped[str] = mapped_column(String(50), index=True)  # Casual, Formal, Party, Gym
    price: Mapped[float] = mapped_column(Float, index=True)
    old_price: Mapped[float | None] = mapped_column(Float, default=None)  # цена до скидки
    rating: Mapped[float] = mapped_column(Float, index=True)  # 0..5
    reviews_count: Mapped[int] = mapped_column(default=0)  # по нему считается «Most Popular»
    colors: Mapped[str] = mapped_column(String(200))  # хранится через pack_list
    sizes: Mapped[str] = mapped_column(String(200))  # хранится через pack_list

    @property
    def list_price(self) -> float:
        """Цена до скидки (если скидки нет — обычная цена)."""
        if self.old_price and self.old_price > self.price:
            return self.old_price
        return self.price

    @property
    def discount(self) -> int | None:
        """Скидка в процентах, например 20 (или None, если скидки нет)."""
        if self.list_price > self.price:
            return round((self.list_price - self.price) / self.list_price * 100)
        return None


class CartItem(Base):
    __tablename__ = "cart_items"
    # Один и тот же товар того же размера и цвета у пользователя — одна строка (дальше растёт quantity)
    __table_args__ = (UniqueConstraint("user_id", "product_id", "size", "color"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    size: Mapped[str] = mapped_column(String(20))
    color: Mapped[str] = mapped_column(String(30))
    quantity: Mapped[int] = mapped_column(default=1)

    product: Mapped[Product] = relationship(lazy="joined")

    @property
    def line_total(self) -> float:
        return round(self.product.price * self.quantity, 2)
