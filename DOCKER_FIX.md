# 🔧 Исправление проблем с Docker

## ❌ Проблема: `sqlite3.OperationalError: unable to open database file`

### Описание:
При запуске в Docker контейнере возникала ошибка создания session файла Telegram из-за прав доступа.

---

## ✅ Исправления (уже применены):

### 1. **Dockerfile** - добавлен непривилегированный пользователь:
```dockerfile
# Создание пользователя appuser (UID 1000)
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser
```

### 2. **docker-compose.yml** - монтирование всего каталога:
```yaml
volumes:
  # Весь рабочий каталог (для session файлов)
  - .:/app

# Права пользователя
user: "1000:1000"
```

### 3. **docker-entrypoint.sh** - инициализация окружения:
```bash
# Создание директорий
mkdir -p /app/temp /app/processed_images /app/logs

# Установка прав на session файл
chmod 600 /app/copier_session.session
```

---

## 🚀 Как использовать (исправленная версия):

### Шаг 1: Подготовка

```bash
# Создайте .env файл
cp env.example .env
nano .env  # Заполните все поля

# Создайте необходимые директории
mkdir -p temp processed_images logs
chmod 777 temp processed_images logs
```

### Шаг 2: Первая авторизация (НОВЫЙ СПОСОБ)

**Вариант A: Автоматический скрипт (рекомендуется)**
```bash
bash first-auth.sh
```

**Вариант B: Вручную**
```bash
# Сборка образа
docker-compose build

# Запуск для авторизации (интерактивный режим)
docker-compose run --rm copier

# Введите номер телефона и код из Telegram
```

### Шаг 3: Запуск в production

```bash
# После успешной авторизации
docker-compose up -d

# Проверка логов
docker-compose logs -f
```

---

## 📊 Проверка работы:

### 1. Проверка прав на файлы:
```bash
ls -la copier_session.session*
# Должно быть: -rw------- (600)
```

### 2. Проверка контейнера:
```bash
docker-compose ps
# STATUS должен быть "Up"
```

### 3. Проверка логов:
```bash
docker-compose logs --tail=50
# Должно быть:
# ✅ Авторизован как: Your Name
# ✅ Исходный канал: ...
# ✅ Целевой канал: ...
# 🔁 Запуск мониторинга
```

---

## 🔄 Миграция со старой версии:

Если у вас уже был запущен контейнер со старой версией:

```bash
# 1. Остановите старый контейнер
docker-compose down

# 2. Создайте бэкап session файла
cp copier_session.session copier_session.session.backup

# 3. Пересоберите образ
docker-compose build --no-cache

# 4. Если session файл существует - просто запустите
docker-compose up -d

# 5. Если нет - выполните первую авторизацию
bash first-auth.sh
```

---

## 🐛 Troubleshooting:

### Проблема: Permission denied при создании session

**Решение:**
```bash
# Дайте права на директорию
chmod 777 . 2>/dev/null || sudo chmod 777 .

# Или измените владельца
sudo chown -R 1000:1000 .
```

### Проблема: Session файл не создается

**Решение:**
```bash
# Проверьте директорию внутри контейнера
docker-compose run --rm copier ls -la /app

# Проверьте пользователя
docker-compose run --rm copier whoami
# Должно быть: appuser

# Проверьте права на запись
docker-compose run --rm copier touch /app/test.txt
docker-compose run --rm copier rm /app/test.txt
```

### Проблема: Контейнер падает сразу после запуска

**Решение:**
```bash
# Посмотрите полные логи
docker-compose logs

# Запустите в интерактивном режиме для отладки
docker-compose run --rm copier bash

# Внутри контейнера проверьте
ls -la
env | grep -E "API_ID|API_HASH|SOURCE|TARGET"
python -c "from config import Config; Config.validate()"
```

---

## 💡 Рекомендации:

### 1. Автоматический бэкап session файла:
```bash
# Добавьте в crontab
crontab -e

# Бэкап каждый день в 3:00
0 3 * * * cd /path/to/telegram-post-copier && cp copier_session.session backups/session_$(date +\%Y\%m\%d).session
```

### 2. Мониторинг контейнера:
```bash
# Автоматический перезапуск при падении (уже настроено)
# В docker-compose.yml: restart: unless-stopped

# Дополнительно: мониторинг логов
tail -f logs/*.log 2>/dev/null || docker-compose logs -f
```

### 3. Безопасность:
```bash
# Проверьте что .env в .gitignore
grep ".env" .gitignore

# Проверьте что session файлы в .gitignore
grep "*.session" .gitignore

# Проверьте права (должно быть 600)
ls -la .env copier_session.session
```

---

## 📋 Чеклист после исправления:

- [ ] ✅ Dockerfile обновлен (пользователь appuser)
- [ ] ✅ docker-compose.yml обновлен (volume и user)
- [ ] ✅ docker-entrypoint.sh создан
- [ ] ✅ first-auth.sh создан
- [ ] ✅ Директории созданы (temp, logs, processed_images)
- [ ] ✅ .env файл заполнен
- [ ] ✅ Первая авторизация выполнена
- [ ] ✅ Session файл создан и имеет права 600
- [ ] ✅ Контейнер запущен (docker-compose up -d)
- [ ] ✅ Логи проверены (нет ошибок)
- [ ] ✅ Тестовый пост скопирован успешно

---

## 🎯 Итоговая команда для деплоя:

```bash
# Полный деплой с нуля (одной командой)
cd /path/to/telegram-post-copier && \
cp env.example .env && \
nano .env && \
bash first-auth.sh && \
docker-compose up -d && \
docker-compose logs -f
```

---

<div align="center">

**Проблема решена! ✅**

Теперь Docker работает корректно с правильными правами доступа.

</div>

