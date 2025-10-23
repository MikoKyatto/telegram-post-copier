#!/bin/bash
# 🔧 Полное исправление на сервере

if [ -z "$1" ]; then
    echo "❌ Использование: bash FULL_FIX_SERVER.sh user@server_ip"
    exit 1
fi

SERVER=$1
REMOTE_DIR="/opt/telegram-post-copier"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🔧 ПОЛНОЕ ИСПРАВЛЕНИЕ DOCKER НА СЕРВЕРЕ                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "📤 Шаг 1: Копирование исправленного Dockerfile..."
scp Dockerfile $SERVER:$REMOTE_DIR/

echo ""
echo "🧹 Шаг 2: Очистка старых образов на сервере..."
ssh $SERVER << 'EOFSERVER'
cd /opt/telegram-post-copier

echo "🛑 Остановка и удаление контейнеров..."
docker-compose down -v 2>/dev/null || true

echo "🗑️  Удаление старых образов..."
docker images | grep telegram-post-copier | awk '{print $3}' | xargs docker rmi -f 2>/dev/null || true
docker system prune -f

echo "✅ Очистка завершена"
EOFSERVER

echo ""
echo "🐳 Шаг 3: Пересборка образа с нуля..."
ssh $SERVER << 'EOFSERVER'
cd /opt/telegram-post-copier

echo "🔨 Сборка нового образа..."
docker-compose build --no-cache

if [ $? -eq 0 ]; then
    echo "✅ Образ успешно собран!"
else
    echo "❌ Ошибка при сборке"
    exit 1
fi
EOFSERVER

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ ИСПРАВЛЕНИЯ ПРИМЕНЕНЫ!                                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Следующие шаги на сервере:"
echo ""
echo "ssh $SERVER"
echo "cd $REMOTE_DIR"
echo ""
echo "# Если session файл уже есть:"
echo "docker-compose up -d"
echo ""
echo "# Если нет (первая авторизация):"
echo "docker-compose run --rm copier"
echo "# Введите номер телефона и код"
echo "# После авторизации:"
echo "docker-compose up -d"
echo ""
echo "# Проверка логов:"
echo "docker-compose logs -f"
