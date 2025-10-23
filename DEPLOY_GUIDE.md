# 🚀 Руководство по Деплою и Бэкапу

Полное руководство по загрузке на GitHub, деплою на сервер и созданию бэкапов.

---

## 📋 Содержание

1. [Загрузка на GitHub](#1-загрузка-на-github)
2. [Деплой на сервер](#2-деплой-на-сервер)
3. [Создание бэкапов](#3-создание-бэкапов)
4. [Восстановление из бэкапа](#4-восстановление-из-бэкапа)
5. [Обновление на сервере](#5-обновление-на-сервере)

---

## 1. Загрузка на GitHub

### Быстрый метод (рекомендуется):

```bash
bash git-push.sh "Initial commit"
```

### Ручной метод:

```bash
# 1. Инициализация Git (если еще не сделано)
git init

# 2. Добавление remote
git remote add origin https://github.com/MikoKyatto/telegram-post-copier.git

# 3. Добавление всех файлов
git add .

# 4. Коммит
git commit -m "Initial commit with full project"

# 5. Установка главной ветки
git branch -M main

# 6. Push на GitHub
git push -u origin main
```

### Если требуется авторизация:

**Вариант A: HTTPS с токеном**
```bash
# Создайте Personal Access Token: https://github.com/settings/tokens
# Используйте токен вместо пароля при push
```

**Вариант B: SSH**
```bash
# 1. Сгенерируйте SSH ключ
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. Добавьте ключ на GitHub: https://github.com/settings/keys

# 3. Измените remote на SSH
git remote set-url origin git@github.com:MikoKyatto/telegram-post-copier.git

# 4. Push
git push -u origin main
```

---

## 2. Деплой на сервер

### Подготовка сервера:

1. **Создайте VPS** на любом провайдере:
   - DigitalOcean ($6/мес)
   - Hetzner (€4/мес)
   - Vultr ($5/мес)

2. **Минимальные требования:**
   - 1 CPU
   - 1 GB RAM
   - 10 GB Disk
   - Ubuntu 20.04/22.04

### Деплой одной командой:

```bash
bash deploy.sh user@your_server_ip
```

**Например:**
```bash
bash deploy.sh root@45.67.89.123
```

### Что делает скрипт:

1. ✅ Проверяет SSH подключение
2. ✅ Устанавливает Docker и Docker Compose (если нужно)
3. ✅ Создает директорию `/opt/telegram-post-copier`
4. ✅ Копирует все файлы проекта
5. ✅ Копирует `.env` и session файлы
6. ✅ Собирает Docker образ
7. ✅ Запускает контейнер
8. ✅ Показывает логи

### Ручной деплой:

```bash
# 1. Подключитесь к серверу
ssh user@server_ip

# 2. Установите Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 3. Установите Docker Compose
sudo apt-get update
sudo apt-get install -y docker-compose

# 4. Клонируйте проект
git clone https://github.com/MikoKyatto/telegram-post-copier.git
cd telegram-post-copier

# 5. Создайте .env
nano .env
# Заполните все поля

# 6. Первая авторизация (если нужно)
docker-compose run --rm copier python copier.py
# Введите номер телефона и код

# 7. Запуск
docker-compose up -d

# 8. Проверка
docker-compose logs -f
```

---

## 3. Создание бэкапов

### Локальный бэкап:

```bash
bash backup.sh
```

**Что сохраняется:**
- ✅ Все `.py` файлы
- ✅ Вся документация (`.md`)
- ✅ Конфигурация (`.env`)
- ✅ Session файлы (авторизация Telegram)
- ✅ Docker файлы
- ✅ Скрипты

**Куда сохраняется:**
```
backups/telegram-copier-backup-YYYYMMDD_HHMMSS.tar.gz
```

### Бэкап с сервера:

```bash
# Локально выполните:
ssh user@server_ip "cd /opt/telegram-post-copier && bash backup.sh"

# Скопируйте бэкап на локальную машину
scp user@server_ip:/opt/telegram-post-copier/backups/*.tar.gz ./backups/
```

### Автоматические бэкапы (cron):

**На локальной машине:**
```bash
# Открыть crontab
crontab -e

# Добавить строку (бэкап каждый день в 3:00)
0 3 * * * cd /Users/f0x01/Documents/telegram-post-copier && bash backup.sh
```

**На сервере:**
```bash
# SSH на сервер
ssh user@server_ip

# Открыть crontab
crontab -e

# Добавить строку (бэкап каждый день в 3:00)
0 3 * * * cd /opt/telegram-post-copier && bash backup.sh

# Опционально: копировать на другой сервер
0 4 * * * scp /opt/telegram-post-copier/backups/*.tar.gz backup-server:/backups/
```

### Бэкап в облако:

**Dropbox:**
```bash
# Установите Dropbox Uploader
curl -o dropbox_uploader.sh https://raw.githubusercontent.com/andreafabrizi/Dropbox-Uploader/master/dropbox_uploader.sh
chmod +x dropbox_uploader.sh
./dropbox_uploader.sh

# После настройки:
bash backup.sh
./dropbox_uploader.sh upload backups/*.tar.gz /
```

**Google Drive (с rclone):**
```bash
# Установите rclone
curl https://rclone.org/install.sh | sudo bash

# Настройте Google Drive
rclone config

# Загрузите бэкап
bash backup.sh
rclone copy backups/ gdrive:/telegram-copier-backups/
```

---

## 4. Восстановление из бэкапа

### Локальное восстановление:

```bash
# 1. Разархивируйте бэкап
tar -xzf backups/telegram-copier-backup-YYYYMMDD_HHMMSS.tar.gz

# 2. Перейдите в директорию
cd telegram-copier-backup-YYYYMMDD_HHMMSS

# 3. Запустите скрипт восстановления
bash restore.sh
```

**Скрипт восстановления:**
- ✅ Создаст директорию `../telegram-post-copier-restored`
- ✅ Скопирует все файлы
- ✅ Установит правильные права доступа
- ✅ Создаст необходимые директории

### Восстановление на сервере:

```bash
# 1. Скопируйте бэкап на сервер
scp backups/telegram-copier-backup-*.tar.gz user@server_ip:/tmp/

# 2. SSH на сервер
ssh user@server_ip

# 3. Разархивируйте
cd /tmp
tar -xzf telegram-copier-backup-*.tar.gz
cd telegram-copier-backup-*

# 4. Восстановите
bash restore.sh

# 5. Перейдите в восстановленную директорию
cd ../telegram-post-copier-restored

# 6. Запустите
docker-compose up -d
```

---

## 5. Обновление на сервере

### Метод 1: Git Pull (рекомендуется)

```bash
# На сервере
ssh user@server_ip
cd /opt/telegram-post-copier

# Остановить контейнер
docker-compose down

# Создать бэкап перед обновлением
bash backup.sh

# Получить обновления
git pull origin main

# Пересобрать образ
docker-compose build

# Запустить
docker-compose up -d

# Проверить логи
docker-compose logs -f
```

### Метод 2: Повторный деплой

```bash
# Локально
bash deploy.sh user@server_ip
```

### Метод 3: Ручное копирование файлов

```bash
# Локально
rsync -avz --exclude '.git' ./ user@server_ip:/opt/telegram-post-copier/

# На сервере
ssh user@server_ip
cd /opt/telegram-post-copier
docker-compose down
docker-compose build
docker-compose up -d
```

---

## 🔧 Полезные команды

### Управление на сервере:

```bash
# Статус
docker-compose ps

# Логи
docker-compose logs -f

# Последние 100 строк логов
docker-compose logs --tail=100

# Перезапуск
docker-compose restart

# Остановка
docker-compose down

# Полная очистка и перезапуск
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Мониторинг:

```bash
# Использование ресурсов
docker stats

# Дисковое пространство
df -h

# Логи системы
journalctl -u docker -f
```

### Очистка:

```bash
# Удаление старых Docker образов
docker system prune -a

# Удаление старых бэкапов (старше 30 дней)
find backups/ -name "*.tar.gz" -mtime +30 -delete
```

---

## 📊 Чеклист деплоя

### Перед деплоем:

- [ ] ✅ Все файлы закоммичены в Git
- [ ] ✅ Загружено на GitHub (`bash git-push.sh`)
- [ ] ✅ Создан бэкап (`bash backup.sh`)
- [ ] ✅ `.env` файл заполнен правильно
- [ ] ✅ Session файл создан (первая авторизация)
- [ ] ✅ Проверена конфигурация (`python test_config.py`)

### Деплой:

- [ ] ✅ VPS создан и доступен по SSH
- [ ] ✅ Выполнен деплой (`bash deploy.sh`)
- [ ] ✅ Контейнер запущен
- [ ] ✅ Логи проверены (нет ошибок)

### После деплоя:

- [ ] ✅ Создан тестовый пост
- [ ] ✅ Пост успешно скопирован
- [ ] ✅ Настроен автоматический бэкап (cron)
- [ ] ✅ Бэкап скопирован в безопасное место

---

## 🆘 Troubleshooting

### Проблема: Git push требует авторизацию

**Решение:**
```bash
# Используйте SSH
git remote set-url origin git@github.com:MikoKyatto/telegram-post-copier.git
```

### Проблема: SSH не подключается к серверу

**Решение:**
```bash
# Проверьте SSH ключ
ssh-keygen -t ed25519
ssh-copy-id user@server_ip
```

### Проблема: Docker не запускается на сервере

**Решение:**
```bash
# Переустановите Docker
sudo apt-get remove docker docker-engine docker.io containerd runc
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Проблема: Нет места на диске

**Решение:**
```bash
# Очистите Docker
docker system prune -a

# Удалите старые логи
find . -name "*.log" -mtime +7 -delete
```

---

## 📚 Дополнительные ресурсы

- [Основная документация](README.md)
- [Инструкция для новичков](SETUP_GUIDE.md)
- [Быстрый старт](GET_STARTED.md)
- [Структура проекта](PROJECT_STRUCTURE.md)

---

<div align="center">

**🦄 Удачного деплоя!**

Made with 💜

</div>

