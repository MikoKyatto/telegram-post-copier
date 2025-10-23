"""
🔧 Конфигурация проекта Telegram Post Copier
Централизованное управление настройками
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Класс для управления конфигурацией приложения"""
    
    # 🔑 Telegram API
    API_ID = int(os.getenv('API_ID', 0))
    API_HASH = os.getenv('API_HASH', '')
    SESSION_NAME = 'temp/copier_session'  # Используем temp/ директорию с правами 777
    
    # 📢 Каналы
    SOURCE_CHANNEL = os.getenv('SOURCE_CHANNEL', '')
    TARGET_CHANNEL = os.getenv('TARGET_CHANNEL', '')
    
    # 🧠 LLM Configuration (multi-provider with auto-fallback)
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'auto')  # auto, openai, deepseek, xai, google, cohere, huggingface
    LLM_MODEL = os.getenv('LLM_MODEL', 'auto')  # auto or specific model
    LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', '0.7'))
    
    # API Keys (fill in available ones - bot will try all automatically)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
    XAI_API_KEY = os.getenv('XAI_API_KEY', '')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')  # Google AI Studio (Gemini) - FREE
    COHERE_API_KEY = os.getenv('COHERE_API_KEY', '')  # Cohere - has free tier
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')  # HuggingFace - FREE
    
    # 🔗 Брендинг
    YOUR_LINK = os.getenv('YOUR_LINK', 't.me/your_channel')
    YOUR_BRAND_NAME = os.getenv('YOUR_BRAND_NAME', 'Ваш VPN')
    
    # 🎯 Стиль канала
    CHANNEL_STYLE = os.getenv(
        'CHANNEL_STYLE',
        'Информативный стиль о блокировках интернета, с акцентом на обход через VPN'
    )
    
    # ⏱️ Настройки мониторинга
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '300'))  # секунды
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    
    # 🔍 OCR настройки
    OCR_LANGUAGE = os.getenv('OCR_LANGUAGE', 'rus+eng')
    OLD_LINK_PATTERN = os.getenv(
        'OLD_LINK_PATTERN',
        't.me/na_svyazi_helpdesk|t.me/nasvyazi'
    )
    
    # 📁 Пути
    TEMP_DIR = 'temp'
    PROCESSED_DIR = 'processed_images'
    
    @classmethod
    def validate(cls):
        """Валидация критических настроек"""
        errors = []
        
        if not cls.API_ID or cls.API_ID == 0:
            errors.append("❌ API_ID не установлен")
        if not cls.API_HASH:
            errors.append("❌ API_HASH не установлен")
        if not cls.SOURCE_CHANNEL:
            errors.append("❌ SOURCE_CHANNEL не установлен")
        if not cls.TARGET_CHANNEL:
            errors.append("❌ TARGET_CHANNEL не установлен")
            
        # LLM опционально - бот может работать без AI
        has_llm_key = any([
            cls.OPENAI_API_KEY,
            cls.DEEPSEEK_API_KEY,
            cls.XAI_API_KEY,
            cls.GOOGLE_API_KEY,
            cls.COHERE_API_KEY,
            cls.HUGGINGFACE_API_KEY
        ])
        
        if not has_llm_key:
            # Предупреждение, но не ошибка - бот может копировать без AI
            pass
            
        return errors


# Создание временных директорий
os.makedirs(Config.TEMP_DIR, exist_ok=True)
os.makedirs(Config.PROCESSED_DIR, exist_ok=True)

