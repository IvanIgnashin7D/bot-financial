FROM python:3.14-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходники, конфигурацию alembic и папки миграций
COPY alembic.ini .
COPY migrations ./migrations
COPY source ./source

CMD ["sh", "-c", "alembic upgrade head && python source/main.py"]