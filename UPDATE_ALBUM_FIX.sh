#!/bin/bash

###############################################################################
# 🎨 UPDATE ALBUM FIX SCRIPT
# Обновление с исправлениями альбомов и изображений
###############################################################################

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                                ║${NC}"
echo -e "${BLUE}║  🎨 ОБНОВЛЕНИЕ: АЛЬБОМЫ И ИЗОБРАЖЕНИЯ                         ║${NC}"
echo -e "${BLUE}║                                                                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}✅ Исправления:${NC}"
echo "  1. Файлы с расширением (.jpg, не unnamed)"
echo "  2. Альбомы одним сообщением"
echo "  3. Event-based мониторинг"
echo "  4. Группировка по grouped_id"
echo ""

# Проверка наличия git
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ git не установлен!${NC}"
    exit 1
fi

# Проверка наличия docker-compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose не установлен!${NC}"
    exit 1
fi

echo -e "${YELLOW}📥 Шаг 1/5: Получение обновлений...${NC}"
git fetch origin
git pull origin main
echo -e "${GREEN}✅ Обновления получены${NC}"
echo ""

echo -e "${YELLOW}⏹️  Шаг 2/5: Остановка контейнера...${NC}"
docker-compose down
echo -e "${GREEN}✅ Контейнер остановлен${NC}"
echo ""

echo -e "${YELLOW}🔨 Шаг 3/5: Пересборка образа...${NC}"
docker-compose build --no-cache
echo -e "${GREEN}✅ Образ пересобран${NC}"
echo ""

echo -e "${YELLOW}🚀 Шаг 4/5: Запуск контейнера...${NC}"
docker-compose up -d
echo -e "${GREEN}✅ Контейнер запущен${NC}"
echo ""

echo -e "${YELLOW}📊 Шаг 5/5: Проверка логов...${NC}"
sleep 3
echo ""

docker-compose logs --tail 30

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ ОБНОВЛЕНИЕ ЗАВЕРШЕНО!${NC}"
echo ""
echo -e "${YELLOW}🧪 Для проверки:${NC}"
echo "  1. Опубликуйте альбом в исходном канале"
echo "  2. Смотрите логи: docker-compose logs -f"
echo "  3. Проверьте целевой канал - альбом должен быть ОДНИМ сообщением"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}📄 Подробности: ALBUM_FIX_EXPLANATION.md${NC}"
echo ""

