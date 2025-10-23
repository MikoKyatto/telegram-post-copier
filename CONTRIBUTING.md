# 🤝 Contributing to Telegram Post Copier

Спасибо за интерес к проекту! 🎉

## 🌟 Как внести вклад

### 1. Создание Issue

Если нашли баг или есть идея:
1. Проверьте, нет ли уже такого Issue
2. Создайте новый Issue с описанием
3. Используйте шаблон (если есть)

### 2. Создание Pull Request

1. Fork репозитория
2. Создайте feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Внесите изменения
4. Проверьте код:
   ```bash
   make lint
   make test
   ```
5. Commit:
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. Push:
   ```bash
   git push origin feature/amazing-feature
   ```
7. Создайте Pull Request

## 📝 Стандарты кода

### Python

- Следуйте PEP 8
- Используйте type hints
- Документируйте функции docstrings
- Максимальная длина строки: 100 символов

Пример:
```python
def process_message(message: str, max_length: int = 100) -> str:
    """
    Обрабатывает сообщение
    
    Args:
        message: Исходное сообщение
        max_length: Максимальная длина
        
    Returns:
        Обработанное сообщение
    """
    return message[:max_length]
```

### Commit Messages

Формат:
```
<type>: <description>

<body>
```

Types:
- `feat`: Новая функция
- `fix`: Исправление бага
- `docs`: Документация
- `style`: Форматирование
- `refactor`: Рефакторинг
- `test`: Тесты
- `chore`: Обслуживание

Пример:
```
feat: добавлена поддержка видео

Реализована обработка видео постов с помощью FFmpeg.
Добавлены новые зависимости в requirements.txt.
```

## 🧪 Тестирование

Перед отправкой PR убедитесь:

```bash
# Проверка кода
make lint

# Форматирование
make format

# Тесты
make test
```

## 📚 Документация

При добавлении новых функций:
- Обновите README.md
- Добавьте docstrings в код
- Обновите SETUP_GUIDE.md (если нужно)

## ⚡ Приоритеты

Особенно приветствуются:
- 🐛 Исправления багов
- 📖 Улучшение документации
- 🧪 Добавление тестов
- 🌍 Переводы на другие языки
- ✨ Оптимизация производительности

## 💬 Общение

- GitHub Issues - для багов и feature requests
- GitHub Discussions - для вопросов и идей
- Telegram - для быстрого общения

## 📜 Лицензия

Внося вклад, вы соглашаетесь с MIT License.

---

Спасибо за вклад в проект! 🦄

