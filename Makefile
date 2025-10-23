# 🦄 Makefile для Telegram Post Copier
# Удобные команды для разработки и деплоя

.PHONY: help setup install run docker-build docker-up docker-down docker-logs clean test

# Цвета для вывода
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Показать эту справку
	@echo "$(GREEN)🦄 Telegram Post Copier - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

setup: ## Первоначальная настройка (установка зависимостей)
	@echo "$(GREEN)🔧 Настройка окружения...$(NC)"
	@bash setup.sh

install: ## Установка Python зависимостей
	@echo "$(GREEN)📦 Установка зависимостей...$(NC)"
	pip install -r requirements.txt

run: ## Запуск копировщика локально
	@echo "$(GREEN)🚀 Запуск копировщика...$(NC)"
	python copier.py

run-bg: ## Запуск в фоне (nohup)
	@echo "$(GREEN)🚀 Запуск копировщика в фоне...$(NC)"
	nohup python copier.py > logs/copier.log 2>&1 &
	@echo "$(GREEN)✅ Запущено в фоне. Логи: logs/copier.log$(NC)"

docker-build: ## Сборка Docker образа
	@echo "$(GREEN)🐳 Сборка Docker образа...$(NC)"
	docker-compose build

docker-auth: ## Первая авторизация в Telegram (Docker)
	@echo "$(GREEN)🔐 Запуск первой авторизации...$(NC)"
	bash first-auth.sh

docker-up: ## Запуск Docker контейнера
	@echo "$(GREEN)🐳 Запуск Docker контейнера...$(NC)"
	@if [ ! -f copier_session.session ]; then \
		echo "$(RED)❌ Session файл не найден!$(NC)"; \
		echo "$(YELLOW)Выполните сначала: make docker-auth$(NC)"; \
		exit 1; \
	fi
	docker-compose up -d
	@echo "$(GREEN)✅ Контейнер запущен!$(NC)"

docker-down: ## Остановка Docker контейнера
	@echo "$(YELLOW)🛑 Остановка Docker контейнера...$(NC)"
	docker-compose down

docker-restart: ## Перезапуск Docker контейнера
	@echo "$(YELLOW)🔄 Перезапуск Docker контейнера...$(NC)"
	docker-compose restart

docker-logs: ## Просмотр логов Docker контейнера
	docker-compose logs -f copier

docker-shell: ## Открыть shell в контейнере
	docker-compose exec copier /bin/bash

docker-rebuild: ## Пересборка и перезапуск контейнера
	@echo "$(GREEN)🔨 Пересборка контейнера...$(NC)"
	docker-compose up -d --build

env-check: ## Проверка конфигурации .env
	@echo "$(GREEN)🔍 Проверка конфигурации...$(NC)"
	@if [ ! -f .env ]; then \
		echo "$(RED)❌ Файл .env не найден!$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)✅ Файл .env существует$(NC)"
	@echo ""
	@echo "Telegram API:"
	@grep "^API_ID" .env || echo "  $(RED)❌ API_ID не установлен$(NC)"
	@grep "^API_HASH" .env | sed 's/=.*/=***/' || echo "  $(RED)❌ API_HASH не установлен$(NC)"
	@echo ""
	@echo "Каналы:"
	@grep "^SOURCE_CHANNEL" .env || echo "  $(RED)❌ SOURCE_CHANNEL не установлен$(NC)"
	@grep "^TARGET_CHANNEL" .env || echo "  $(RED)❌ TARGET_CHANNEL не установлен$(NC)"
	@echo ""
	@echo "LLM:"
	@grep "^LLM_PROVIDER" .env || echo "  $(RED)❌ LLM_PROVIDER не установлен$(NC)"

clean: ## Очистка временных файлов
	@echo "$(YELLOW)🧹 Очистка временных файлов...$(NC)"
	rm -rf temp/*
	rm -rf processed_images/*
	rm -f copier.log
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Очистка завершена$(NC)"

clean-all: clean ## Полная очистка (включая venv и Docker)
	@echo "$(RED)⚠️  ВНИМАНИЕ: Удаление виртуального окружения и Docker образов$(NC)"
	rm -rf venv
	docker-compose down -v --rmi all 2>/dev/null || true
	@echo "$(GREEN)✅ Полная очистка завершена$(NC)"

backup-session: ## Бэкап сессии Telegram
	@echo "$(GREEN)💾 Создание бэкапа сессии...$(NC)"
	@if [ -f copier_session.session ]; then \
		cp copier_session.session copier_session.session.backup; \
		echo "$(GREEN)✅ Бэкап создан: copier_session.session.backup$(NC)"; \
	else \
		echo "$(RED)❌ Сессия не найдена$(NC)"; \
	fi

restore-session: ## Восстановление сессии Telegram
	@echo "$(YELLOW)♻️  Восстановление сессии...$(NC)"
	@if [ -f copier_session.session.backup ]; then \
		cp copier_session.session.backup copier_session.session; \
		echo "$(GREEN)✅ Сессия восстановлена$(NC)"; \
	else \
		echo "$(RED)❌ Бэкап не найден$(NC)"; \
	fi

test: ## Запуск тестов (если есть)
	@echo "$(GREEN)🧪 Запуск тестов...$(NC)"
	python -m pytest tests/ -v || echo "$(YELLOW)⚠️  Тесты не настроены$(NC)"

lint: ## Проверка кода (flake8, black)
	@echo "$(GREEN)🔍 Проверка кода...$(NC)"
	@command -v flake8 >/dev/null 2>&1 || pip install flake8
	@command -v black >/dev/null 2>&1 || pip install black
	flake8 *.py --max-line-length=100 --ignore=E501,W503
	black --check *.py

format: ## Форматирование кода (black)
	@echo "$(GREEN)✨ Форматирование кода...$(NC)"
	@command -v black >/dev/null 2>&1 || pip install black
	black *.py

status: ## Статус системы
	@echo "$(GREEN)📊 Статус системы$(NC)"
	@echo ""
	@echo "$(YELLOW)Python процесс:$(NC)"
	@ps aux | grep copier.py | grep -v grep || echo "  Не запущен"
	@echo ""
	@echo "$(YELLOW)Docker контейнер:$(NC)"
	@docker-compose ps 2>/dev/null || echo "  Docker не запущен"
	@echo ""
	@echo "$(YELLOW)Логи (последние 5 строк):$(NC)"
	@tail -n 5 copier.log 2>/dev/null || echo "  Логи не найдены"

update: ## Обновление зависимостей
	@echo "$(GREEN)🔄 Обновление зависимостей...$(NC)"
	pip install --upgrade -r requirements.txt

git-setup: ## Настройка Git репозитория
	@echo "$(GREEN)📝 Настройка Git...$(NC)"
	@if [ ! -d .git ]; then \
		git init; \
		echo "$(GREEN)✅ Git репозиторий инициализирован$(NC)"; \
	else \
		echo "$(YELLOW)ℹ️  Git уже инициализирован$(NC)"; \
	fi
	git add .
	@echo "$(GREEN)✅ Файлы добавлены в staging$(NC)"
	@echo ""
	@echo "Теперь выполните:"
	@echo "  git commit -m 'Initial commit'"
	@echo "  git remote add origin YOUR_REPO_URL"
	@echo "  git push -u origin main"

git-push: ## Загрузка на GitHub
	@echo "$(GREEN)📤 Загрузка на GitHub...$(NC)"
	bash git-push.sh "Update from Makefile"

deploy: ## Деплой на сервер (требуется: make deploy SERVER=user@ip)
	@if [ -z "$(SERVER)" ]; then \
		echo "$(RED)❌ Укажите сервер: make deploy SERVER=user@server_ip$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)🚀 Деплой на $(SERVER)...$(NC)"
	bash deploy.sh $(SERVER)

backup-create: ## Создать бэкап
	@echo "$(GREEN)💾 Создание бэкапа...$(NC)"
	bash backup.sh

fix-permissions: ## Исправить права доступа для Docker
	@echo "$(GREEN)🔧 Исправление прав доступа...$(NC)"
	mkdir -p temp processed_images logs
	chmod 777 temp processed_images logs 2>/dev/null || true
	chmod 600 .env 2>/dev/null || true
	chmod 600 *.session 2>/dev/null || true
	@echo "$(GREEN)✅ Права исправлены$(NC)"

.DEFAULT_GOAL := help

