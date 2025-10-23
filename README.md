<<<<<<< HEAD
# telegram-post-copier
""" 🤖 Telegram Post Copier with AI Agent Автоматическое копирование и AI-обработка постов из Telegram каналов """
# 🦄 Telegram Post Copier with AI

> **Революционизируем контент-автоматизацию для Telegram каналов**

Автоматическое копирование и AI-трансформация постов из любого Telegram канала в ваш собственный. Никаких дубликатов, только уникальный контент с вашим брендингом.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Что это такое?

**Telegram Post Copier** — это не просто скрипт для копирования постов. Это полноценная AI-платформа, которая:

- 🤖 **Переписывает тексты** с помощью LLM (DeepSeek, OpenAI, xAI Grok) - никаких дубликатов!
- 🎨 **Обрабатывает изображения** через OCR + CV - заменяет чужие ссылки на ваши
- 📊 **Проверяет уникальность** контента перед публикацией
- 🔄 **Работает 24/7** в Docker-контейнере
- 💰 **Бесплатные опции** - поддержка DeepSeek и других бюджетных LLM
- 🎯 **Добавляет Call-to-Action** с вашим брендингом и ссылками

### Идеально для:
- 📱 VPN-сервисов, которые мониторят блокировки
- 📰 Новостных каналов с агрегацией контента
- 💼 SMM-агентств, управляющих множеством каналов
- 🔐 Любых проектов, требующих автоматизации Telegram

---

## ✨ Ключевые фичи

### 🧠 AI-Powered Rewriting
```python
Оригинал:
"Ограничения в регионах Москва и СПб. 
Подробнее: t.me/old_channel"

После AI обработки:
"🚨 Внимание! Новые блокировки зафиксированы в Москве 
и Санкт-Петербурге. Обходите ограничения безопасно с 
нашим VPN: t.me/your_channel 🔒"
```

### 🎨 Smart Image Processing
- **OCR-детекция** текста на изображениях (Tesseract)
- **Inpainting** для удаления старых ссылок/логотипов
- **Автоматическое наложение** вашего брендинга
- Поддержка русского и английского языков

### 🔌 Flexible LLM Support
Выбирайте провайдера под ваш бюджет:

| Провайдер | Стоимость | Качество | Рекомендация |
|-----------|-----------|----------|--------------|
| **DeepSeek** | ~$0.001/пост | ⭐⭐⭐⭐ | ✅ Лучший выбор |
| OpenAI GPT-4 | ~$0.03/пост | ⭐⭐⭐⭐⭐ | Премиум качество |
| xAI Grok | ~$0.02/пост | ⭐⭐⭐⭐ | Новый, быстрый |

---

## 🎯 Quick Start

### Шаг 1: Получение Telegram API ключей

1. Перейдите на https://my.telegram.org
2. Введите номер телефона → Получите код в Telegram
3. Выберите **"API development tools"**
4. Создайте приложение:
   - **App title**: `InternetBlockagesCopier`
   - **Platform**: `Other`
5. Сохраните `api_id` и `api_hash` 🔑

### Шаг 2: Регистрация в LLM провайдере

#### Вариант A: DeepSeek (рекомендуется 💰)
1. Зайдите на https://platform.deepseek.com/
2. Регистрация → Получите API key
3. Бесплатный кредит на старте!

#### Вариант B: OpenAI
1. https://platform.openai.com/
2. Создайте API key
3. Добавьте баланс (от $5)

#### Вариант C: xAI Grok
1. https://x.ai/api
2. Early access → API key

### Шаг 3: Клонирование и настройка

```bash
# Клонирование репозитория
git clone https://github.com/yourusername/telegram-post-copier.git
cd telegram-post-copier

# Создание .env файла
cp env.example .env

# Редактирование .env
nano .env
```

Заполните `.env`:

```bash
# 🔑 Telegram API
API_ID=12345678
API_HASH=your_api_hash_here

# 📢 Каналы
SOURCE_CHANNEL=nasvyazi_helpdesk  # Канал источник
TARGET_CHANNEL=your_vpn_channel   # Ваш канал

# 🧠 LLM Configuration
LLM_PROVIDER=deepseek             # deepseek, openai, xai
DEEPSEEK_API_KEY=sk-xxxxx         # Ваш ключ

# 🔗 Брендинг
YOUR_LINK=t.me/your_channel
YOUR_BRAND_NAME=Ваш VPN Сервис
```

### Шаг 4: Первый запуск (локально)

```bash
# Установка зависимостей
pip install -r requirements.txt

# Для Linux/Mac: установка Tesseract
sudo apt install tesseract-ocr tesseract-ocr-rus  # Ubuntu/Debian
brew install tesseract tesseract-lang               # macOS

# Для Windows: скачайте с
# https://github.com/UB-Mannheim/tesseract/wiki

# Запуск
python copier.py
```

При первом запуске:
1. Введите номер телефона
2. Получите код из Telegram
3. Введите код → Авторизация сохранится в `.session` файле

### Шаг 5: Деплой в Docker (production)

```bash
# Сборка образа
docker-compose build

# ВАЖНО: Первая авторизация вручную
docker-compose run --rm copier python copier.py
# → Введите код от Telegram

# Запуск в фоне
docker-compose up -d

# Проверка логов
docker-compose logs -f copier
```

---

## 📁 Структура проекта

```
telegram-post-copier/
├── 🤖 copier.py              # Основной скрипт
├── 🧠 llm_client.py          # LLM интеграция
├── 🎨 image_processor.py     # Обработка изображений
├── ⚙️ config.py              # Конфигурация
├── 📦 requirements.txt       # Python зависимости
├── 🐳 Dockerfile             # Docker образ
├── 🐳 docker-compose.yml     # Docker Compose
├── 📄 env.example            # Пример конфигурации
├── 🙈 .gitignore             # Git ignore
└── 📖 README.md              # Эта документация
```

---

## ⚙️ Продвинутая конфигурация

### Настройка интервала проверки

В `.env`:
```bash
CHECK_INTERVAL=300  # Проверка каждые 5 минут (в секундах)
```

### Настройка стиля канала

```bash
CHANNEL_STYLE="Энергичный и мотивирующий стиль о технологиях, 
с фокусом на свободу интернета и privacy"
```

AI будет адаптировать все посты под этот стиль!

### Настройка OCR

```bash
OCR_LANGUAGE=rus+eng                              # Языки для распознавания
OLD_LINK_PATTERN=t.me/old_channel|example\.com   # Regex паттерн для замены
```

### Настройка температуры LLM

```bash
LLM_TEMPERATURE=0.7  # 0.0-1.0, чем выше - тем креативнее
```

---

## 🛠️ Команды управления

### Docker Compose

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Логи (real-time)
docker-compose logs -f copier

# Логи (последние 100 строк)
docker-compose logs --tail=100 copier

# Статус
docker-compose ps

# Пересборка после изменений
docker-compose up -d --build
```

### Управление данными

```bash
# Бэкап сессии (ВАЖНО!)
cp copier_session.session copier_session.session.backup

# Очистка временных файлов
rm -rf temp/* processed_images/*

# Очистка логов
rm copier.log
```

---

## 📊 Мониторинг и логи

### Структура логов

```
2025-10-23 14:30:15 | INFO | copier | 🚀 TelegramPostCopier инициализирован
2025-10-23 14:30:16 | INFO | copier | 🔐 Подключение к Telegram...
2025-10-23 14:30:17 | INFO | copier | ✅ Авторизован как: John Doe (@johndoe)
2025-10-23 14:30:18 | INFO | copier | 📡 Подключение к исходному каналу: nasvyazi_helpdesk
2025-10-23 14:30:19 | INFO | copier | ✅ Исходный канал: На связи Helpdesk
2025-10-23 14:30:20 | INFO | copier | 📢 Подключение к целевому каналу: your_channel
2025-10-23 14:30:21 | INFO | copier | ✅ Целевой канал: Your VPN Channel
2025-10-23 14:30:22 | INFO | copier | 🔁 Запуск мониторинга (интервал: 300сек)
2025-10-23 14:35:22 | INFO | copier | 🔄 Обработка поста ID 12345
2025-10-23 14:35:23 | INFO | llm_client | 🧠 AI: Переписывание текста...
2025-10-23 14:35:25 | INFO | llm_client | 📊 Уникальность: 78.5%
2025-10-23 14:35:26 | INFO | image_processor | 🎨 Обработка изображения...
2025-10-23 14:35:27 | INFO | image_processor | ✨ Изображение модифицировано (ссылки заменены)
2025-10-23 14:35:28 | INFO | copier | ✅ Пост ID 12345 успешно скопирован
```

### Healthcheck

Docker автоматически проверяет здоровье контейнера:

```bash
# Проверка статуса
docker inspect telegram-post-copier | grep Health
```

---

## 🔒 Безопасность

### Важные файлы для защиты

- ⚠️ `.env` - **НИКОГДА** не коммитить в Git
- ⚠️ `*.session` - Содержит авторизацию Telegram
- ⚠️ `copier.log` - Может содержать чувствительную информацию

### Best Practices

```bash
# Права доступа к .env
chmod 600 .env

# Права доступа к session файлам
chmod 600 *.session

# Добавлено в .gitignore
.env
*.session
*.session-journal
```

---

## 🐛 Troubleshooting

### Проблема: "API_ID не установлен"

**Решение**: Проверьте `.env` файл:
```bash
cat .env | grep API_ID
```
Убедитесь, что `API_ID` — это число (без кавычек).

### Проблема: "Tesseract not found"

**Решение Linux**:
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-rus
```

**Решение macOS**:
```bash
brew install tesseract tesseract-lang
```

**Решение Windows**:
1. Скачайте: https://github.com/UB-Mannheim/tesseract/wiki
2. Установите в `C:\Program Files\Tesseract-OCR`
3. Добавьте в PATH

### Проблема: "FloodWaitError"

**Объяснение**: Telegram ограничивает частоту запросов.

**Решение**: Увеличьте `CHECK_INTERVAL` в `.env`:
```bash
CHECK_INTERVAL=600  # 10 минут
```

### Проблема: "Не добавляется текст на изображение"

**Причина**: Отсутствует шрифт.

**Решение Linux**:
```bash
sudo apt install fonts-dejavu-core
```

**Решение macOS**: Шрифты уже установлены ✅

### Проблема: "LLM API ошибка"

**Проверка**:
```bash
# DeepSeek
curl https://api.deepseek.com/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"test"}]}'

# OpenAI
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"test"}]}'
```

---

## 🚀 Production Deployment

### На VPS/Dedicated сервере

```bash
# 1. Подключение к серверу
ssh user@your-server.com

# 2. Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 3. Установка Docker Compose
sudo apt install docker-compose

# 4. Клонирование проекта
git clone https://github.com/yourusername/telegram-post-copier.git
cd telegram-post-copier

# 5. Настройка .env
nano .env

# 6. Первая авторизация
docker-compose run --rm copier python copier.py
# Введите код из Telegram

# 7. Запуск в фоне
docker-compose up -d

# 8. Настройка автозапуска
sudo systemctl enable docker
```

### Auto-restart при падении

Docker Compose уже настроен с `restart: unless-stopped`:

```yaml
restart: unless-stopped
```

Контейнер автоматически перезапустится при:
- Ошибке в приложении
- Перезагрузке сервера
- Обновлении Docker

### Мониторинг в production

```bash
# Установка логирования в syslog
docker-compose logs --tail=100 -f | tee /var/log/telegram-copier.log

# Ротация логов
# Добавьте в /etc/logrotate.d/telegram-copier:
/var/log/telegram-copier.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 root root
}
```

---

## 📈 Масштабирование

### Несколько пар каналов

Создайте несколько `.env` файлов:

```bash
# .env.pair1
SOURCE_CHANNEL=channel1
TARGET_CHANNEL=your_channel1

# .env.pair2  
SOURCE_CHANNEL=channel2
TARGET_CHANNEL=your_channel2
```

И несколько `docker-compose` файлов:

```yaml
# docker-compose.pair1.yml
services:
  copier-pair1:
    env_file: .env.pair1
    # ...

# Запуск
docker-compose -f docker-compose.pair1.yml up -d
docker-compose -f docker-compose.pair2.yml up -d
```

---

## 🤝 Contributing

Contributions are welcome! 🎉

### Как помочь проекту:

1. 🍴 Fork репозитория
2. 🌿 Создайте feature branch: `git checkout -b feature/amazing-feature`
3. 💾 Commit изменения: `git commit -m 'Add amazing feature'`
4. 📤 Push в branch: `git push origin feature/amazing-feature`
5. 🔃 Создайте Pull Request

### Идеи для улучшений:

- [ ] Поддержка видео
- [ ] Web UI для управления
- [ ] Telegram bot для контроля
- [ ] Статистика и аналитика
- [ ] Поддержка множественных каналов
- [ ] A/B тестирование текстов
- [ ] Интеграция с другими LLM (Claude, Llama)

---

## 📜 License

MIT License - делайте что хотите! 🎉

---

## 🙏 Благодарности

- **Telethon** - за отличную библиотеку для Telegram
- **DeepSeek** - за доступный AI
- **OpenCV & Tesseract** - за компьютерное зрение
- **Community** - за поддержку и фидбек

---

## 📞 Поддержка

- 📧 Email: support@yourproject.com
- 💬 Telegram: [@your_support_bot](https://t.me/your_support_bot)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/telegram-post-copier/issues)
- 💼 LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

---

## 🌟 Roadmap

### Q1 2025
- [x] Базовое копирование постов
- [x] AI переписывание текстов
- [x] OCR и обработка изображений
- [x] Docker контейнеризация

### Q2 2025
- [ ] Web интерфейс для управления
- [ ] Поддержка видео и GIF
- [ ] Расширенная аналитика
- [ ] Telegram bot интерфейс

### Q3 2025
- [ ] Поддержка множественных каналов (N→M)
- [ ] A/B тестирование контента
- [ ] Автоматическая оптимизация времени публикации
- [ ] Интеграция с соц. сетями (Twitter, VK)

---

<div align="center">

## ⭐ Нравится проект? Поставьте звезду!

Made with 💜 by [Your Name](https://github.com/yourusername)

**Автоматизируем будущее, один пост за раз** 🚀

</div>

>>>>>>> 9311d57 (commit-startup)
