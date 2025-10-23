"""
🧠 LLM Client - Универсальный клиент с поддержкой множества провайдеров и автоматическим fallback
Поддержка: OpenAI, DeepSeek, xAI Grok, Google Gemini, Cohere, HuggingFace
"""

import requests
from typing import Optional, List, Dict, Any
from config import Config
import logging

logger = logging.getLogger(__name__)


class LLMProvider:
    """Базовый класс для LLM провайдера"""
    
    def __init__(self, name: str, api_key: str, model: str):
        self.name = name
        self.api_key = api_key
        self.model = model
        self.is_available = bool(api_key)
    
    def generate(self, prompt: str, system_prompt: str = "", temperature: float = 0.7, max_tokens: int = 1000) -> Optional[str]:
        """Генерация текста (должен быть переопределен в наследниках)"""
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    """OpenAI / DeepSeek / xAI (OpenAI-совместимые API)"""
    
    def __init__(self, name: str, api_key: str, model: str, base_url: Optional[str] = None):
        super().__init__(name, api_key, model)
        self.base_url = base_url
        if self.is_available:
            try:
                from openai import OpenAI
                self.client = OpenAI(
                    api_key=api_key,
                    base_url=base_url
                ) if base_url else OpenAI(api_key=api_key)
            except Exception as e:
                logger.warning(f"⚠️ {name}: Не удалось инициализировать клиент: {e}")
                self.is_available = False
    
    def generate(self, prompt: str, system_prompt: str = "", temperature: float = 0.7, max_tokens: int = 1000) -> Optional[str]:
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"⚠️ {self.name}: Ошибка генерации: {e}")
            return None


class GoogleGeminiProvider(LLMProvider):
    """Google AI Studio (Gemini)"""
    
    def __init__(self, name: str, api_key: str, model: str = "gemini-1.5-flash"):
        super().__init__(name, api_key, model)
        if self.is_available:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                self.client = genai.GenerativeModel(model)
            except Exception as e:
                logger.warning(f"⚠️ {name}: Не удалось инициализировать клиент: {e}")
                self.is_available = False
    
    def generate(self, prompt: str, system_prompt: str = "", temperature: float = 0.7, max_tokens: int = 1000) -> Optional[str]:
        try:
            # Gemini не поддерживает отдельный system prompt, комбинируем
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
            
            response = self.client.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            return response.text.strip()
        except Exception as e:
            logger.warning(f"⚠️ {self.name}: Ошибка генерации: {e}")
            return None


class CohereProvider(LLMProvider):
    """Cohere AI"""
    
    def __init__(self, name: str, api_key: str, model: str = "command-r-plus"):
        super().__init__(name, api_key, model)
        if self.is_available:
            try:
                import cohere
                self.client = cohere.Client(api_key)
            except Exception as e:
                logger.warning(f"⚠️ {name}: Не удалось инициализировать клиент: {e}")
                self.is_available = False
    
    def generate(self, prompt: str, system_prompt: str = "", temperature: float = 0.7, max_tokens: int = 1000) -> Optional[str]:
        try:
            # Cohere использует preamble для system prompt
            preamble = system_prompt if system_prompt else None
            
            response = self.client.chat(
                message=prompt,
                preamble=preamble,
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.text.strip()
        except Exception as e:
            logger.warning(f"⚠️ {self.name}: Ошибка генерации: {e}")
            return None


class HuggingFaceProvider(LLMProvider):
    """HuggingFace Inference API"""
    
    def __init__(self, name: str, api_key: str, model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"):
        super().__init__(name, api_key, model)
        self.api_url = f"https://api-inference.huggingface.co/models/{model}"
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def generate(self, prompt: str, system_prompt: str = "", temperature: float = 0.7, max_tokens: int = 1000) -> Optional[str]:
        try:
            # Форматируем промпт
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "temperature": temperature,
                    "max_new_tokens": max_tokens,
                    "return_full_text": False
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").strip()
            return None
        except Exception as e:
            logger.warning(f"⚠️ {self.name}: Ошибка генерации: {e}")
            return None


class LLMClient:
    """Универсальный клиент с автоматическим fallback между провайдерами"""
    
    def __init__(self):
        self.temperature = Config.LLM_TEMPERATURE
        self.providers: List[LLMProvider] = []
        self.current_provider_index = 0
        
        # Инициализация всех доступных провайдеров
        self._initialize_providers()
        
        # Фильтруем только доступные
        self.providers = [p for p in self.providers if p.is_available]
        
        if not self.providers:
            logger.error("❌ Ни один LLM провайдер не доступен! Проверьте API ключи в .env")
            raise ValueError("Нет доступных LLM провайдеров")
        
        logger.info(f"✅ Доступные LLM провайдеры: {[p.name for p in self.providers]}")
    
    def _initialize_providers(self):
        """Инициализация всех провайдеров"""
        
        # Только ПРОВЕРЕННЫЕ рабочие модели
        default_models = {
            "deepseek": "deepseek-chat",
        }
        
        use_custom_model = Config.LLM_MODEL != 'auto' and Config.LLM_PROVIDER != 'auto'
        
        # DeepSeek - РАБОТАЕТ, если есть баланс
        if Config.DEEPSEEK_API_KEY:
            model = Config.LLM_MODEL if (use_custom_model and Config.LLM_PROVIDER == 'deepseek') else default_models["deepseek"]
            self.providers.append(OpenAIProvider("DeepSeek", Config.DEEPSEEK_API_KEY, model, "https://api.deepseek.com"))
    
    def _generate_with_fallback(self, prompt: str, system_prompt: str = "", temperature: float = None, max_tokens: int = 1000) -> Optional[str]:
        """Генерация с автоматическим переключением между провайдерами"""
        if temperature is None:
            temperature = self.temperature
        
        # Пробуем все провайдеры по очереди
        for i, provider in enumerate(self.providers):
            logger.info(f"🤖 Попытка генерации через {provider.name} (модель: {provider.model})...")
            result = provider.generate(prompt, system_prompt, temperature, max_tokens)
            
            if result:
                logger.info(f"✅ {provider.name}: Успешно сгенерирован текст")
                # Переставляем успешный провайдер на первое место для следующего раза
                if i > 0:
                    self.providers[0], self.providers[i] = self.providers[i], self.providers[0]
                return result
            else:
                logger.warning(f"⚠️ {provider.name}: Не удалось сгенерировать, пробуем следующий...")
        
        logger.error("❌ Все LLM провайдеры недоступны!")
        return None
    
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
            
            system_prompt = "Ты - профессиональный SMM-специалист, который умеет переписывать посты, сохраняя смысл, но делая их уникальными и авторскими."
            
            # Вызов с fallback
            result = self._generate_with_fallback(prompt, system_prompt)
            
            if result:
                return result
            else:
                # Если все провайдеры недоступны, возвращаем оригинал с простой модификацией
                logger.warning("⚠️ Используем fallback: простая модификация текста")
                return self._simple_text_modification(original_text)
            
        except Exception as e:
            logger.error(f"Ошибка при переписывании текста: {e}")
            return original_text
    
    def _simple_text_modification(self, text: str) -> str:
        """Простая модификация текста если все LLM недоступны"""
        # Добавляем брендинг и призыв к действию
        modified = f"{text}\n\n🔒 Защитись от блокировок с {Config.YOUR_BRAND_NAME}: {Config.YOUR_LINK}"
        return modified
    
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
            
            result = self._generate_with_fallback(prompt, "", 0.5, 500)
            
            if result:
                return result
            else:
                # Простой CTA вручную
                return f"{text}\n\n🔒 Защититесь от блокировок с {Config.YOUR_BRAND_NAME}: {Config.YOUR_LINK}"
            
        except Exception as e:
            logger.error(f"Ошибка при добавлении CTA: {e}")
            return f"{text}\n\n🔒 Защититесь от блокировок с {Config.YOUR_BRAND_NAME}: {Config.YOUR_LINK}"


# Singleton instance
_llm_client = None

def get_llm_client() -> LLMClient:
    """Получить глобальный экземпляр LLM клиента"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
