# 🚨 КРИТИЧЕСКАЯ ОШИБКА - ДИСК ПЕРЕПОЛНЕН!

## ❌ Проблема

```
OSError: [Errno 28] No space left on device
sqlite3.OperationalError: database or disk is full
```

**На сервере закончилось место на диске!** Логи и временные файлы заполнили все свободное пространство.

---

## 🚀 СРОЧНОЕ РЕШЕНИЕ (2 минуты)

### 1. Подключитесь к серверу и запустите скрипт очистки:

```bash
ssh root@80.92.204.27
cd /opt/telegram-post-copier

# Скачайте обновленный код
git pull origin main

# Запустите скрипт экстренной очистки
bash EMERGENCY_DISK_CLEANUP.sh
```

Скрипт автоматически:
- ✅ Остановит контейнеры
- ✅ Очистит неиспользуемые Docker образы и volumes
- ✅ Удалит логи Docker контейнеров
- ✅ Очистит системные логи (journalctl)
- ✅ Удалит старые логи приложения
- ✅ Очистит обработанные изображения
- ✅ Очистит APT кеш

---

## 📊 Проверка места на диске

### До очистки:
```bash
df -h
```

### После очистки:
Скрипт автоматически покажет результат.

---

## 🔄 Запуск после очистки

```bash
# Пересоберите с новой версией (с ротацией логов)
docker-compose build --no-cache

# Запустите
docker-compose up -d

# Проверьте логи
docker-compose logs -f --tail 50
```

---

## ✅ Что исправлено в коде

### Добавлена ротация логов:

```python
from logging.handlers import RotatingFileHandler

# Ротация: макс 10MB на файл, хранить 5 файлов = макс 50MB
file_handler = RotatingFileHandler(
    'logs/copier.log',
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5  # Хранить 5 файлов
)
```

**Теперь логи не будут бесконечно расти!**

---

## 🔍 Дополнительная диагностика

### Найти самые большие файлы:

```bash
du -h /opt/telegram-post-copier | sort -rh | head -20
du -h /var/lib/docker | sort -rh | head -20
```

### Очистить логи вручную:

```bash
# Логи приложения
rm -f /opt/telegram-post-copier/logs/*.log*

# Логи Docker
docker system prune -af --volumes

# Логи systemd
journalctl --vacuum-time=1d
```

---

## 🛡️ Профилактика

### Настройте автоматическую очистку (cron):

```bash
# Открыть crontab
crontab -e

# Добавить задачу (очистка каждую неделю в воскресенье в 3:00)
0 3 * * 0 cd /opt/telegram-post-copier && bash EMERGENCY_DISK_CLEANUP.sh >> /var/log/cleanup.log 2>&1
```

---

## 📋 Чеклист

- [ ] Запустить `EMERGENCY_DISK_CLEANUP.sh`
- [ ] Проверить свободное место: `df -h`
- [ ] Обновить код: `git pull origin main`
- [ ] Пересобрать: `docker-compose build --no-cache`
- [ ] Запустить: `docker-compose up -d`
- [ ] Проверить работу: `docker-compose logs -f`
- [ ] Настроить автоочистку через cron (опционально)

---

## 🎯 Результат

После выполнения:
- ✅ Диск освобожден
- ✅ Логи ротируются автоматически
- ✅ Максимальный размер логов: 50 MB (5 файлов × 10 MB)
- ✅ Проблема не повторится

**Время решения: 2-5 минут**

