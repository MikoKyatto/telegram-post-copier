#!/bin/bash
# 🔧 Быстрое обновление Dockerfile на сервере

if [ -z "$1" ]; then
    echo "❌ Использование: bash UPDATE_DOCKERFILE_ON_SERVER.sh user@server_ip"
    exit 1
fi

SERVER=$1
REMOTE_DIR="/opt/telegram-post-copier"

echo "📤 Копирование исправленного Dockerfile на $SERVER..."
scp Dockerfile $SERVER:$REMOTE_DIR/

echo ""
echo "🔧 Пересборка на сервере..."
ssh $SERVER << 'EOFSERVER'
cd /opt/telegram-post-copier
echo "🛑 Остановка контейнера..."
docker-compose down
echo "🐳 Пересборка образа..."
docker-compose build --no-cache
echo "✅ Готово! Для запуска выполните:"
echo "   docker-compose up -d"
EOFSERVER

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ Dockerfile обновлен и пересобран!                      ║"
echo "║                                                            ║"
echo "║  Теперь запустите на сервере:                              ║"
echo "║    ssh $SERVER                                             ║"
echo "║    cd $REMOTE_DIR                                          ║"
echo "║                                                            ║"
echo "║  Если session файл есть:                                   ║"
echo "║    docker-compose up -d                                    ║"
echo "║                                                            ║"
echo "║  Если нет (первый запуск):                                 ║"
echo "║    bash first-auth.sh                                      ║"
echo "║    docker-compose up -d                                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
