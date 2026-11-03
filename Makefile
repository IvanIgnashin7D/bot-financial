.PHONY: help up down restart logs build migrate shell clean compile-deps

help:
	@echo "Доступные команды:"
	@echo "  make up           - Запустить контейнеры в фоне"
	@echo "  make down         - Остановить все контейнеры"
	@echo "  make build        - Пересобрать образы и запустить проект"
	@echo "  make restart      - Перезапустить контейнеры"
	@echo "  make status       - Проверить статус контейнеров"
	@echo "  make logs         - Смотреть логи всех сервисов в реальном времени"
	@echo "  make logs-bot     - Смотреть логи только бота"
	@echo "  make migrate      - Сгенерировать и применить миграцию (make migrate m=\"init\")"
	@echo "  make clean        - Остановить проект и удалить базу данных (volumes)"
	@echo "  make compile-deps - Скомпилировать requirements.txt из requirements.in"

# Запуск и остановка
up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose up --build -d

restart: down build

status:
	docker compose ps

logs:
	docker compose logs -f

logs-bot:
	docker compose logs -f bot

# Миграции Alembic через контейнер
migrate:
	docker compose exec bot alembic revision --autogenerate -m "$(m)"
	docker compose exec bot alembic upgrade head

# Вход в терминал контейнера бота
shell:
	docker compose exec bot /bin/sh

# Управление зависимостями
compile-deps:
	pip-compile .\requirements.in

# Полная очистка с удалением БД
clean:
	docker compose down -v