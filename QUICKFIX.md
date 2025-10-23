# ⚡ Быстрое исправление для сервера

Если у вас уже развернут проект на сервере и возникла ошибка SQLite:

## 1. Скопируйте новые файлы на сервер:

```bash
# Локально выполните:
scp Dockerfile docker-compose.yml docker-entrypoint.sh first-auth.sh root@YOUR_SERVER_IP:/opt/telegram-post-copier/
```

## 2. На сервере пересоберите контейнер:

```bash
# SSH на сервер
ssh root@YOUR_SERVER_IP

cd /opt/telegram-post-copier

# Остановите старый контейнер
docker-compose down

# Создайте директории с правами
mkdir -p temp processed_images logs
chmod 777 temp processed_images logs

# Пересоберите образ
docker-compose build --no-cache

# Если session файл уже был:
if [ -f "copier_session.session" ]; then
    docker-compose up -d
else
    bash first-auth.sh
fi
```

## 3. Проверьте работу:

```bash
docker-compose logs -f
```

Должно быть:
```
✅ Авторизован как: ...
✅ Исходный канал: ...
🔁 Запуск мониторинга
```

