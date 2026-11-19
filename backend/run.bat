@echo off
rem Запуск одной командой: run.bat (Windows)
cd /d "%~dp0"

if not exist .venv (
  echo ^>^>^> Создаю виртуальное окружение...
  python -m venv .venv
)

call .venv\Scripts\activate.bat
echo ^>^>^> Ставлю зависимости...
pip install -q -r requirements.txt

echo ^>^>^> Сервер: http://localhost:8000   Документация (Swagger): http://localhost:8000/docs
uvicorn app.main:app --reload --port 8000
