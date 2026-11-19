"""Точка входа. Запуск: uvicorn app.main:app --reload --port 8000"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .config import STATIC_DIR
from .database import Base, SessionLocal, engine
from .routers import auth, cart, products
from .seed import seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте: создаём таблицы (если их нет) и наполняем каталог (если он пустой)
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        seed(db)
    yield


app = FastAPI(
    title="SHOP.CO — бэкенд магазина одежды",
    description=(
        "Учебный бэкенд: каталог (пагинация + фильтры + сортировка), регистрация/вход с accessToken, корзина.\n\n"
        "**Как проверить корзину в Swagger:** выполните `POST /auth/register`, скопируйте `accessToken`, "
        "нажмите кнопку **Authorize** справа вверху и вставьте токен."
    ),
    lifespan=lifespan,
)

# CORS: разрешаем запросы с любого адреса, чтобы фронтенд (например, localhost:5173) мог ходить к бэку
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")
