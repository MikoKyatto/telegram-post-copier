# ⚡ Quick Start Guide

> **Запуск бота за 5 минут**

## 🚀 Для опытных пользователей

```bash
# 1. Клонирование
git clone https://github.com/yourusername/telegram-post-copier.git
cd telegram-post-copier

# 2. Настройка
cp env.example .env
nano .env  # Заполните: API_ID, API_HASH, каналы, LLM ключ

# 3. Установка
bash setup.sh

# 4. Тестирование конфигурации
python test_config.py

# 5. Запуск
python copier.py
# Или с Docker:
docker-compose up -d
```

## 📋 Минимальная конфигурация .env

```bash
API_ID=12345678
API_HASH=your_hash
SOURCE_CHANNEL=nasvyazi_helpdesk
TARGET_CHANNEL=your_channel
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-xxxxx
YOUR_LINK=t.me/your_channel
YOUR_BRAND_NAME=Your VPN
```

## 🔑 Где получить ключи

| Что нужно | Где получить | Время |
|-----------|--------------|-------|
| **Telegram API** | https://my.telegram.org | 2 мин |
| **DeepSeek API** | https://platform.deepseek.com | 2 мин |

## ✅ Проверка

```bash
# Тест конфигурации
python test_config.py

# Тест одного поста
python copier.py  # Ctrl+C после первого поста

# Логи
tail -f copier.log
```

## 🐳 Docker (рекомендуется)

```bash
# Сборка
docker-compose build

# Первая авторизация
docker-compose run --rm copier python copier.py
# Введите номер телефона и код

# Запуск
docker-compose up -d

# Логи
docker-compose logs -f
```

## ⚙️ Makefile команды

```bash
make setup          # Полная настройка
make run            # Запуск локально
make docker-up      # Запуск Docker
make docker-logs    # Просмотр логов
make clean          # Очистка
make env-check      # Проверка .env
```

## 🆘 Проблемы?

```bash
# Проверка зависимостей
pip list | grep -E "telethon|opencv|pytesseract"

# Проверка Tesseract
tesseract --version

# Права на .env
chmod 600 .env

# Переавторизация
rm copier_session.session
python copier.py
```

## 📖 Полная документация

- 📘 [README.md](README.md) - Полное руководство
- 📗 [SETUP_GUIDE.md](SETUP_GUIDE.md) - Пошаговая инструкция для новичков
- 📕 [CONTRIBUTING.md](CONTRIBUTING.md) - Как внести вклад

---

**Вопросы?** Создайте [Issue](https://github.com/yourusername/telegram-post-copier/issues)

🦄 Удачи!

