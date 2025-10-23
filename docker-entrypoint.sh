#!/bin/bash
set -e

# 🚀 Docker entrypoint для Telegram Post Copier
# Подготовка окружения перед запуском

echo "🔧 Подготовка окружения..."

# Создание необходимых директорий
mkdir -p /app/temp /app/processed_images /app/logs

# Установка прав доступа на рабочую директорию
# Если текущий пользователь не root, значит мы appuser
if [ "$(id -u)" != "0" ]; then
    # Пытаемся установить права на /app (через volume)
    # Это нужно для создания session файлов
    touch /app/.write_test 2>/dev/null && rm /app/.write_test 2>/dev/null || {
        echo "⚠️  Нет прав на запись в /app"
        echo "На хосте выполните: sudo chown -R 1000:1000 /opt/telegram-post-copier"
    }
fi

# Установка прав доступа для session файлов
if [ -f "/app/copier_session.session" ]; then
    chmod 600 /app/copier_session.session 2>/dev/null || true
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

