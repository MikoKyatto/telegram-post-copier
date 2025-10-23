#!/bin/bash

# 🔧 ОКОНЧАТЕЛЬНОЕ ИСПРАВЛЕНИЕ ВСЕХ ПРОБЛЕМ С ПРАВАМИ

if [ -z "$1" ]; then
    echo "❌ Использование: bash ULTIMATE_FIX.sh user@server_ip"
    exit 1
fi

SERVER=$1
REMOTE_DIR="/opt/telegram-post-copier"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🔧 ОКОНЧАТЕЛЬНОЕ ИСПРАВЛЕНИЕ                              ║"
echo "║     (Права доступа для всей директории)                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "📤 Копирование обновленных файлов..."
scp copier.py docker-entrypoint.sh $SERVER:$REMOTE_DIR/

echo ""
echo "🔧 ГЛАВНОЕ ИСПРАВЛЕНИЕ: установка прав на ВСЮ директорию..."
ssh $SERVER << 'EOFSERVER'
cd /opt/telegram-post-copier

echo "🔒 Установка владельца UID 1000 (appuser) на ВСЮ директорию..."
chown -R 1000:1000 .

echo "📁 Установка прав на директории..."
chmod 755 .
chmod 777 temp processed_images logs 2>/dev/null || true
chmod 644 .env 2>/dev/null || true
chmod 644 *.py *.sh 2>/dev/null || true
chmod +x *.sh 2>/dev/null || true

echo ""
echo "✅ Права установлены!"
echo ""
echo "Проверка:"
ls -la | head -20
EOFSERVER

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ ВСЕ ИСПРАВЛЕНО!                                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Теперь запустите на сервере:"
echo ""
echo "  ssh $SERVER"
echo "  cd $REMOTE_DIR"
echo "  docker-compose run --rm copier"
echo ""
echo "Или одной командой:"
echo "  ssh $SERVER 'cd $REMOTE_DIR && docker-compose run --rm copier'"
