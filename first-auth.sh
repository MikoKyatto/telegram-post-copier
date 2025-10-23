#!/bin/bash

# 🔐 Скрипт для первой авторизации в Telegram
# Использование: bash first-auth.sh

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║  🔐 ПЕРВАЯ АВТОРИЗАЦИЯ В TELEGRAM                          ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Проверка .env файла
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден!"
    echo "Создайте его: cp env.example .env"
    echo "И заполните необходимые поля"
    exit 1
fi

echo "✅ .env файл найден"
echo ""

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен"
    echo "Установите Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен"
    echo "Установите Docker Compose"
    exit 1
fi

echo "✅ Docker и Docker Compose установлены"
echo ""

# Создание необходимых директорий
echo "📁 Создание директорий..."
mkdir -p temp processed_images logs
chmod 777 temp processed_images logs 2>/dev/null || true
echo "✅ Директории созданы"
echo ""

# Сборка образа
echo "🐳 Сборка Docker образа..."
docker-compose build
echo "✅ Образ собран"
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║  📱 ВАЖНО: Приготовьте телефон с Telegram!                 ║"
echo "║                                                            ║"
echo "║  Сейчас бот попросит:                                      ║"
echo "║  1. Номер телефона (с кодом страны, например +7...)       ║"
echo "║  2. Код из Telegram (придет в приложение)                 ║"
echo "║                                                            ║"
echo "║  После успешной авторизации:                               ║"
echo "║  • Файл copier_session.session будет создан                ║"
echo "║  • Повторная авторизация не потребуется                    ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

read -p "Готовы продолжить? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Отменено"
    exit 0
fi

echo ""
echo "🚀 Запуск авторизации..."
echo "═══════════════════════════════════════════════════════════"
echo ""

# Запуск в интерактивном режиме для авторизации
docker-compose run --rm copier

echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""

# Проверка создания session файла
if [ -f "copier_session.session" ]; then
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║  ✅ АВТОРИЗАЦИЯ УСПЕШНА!                                   ║"
    echo "║                                                            ║"
    echo "║  Session файл создан: copier_session.session              ║"
    echo "║                                                            ║"
    echo "║  🔒 ВАЖНО: Сохраните бэкап session файла:                  ║"
    echo "║     bash backup.sh                                         ║"
    echo "║                                                            ║"
    echo "║  🚀 Теперь можно запустить бота:                           ║"
    echo "║     docker-compose up -d                                   ║"
    echo "║                                                            ║"
    echo "║  📋 Проверить логи:                                        ║"
    echo "║     docker-compose logs -f                                 ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    
    # Установка прав доступа
    chmod 600 copier_session.session 2>/dev/null || true
    
else
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║  ⚠️  Session файл не создан                                ║"
    echo "║                                                            ║"
    echo "║  Возможные причины:                                        ║"
    echo "║  • Авторизация была прервана (Ctrl+C)                      ║"
    echo "║  • Неверный код из Telegram                                ║"
    echo "║  • Ошибка в .env конфигурации                              ║"
    echo "║                                                            ║"
    echo "║  Попробуйте снова: bash first-auth.sh                     ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
fi

