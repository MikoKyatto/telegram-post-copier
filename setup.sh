#!/bin/bash

# 🚀 Скрипт быстрой установки Telegram Post Copier
# Автоматическая настройка окружения

set -e

echo "=============================================="
echo "🦄 Telegram Post Copier - Quick Setup"
echo "=============================================="
echo ""

# Проверка операционной системы
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "🖥️  Обнаружена ОС: $MACHINE"
echo ""

# Функция для проверки команды
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Проверка Python
echo "🐍 Проверка Python..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✅ Python установлен: $PYTHON_VERSION"
else
    echo "❌ Python 3 не найден!"
    echo "Установите Python 3.10+: https://www.python.org/downloads/"
    exit 1
fi

# Проверка pip
echo ""
echo "📦 Проверка pip..."
if command_exists pip3; then
    echo "✅ pip установлен"
else
    echo "❌ pip не найден! Установите: python3 -m ensurepip"
    exit 1
fi

# Проверка Docker
echo ""
echo "🐳 Проверка Docker..."
if command_exists docker; then
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | tr -d ',')
    echo "✅ Docker установлен: $DOCKER_VERSION"
    DOCKER_INSTALLED=true
else
    echo "⚠️  Docker не установлен"
    echo "Скачайте с https://www.docker.com/products/docker-desktop"
    DOCKER_INSTALLED=false
fi

# Проверка Docker Compose
if [ "$DOCKER_INSTALLED" = true ]; then
    if command_exists docker-compose; then
        echo "✅ Docker Compose установлен"
    else
        echo "⚠️  Docker Compose не установлен"
    fi
fi

# Проверка Tesseract
echo ""
echo "🔍 Проверка Tesseract OCR..."
if command_exists tesseract; then
    TESSERACT_VERSION=$(tesseract --version | head -n1)
    echo "✅ Tesseract установлен: $TESSERACT_VERSION"
else
    echo "⚠️  Tesseract не установлен"
    if [ "$MACHINE" = "Linux" ]; then
        echo "Установите: sudo apt install tesseract-ocr tesseract-ocr-rus"
    elif [ "$MACHINE" = "Mac" ]; then
        echo "Установите: brew install tesseract tesseract-lang"
    fi
fi

# Создание виртуального окружения
echo ""
echo "🔧 Настройка виртуального окружения..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано"
else
    echo "ℹ️  Виртуальное окружение уже существует"
fi

# Активация и установка зависимостей
echo ""
echo "📚 Установка зависимостей..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Зависимости установлены"

# Создание .env из шаблона
echo ""
if [ ! -f ".env" ]; then
    echo "📝 Создание .env файла..."
    cp env.example .env
    echo "✅ .env файл создан"
    echo ""
    echo "⚠️  ВАЖНО: Отредактируйте .env файл и добавьте ваши API ключи!"
    echo "   nano .env"
else
    echo "ℹ️  .env файл уже существует"
fi

# Создание необходимых директорий
echo ""
echo "📁 Создание директорий..."
mkdir -p temp processed_images logs
echo "✅ Директории созданы"

# Установка прав доступа
echo ""
echo "🔒 Настройка прав доступа..."
chmod 600 .env 2>/dev/null || true
chmod 600 *.session 2>/dev/null || true
echo "✅ Права доступа настроены"

echo ""
echo "=============================================="
echo "✅ Установка завершена!"
echo "=============================================="
echo ""
echo "📋 Следующие шаги:"
echo ""
echo "1. Отредактируйте .env файл:"
echo "   nano .env"
echo ""
echo "2. Добавьте ваши ключи:"
echo "   - API_ID и API_HASH (от my.telegram.org)"
echo "   - LLM API ключ (DeepSeek/OpenAI/xAI)"
echo "   - Настройте каналы"
echo ""
echo "3. Запустите бота:"
echo "   source venv/bin/activate"
echo "   python copier.py"
echo ""
echo "Или используйте Docker:"
echo "   docker-compose up -d"
echo ""
echo "📖 Полная документация в README.md"
echo ""
echo "🦄 Удачи в автоматизации контента!"

