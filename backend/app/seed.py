"""Стартовые товары. Заполняются один раз, когда таблица products пустая.

В image лежит просто номер товара ("1", "2", ...): бэк картинки не отдаёт,
путь к файлу студенты подставляют у себя на фронтенде, например f"/img/{image}.png".
"""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .constants import COLORS, SIZES
from .models import Product, pack_list

DESCRIPTIONS = {
    "T-shirts": "Soft cotton t-shirt with a regular fit. Comfortable for every day.",
    "Shirts": "Classic shirt made of breathable fabric. Looks great on its own or under a jacket.",
    "Hoodie": "Warm hoodie with a soft lining and a relaxed fit.",
    "Shorts": "Lightweight shorts with a comfortable waistband for warm days.",
    "Jeans": "Durable denim with a stretch for a comfortable fit all day long.",
}

# Описания конкретных товаров (из моковых карточек фронтенда). У остальных — общее описание категории.
PRODUCT_DESCRIPTIONS = {
    "T-shirt with Tape Details": (
        "A black t-shirt with tape details on the chest. Soft cotton and a regular fit for every day."
    ),
    "Skinny Fit Jeans": "Slim jeans in a light wash. Stretch denim that moves with you and keeps its shape.",
    "Checkered Shirt": "A checkered shirt in soft flannel. Wear it buttoned up or open over a t-shirt.",
    "Sleeve Striped T-shirt": "A bold striped t-shirt with contrast sleeves. Cotton jersey with a regular fit.",
    "Vertical Striped Shirt": "A shirt with thin vertical stripes. Light, breathable fabric for warm days.",
}

# Размеры по категориям (чтобы данные выглядели правдоподобно)
SIZES_BY_CATEGORY = {
    "T-shirts": SIZES[:7],
    "Shirts": SIZES[1:7],
    "Hoodie": SIZES[2:8],
    "Shorts": SIZES[1:8],
    "Jeans": SIZES[2:9],
}

# (название, категория, стиль, цена, цена до скидки, рейтинг)
PRODUCTS = [
    ("Gradient Graphic T-shirt", "T-shirts", "Casual", 145, None, 3.5),
    ("Polo with Tipping Details", "T-shirts", "Casual", 180, None, 4.5),
    ("Black Striped T-shirt", "T-shirts", "Casual", 120, 150, 5.0),
    ("Skinny Fit Jeans", "Jeans", "Casual", 240, 260, 3.5),
    ("Checkered Shirt", "Shirts", "Formal", 180, None, 4.5),
    ("Sleeve Striped T-shirt", "T-shirts", "Casual", 130, 160, 4.5),
    ("Vertical Striped Shirt", "Shirts", "Formal", 212, 232, 5.0),
    ("Courage Graphic T-shirt", "T-shirts", "Casual", 145, None, 4.0),
    ("Loose Fit Bermuda Shorts", "Shorts", "Casual", 80, None, 3.0),
    ("Polo with Contrast Trims", "T-shirts", "Casual", 212, 242, 4.0),
    ("T-shirt with Tape Details", "T-shirts", "Casual", 120, None, 4.5),
    ("One Life Graphic T-shirt", "T-shirts", "Casual", 260, 300, 4.5),
    ("Faded Skinny Jeans", "Jeans", "Casual", 210, None, 4.5),
    ("Classic Oxford Shirt", "Shirts", "Formal", 150, None, 4.0),
    ("Slim Fit Dress Shirt", "Shirts", "Formal", 175, None, 4.5),
    ("Relaxed Hoodie", "Hoodie", "Casual", 195, 230, 4.5),
    ("Zip-Up Hoodie", "Hoodie", "Gym", 160, None, 4.0),
    ("Oversized Graphic Hoodie", "Hoodie", "Party", 220, None, 3.5),
    ("Athletic Training Shorts", "Shorts", "Gym", 60, None, 4.0),
    ("Cargo Shorts", "Shorts", "Casual", 95, 110, 3.5),
    ("Denim Shorts", "Shorts", "Party", 85, None, 4.0),
    ("Straight Leg Jeans", "Jeans", "Formal", 230, None, 4.0),
    ("Gym Performance T-shirt", "T-shirts", "Gym", 70, None, 4.5),
    ("Party Sequin Shirt", "Shirts", "Party", 190, 220, 3.5),
]


def seed(db: Session) -> None:
    if db.scalar(select(func.count(Product.id))):
        return  # уже заполнено

    for index, (name, category, style, price, old_price, rating) in enumerate(PRODUCTS):
        colors = [COLORS[(index + step * 3) % len(COLORS)] for step in range(3)]
        db.add(
            Product(
                name=name,
                image=str(index + 1),  # номер товара: "1", "2", ... (совпадает с id на свежей базе)
                alt=name,
                description=PRODUCT_DESCRIPTIONS.get(name, DESCRIPTIONS[category]),
                category=category,
                dress_style=style,
                price=price,
                old_price=old_price,
                rating=rating,
                reviews_count=40 + (index * 37) % 400,  # разные числа, чтобы сортировка по популярности была заметна
                colors=pack_list(colors),
                sizes=pack_list(SIZES_BY_CATEGORY[category]),
            )
        )
    db.commit()
