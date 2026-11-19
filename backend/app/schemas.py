"""Схемы запросов и ответов (то, что видит фронтенд).

В JSON все поля в camelCase (accessToken, oldPrice), в Python-коде — snake_case.
Перевод между ними делает alias_generator=to_camel.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from pydantic.alias_generators import to_camel

from .models import unpack_list


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)


# ---------- Авторизация ----------


class RegisterIn(CamelModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72, description="Минимум 6 символов")
    name: str = Field(min_length=1, max_length=100)


class LoginIn(CamelModel):
    email: EmailStr
    password: str


class UserOut(CamelModel):
    id: int
    email: str
    name: str


class AuthOut(CamelModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Товары ----------


class ProductOut(CamelModel):
    id: int
    name: str
    image: str
    alt: str
    description: str
    category: str
    dress_style: str
    price: float
    old_price: float | None
    discount: int | None = Field(description="Скидка в %, null если скидки нет")
    rating: float
    reviews_count: int
    colors: list[str]
    sizes: list[str]

    @field_validator("colors", "sizes", mode="before")
    @classmethod
    def split_list(cls, value):
        # В БД список лежит строкой ',red,blue,', наружу отдаём настоящий массив
        return unpack_list(value) if isinstance(value, str) else value


class ProductPage(CamelModel):
    items: list[ProductOut]
    total: int = Field(description="Сколько товаров всего подошло под фильтры")
    page: int
    limit: int
    pages: int = Field(description="Сколько всего страниц")


# ---------- Корзина ----------


class CartItemCreate(CamelModel):
    product_id: int
    size: str
    color: str
    quantity: int = Field(default=1, ge=1, le=99)


class CartItemUpdate(CamelModel):
    quantity: int = Field(ge=1, le=99, description="Чтобы убрать товар — DELETE /cart/items/{id}")


class CartItemOut(CamelModel):
    id: int = Field(description="id строки корзины (не путать с productId)")
    product_id: int
    size: str
    color: str
    quantity: int
    line_total: float = Field(description="price * quantity")
    product: ProductOut


class CartOut(CamelModel):
    items: list[CartItemOut]
    items_count: int = Field(description="Сумма quantity по всем строкам (число в значке корзины)")
    subtotal: float = Field(description="Сумма по ценам до скидки")
    discount: float = Field(description="На сколько уменьшилась сумма из-за скидок на товары")
    delivery_fee: float
    total: float = Field(description="subtotal - discount + deliveryFee")
