# 🎯 GET STARTED - Начните за 3 шага

> **Самый быстрый способ запустить Telegram Post Copier**

---

## 🚀 Шаг 1: Установка (2 минуты)

### Скачайте проект:

```bash
# Клонируйте репозиторий
git clone https://github.com/yourusername/telegram-post-copier.git
cd telegram-post-copier

# Автоматическая установка
bash setup.sh
```

**Что делает setup.sh:**
- ✅ Проверяет Python, Docker, Tesseract
- ✅ Создает виртуальное окружение
- ✅ Устанавливает все зависимости
- ✅ Создает .env файл из шаблона

---

## 🔑 Шаг 2: Получение ключей (5 минут)

### A. Telegram API (2 мин)

1. Откройте: https://my.telegram.org
2. Войдите с номером телефона
3. Перейдите в "API development tools"
4. Создайте приложение
5. Сохраните **api_id** и **api_hash**

### B. DeepSeek API (2 мин)

1. Откройте: https://platform.deepseek.com/
2. Зарегистрируйтесь (через Google проще всего)
3. Перейдите в "API Keys"
4. Создайте новый ключ
5. Сохраните ключ (начинается с `sk-`)

### C. Заполните .env (1 мин)

```bash
# Откройте файл
nano .env

# Заполните эти поля:
API_ID=12345678                    # Ваш api_id от Telegram
API_HASH=abcdef1234567890          # Ваш api_hash от Telegram
SOURCE_CHANNEL=nasvyazi_helpdesk   # Канал-источник
TARGET_CHANNEL=your_channel        # Ваш канал
DEEPSEEK_API_KEY=sk-xxxxx          # Ваш ключ от DeepSeek
YOUR_LINK=t.me/your_channel        # Ваша ссылка
YOUR_BRAND_NAME=Ваш VPN            # Название бренда

# Сохраните: Ctrl+O, Enter, Ctrl+X
```

---

## ▶️ Шаг 3: Запуск (30 секунд)

### Вариант A: Локальный запуск

```bash
# Проверьте конфигурацию
python test_config.py

# Запустите бота
python copier.py

# При первом запуске:
# 1. Введите номер телефона
# 2. Введите код из Telegram
# 3. Готово!
```

### Вариант B: Docker (рекомендуется)

```bash
# Сборка
docker-compose build

# Первая авторизация
docker-compose run --rm copier python copier.py
# Введите номер и код

# Запуск в фоне
docker-compose up -d

# Проверка логов
docker-compose logs -f
```

---

## ✅ Проверка работы

### 1. Создайте тестовый пост

В исходном канале (SOURCE_CHANNEL) опубликуйте:
```
Тест блокировки: Москва, МТС
Подробнее: t.me/test_channel
```

### 2. Подождите 5 минут

Бот проверяет новые посты каждые 5 минут (настраивается в .env).

### 3. Проверьте ваш канал

В вашем канале (TARGET_CHANNEL) должен появиться переписанный пост:
```
🚨 Новые ограничения зафиксированы в Москве
Провайдер МТС начал блокировки.
Обходите с нашим VPN: t.me/your_channel 🔒
```

---

## 📊 Мониторинг

### Просмотр логов:

```bash
# Локальный запуск
tail -f copier.log

# Docker
docker-compose logs -f copier

# Последние 100 строк
docker-compose logs --tail=100 copier
```

### Ожидаемый вывод:

```
2025-10-23 14:30:15 | INFO | 🚀 TelegramPostCopier инициализирован
2025-10-23 14:30:16 | INFO | ✅ Авторизован как: John Doe
2025-10-23 14:30:17 | INFO | ✅ Исходный канал: На связи Helpdesk
2025-10-23 14:30:18 | INFO | ✅ Целевой канал: Your VPN Channel
2025-10-23 14:30:19 | INFO | 🔁 Запуск мониторинга
2025-10-23 14:35:20 | INFO | 🔄 Обработка поста ID 12345
2025-10-23 14:35:22 | INFO | 🧠 AI: Переписывание текста...
2025-10-23 14:35:24 | INFO | 📊 Уникальность: 78.5%
2025-10-23 14:35:25 | INFO | ✅ Пост ID 12345 успешно скопирован
```

---

## 🎛️ Настройка (опционально)

### Изменить интервал проверки:

```bash
# В .env файле:
CHECK_INTERVAL=300  # секунды (300 = 5 минут)
```

### Изменить стиль канала:

```bash
# В .env файле:
CHANNEL_STYLE="Ваш уникальный стиль: энергичный, технический, официальный..."
```

### Настроить температуру AI:

```bash
# В .env файле:
LLM_TEMPERATURE=0.7  # 0.0-1.0 (выше = креативнее)
```

---

## 🆘 Проблемы?

### ❌ "API_ID не установлен"

**Решение**: Проверьте .env файл:
```bash
cat .env | grep API_ID
```
API_ID должен быть числом без кавычек.

### ❌ "Tesseract не найден"

**Решение для macOS**:
```bash
brew install tesseract tesseract-lang
```

**Решение для Linux**:
```bash
sudo apt install tesseract-ocr tesseract-ocr-rus
```

### ❌ "FloodWaitError"

**Решение**: Увеличьте интервал в .env:
```bash
CHECK_INTERVAL=600  # 10 минут
```

### ❌ Бот не видит новые посты

**Проверьте**:
1. SOURCE_CHANNEL указан без @
2. Вы участник канала (если он приватный)
3. Интервал CHECK_INTERVAL не слишком большой

---

## 📚 Дальнейшее чтение

После успешного запуска:

- 📖 [README.md](README.md) - Полная документация
- 📗 [SETUP_GUIDE.md](SETUP_GUIDE.md) - Детальная инструкция
- 📊 [DEMO.md](DEMO.md) - Примеры работы
- 🏗️ [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Архитектура

---

## 🎓 Полезные команды

```bash
# Makefile команды (если установлен make)
make help          # Показать все команды
make setup         # Полная установка
make run           # Запуск
make docker-up     # Docker запуск
make docker-logs   # Логи
make clean         # Очистка
make env-check     # Проверка .env
```

---

## 💡 Советы

### 1. Начните с малого
Сначала протестируйте на 1 канале, потом масштабируйте.

### 2. Мониторьте уникальность
Следите за процентом уникальности в логах. Должен быть >70%.

### 3. Сохраните session файл
Сделайте бэкап `copier_session.session` - он содержит авторизацию.

### 4. Используйте Docker в production
Docker автоматически перезапустит бота при падении.

### 5. Настройте стиль канала
Опишите стиль в CHANNEL_STYLE - AI адаптирует все посты под него.

---

## 🌟 Первые шаги после запуска

1. ✅ Убедитесь, что бот видит новые посты (логи)
2. ✅ Проверьте качество переписанных текстов
3. ✅ Настройте стиль под ваш бренд
4. ✅ Добавьте свои ссылки и брендинг
5. ✅ Мониторьте уникальность (должна быть >70%)
6. ✅ Сделайте бэкап session файла
7. ✅ Задеплойте на VPS (если нужна работа 24/7)

---

## 🚀 Production Deployment

Если хотите, чтобы бот работал 24/7:

```bash
# На вашем VPS
ssh user@your-server.com

# Установите Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Клонируйте проект
git clone https://github.com/yourusername/telegram-post-copier.git
cd telegram-post-copier

# Настройте .env
nano .env

# Авторизация
docker-compose run --rm copier python copier.py

# Запуск
docker-compose up -d
```

---

## 📞 Нужна помощь?

1. 📖 Читайте [SETUP_GUIDE.md](SETUP_GUIDE.md) - подробная инструкция
2. 🔍 Проверьте Troubleshooting в [README.md](README.md)
3. 🐛 Создайте Issue на GitHub
4. 💬 Напишите в Telegram: @your_support_bot

---

<div align="center">

## 🎉 Готово!

**Вы запустили Telegram Post Copier with AI**

Теперь ваш канал автоматически получает уникальный контент 24/7

---

### ⭐ Нравится проект? Поставьте звезду на GitHub!

[⭐ Star on GitHub](https://github.com/yourusername/telegram-post-copier)

---

🦄 **Автоматизируем будущее, один пост за раз**

</div>

