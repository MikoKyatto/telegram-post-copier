"""
🛠️ Утилиты - вспомогательные функции
"""

import re
import hashlib
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def extract_links(text: str) -> list[str]:
    """
    Извлекает все ссылки из текста
    
    Args:
        text: Текст для поиска
        
    Returns:
        Список найденных ссылок
    """
    # Паттерн для t.me и http(s) ссылок
    pattern = r'(?:https?://|t\.me/)[\w\d\-._~:/?#\[\]@!$&\'()*+,;=]+'
    links = re.findall(pattern, text)
    return links


def replace_links(text: str, old_pattern: str, new_link: str) -> str:
    """
    Заменяет ссылки в тексте
    
    Args:
        text: Исходный текст
        old_pattern: Regex паттерн старой ссылки
        new_link: Новая ссылка
        
    Returns:
        Текст с замененными ссылками
    """
    return re.sub(old_pattern, new_link, text, flags=re.IGNORECASE)


def calculate_text_hash(text: str) -> str:
    """
    Вычисляет хеш текста (для проверки дубликатов)
    
    Args:
        text: Текст
        
    Returns:
        SHA256 хеш
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def clean_text(text: str) -> str:
    """
    Очищает текст от лишних символов
    
    Args:
        text: Исходный текст
        
    Returns:
        Очищенный текст
    """
    # Удаление множественных пробелов
    text = re.sub(r'\s+', ' ', text)
    # Удаление пробелов в начале/конце
    text = text.strip()
    return text


def truncate_text(text: str, max_length: int = 4096, suffix: str = "...") -> str:
    """
    Обрезает текст до максимальной длины (лимит Telegram - 4096)
    
    Args:
        text: Исходный текст
        max_length: Максимальная длина
        suffix: Суффикс для обрезанного текста
        
    Returns:
        Обрезанный текст
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def is_valid_telegram_username(username: str) -> bool:
    """
    Проверяет валидность Telegram username
    
    Args:
        username: Username для проверки
        
    Returns:
        True если валиден
    """
    # Telegram username: 5-32 символа, только буквы, цифры и подчеркивание
    pattern = r'^[a-zA-Z0-9_]{5,32}$'
    return bool(re.match(pattern, username))


def format_telegram_link(username: str) -> str:
    """
    Форматирует Telegram username в полную ссылку
    
    Args:
        username: Username (с @ или без)
        
    Returns:
        Полная ссылка t.me/username
    """
    # Удаляем @ если есть
    username = username.lstrip('@')
    return f"t.me/{username}"


def extract_channel_username(text: str) -> Optional[str]:
    """
    Извлекает username канала из текста/ссылки
    
    Args:
        text: Текст или ссылка
        
    Returns:
        Username или None
    """
    # Паттерны для разных форматов
    patterns = [
        r't\.me/([a-zA-Z0-9_]+)',
        r'@([a-zA-Z0-9_]+)',
        r'telegram\.me/([a-zA-Z0-9_]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    return None


def count_words(text: str) -> int:
    """
    Подсчитывает количество слов в тексте
    
    Args:
        text: Текст
        
    Returns:
        Количество слов
    """
    return len(text.split())


def estimate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """
    Оценивает время чтения текста
    
    Args:
        text: Текст
        words_per_minute: Слов в минуту (средняя скорость чтения)
        
    Returns:
        Время чтения в секундах
    """
    words = count_words(text)
    minutes = words / words_per_minute
    return int(minutes * 60)


class RateLimiter:
    """Простой rate limiter для предотвращения флуда"""
    
    def __init__(self, max_requests: int = 20, time_window: int = 60):
        """
        Args:
            max_requests: Максимум запросов
            time_window: Временное окно в секундах
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    def is_allowed(self) -> bool:
        """
        Проверяет, разрешен ли запрос
        
        Returns:
            True если разрешен
        """
        import time
        
        current_time = time.time()
        
        # Удаляем старые запросы
        self.requests = [
            req_time for req_time in self.requests
            if current_time - req_time < self.time_window
        ]
        
        # Проверяем лимит
        if len(self.requests) < self.max_requests:
            self.requests.append(current_time)
            return True
        
        return False
    
    def wait_time(self) -> float:
        """
        Возвращает время ожидания до следующего доступного запроса
        
        Returns:
            Секунды ожидания
        """
        import time
        
        if not self.requests:
            return 0.0
        
        current_time = time.time()
        oldest_request = min(self.requests)
        wait = self.time_window - (current_time - oldest_request)
        
        return max(0.0, wait)


# Глобальный rate limiter
telegram_rate_limiter = RateLimiter(max_requests=20, time_window=60)

