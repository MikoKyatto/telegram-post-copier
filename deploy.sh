#!/bin/bash

# 🚀 Скрипт деплоя на сервер
# Использование: bash deploy.sh user@server_ip

set -e

if [ -z "$1" ]; then
    echo "❌ Ошибка: укажите сервер"
    echo "Использование: bash deploy.sh user@server_ip"
    exit 1
fi

SERVER=$1
PROJECT_NAME="telegram-post-copier"
REMOTE_DIR="/opt/$PROJECT_NAME"

echo "🚀 Деплой Telegram Post Copier на сервер $SERVER"
echo "================================================"

# Проверка SSH подключения
echo ""
echo "🔐 Проверка SSH подключения..."
ssh -o ConnectTimeout=5 $SERVER "echo '✅ SSH подключение работает'" || {
    echo "❌ Ошибка подключения к серверу"
    exit 1
}

# Установка Docker на сервере (если нет)
echo ""
echo "🐳 Проверка Docker на сервере..."
ssh $SERVER "command -v docker >/dev/null 2>&1" || {
    echo "📦 Установка Docker..."
    ssh $SERVER "curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo usermod -aG docker \$USER"
    echo "✅ Docker установлен"
}

# Установка Docker Compose (если нет)
echo ""
echo "🐳 Проверка Docker Compose на сервере..."
ssh $SERVER "command -v docker-compose >/dev/null 2>&1" || {
    echo "📦 Установка Docker Compose..."
    ssh $SERVER "sudo apt-get update && sudo apt-get install -y docker-compose"
    echo "✅ Docker Compose установлен"
}

# Создание директории на сервере
echo ""
echo "📁 Создание директории на сервере..."
ssh $SERVER "sudo mkdir -p $REMOTE_DIR && sudo chown -R \$USER:\$USER $REMOTE_DIR"

# Копирование файлов
echo ""
echo "📤 Копирование файлов на сервер..."
rsync -avz --progress \
    --exclude '.git' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude 'venv' \
    --exclude 'temp/*' \
    --exclude 'processed_images/*' \
    --exclude '*.log' \
    --exclude '.env' \
    ./ $SERVER:$REMOTE_DIR/

echo "✅ Файлы скопированы"

# Копирование .env (если есть)
if [ -f ".env" ]; then
    echo ""
    echo "🔐 Копирование .env файла..."
    scp .env $SERVER:$REMOTE_DIR/.env
    echo "✅ .env скопирован"
else
    echo ""
    echo "⚠️  Файл .env не найден локально"
    echo "Не забудьте создать .env на сервере!"
fi

# Копирование session файла (если есть)
if [ -f "copier_session.session" ]; then
    echo ""
    echo "🔑 Копирование session файла..."
    scp copier_session.session* $SERVER:$REMOTE_DIR/ 2>/dev/null || true
    echo "✅ Session файл скопирован"
fi

# Установка прав доступа
echo ""
echo "🔒 Установка прав доступа..."
ssh $SERVER "cd $REMOTE_DIR && chmod 600 .env 2>/dev/null || true && chmod 600 *.session 2>/dev/null || true"

# Установка прав на директории
echo ""
echo "🔒 Установка прав на директории..."
ssh $SERVER "cd $REMOTE_DIR && mkdir -p temp processed_images logs && chmod 777 temp processed_images logs"

# Сборка и запуск Docker
echo ""
echo "🐳 Сборка Docker образа на сервере..."
ssh $SERVER "cd $REMOTE_DIR && docker-compose build"

# Проверка наличия session файла
echo ""
if ssh $SERVER "test -f $REMOTE_DIR/copier_session.session"; then
    echo "✅ Session файл найден, запуск контейнера..."
    ssh $SERVER "cd $REMOTE_DIR && docker-compose up -d"
else
    echo "⚠️  Session файл не найден!"
    echo ""
    echo "📱 Необходима первая авторизация в Telegram"
    echo "Выполните на сервере:"
    echo "  ssh $SERVER"
    echo "  cd $REMOTE_DIR"
    echo "  bash first-auth.sh"
    echo ""
    echo "После авторизации запустите:"
    echo "  docker-compose up -d"
    echo ""
    exit 0
fi

# Проверка статуса
echo ""
echo "📊 Проверка статуса..."
sleep 3
ssh $SERVER "cd $REMOTE_DIR && docker-compose ps"

# Показываем логи
echo ""
echo "📋 Последние логи (Ctrl+C для выхода):"
echo "─────────────────────────────────────────"
ssh $SERVER "cd $REMOTE_DIR && docker-compose logs --tail=50 -f" || true

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║  ✅ ДЕПЛОЙ ЗАВЕРШЁН!                                       ║"
echo "║                                                            ║"
echo "║  📊 Проверить статус:                                      ║"
echo "║     ssh $SERVER 'cd $REMOTE_DIR && docker-compose ps'      ║"
echo "║                                                            ║"
echo "║  📋 Посмотреть логи:                                       ║"
echo "║     ssh $SERVER 'cd $REMOTE_DIR && docker-compose logs -f' ║"
echo "║                                                            ║"
echo "║  🔄 Перезапустить:                                         ║"
echo "║     ssh $SERVER 'cd $REMOTE_DIR && docker-compose restart' ║"
echo "║                                                            ║"
echo "║  🛑 Остановить:                                            ║"
echo "║     ssh $SERVER 'cd $REMOTE_DIR && docker-compose down'    ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"

