.PHONY: help up down restart logs logs-bot build makemigrations migrate status shell clean compile-deps

help:
	@echo "Доступные команды:"
	@echo "  make up              - Запустить контейнеры в фоне"
	@echo "  make down            - Остановить все контейнеры"
	@echo "  make build           - Пересобрать образы и запустить проект"
	@echo "  make restart         - Перезапустить контейнеры"
	@echo "  make status          - Проверить статус контейнеров"
	@echo "  make logs            - Смотреть логи всех сервисов"
	@echo "  make logs-bot        - Смотреть логи только бота"
	@echo "  make makemigrations  - Создать новую миграцию (make makemigrations m=\"название\")"
	@echo "  make migrate         - Применить существующие миграции к БД"
	@echo "  make clean           - Остановить проект и удалить БД (volumes)"
	@echo "  make compile-deps    - Скомпилировать requirements.txt"

# Запуск и сборка
up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose up --build -d

restart: down build

status:
	docker compose ps

# Логи
logs:
	docker compose logs -f

logs-bot:
	docker compose logs -f bot

# Создание нового файла миграции (только при изменении models.py)
makemigrations:
	docker compose exec bot alembic revision --autogenerate -m "$(m)"

# Принудительный накат миграций вручную
migrate:
	docker compose exec bot alembic upgrade head

# Вход в контейнер
shell:
	docker compose exec bot /bin/sh

compile-deps:
	pip-compile .\requirements.in

clean:
	docker compose down -v