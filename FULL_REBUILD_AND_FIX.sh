#!/bin/bash

# 🚀 ПОЛНАЯ ПЕРЕСБОРКА И ИСПРАВЛЕНИЕ
# Этот скрипт выполняется НА СЕРВЕРЕ

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🚀 ПОЛНАЯ ОЧИСТКА И ПЕРЕСБОРКА                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

cd /opt/telegram-post-copier

echo "📥 ШАГ 1/6: Подтягивание изменений с GitHub..."
git pull origin main || echo "⚠️  Git pull failed, continuing..."
echo "✅ Изменения загружены"
echo ""

echo "🗑️  ШАГ 2/6: Остановка и удаление старых контейнеров..."
docker-compose down -v 2>/dev/null || true
docker rm -f $(docker ps -aq --filter "name=telegram-post-copier") 2>/dev/null || true
echo "✅ Контейнеры удалены"
echo ""

echo "🗑️  ШАГ 3/6: Удаление старых образов..."
docker rmi telegram-post-copier_copier 2>/dev/null || true
docker image prune -f
echo "✅ Образы очищены"
echo ""

echo "🔒 ШАГ 4/6: Установка правильных прав доступа..."
# Создание необходимых директорий
mkdir -p temp processed_images logs

# КРИТИЧНО: установить владельца на ВСЮ директорию
chown -R 1000:1000 .

# Установить правильные права
chmod 755 .
chmod 777 temp processed_images logs
chmod 644 .env 2>/dev/null || echo "⚠️  .env not found"
chmod 644 *.py 2>/dev/null || true
chmod +x *.sh 2>/dev/null || true

echo "✅ Права установлены"
echo ""
echo "Проверка прав:"
ls -la | grep -E "(drwx|\.env|\.py)" | head -10
echo ""

echo "🔨 ШАГ 5/6: Сборка нового образа..."
docker-compose build --no-cache
echo "✅ Образ собран"
echo ""

echo "🔍 ШАГ 6/6: Проверка окружения внутри контейнера..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
docker-compose run --rm copier /bin/bash -c "
echo 'Текущий пользователь:'
id
echo ''
echo 'Права на /app:'
ls -la /app | head -10
echo ''
echo 'Проверка записи в /app:'
touch /app/.test_write && rm /app/.test_write && echo '✅ Запись РАБОТАЕТ' || echo '❌ Запись НЕ РАБОТАЕТ'
"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ ВСЁ ГОТОВО!                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Теперь запустите АВТОРИЗАЦИЮ:"
echo ""
echo "   docker-compose run --rm copier"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
