#!/bin/bash

# 🚀 Быстрый запуск Telegram Post Copier

set -e

echo "🦄 Запуск Telegram Post Copier..."
echo ""

# Проверка .env
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден!"
    echo "Создайте его из env.example:"
    echo "  cp env.example .env"
    echo "  nano .env"
    exit 1
fi

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo "❌ Виртуальное окружение не найдено!"
    echo "Запустите setup.sh сначала:"
    echo "  bash setup.sh"
    exit 1
fi

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Запуск
echo "✅ Запуск копировщика..."
echo ""
python copier.py

