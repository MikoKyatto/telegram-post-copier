# 🔧 Исправление HuggingFace токена

## ❌ Проблема

```
⚠️ HuggingFace: HTTP 403: This authentication method does not have sufficient permissions to call Inference Providers
```

**Ваш токен не имеет прав на Inference API!**

---

## ✅ Решение (2 минуты)

### 1. Создайте новый токен с правильными правами:

1. Перейдите: **https://huggingface.co/settings/tokens**
2. Нажмите **"Create new token"**
3. **ИМЯ**: `telegram-bot-inference`
4. **TYPE**: выберите **"Write"** (не Read!)
   - ⚠️ Это критично! Read-only токены НЕ работают с Inference API
5. Нажмите **"Generate token"**
6. Скопируйте новый токен (начинается с `hf_...`)

### 2. Замените токен в .env на сервере:

```bash
ssh root@80.92.204.27
cd /opt/telegram-post-copier
nano .env
```

Замените:
```env
# БЫЛО (старый токен без прав):
HUGGINGFACE_API_KEY=hf_старый_токен

# ДОЛЖНО БЫТЬ (новый токен с Write правами):
HUGGINGFACE_API_KEY=hf_ваш_новый_токен_с_write_правами
```

### 3. Перезапустите:

```bash
docker-compose restart
docker-compose logs -f
```

---

## 📊 Проверка

В логах должно быть:
```
🧪 Тестирование HuggingFace...
✅ HuggingFace: РАБОТАЕТ
```

Вместо ошибки 403.

---

## 💡 Почему это важно?

- **Read** токены = только чтение моделей/датасетов
- **Write** токены = доступ к Inference API (генерация текста)

Для работы бота нужен **Write** токен!

