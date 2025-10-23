#!/bin/bash

# 🚀 Скрипт для загрузки проекта на GitHub
# Использование: bash git-push.sh "commit message"

set -e

REPO_URL="https://github.com/MikoKyatto/telegram-post-copier.git"
COMMIT_MSG="${1:-Initial commit with full project}"

echo "🚀 Загрузка проекта на GitHub"
echo "=============================="
echo "📍 Репозиторий: $REPO_URL"
echo "💬 Commit: $COMMIT_MSG"
echo ""

# Проверка Git
if ! command -v git &> /dev/null; then
    echo "❌ Git не установлен. Установите: https://git-scm.com/"
    exit 1
fi

# Инициализация Git (если еще не инициализирован)
if [ ! -d ".git" ]; then
    echo "📦 Инициализация Git репозитория..."
    git init
    echo "✅ Git инициализирован"
fi

# Проверка/добавление remote
echo ""
echo "🔗 Настройка remote..."
if git remote get-url origin &> /dev/null; then
    echo "ℹ️  Remote origin уже существует"
    CURRENT_REMOTE=$(git remote get-url origin)
    if [ "$CURRENT_REMOTE" != "$REPO_URL" ]; then
        echo "⚠️  Текущий remote: $CURRENT_REMOTE"
        echo "🔄 Обновление на: $REPO_URL"
        git remote set-url origin "$REPO_URL"
    fi
else
    echo "➕ Добавление remote origin..."
    git remote add origin "$REPO_URL"
fi
echo "✅ Remote настроен"

# Проверка .gitignore
if [ ! -f ".gitignore" ]; then
    echo ""
    echo "⚠️  .gitignore не найден, создаю..."
    cat > .gitignore << 'EOF'
# Секретные файлы
.env
*.session
*.session-journal

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Docker
*.log

# Временные файлы
temp/
tmp/
processed_images/
*.tmp
backups/

# OS
.DS_Store
Thumbs.db
EOF
    echo "✅ .gitignore создан"
fi

# Добавление всех файлов
echo ""
echo "📋 Добавление файлов в Git..."
git add .

# Проверка что есть что коммитить
if git diff --staged --quiet; then
    echo "ℹ️  Нет изменений для коммита"
    
    # Проверка что есть хоть один коммит
    if ! git rev-parse HEAD &> /dev/null; then
        echo "⚠️  Репозиторий пуст, создаю первый коммит..."
        git add .
    else
        echo "✅ Репозиторий уже актуален"
        exit 0
    fi
fi

# Коммит
echo ""
echo "💾 Создание коммита..."
git commit -m "$COMMIT_MSG"
echo "✅ Коммит создан"

# Настройка главной ветки (main)
echo ""
echo "🌿 Проверка ветки..."
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "🔄 Переименование ветки в main..."
    git branch -M main
fi
echo "✅ Ветка: main"

# Push
echo ""
echo "📤 Загрузка на GitHub..."
echo "⏳ Это может занять некоторое время..."

if git push -u origin main; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║  ✅ УСПЕШНО ЗАГРУЖЕНО НА GITHUB!                           ║"
    echo "║                                                            ║"
    echo "║  🌐 Репозиторий:                                           ║"
    echo "║     $REPO_URL"
    echo "║                                                            ║"
    echo "║  📊 Просмотреть:                                           ║"
    echo "║     https://github.com/MikoKyatto/telegram-post-copier     ║"
    echo "║                                                            ║"
    echo "║  📥 Клонировать на другой машине:                          ║"
    echo "║     git clone $REPO_URL"
    echo "║                                                            ║"
    echo "║  🔄 Обновить на другой машине:                             ║"
    echo "║     git pull origin main                                   ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
else
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║  ⚠️  ОШИБКА ПРИ ЗАГРУЗКЕ                                   ║"
    echo "║                                                            ║"
    echo "║  Возможные причины:                                        ║"
    echo "║  • Нет прав доступа к репозиторию                          ║"
    echo "║  • Требуется авторизация                                   ║"
    echo "║  • Проблемы с сетью                                        ║"
    echo "║                                                            ║"
    echo "║  Решение:                                                  ║"
    echo "║  1. Убедитесь что вы владелец репозитория                  ║"
    echo "║  2. Настройте GitHub токен:                                ║"
    echo "║     https://github.com/settings/tokens                     ║"
    echo "║  3. Используйте SSH вместо HTTPS:                          ║"
    echo "║     git remote set-url origin git@github.com:MikoKyatto/telegram-post-copier.git"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    exit 1
fi

echo ""
echo "💡 Следующие шаги:"
echo "  • Деплой на сервер: bash deploy.sh user@server_ip"
echo "  • Создать бэкап: bash backup.sh"
echo "  • Обновить README с правильными ссылками"

