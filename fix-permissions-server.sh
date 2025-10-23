#!/bin/bash

# 🔒 Скрипт для исправления прав доступа на сервере

if [ -z "$1" ]; then
    echo "❌ Использование: bash fix-permissions-server.sh user@server_ip"
    exit 1
fi

SERVER=$1
REMOTE_DIR="/opt/telegram-post-copier"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🔒 ИСПРАВЛЕНИЕ ПРАВ ДОСТУПА НА СЕРВЕРЕ                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "🔧 Установка правильных прав доступа..."
ssh $SERVER << EOFSERVER
cd $REMOTE_DIR

echo "📁 Права на .env файл..."
chmod 644 .env
chown 1000:1000 .env

echo "📁 Права на директории..."
chmod 777 temp processed_images logs 2>/dev/null || true
chown -R 1000:1000 temp processed_images logs 2>/dev/null || true

echo "📁 Права на session файлы (если есть)..."
if ls *.session 1> /dev/null 2>&1; then
    chmod 644 *.session
    chown 1000:1000 *.session*
fi

echo ""
echo "✅ Права установлены!"
echo ""
echo "Проверка .env:"
ls -la .env

echo ""
echo "Проверка директорий:"
ls -ld temp processed_images logs
EOFSERVER

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ ПРАВА ДОСТУПА ИСПРАВЛЕНЫ!                              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Теперь на сервере запустите:"
echo ""
echo "  ssh $SERVER"
echo "  cd $REMOTE_DIR"
echo "  docker-compose run --rm copier"
echo ""
echo "Или сразу:"
echo "  ssh $SERVER 'cd $REMOTE_DIR && docker-compose run --rm copier'"

