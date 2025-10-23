#!/bin/bash
# 🔧 Скрипт для быстрого исправления на сервере

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🔧 ИСПРАВЛЕНИЕ DOCKER НА СЕРВЕРЕ                          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

if [ -z "$1" ]; then
    echo "❌ Использование: bash FIX_ON_SERVER.sh user@server_ip"
    exit 1
fi

SERVER=$1
REMOTE_DIR="/opt/telegram-post-copier"

echo "📤 Копирование исправленных файлов на $SERVER..."
scp Dockerfile docker-compose.yml docker-entrypoint.sh first-auth.sh utils.py $SERVER:$REMOTE_DIR/

echo ""
echo "🔧 Применение исправлений на сервере..."
ssh $SERVER << 'EOF'
cd /opt/telegram-post-copier

echo "🛑 Остановка контейнера..."
docker-compose down

echo "📁 Создание директорий с правами..."
mkdir -p temp processed_images logs
chmod 777 temp processed_images logs

echo "🐳 Пересборка образа..."
docker-compose build --no-cache

echo ""
if [ -f "copier_session.session" ]; then
    echo "✅ Session файл найден, запуск..."
    docker-compose up -d
    echo ""
    echo "📋 Логи (Ctrl+C для выхода):"
    docker-compose logs -f
else
    echo "⚠️  Session файл не найден"
    echo "Выполните: bash first-auth.sh"
    echo "Затем: docker-compose up -d"
fi
EOF

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ ИСПРАВЛЕНИЯ ПРИМЕНЕНЫ!                                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
