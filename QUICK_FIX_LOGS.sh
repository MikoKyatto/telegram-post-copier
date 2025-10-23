#!/bin/bash

# 🔧 Быстрое исправление логирования

if [ -z "$1" ]; then
    echo "❌ Использование: bash QUICK_FIX_LOGS.sh user@server_ip"
    exit 1
fi

SERVER=$1
REMOTE_DIR="/opt/telegram-post-copier"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🔧 ИСПРАВЛЕНИЕ ЛОГИРОВАНИЯ                                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "📤 Копирование исправленного copier.py..."
scp copier.py $SERVER:$REMOTE_DIR/

echo ""
echo "🔧 Установка прав на директорию logs..."
ssh $SERVER << EOFSERVER
cd $REMOTE_DIR

# Создание директории с правильными правами
mkdir -p logs
chmod 777 logs
chown -R 1000:1000 logs

echo "✅ Права установлены"
echo ""
echo "Проверка:"
ls -ld logs
EOFSERVER

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ ИСПРАВЛЕНО!                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Теперь запустите на сервере:"
echo ""
echo "  ssh $SERVER"
echo "  cd $REMOTE_DIR"
echo "  docker-compose run --rm copier"
