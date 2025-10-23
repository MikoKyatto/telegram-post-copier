#!/bin/bash
# 🔧 ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ - Python зависимости

if [ -z "$1" ]; then
    echo "❌ Использование: bash FINAL_FIX_SERVER.sh user@server_ip"
    exit 1
fi

SERVER=$1
REMOTE_DIR="/opt/telegram-post-copier"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🔧 ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ DOCKERFILE                       ║"
echo "║     (Исправление Python зависимостей)                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "📤 Копирование исправленного Dockerfile..."
scp Dockerfile $SERVER:$REMOTE_DIR/

echo ""
echo "🧹 Полная очистка Docker на сервере..."
ssh $SERVER << 'EOFSERVER'
cd /opt/telegram-post-copier

echo "🛑 Остановка всех контейнеров..."
docker-compose down -v 2>/dev/null || true

echo "🗑️  Удаление всех образов проекта..."
docker images | grep -E "telegram|copier|opt" | awk '{print $3}' | xargs docker rmi -f 2>/dev/null || true

echo "🧹 Глубокая очистка Docker..."
docker system prune -a -f --volumes

echo "✅ Очистка завершена"
EOFSERVER

echo ""
echo "🐳 Пересборка образа с нуля..."
ssh $SERVER << 'EOFSERVER'
cd /opt/telegram-post-copier

echo "🔨 Сборка (это может занять 2-3 минуты)..."
docker-compose build --no-cache

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Образ успешно собран!"
    echo ""
    echo "🧪 Тест Python зависимостей..."
    docker-compose run --rm copier python -c "import telethon; print('✅ Telethon:', telethon.__version__)"
    
    if [ $? -eq 0 ]; then
        echo "✅ Все зависимости на месте!"
    else
        echo "⚠️  Проблема с зависимостями"
    fi
else
    echo "❌ Ошибка при сборке"
    exit 1
fi
EOFSERVER

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ ВСЕ ИСПРАВЛЕНО!                                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Теперь на сервере:"
echo ""
echo "ssh $SERVER"
echo "cd $REMOTE_DIR"
echo ""
echo "# Авторизация в Telegram:"
echo "docker-compose run --rm copier"
echo ""
echo "# После ввода кода (Ctrl+C для выхода), запустите:"
echo "docker-compose up -d"
echo ""
echo "# Проверка:"
echo "docker-compose logs -f"
