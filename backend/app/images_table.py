"""Таблица «номер картинки → товар» в Markdown.

Запуск из папки clothes-shop:  python -m app.images_table > IMAGES.md
Нужна, чтобы понимать, какую картинку под каким номером положить в static/images/.
"""

from sqlalchemy import select

from .config import STATIC_DIR
from .database import SessionLocal
from .models import Product


def main() -> None:
    with SessionLocal() as db:
        products = db.scalars(select(Product).order_by(Product.id)).all()

    print("# Какая картинка к какому товару\n")
    print("Номер в колонке `image` = имя файла в `static/images/` (формат PNG). Колонка «Картинка» показывает, лежит ли уже файл.\n")
    print("| image | Картинка | Название | Категория | Стиль |")
    print("|------:|----------|----------|-----------|-------|")
    for product in products:
        name = product.name.replace("|", "\\|")  # символ «|» в названии ломает колонки таблицы
        files = sorted(path.name for path in (STATIC_DIR / "images").glob(f"{product.image}.*"))
        picture = f"✅ {files[0]}" if files else "—"
        print(f"| {product.image} | {picture} | {name} | {product.category} | {product.dress_style} |")


if __name__ == "__main__":
    main()
