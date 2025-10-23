"""
🧠 LLM Client - Универсальный клиент для работы с разными LLM провайдерами
Поддержка: OpenAI, DeepSeek, xAI Grok
"""

import requests
from typing import Optional
from config import Config
import logging

logger = logging.getLogger(__name__)


class LLMClient:
    """Универсальный клиент для работы с LLM API"""
    
    def __init__(self):
        self.provider = Config.LLM_PROVIDER.lower()
        self.model = Config.LLM_MODEL
        self.temperature = Config.LLM_TEMPERATURE
        
        # Инициализация в зависимости от провайдера
        if self.provider == 'openai':
            from openai import OpenAI
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            self.api_type = 'openai'
        elif self.provider == 'deepseek':
            # DeepSeek использует OpenAI-совместимый API
            from openai import OpenAI
            self.client = OpenAI(
                api_key=Config.DEEPSEEK_API_KEY,
                base_url="https://api.deepseek.com"
            )
            self.api_type = 'openai'
        elif self.provider == 'xai':
            # xAI Grok тоже использует OpenAI-совместимый API
            from openai import OpenAI
            self.client = OpenAI(
                api_key=Config.XAI_API_KEY,
                base_url="https://api.x.ai/v1"
            )
            self.api_type = 'openai'
        else:
            raise ValueError(f"Неподдерживаемый провайдер: {self.provider}")
    
    def rewrite_text(self, original_text: str, has_links: bool = True) -> str:
        """
        Переписывает текст поста, делая его уникальным
        
        Args:
            original_text: Оригинальный текст поста
            has_links: Есть ли в тексте ссылки для замены
            
        Returns:
            Переписанный уникальный текст
        """
        try:
            if not original_text or len(original_text.strip()) < 10:
                return original_text
            
            # Формируем промпт в зависимости от наличия ссылок
            if has_links:
                prompt = self._build_rewrite_prompt_with_links(original_text)
            else:
                prompt = self._build_rewrite_prompt_simple(original_text)
            
            # Вызов API
            if self.api_type == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "Ты - профессиональный SMM-специалист, который умеет переписывать посты, сохраняя смысл, но делая их уникальными и авторскими."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=self.temperature,
                    max_tokens=1000
                )
                return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Ошибка при переписывании текста: {e}")
            # Возвращаем оригинал в случае ошибки
            return original_text
    
    def _build_rewrite_prompt_with_links(self, text: str) -> str:
        """Строит промпт для текста со ссылками"""
        return f"""Перепиши этот текст о блокировках интернета так, чтобы он был уникальным, но сохранял весь смысл:

ОРИГИНАЛЬНЫЙ ТЕКСТ:
{text}

ТРЕБОВАНИЯ:
1. Замени ВСЕ ссылки (t.me/..., https://...) на "{Config.YOUR_LINK}"
2. Перефразируй текст, сохраняя все факты и детали
3. Добавь короткий призыв к действию про VPN в конце (1-2 предложения)
4. Используй стиль: {Config.CHANNEL_STYLE}
5. Упомяни "{Config.YOUR_BRAND_NAME}" как решение проблемы
6. Сохрани все важные данные: регионы, провайдеры, время
7. Сделай текст живым и срочным, но информативным
8. НЕ используй фразы типа "по данным мониторинга" - пиши от своего лица

ПЕРЕПИСАННЫЙ ТЕКСТ:"""
    
    def _build_rewrite_prompt_simple(self, text: str) -> str:
        """Строит промпт для текста без ссылок"""
        return f"""Слегка перефразируй этот текст о блокировках интернета, сохраняя все факты:

ОРИГИНАЛЬНЫЙ ТЕКСТ:
{text}

ТРЕБОВАНИЯ:
1. Сохрани все данные: регионы, провайдеры, время
2. Слегка измени формулировки
3. Добавь упоминание "{Config.YOUR_BRAND_NAME}" как решения (естественно)
4. Используй стиль: {Config.CHANNEL_STYLE}
5. Сделай текст немного более живым

ПЕРЕПИСАННЫЙ ТЕКСТ:"""
    
    def check_uniqueness(self, original: str, rewritten: str) -> float:
        """
        Оценивает уникальность переписанного текста (примерно)
        
        Returns:
            Процент различия (0-100)
        """
        # Простая оценка на основе различающихся слов
        original_words = set(original.lower().split())
        rewritten_words = set(rewritten.lower().split())
        
        if not original_words:
            return 0.0
        
        different_words = rewritten_words - original_words
        uniqueness = (len(different_words) / len(original_words)) * 100
        
        return min(uniqueness, 100.0)
    
    def enhance_with_cta(self, text: str) -> str:
        """
        Добавляет Call-to-Action если его нет
        
        Args:
            text: Текст поста
            
        Returns:
            Текст с CTA
        """
        try:
            prompt = f"""Добавь короткий Call-to-Action (призыв к действию) в конец этого текста:

ТЕКСТ:
{text}

ТРЕБОВАНИЯ:
1. CTA должен быть про защиту от блокировок через VPN
2. Упомяни "{Config.YOUR_BRAND_NAME}"
3. Добавь ссылку "{Config.YOUR_LINK}"
4. Максимум 2 предложения
5. Естественно вписывается в текст

ТЕКСТ С CTA:"""
            
            if self.api_type == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=500
                )
                return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Ошибка при добавлении CTA: {e}")
            # Добавляем простой CTA вручную
            return f"{text}\n\n🔒 Защититесь от блокировок с {Config.YOUR_BRAND_NAME}: {Config.YOUR_LINK}"
    

# Singleton instance
_llm_client = None

def get_llm_client() -> LLMClient:
    """Получить глобальный экземпляр LLM клиента"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client

