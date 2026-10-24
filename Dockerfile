FROM python:3.14-slim

WORKDIR /app

# Сначала копируем только зависимости (для кэширования слоев Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем ВСЁ остальное (включая alembic и .env, если он нужен внутри)
COPY . .


# Запускаем сервер, слушая все интерфейсы
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]