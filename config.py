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
    SESSION_NAME = 'copier_session'
    
    # 📢 Каналы
    SOURCE_CHANNEL = os.getenv('SOURCE_CHANNEL', '')
    TARGET_CHANNEL = os.getenv('TARGET_CHANNEL', '')
    
    # 🧠 LLM Configuration
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'deepseek')  # openai, deepseek, xai
    LLM_MODEL = os.getenv('LLM_MODEL', 'deepseek-chat')
    LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', '0.7'))
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
    XAI_API_KEY = os.getenv('XAI_API_KEY', '')
    
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
            
        # Проверка наличия хотя бы одного API ключа для LLM
        if cls.LLM_PROVIDER == 'openai' and not cls.OPENAI_API_KEY:
            errors.append("❌ OPENAI_API_KEY не установлен")
        elif cls.LLM_PROVIDER == 'deepseek' and not cls.DEEPSEEK_API_KEY:
            errors.append("❌ DEEPSEEK_API_KEY не установлен")
        elif cls.LLM_PROVIDER == 'xai' and not cls.XAI_API_KEY:
            errors.append("❌ XAI_API_KEY не установлен")
            
        return errors


# Создание временных директорий
os.makedirs(Config.TEMP_DIR, exist_ok=True)
os.makedirs(Config.PROCESSED_DIR, exist_ok=True)

