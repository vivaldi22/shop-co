"""Корзина (CRUD). Все методы требуют токен. Каждый метод возвращает корзину целиком —
фронтенду достаточно подставить ответ в состояние."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import CartItem, Product, User, unpack_list
from ..schemas import CartItemCreate, CartItemOut, CartItemUpdate, CartOut

router = APIRouter(prefix="/cart", tags=["Корзина"])

DELIVERY_FEE = 15.0  # как в макете: Delivery Fee $15 (для пустой корзины — 0)
MAX_QUANTITY = 99


def get_cart_items(db: Session, user: User) -> list[CartItem]:
    return list(db.scalars(select(CartItem).where(CartItem.user_id == user.id).order_by(CartItem.id)).all())


def build_cart(items: list[CartItem]) -> CartOut:
    subtotal = sum(i.product.list_price * i.quantity for i in items)  # цены до скидки
    pay_for_goods = sum(i.product.price * i.quantity for i in items)  # реальные цены
    discount = subtotal - pay_for_goods
    delivery_fee = DELIVERY_FEE if items else 0.0
    return CartOut(
        items=[CartItemOut.model_validate(i) for i in items],
        items_count=sum(i.quantity for i in items),
        subtotal=round(subtotal, 2),
        discount=round(discount, 2),
        delivery_fee=delivery_fee,
        total=round(pay_for_goods + delivery_fee, 2),
    )


def get_own_item(db: Session, user: User, item_id: int) -> CartItem:
    # Ищем строку только среди корзины текущего пользователя — чужую трогать нельзя
    item = db.scalar(select(CartItem).where(CartItem.id == item_id, CartItem.user_id == user.id))
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Позиция корзины не найдена")
    return item


@router.get("", response_model=CartOut)
def get_cart(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """READ: моя корзина с итогами."""
    return build_cart(get_cart_items(db, user))


@router.post("/items", response_model=CartOut, status_code=status.HTTP_201_CREATED)
def add_item(data: CartItemCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """CREATE: добавить товар. Если такой же (товар + размер + цвет) уже есть — увеличится quantity."""
    product = db.get(Product, data.product_id)
    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Товар не найден")
    if data.size not in unpack_list(product.sizes):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Размер {data.size} недоступен для этого товара")
    if data.color not in unpack_list(product.colors):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Цвет {data.color} недоступен для этого товара")

    item = db.scalar(
        select(CartItem).where(
            CartItem.user_id == user.id,
            CartItem.product_id == product.id,
            CartItem.size == data.size,
            CartItem.color == data.color,
        )
    )
    if item:
        item.quantity = min(item.quantity + data.quantity, MAX_QUANTITY)
    else:
        db.add(CartItem(user_id=user.id, product_id=product.id, size=data.size, color=data.color, quantity=data.quantity))
    db.commit()
    return build_cart(get_cart_items(db, user))


@router.patch("/items/{item_id}", response_model=CartOut)
def update_item(
    item_id: int, data: CartItemUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """UPDATE: поменять количество (кнопки «−» и «+»)."""
    item = get_own_item(db, user, item_id)
    item.quantity = data.quantity
    db.commit()
    return build_cart(get_cart_items(db, user))


@router.delete("/items/{item_id}", response_model=CartOut)
def delete_item(item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """DELETE: убрать позицию (иконка корзины/крестик)."""
    db.delete(get_own_item(db, user, item_id))
    db.commit()
    return build_cart(get_cart_items(db, user))


@router.delete("", response_model=CartOut)
def clear_cart(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Очистить корзину целиком."""
    for item in get_cart_items(db, user):
        db.delete(item)
    db.commit()
    return build_cart([])
