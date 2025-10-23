# 🔧 ИСПРАВЛЕНИЕ .env - Ваши ключи перепутаны!

## ❌ ПРОБЛЕМА В ВАШЕМ .env:

```env
GROQ_API_KEY=xai-bG3bs3RlYhA8...  ← ЭТО КЛЮЧ ОТ xAI!!!
```

**Groq** и **xAI** - это РАЗНЫЕ сервисы!
- Groq: ключ начинается с `gsk_`
- xAI: ключ начинается с `xai-`

---

## ✅ ПРАВИЛЬНАЯ КОНФИГУРАЦИЯ:

### 1. Получите НАСТОЯЩИЙ ключ Groq (2 минуты):

1. Перейдите: **https://console.groq.com/keys**
2. Войдите через Google/GitHub
3. Нажмите **"Create API Key"**
4. Скопируйте ключ (начинается с `gsk_...`)

### 2. Исправьте .env на сервере:

```bash
ssh root@80.92.204.27
cd /opt/telegram-post-copier
nano .env
```

Замените строки:

```env
# БЫЛО (НЕПРАВИЛЬНО):
GROQ_API_KEY=xai-bG3bs3RlYhA8...

# ДОЛЖНО БЫТЬ:
GROQ_API_KEY=gsk_ваш_реальный_ключ_groq

# И если хотите использовать xAI, добавьте отдельно:
XAI_API_KEY=xai-bG3bs3RlYhA8...  # ваш ключ от xAI
```

---

## 📝 ПРОВЕРЬТЕ ДРУГИЕ КЛЮЧИ:

Ваш текущий .env:

✅ **OPENAI_API_KEY** - правильный формат (`sk-proj-...`)
✅ **DEEPSEEK_API_KEY** - правильный формат (`sk-...`)
❌ **GROQ_API_KEY** - НЕПРАВИЛЬНО! Это ключ от xAI
✅ **GOOGLE_API_KEY** - правильный формат (`AIzaSy...`)
✅ **COHERE_API_KEY** - правильный формат
✅ **HUGGINGFACE_API_KEY** - правильный формат (`hf_...`)

---

## 🚀 ПОСЛЕ ИСПРАВЛЕНИЯ:

```bash
# Перезапустите бота
docker-compose restart

# Смотрите логи
docker-compose logs -f
```

Вы увидите:
```
🧪 Тестирование Groq...
✅ Groq: РАБОТАЕТ
🧪 Тестирование Google Gemini...
✅ Google Gemini: РАБОТАЕТ
🧪 Тестирование HuggingFace...
✅ HuggingFace: РАБОТАЕТ
🧪 Тестирование DeepSeek...
❌ DeepSeek: не прошел тест (Insufficient Balance)
🧪 Тестирование OpenAI...
❌ OpenAI: не прошел тест (exceeded quota)

✅ Доступные LLM провайдеры: ['Groq', 'Google Gemini', 'HuggingFace']
```

---

## 💡 ПОЧЕМУ НЕ РАБОТАЛИ:

1. **Groq** - у вас был ключ от xAI вместо Groq
2. **DeepSeek** - нет баланса (402 Payment Required)
3. **OpenAI** - превышена квота (429 Too Many Requests)
4. **Google Gemini** - ДОЛЖЕН РАБОТАТЬ с вашим ключом!
5. **HuggingFace** - ДОЛЖЕН РАБОТАТЬ с вашим ключом!

---

## 🎯 МИНИМАЛЬНАЯ РАБОЧАЯ КОНФИГУРАЦИЯ:

Для "запустил и забыл" оставьте ТОЛЬКО бесплатные:

```env
LLM_PROVIDER=auto
LLM_MODEL=auto

# БЕСПЛАТНЫЕ (получите Groq!):
GROQ_API_KEY=gsk_ваш_новый_ключ     # Получите: https://console.groq.com/keys
GOOGLE_API_KEY=AIzaSyDipRA...       # У вас есть!
HUGGINGFACE_API_KEY=hf_bQAsVU...    # У вас есть!

# Остальные можно закомментировать если нет баланса:
# DEEPSEEK_API_KEY=...
# OPENAI_API_KEY=...
```

---

## ⏱️ ПЛАН ДЕЙСТВИЙ (5 минут):

1. Получите ключ Groq: https://console.groq.com/keys (2 мин)
2. На сервере: `nano .env` → исправьте GROQ_API_KEY (1 мин)
3. Перезапустите: `docker-compose restart` (1 мин)
4. Проверьте: `docker-compose logs -f` (1 мин)

После этого у вас будет 3 РАБОЧИХ бесплатных LLM!

