#!/usr/bin/env bash
# Запуск одной командой: ./run.sh
# Создаёт виртуальное окружение, ставит зависимости и стартует сервер.
set -e
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  echo ">>> Создаю виртуальное окружение (.venv)..."
  python3 -m venv .venv
fi

source .venv/bin/activate
echo ">>> Ставлю зависимости..."
pip install -q -r requirements.txt

echo ">>> Сервер: http://localhost:8000   Документация (Swagger): http://localhost:8000/docs"
uvicorn app.main:app --reload --port 8000
