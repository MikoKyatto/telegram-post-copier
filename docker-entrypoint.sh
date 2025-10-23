#!/bin/bash
set -e

# 🚀 Docker entrypoint для Telegram Post Copier
# Подготовка окружения перед запуском

echo "🔧 Подготовка окружения..."

# Создание необходимых директорий
mkdir -p /app/temp /app/processed_images /app/logs

# Установка прав доступа для session файлов
if [ -f "/app/copier_session.session" ]; then
    chmod 600 /app/copier_session.session
    echo "✅ Session файл найден"
fi

# Проверка .env файла
if [ ! -f "/app/.env" ]; then
    echo "⚠️  WARNING: .env файл не найден!"
    echo "Создайте .env из env.example"
    if [ -f "/app/env.example" ]; then
        echo "Можно скопировать: cp env.example .env"
    fi
fi

echo "✅ Окружение подготовлено"
echo "🚀 Запуск Telegram Post Copier..."
echo ""

# Запуск основного приложения
exec python -u copier.py

