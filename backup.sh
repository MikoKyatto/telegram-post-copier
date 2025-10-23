#!/bin/bash

# 💾 Скрипт создания бэкапа
# Создает полный бэкап проекта включая .env и session файлы

set -e

BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="telegram-copier-backup-$TIMESTAMP"
BACKUP_FILE="$BACKUP_DIR/$BACKUP_NAME.tar.gz"

echo "💾 Создание бэкапа Telegram Post Copier"
echo "========================================"

# Создание директории для бэкапов
mkdir -p $BACKUP_DIR

# Список файлов для бэкапа
echo ""
echo "📦 Подготовка файлов для бэкапа..."

FILES_TO_BACKUP=(
    "*.py"
    "*.md"
    "*.sh"
    "*.txt"
    ".env"
    "*.session"
    "*.session-journal"
    "requirements.txt"
    "Dockerfile"
    "docker-compose.yml"
    ".dockerignore"
    ".gitignore"
    "Makefile"
    "env.example"
    "LICENSE"
)

# Создание временной директории
TEMP_DIR=$(mktemp -d)
TEMP_BACKUP="$TEMP_DIR/$BACKUP_NAME"
mkdir -p "$TEMP_BACKUP"

# Копирование файлов
echo "📋 Копирование файлов..."
for pattern in "${FILES_TO_BACKUP[@]}"; do
    for file in $pattern; do
        if [ -f "$file" ]; then
            cp "$file" "$TEMP_BACKUP/" 2>/dev/null || true
        fi
    done
done

# Копирование .github
if [ -d ".github" ]; then
    cp -r .github "$TEMP_BACKUP/" 2>/dev/null || true
fi

# Создание информационного файла
echo ""
echo "ℹ️  Создание информационного файла..."
cat > "$TEMP_BACKUP/BACKUP_INFO.txt" << EOF
╔════════════════════════════════════════════════════════════╗
║          TELEGRAM POST COPIER - BACKUP INFO                ║
╚════════════════════════════════════════════════════════════╝

📅 Дата создания: $(date '+%Y-%m-%d %H:%M:%S')
💻 Hostname: $(hostname)
👤 User: $(whoami)
📁 Исходная директория: $(pwd)

📦 Содержимое бэкапа:
$(ls -1 "$TEMP_BACKUP" | sed 's/^/  ✓ /')

🔐 Критические файлы:
$(ls -1 "$TEMP_BACKUP"/.env 2>/dev/null | sed 's/^/  ✓ /' || echo "  ⚠️  .env не найден")
$(ls -1 "$TEMP_BACKUP"/*.session 2>/dev/null | sed 's/^/  ✓ /' || echo "  ⚠️  Session файлы не найдены")

📊 Статистика:
  • Всего файлов: $(find "$TEMP_BACKUP" -type f | wc -l | xargs)
  • Размер: $(du -sh "$TEMP_BACKUP" | cut -f1)

🔄 Восстановление:
  1. Разархивируйте: tar -xzf $BACKUP_NAME.tar.gz
  2. Перейдите: cd $BACKUP_NAME
  3. Запустите: bash restore.sh

⚠️  ВАЖНО:
  • Храните бэкап в безопасном месте
  • Файл .env содержит секретные ключи
  • Session файлы содержат авторизацию Telegram
  • НЕ делитесь бэкапом публично

EOF

# Создание скрипта восстановления
cat > "$TEMP_BACKUP/restore.sh" << 'EOF'
#!/bin/bash

# 🔄 Скрипт восстановления из бэкапа

set -e

echo "🔄 Восстановление Telegram Post Copier из бэкапа"
echo "================================================"

TARGET_DIR="../telegram-post-copier-restored"

# Проверка существующей директории
if [ -d "$TARGET_DIR" ]; then
    echo "⚠️  Директория $TARGET_DIR уже существует!"
    read -p "Перезаписать? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Отменено"
        exit 1
    fi
    rm -rf "$TARGET_DIR"
fi

# Создание директории
echo ""
echo "📁 Создание директории $TARGET_DIR..."
mkdir -p "$TARGET_DIR"

# Копирование всех файлов
echo "📋 Копирование файлов..."
cp -r * "$TARGET_DIR/" 2>/dev/null || true
cp -r .* "$TARGET_DIR/" 2>/dev/null || true

# Удаление служебных файлов
rm -f "$TARGET_DIR/restore.sh" 2>/dev/null || true
rm -f "$TARGET_DIR/BACKUP_INFO.txt" 2>/dev/null || true

cd "$TARGET_DIR"

# Установка прав доступа
echo "🔒 Установка прав доступа..."
chmod 600 .env 2>/dev/null || true
chmod 600 *.session 2>/dev/null || true
chmod +x *.sh 2>/dev/null || true

# Создание директорий
echo "📁 Создание рабочих директорий..."
mkdir -p temp processed_images logs

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║  ✅ ВОССТАНОВЛЕНИЕ ЗАВЕРШЕНО!                              ║"
echo "║                                                            ║"
echo "║  📁 Файлы восстановлены в: $TARGET_DIR                     ║"
echo "║                                                            ║"
echo "║  🚀 Следующие шаги:                                        ║"
echo "║     1. cd $TARGET_DIR                                      ║"
echo "║     2. Проверьте .env файл                                 ║"
echo "║     3. bash setup.sh (если нужно)                          ║"
echo "║     4. python copier.py или docker-compose up -d           ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
EOF

chmod +x "$TEMP_BACKUP/restore.sh"

# Создание архива
echo ""
echo "🗜️  Создание архива..."
cd "$TEMP_DIR"
tar -czf "$BACKUP_FILE" "$BACKUP_NAME" 2>/dev/null

# Переход обратно
cd - > /dev/null

# Очистка временных файлов
rm -rf "$TEMP_DIR"

# Информация о бэкапе
BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║  ✅ БЭКАП СОЗДАН УСПЕШНО!                                  ║"
echo "║                                                            ║"
echo "║  📦 Файл: $BACKUP_FILE                                     ║"
echo "║  📊 Размер: $BACKUP_SIZE                                   ║"
echo "║  📅 Дата: $TIMESTAMP                                       ║"
echo "║                                                            ║"
echo "║  🔄 Восстановление:                                        ║"
echo "║     tar -xzf $BACKUP_FILE                                  ║"
echo "║     cd $BACKUP_NAME                                        ║"
echo "║     bash restore.sh                                        ║"
echo "║                                                            ║"
echo "║  ☁️  Скопируйте на безопасное хранилище:                   ║"
echo "║     • Внешний диск                                         ║"
echo "║     • Облако (Dropbox, Google Drive, etc.)                 ║"
echo "║     • Другой сервер                                        ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"

# Список бэкапов
echo ""
echo "📋 Список бэкапов:"
ls -lh $BACKUP_DIR/*.tar.gz 2>/dev/null | awk '{print "  • " $9 " (" $5 ")"}'

echo ""
echo "💡 Совет: Регулярно создавайте бэкапы (особенно перед обновлениями)"
echo "💡 Добавьте в cron для автоматических бэкапов:"
echo "   0 3 * * * cd $(pwd) && bash backup.sh"

