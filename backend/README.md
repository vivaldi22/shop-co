# SHOP.CO — бэкенд магазина одежды

Учебный бэкенд на FastAPI для макета «E-commerce Website Template (SHOP.CO)».
Что умеет: **каталог** (пагинация + фильтры + сортировка), **регистрация и вход** (возвращают `accessToken`), **корзина** (CRUD).

## Запуск (одна команда)

Нужен **Python 3.10+** (проверить: `python3 --version`).

| Система | Команда (из папки `clothes-shop`) |
|---------|-----------------------------------|
| macOS / Linux | `./run.sh` |
| Windows | `run.bat` |

Скрипт сам создаст виртуальное окружение, поставит зависимости и запустит сервер.
Первый запуск занимает минуту, дальше — секунды.

Когда увидите `Application startup complete` — готово:

- Сервер: <http://localhost:8000>
- **Swagger (документация, где можно нажимать кнопки): <http://localhost:8000/docs>**

Остановить сервер: `Ctrl + C`.

<details>
<summary>Если скрипт не подошёл — запуск руками</summary>

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
</details>

Каталог (24 товара) создаётся сам при первом запуске. База — файл `shop.db`.
Первые 9 товаров — как на странице каталога макета SHOP.CO (порядок, названия, цены и рейтинги совпадают), остальные добавлены, чтобы работали фильтры, сортировка и пагинация.
**Хотите чистую базу** — остановите сервер, удалите `shop.db`, запустите снова.

## Проверка за 1 минуту в Swagger

1. Откройте <http://localhost:8000/docs>.
2. `GET /products` → **Try it out → Execute** — увидите карточки.
3. `POST /auth/register` → вставьте `{"email": "me@test.com", "password": "123456", "name": "Никита"}` → Execute → скопируйте `accessToken` из ответа.
4. Нажмите **Authorize** (справа вверху), вставьте токен → **Authorize**.
5. `POST /cart/items` → `{"productId": 3, "size": "Large", "color": "blue"}` → в ответе будет корзина.

## Какие поля есть в бэке

В JSON все поля пишутся в **camelCase** (`accessToken`, `oldPrice`).

### Пользователь (user)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | number | id пользователя |
| `email` | string | Уникальный (регистр не важен: `A@b.co` = `a@b.co`) |
| `name` | string | Имя |
| `password` | string | **Только при регистрации/входе**, минимум 6 символов. В базе хранится хеш, в ответах пароля нет |

### Карточка товара (product)

| Поле | Тип | Пример | Описание |
|------|-----|--------|----------|
| `id` | number | `3` | |
| `name` | string | `"Black Striped T-shirt"` | Название |
| `image` | string | `"3"` | Номер товара = имя файла `static/images/3.png` (см. «Картинки»; у `id` 10+ файла пока нет) |
| `alt` | string | `"Black Striped T-shirt"` | Текст для `<img alt>` |
| `description` | string | `"Soft cotton t-shirt..."` | Описание |
| `category` | string | `"T-shirts"` | `T-shirts`, `Shirts`, `Shorts`, `Hoodie`, `Jeans` |
| `dressStyle` | string | `"Casual"` | `Casual`, `Formal`, `Party`, `Gym` |
| `price` | number | `120` | Цена **числом** (знак `$` рисует фронтенд) |
| `oldPrice` | number \| null | `150` | Цена до скидки; `null` — скидки нет |
| `discount` | number \| null | `20` | Скидка в % (считает бэк); `null` — скидки нет |
| `rating` | number | `4.5` | От 0 до 5, **числом** (звёзды рисует фронтенд) |
| `reviewsCount` | number | `114` | Число отзывов — по нему сортировка «Most Popular» |
| `colors` | string[] | `["yellow","blue","white"]` | Доступные цвета |
| `sizes` | string[] | `["XX-Small","Small","Large"]` | Доступные размеры |

> **Что изменилось по сравнению с вашими текущими карточками:**
> `price` теперь число, а не `"$120"`; `rating` — число `4.5`, а не картинка `rating4_5`;
> `image` — строка с номером товара, а не импорт файла (картинка лежит в `static/images/{image}.png`). Добавились поля из макета: `oldPrice`, `discount`, `colors`, `sizes`, `dressStyle`, `reviewsCount`.

### Позиция корзины (cartItem)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | number | id **строки корзины** — его используют в `PATCH` и `DELETE` (не путать с `productId`) |
| `productId` | number | id товара |
| `size` | string | Выбранный размер (должен быть в `product.sizes`) |
| `color` | string | Выбранный цвет (должен быть в `product.colors`) |
| `quantity` | number | Количество, 1–99 |
| `lineTotal` | number | `price × quantity` |
| `product` | object | Вся карточка товара (чтобы рисовать корзину без лишних запросов) |

Корзина целиком (`cart`):

| Поле | Описание |
|------|----------|
| `items` | Массив позиций |
| `itemsCount` | Сумма `quantity` — число в значке корзины |
| `subtotal` | Сумма по ценам **до** скидки (Subtotal) |
| `discount` | На сколько снизилась сумма из-за скидок (Discount) |
| `deliveryFee` | Доставка: 15, для пустой корзины 0 (Delivery Fee) |
| `total` | `subtotal − discount + deliveryFee` (Total) |

## Эндпоинты

🔒 — нужен заголовок `Authorization: Bearer <accessToken>`.

| Метод | Адрес | Что делает |
|-------|-------|-----------|
| `POST` | `/auth/register` | Регистрация → `accessToken` |
| `POST` | `/auth/login` | Вход → `accessToken` |
| `GET` | `/auth/me` 🔒 | Кто я (проверить токен) |
| `GET` | `/products` | Карточки: пагинация + фильтры + сортировка |
| `GET` | `/products/{id}` | Один товар |
| `GET` | `/cart` 🔒 | Моя корзина |
| `POST` | `/cart/items` 🔒 | Добавить товар (тот же товар+размер+цвет → вырастет `quantity`) |
| `PATCH` | `/cart/items/{id}` 🔒 | Изменить количество |
| `DELETE` | `/cart/items/{id}` 🔒 | Убрать позицию |
| `DELETE` | `/cart` 🔒 | Очистить корзину |

Каждый метод корзины возвращает **корзину целиком** — просто положите ответ в состояние.

### Регистрация и вход

```jsonc
// POST /auth/register   (вход: POST /auth/login — то же, но без name)
{ "email": "me@test.com", "password": "123456", "name": "Никита" }

// Ответ 201 (для login — 200)
{
  "accessToken": "eyJhbGciOi...",
  "tokenType": "bearer",
  "user": { "id": 1, "email": "me@test.com", "name": "Никита" }
}
```

Токен живёт 24 часа. Методы с 🔒 принимают его в заголовке `Authorization: Bearer <accessToken>`.

### Каталог: `GET /products`

Все параметры необязательные. Списки передаются повторением параметра: `?category=Jeans&category=Shirts`.

| Параметр | По умолчанию | Описание |
|----------|--------------|----------|
| `page` | `1` | Номер страницы (с 1) |
| `limit` | `9` | Карточек на странице (1–100) |
| `search` | — | Поиск по названию |
| `category` | — | `T-shirts`, `Shirts`, `Shorts`, `Hoodie`, `Jeans` (можно несколько) |
| `dressStyle` | — | `Casual`, `Formal`, `Party`, `Gym` (можно несколько) |
| `colors` | — | Подходит любой из выбранных цветов |
| `sizes` | — | Подходит любой из выбранных размеров |
| `minPrice`, `maxPrice` | — | Диапазон цены |
| `sortBy` | `popular` | `popular` (по числу отзывов), `price`, `rating`, `name` |
| `order` | `desc` | `asc` — по возрастанию, `desc` — по убыванию |

Фильтры комбинируются через **И** (категория **и** цвет **и** цена), значения внутри одного фильтра — через **ИЛИ**.

**Допустимые значения для панели фильтров** (пишите в HTML как есть, с учётом регистра):

| Фильтр | Значения |
|--------|----------|
| `category` | `T-shirts`, `Shirts`, `Shorts`, `Hoodie`, `Jeans` |
| `dressStyle` | `Casual`, `Formal`, `Party`, `Gym` |
| `colors` | `green`, `red`, `yellow`, `orange`, `cyan`, `blue`, `purple`, `pink`, `white`, `black` |
| `sizes` | `XX-Small`, `X-Small`, `Small`, `Medium`, `Large`, `X-Large`, `XX-Large`, `3X-Large`, `4X-Large` |
| `minPrice` / `maxPrice` | цены товаров лежат в диапазоне от 60 до 260 |

Ответ:

```jsonc
{
  "items": [ { /* карточка товара */ } ],
  "total": 24,      // всего товаров под фильтры
  "page": 1,
  "limit": 9,
  "pages": 3        // всего страниц
}
```

Примеры (дешёвые джинсы и рубашки, по возрастанию цены, вторая страница):

```
GET /products?category=Jeans&category=Shirts&maxPrice=250&sortBy=price&order=asc&page=2
```

### Ошибки

Ответ с ошибкой всегда такой: `{"detail": "понятный текст"}`.

| Код | Когда |
|-----|-------|
| `401` | Нет токена / токен неверный или просрочен / неверный email или пароль при входе |
| `404` | Нет такого товара или позиции корзины |
| `409` | Email уже занят (регистрация) |
| `422` | Данные не прошли проверку: пароль короче 6 символов, плохой email, `quantity` вне 1–99, размер или цвет недоступны для товара, неизвестное значение `sortBy` |

CORS открыт для любых адресов — фронтенд с `localhost:5173` и т. п. сможет ходить к бэку.

## Картинки

В `image` лежит номер товара (`"1"`, `"2"`, …). Это же имя файла в `static/images/`, поэтому картинка товара доступна по адресу:

```
http://localhost:8000/static/images/{image}.png
```

**Что уже есть.** Файлы `1.png` – `9.png` — первые 9 товаров, как на странице каталога макета. У остальных (`10`–`24`) файлов пока нет: бэк отвечает на них `404`, поэтому на фронте нужна запасная картинка. Какие товары с картинкой, а какие без — в таблице [IMAGES.md](IMAGES.md) (колонка «Картинка»).

Пример для фронтенда:

```tsx
const IMAGE_BASE_URL = "http://localhost:8000/static/images";

<img
  src={`${IMAGE_BASE_URL}/${product.image}.png`}
  alt={product.alt}
  onError={(e) => (e.currentTarget.src = "/placeholder.png")} // файла нет → запасная картинка
/>
```

**Как добавить свою картинку.** Положите `N.png` в `static/images/`, где `N` — значение `image` нужного товара. Перезапускать сервер не нужно. Формат — PNG (с другим расширением придётся менять ссылку на фронтенде).

Таблица `IMAGES.md` собирается из базы. Если поменяли товары в `app/seed.py` или добавили файлы, обновите её: `python -m app.images_table > IMAGES.md`.

## Из чего состоит проект

```
clothes-shop/
├── run.sh / run.bat      запуск одной командой
├── requirements.txt      зависимости
├── static/images/        картинки товаров: 1.png, 2.png, …
├── IMAGES.md             какая картинка к какому товару
└── app/
    ├── main.py           сборка приложения, CORS, роутеры
    ├── models.py         таблицы БД (User, Product, CartItem)
    ├── schemas.py        формат запросов и ответов (камелкейс)
    ├── seed.py           стартовые товары
    ├── images_table.py   собирает IMAGES.md из базы
    ├── constants.py      списки цветов и размеров
    ├── security.py       хеш пароля и JWT
    ├── deps.py           «кто сейчас авторизован»
    └── routers/          auth.py · products.py · cart.py
```

Хотите добавить поле товару? Три места: колонка в `models.py` → поле в `ProductOut` в `schemas.py` → значение в `seed.py` (и удалить `shop.db`).
