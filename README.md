# 🦄 Telegram Post Copier with AI

> **Революционная AI-платформа для автоматизации контента в Telegram**

Автоматическое копирование и AI-трансформация постов из любого Telegram канала в ваш собственный. Никаких дубликатов, только уникальный контент с вашим брендингом.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AI-Powered](https://img.shields.io/badge/AI-Powered-purple.svg)](https://github.com/MikoKyatto/telegram-post-copier)

---

## 🚀 Что это такое?

**Telegram Post Copier** — это полноценная AI-платформа для автоматизации контента, которая:

- 🤖 **Переписывает тексты** через 6 LLM провайдеров с автоматическим переключением
- 🎨 **Обрабатывает изображения** через OCR + CV - заменяет чужие ссылки на ваши
- 📊 **Проверяет уникальность** контента перед публикацией
- 🔄 **Работает 24/7** в Docker-контейнере на сервере
- 🆓 **БЕСПЛАТНЫЕ опции** - Google Gemini, HuggingFace, Cohere
- 🎯 **Добавляет Call-to-Action** с вашим брендингом
- 🛡️ **Автоматический fallback** - если один API недоступен, переключается на другой

### 💡 Идеально для:
- 📱 VPN-сервисов, мониторящих блокировки интернета
- 📰 Новостных каналов с агрегацией контента
- 💼 SMM-агентств, управляющих множеством каналов
- 🔐 Любых проектов, требующих автоматизации Telegram

---

## ✨ Ключевые возможности

### 🧠 AI-Powered Rewriting с автофоллбэком

```python
Оригинал:
"Ограничения в регионах Москва и СПб. 
Подробнее: t.me/old_channel"

После AI обработки:
"🚨 Внимание! Новые блокировки зафиксированы в Москве 
и Санкт-Петербурге. Обходите ограничения безопасно с 
XVPN+: t.me/your_channel 🔒"
```

**Автоматическое переключение:**
```
✅ Попытка через Google Gemini... ✅ Успешно
⚠️ Google Gemini недоступен... → пробуем DeepSeek
⚠️ DeepSeek недоступен... → пробуем Cohere
✅ Cohere: Успешно сгенерирован текст!
```

### 🎨 Умная обработка изображений

- **OCR-детекция** текста на изображениях (Tesseract)
- **Inpainting** для удаления старых ссылок/логотипов (OpenCV)
- **Автоматическое наложение** вашего брендинга (Pillow)
- Поддержка **русского и английского** языков
- Сохранение в директорию `processed_images/`

### 🌐 Поддержка 6 LLM провайдеров

| Провайдер | Стоимость | Качество | Скорость | Статус |
|-----------|-----------|----------|----------|---------|
| **Google Gemini** | **🆓 БЕСПЛАТНО** | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | ✅ Рекомендуем |
| **HuggingFace** | **🆓 БЕСПЛАТНО** | ⭐⭐⭐ | ⚡ | ✅ Запасной |
| **Cohere** | 🆓 Trial | ⭐⭐⭐⭐ | ⚡⚡ | ✅ Условно-бесплатно |
| **DeepSeek** | $0.14/1M токенов | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | 💰 Дешево |
| **OpenAI GPT** | $0.50-2/1M токенов | ⭐⭐⭐⭐⭐ | ⚡⭐⚡ | 💰 Премиум |
| **xAI Grok** | $2/1M токенов | ⭐⭐⭐⭐ | ⚡⚡⚡ | 💰 Новый |

**Умная приоритизация:** Успешный провайдер автоматически перемещается в начало списка!

---

## 🎯 Quick Start (5 минут до запуска!)

### Вариант 1: БЕСПЛАТНЫЙ запуск (рекомендуем!)

#### Шаг 1: Получение Telegram API

1. Перейдите на https://my.telegram.org
2. Войдите с вашим номером телефона
3. **"API development tools"** → Создайте приложение
4. Сохраните `api_id` и `api_hash`

#### Шаг 2: Получение бесплатного Google Gemini API

1. Перейдите на https://aistudio.google.com/app/apikey
2. Войдите через Google аккаунт
3. Нажмите **"Create API Key"**
4. Скопируйте ключ (начинается с `AIzaSy...`)

**Лимиты:** 60 запросов/минута БЕСПЛАТНО! Этого хватит для большинства каналов.

> 💡 **Другие бесплатные опции:** HuggingFace, Cohere - смотрите [FREE_LLM_SETUP.md](FREE_LLM_SETUP.md)

#### Шаг 3: Клонирование и настройка

```bash
# Клонирование
git clone https://github.com/MikoKyatto/telegram-post-copier.git
cd telegram-post-copier

# Настройка .env
cp env.example .env
nano .env
```

**Заполните в .env:**
```env
# Telegram API
API_ID=ваш_api_id
API_HASH=ваш_api_hash

# Каналы
SOURCE_CHANNEL=канал_источник
TARGET_CHANNEL=ваш_канал

# AI (БЕСПЛАТНО!)
LLM_PROVIDER=auto
GOOGLE_API_KEY=AIzaSy...  # Ваш ключ Google Gemini

# Брендинг
YOUR_LINK=t.me/your_channel
YOUR_BRAND_NAME=XVPN+
```

#### Шаг 4: Запуск в Docker

```bash
# Сборка
docker-compose build

# Первая авторизация (введите номер телефона и код)
docker-compose run --rm copier

# Запуск в фоне
docker-compose up -d

# Просмотр логов
docker-compose logs -f
```

**Готово!** Бот работает 24/7 с бесплатным AI! 🎉

---

### Вариант 2: С платным API (для больших объемов)

Если нужна высокая производительность, добавьте **DeepSeek** (~$5 хватит на месяцы):

1. Регистрация: https://platform.deepseek.com
2. Пополните баланс на $5-10
3. Получите API key: https://platform.deepseek.com/api_keys
4. Добавьте в `.env`:
   ```env
   LLM_PROVIDER=auto
   GOOGLE_API_KEY=AIzaSy...     # Основной (бесплатно)
   DEEPSEEK_API_KEY=sk-...      # Запасной (дешево)
   
   ```

Бот автоматически переключится на DeepSeek, если Google Gemini недоступен!

---

## 🛠️ Установка на сервер

### Автоматический деплой (один скрипт!)

```bash
# На локальной машине
bash deploy.sh root@ваш_сервер_ip

# Следуйте инструкциям в терминале
```

Скрипт автоматически:
- Установит Docker и Docker Compose
- Скопирует проект на сервер
- Настроит права доступа
- Соберет и запустит контейнер

### Ручная установка

```bash
# 1. Подключитесь к серверу
ssh root@your_server_ip

# 2. Установите Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 3. Установите Docker Compose
apt install docker-compose -y

# 4. Клонируйте проект
cd /opt
git clone https://github.com/MikoKyatto/telegram-post-copier.git
cd telegram-post-copier

# 5. Настройте .env
cp env.example .env
nano .env  # Заполните ваши данные

# 6. Установите права
chown -R 1000:1000 .
chmod 777 temp processed_images logs

# 7. Соберите и запустите
docker-compose build --no-cache
docker-compose run --rm copier  # Авторизация
docker-compose up -d

# 8. Проверьте логи
docker-compose logs -f
```

---

## 📋 Полная конфигурация .env

```env
# ═══════════════════════════════════════════════════════════════
# 🔑 TELEGRAM API
# ═══════════════════════════════════════════════════════════════
API_ID=12345678
API_HASH=abcdef1234567890

# ═══════════════════════════════════════════════════════════════
# 📢 КАНАЛЫ
# ═══════════════════════════════════════════════════════════════
SOURCE_CHANNEL=source_channel_username
TARGET_CHANNEL=your_channel_username

# ═══════════════════════════════════════════════════════════════
# 🧠 LLM ПРОВАЙДЕРЫ (можно указать несколько!)
# ═══════════════════════════════════════════════════════════════
LLM_PROVIDER=auto  # auto = пробовать все по очереди
LLM_MODEL=auto     # auto = дефолтная модель провайдера
LLM_TEMPERATURE=0.7

# 🆓 БЕСПЛАТНЫЕ API:
GOOGLE_API_KEY=AIzaSy...           # Google Gemini (60 запросов/мин)
HUGGINGFACE_API_KEY=hf_...         # HuggingFace (бесплатно)
COHERE_API_KEY=...                 # Cohere (trial бесплатно)

# 💰 ПЛАТНЫЕ API (опционально):
DEEPSEEK_API_KEY=sk-...            # DeepSeek ($0.14/1M)
OPENAI_API_KEY=sk-...              # OpenAI ($0.50-2/1M)
XAI_API_KEY=...                    # xAI Grok ($2/1M)

# ═══════════════════════════════════════════════════════════════
# 🔗 БРЕНДИНГ
# ═══════════════════════════════════════════════════════════════
YOUR_LINK=t.me/your_channel
YOUR_BRAND_NAME=XVPN+

# ═══════════════════════════════════════════════════════════════
# 🎯 СТИЛЬ КАНАЛА
# ═══════════════════════════════════════════════════════════════
CHANNEL_STYLE=Информативный стиль о блокировках интернета, с акцентом на обход через VPN, urgently и мотивирующе

# ═══════════════════════════════════════════════════════════════
# ⏱️ НАСТРОЙКИ МОНИТОРИНГА
# ═══════════════════════════════════════════════════════════════
CHECK_INTERVAL=300  # Проверка новых постов каждые 5 минут
MAX_RETRIES=3

# ═══════════════════════════════════════════════════════════════
# 🔍 OCR НАСТРОЙКИ
# ═══════════════════════════════════════════════════════════════
OCR_LANGUAGE=rus+eng
OLD_LINK_PATTERN=t.me/old_channel|t.me/another_old
```

---

## 🔧 Управление ботом

### Основные команды

```bash
# Запуск в фоне
docker-compose up -d

# Остановка
docker-compose down

# Просмотр логов (реального времени)
docker-compose logs -f

# Перезапуск
docker-compose restart

# Пересборка после изменений
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Проверка статуса
docker-compose ps
```

### Использование Makefile

```bash
# Локальный запуск
make run

# Docker запуск
make docker-up

# Первая авторизация
make docker-auth

# Просмотр логов
make logs

# Пуш в GitHub
make git-push

# Деплой на сервер
make deploy SERVER=root@your_ip

# Создание бекапа
make backup-create

# Исправление прав доступа
make fix-permissions
```

---

## 📊 Мониторинг и логи

### Что вы увидите в логах

```
2025-10-23 11:14:20 | INFO | ============================================================
2025-10-23 11:14:20 | INFO | 🦄 TELEGRAM POST COPIER WITH AI
2025-10-23 11:14:20 | INFO | ============================================================
2025-10-23 11:14:20 | INFO | 📅 Запуск: 2025-10-23 11:14:20
2025-10-23 11:14:20 | INFO | 🤖 LLM Provider: auto
2025-10-23 11:14:20 | INFO | ✅ Доступные провайдеры: ['Google Gemini', 'Cohere', 'HuggingFace']
2025-10-23 11:14:20 | INFO | 📡 Source: testomesok
2025-10-23 11:14:20 | INFO | 📢 Target: rynexradar
2025-10-23 11:14:20 | INFO | ============================================================
2025-10-23 11:14:23 | INFO | ✅ Авторизован как: UserName (@username)
2025-10-23 11:14:44 | INFO | ✅ Исходный канал: Source Channel
2025-10-23 11:14:44 | INFO | ✅ Целевой канал: Your Channel
2025-10-23 11:14:45 | INFO | ✨ Система готова к работе!
2025-10-23 11:14:45 | INFO | 🔁 Запуск мониторинга (интервал: 300сек)

2025-10-23 11:21:45 | INFO | 🔄 Обработка поста ID 2
2025-10-23 11:21:45 | INFO | 🧠 AI: Переписывание текста...
2025-10-23 11:21:45 | INFO | 🤖 Попытка через Google Gemini (модель: gemini-pro)...
2025-10-23 11:21:46 | INFO | ✅ Google Gemini: Успешно сгенерирован текст
2025-10-23 11:21:46 | INFO | 📊 Уникальность: 85.2%
2025-10-23 11:21:47 | INFO | 🎨 Обработка изображения...
2025-10-23 11:21:52 | INFO | ✨ Изображение модифицировано (ссылки заменены)
2025-10-23 11:21:53 | INFO | ✅ Пост успешно опубликован!
```

### Логи с автоматическим переключением

```
2025-10-23 11:22:10 | INFO | 🤖 Попытка через Google Gemini...
2025-10-23 11:22:11 | WARNING | ⚠️ Google Gemini: quota exceeded
2025-10-23 11:22:11 | INFO | 🤖 Попытка через Cohere (модель: command)...
2025-10-23 11:22:13 | INFO | ✅ Cohere: Успешно сгенерирован текст
```

---

## 🐛 Troubleshooting

### Проблема: Ошибка при авторизации

**Решение:**
```bash
# Удалите старую сессию
rm temp/copier_session.session*

# Повторите авторизацию
docker-compose run --rm copier
```

### Проблема: Permission denied

**Решение:**
```bash
# На сервере исправьте права
cd /opt/telegram-post-copier
chown -R 1000:1000 .
chmod 777 temp processed_images logs

# Или используйте скрипт
bash fix-permissions-server.sh root@your_ip
```

### Проблема: ModuleNotFoundError

**Решение:**
```bash
# Пересоберите образ
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Проблема: All LLM providers unavailable

**Решение:**
1. Проверьте API ключи в `.env`
2. Убедитесь что хотя бы один ключ валиден
3. Получите бесплатный Google Gemini: https://aistudio.google.com/app/apikey

### Проблема: Не копирует новые посты

**Решение:**
```bash
# Проверьте логи
docker-compose logs -f

# Убедитесь что бот подписан на source канал
# Убедитесь что бот админ в target канале
```

---

## 📁 Структура проекта

```
telegram-post-copier/
├── 📄 copier.py              # Основной скрипт бота
├── 📄 config.py              # Конфигурация
├── 📄 llm_client.py          # LLM клиент (6 провайдеров + fallback)
├── 📄 image_processor.py     # Обработка изображений
├── 📄 utils.py               # Вспомогательные функции
├── 📄 requirements.txt       # Python зависимости
│
├── 🐳 Dockerfile             # Docker образ
├── 🐳 docker-compose.yml     # Docker Compose конфигурация
├── 🐳 docker-entrypoint.sh   # Entrypoint скрипт
├── 🐳 .dockerignore          # Исключения для Docker
│
├── 🔧 env.example            # Пример конфигурации
├── 🔧 .gitignore             # Git исключения
│
├── 🚀 deploy.sh              # Деплой на сервер
├── 🚀 backup.sh              # Создание бекапов
├── 🚀 git-push.sh            # Пуш в GitHub
├── 🚀 first-auth.sh          # Первая авторизация
├── 🚀 fix-permissions-server.sh  # Исправление прав
├── 🚀 FULL_REBUILD_AND_FIX.sh    # Полная пересборка
│
├── 📖 README.md              # Документация (этот файл)
├── 📖 FREE_LLM_SETUP.md      # Гайд по бесплатным LLM
├── 📖 SETUP_GUIDE.md         # Подробная настройка
├── 📖 DEPLOY_GUIDE.md        # Гайд по деплою
├── 📖 QUICKSTART.md          # Быстрый старт
├── 📖 DEMO.md                # Примеры работы
│
├── 📂 temp/                  # Временные файлы
├── 📂 processed_images/      # Обработанные изображения
├── 📂 logs/                  # Логи приложения
│
└── 📜 Makefile               # Автоматизация команд
```

---

## 🔐 Безопасность

### Важно:

1. **Никогда не коммитьте `.env`** файл в Git!
2. **Храните API ключи в безопасности**
3. **Используйте SSH ключи** для доступа к серверу
4. **Регулярно обновляйте** зависимости
5. **Делайте бекапы** сессий и конфигов

### Рекомендации:

```bash
# Создание бекапа
make backup-create

# Бекап будет сохранен в:
# backups/telegram-post-copier_YYYY-MM-DD_HH-MM-SS.tar.gz

# Восстановление из бекапа
tar -xzf backups/telegram-post-copier_*.tar.gz
```

---

## 🚀 Производительность

### Оптимизация для больших каналов

```env
# Увеличьте интервал проверки
CHECK_INTERVAL=600  # 10 минут вместо 5

# Используйте быстрый LLM
LLM_PROVIDER=auto
GOOGLE_API_KEY=...      # Быстрый и бесплатный
DEEPSEEK_API_KEY=...    # Быстрый и дешевый

# Уменьшите температуру для стабильности
LLM_TEMPERATURE=0.5
```

### Мониторинг ресурсов

```bash
# Использование ресурсов
docker stats telegram-post-copier_copier

# Размер логов
du -sh logs/

# Очистка старых логов (если > 100MB)
truncate -s 0 logs/copier.log
```

---

## 🤝 Contributing

Мы приветствуем вклад в проект! См. [CONTRIBUTING.md](CONTRIBUTING.md)

### Как помочь проекту:

1. 🐛 **Сообщайте об ошибках** через Issues
2. 💡 **Предлагайте новые фичи**
3. 📝 **Улучшайте документацию**
4. 🔧 **Отправляйте Pull Requests**

---

## 📜 License

MIT License - см. [LICENSE](LICENSE)

---

## ❓ FAQ

### Q: Можно ли использовать полностью бесплатно?

**A:** Да! Google Gemini, HuggingFace и Cohere (trial) - все бесплатные. Этого хватит для большинства каналов.

### Q: Сколько постов может обработать в день?

**A:** С Google Gemini (60 запросов/мин) - до **1500 постов в день** бесплатно!

### Q: Нужен ли VPN для работы?

**A:** Зависит от вашего региона. Telegram API обычно доступен без VPN.

### Q: Можно ли запустить несколько ботов?

**A:** Да! Просто создайте отдельные директории с разными `.env` конфигурациями.

### Q: Бот копирует все посты или только новые?

**A:** Только новые посты после запуска. Старые посты можно скопировать вручную, указав начальный ID.

### Q: Как изменить стиль переписывания?

**A:** Отредактируйте `CHANNEL_STYLE` в `.env`:
```env
CHANNEL_STYLE=Краткий новостной стиль, факты без эмоций
# или
CHANNEL_STYLE=Эмоциональный, срочный стиль для блокировок
```

### Q: Работает ли с приватными каналами?

**A:** Да, если ваш аккаунт подписан на приватный канал.

### Q: Можно ли отключить AI обработку?

**A:** В текущей версии нет, но можно закомментировать вызовы `rewrite_text()` в `copier.py`.

---

## 📞 Поддержка

- 📧 **Email:** support@example.com
- 💬 **Telegram:** @your_support_bot
- 🐛 **Issues:** https://github.com/MikoKyatto/telegram-post-copier/issues
- 📖 **Документация:** [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

## 🌟 Благодарности

Проект использует:
- [Telethon](https://github.com/LonamiWebs/Telethon) - Telegram API
- [OpenAI Python](https://github.com/openai/openai-python) - OpenAI API
- [Google Generative AI](https://ai.google.dev/) - Gemini API
- [Cohere Python](https://github.com/cohere-ai/cohere-python) - Cohere API
- [HuggingFace Hub](https://github.com/huggingface/huggingface_hub) - HF API
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - OCR
- [OpenCV](https://opencv.org/) - Computer Vision
- [Pillow](https://python-pillow.org/) - Image Processing

---

## 📈 Roadmap

- [ ] Web UI для управления ботом
- [ ] Поддержка видео контента
- [ ] Расписание публикаций
- [ ] Аналитика эффективности постов
- [ ] Интеграция с другими платформами (VK, Twitter)
- [ ] A/B тестирование разных версий постов
- [ ] Автоматическая генерация хештегов

---

<p align="center">
  <b>Сделано с ❤️ для автоматизации контента</b><br>
  <sub>© 2025 Telegram Post Copier. Unicorn Edition 🦄</sub>
</p>

<p align="center">
  <a href="#-quick-start-5-минут-до-запуска">⬆ Вернуться к началу</a>
</p>
