"""Каталог: список карточек с пагинацией, фильтрацией и сортировкой."""

from math import ceil
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Product
from ..schemas import ProductOut, ProductPage

router = APIRouter(prefix="/products", tags=["Товары"])

SORT_COLUMNS = {
    "popular": Product.reviews_count,  # «Most Popular» из макета
    "price": Product.price,
    "rating": Product.rating,
    "name": Product.name,
}


@router.get("", response_model=ProductPage)
def list_products(
    # пагинация
    page: int = Query(1, ge=1, description="Номер страницы, с 1"),
    limit: int = Query(9, ge=1, le=100, description="Сколько карточек на странице"),
    # фильтры (списки передаются повторением параметра: ?category=Jeans&category=Shirts)
    search: str | None = Query(None, description="Поиск по названию"),
    category: list[str] | None = Query(None, description="T-shirts, Shorts, Shirts, Hoodie, Jeans"),
    colors: list[str] | None = Query(None, description="Подходит любой из выбранных цветов"),
    sizes: list[str] | None = Query(None, description="Подходит любой из выбранных размеров"),
    dress_style: list[str] | None = Query(None, alias="dressStyle", description="Casual, Formal, Party, Gym"),
    min_price: float | None = Query(None, ge=0, alias="minPrice"),
    max_price: float | None = Query(None, ge=0, alias="maxPrice"),
    # сортировка
    sort_by: Literal["popular", "price", "rating", "name"] = Query("popular", alias="sortBy"),
    order: Literal["asc", "desc"] = Query("desc"),
    db: Session = Depends(get_db),
):
    stmt = select(Product)

    if search:
        stmt = stmt.where(Product.name.icontains(search, autoescape=True))
    if category:
        stmt = stmt.where(Product.category.in_(category))
    if dress_style:
        stmt = stmt.where(Product.dress_style.in_(dress_style))
    if colors:
        stmt = stmt.where(or_(*[Product.colors.contains(f",{c},", autoescape=True) for c in colors]))
    if sizes:
        stmt = stmt.where(or_(*[Product.sizes.contains(f",{s},", autoescape=True) for s in sizes]))
    if min_price is not None:
        stmt = stmt.where(Product.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(Product.price <= max_price)

    # total считаем по тем же фильтрам, но без пагинации
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0

    column = SORT_COLUMNS[sort_by]
    primary_order = column.asc() if order == "asc" else column.desc()
    # Product.id — второй ключ, чтобы порядок был стабильным и карточки не «прыгали» между страницами
    items = db.scalars(
        stmt.order_by(primary_order, Product.id).offset((page - 1) * limit).limit(limit)
    ).all()

    return ProductPage(
        items=[ProductOut.model_validate(p) for p in items],
        total=total,
        page=page,
        limit=limit,
        pages=ceil(total / limit),
    )


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(404, "Товар не найден")
    return product
