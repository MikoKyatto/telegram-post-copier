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
    """OpenAI / DeepSeek / xAI / Groq (OpenAI-совместимые API)"""
    
    def __init__(self, name: str, api_key: str, model: str, base_url: Optional[str] = None):
        super().__init__(name, api_key, model)
        self.base_url = base_url
        if self.is_available:
            try:
                from openai import OpenAI
                # ИСПРАВЛЕНИЕ: Правильная инициализация с base_url
                if base_url:
                    self.client = OpenAI(
                        api_key=api_key,
                        base_url=base_url,
                        timeout=30.0  # Добавляем таймаут
                    )
                else:
                    self.client = OpenAI(
                        api_key=api_key,
                        timeout=30.0
                    )
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
                # Убираем префикс models/ если есть
                clean_model = model.replace("models/", "")
                # ИСПРАВЛЕНИЕ: generation_config передается при создании модели, а не в generate_content
                # Используем дефолтные параметры, т.к. temperature будет передаваться в generate()
                self.client = genai.GenerativeModel(clean_model)
                self.genai = genai  # Сохраняем для создания новых моделей с разными параметрами
            except Exception as e:
                logger.warning(f"⚠️ {name}: Не удалось инициализировать клиент: {e}")
                self.is_available = False
    
    def generate(self, prompt: str, system_prompt: str = "", temperature: float = 0.7, max_tokens: int = 1000) -> Optional[str]:
        try:
            # Gemini не поддерживает отдельный system prompt, комбинируем
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            # ИСПРАВЛЕНИЕ: Создаем модель с generation_config при каждом вызове
            model_with_config = self.genai.GenerativeModel(
                model_name=self.model,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                }
            )
            
            # Вызываем generate_content БЕЗ generation_config
            response = model_with_config.generate_content(full_prompt)
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
        # ИСПРАВЛЕНИЕ: Добавляем Content-Type в headers
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generate(self, prompt: str, system_prompt: str = "", temperature: float = 0.7, max_tokens: int = 1000) -> Optional[str]:
        try:
            # ИСПРАВЛЕНИЕ: Форматируем промпт как строку (inputs должен быть строкой, не массивом)
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            payload = {
                "inputs": full_prompt,  # Убедимся что это строка
                "parameters": {
                    "temperature": temperature,
                    "max_new_tokens": max_tokens,
                    "return_full_text": False,
                    "do_sample": True  # Добавляем для лучшей генерации
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
                # ИСПРАВЛЕНИЕ: Проверяем разные форматы ответа
                if isinstance(result, list) and len(result) > 0:
                    # Формат: [{"generated_text": "..."}]
                    generated = result[0].get("generated_text", "").strip()
                    if generated:
                        return generated
                    logger.warning(f"⚠️ {self.name}: Пустой generated_text в ответе")
                elif isinstance(result, dict) and "generated_text" in result:
                    # Альтернативный формат: {"generated_text": "..."}
                    generated = result["generated_text"].strip()
                    if generated:
                        return generated
                else:
                    logger.warning(f"⚠️ {self.name}: Некорректный формат ответа: {result}")
            else:
                logger.warning(f"⚠️ {self.name}: HTTP {response.status_code}: {response.text[:200]}")
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
            logger.warning("⚠️ Ни один LLM провайдер не настроен. Бот будет копировать посты БЕЗ AI обработки.")
            logger.warning("⚠️ Для AI обработки пополните DeepSeek: https://platform.deepseek.com")
        else:
            logger.info(f"✅ Доступные LLM провайдеры: {[p.name for p in self.providers]}")
    
    def _initialize_providers(self):
        """Инициализация всех провайдеров"""
        
        # АКТУАЛЬНЫЕ бесплатные модели (октябрь 2025)
        default_models = {
            "deepseek": "deepseek-chat",
            "groq": "llama-3.1-8b-instant",  # ✅ РАБОТАЕТ!
            "google": "gemini-pro",  # Стабильная версия (без префикса models/)
            "huggingface": "google/flan-t5-base",  # Стабильная бесплатная модель Google
            "xai": "grok-beta"  # xAI Grok модель
        }
        
        use_custom_model = Config.LLM_MODEL != 'auto' and Config.LLM_PROVIDER != 'auto'
        
        # GROQ - БЕСПЛАТНО, быстро! (groq.com)
        if hasattr(Config, 'GROQ_API_KEY') and Config.GROQ_API_KEY:
            model = Config.LLM_MODEL if (use_custom_model and Config.LLM_PROVIDER == 'groq') else default_models["groq"]
            # ИСПРАВЛЕНИЕ: Правильный base_url для Groq
            provider = OpenAIProvider("Groq", Config.GROQ_API_KEY, model, "https://api.groq.com/openai/v1")
            if self._test_provider(provider):
                self.providers.append(provider)
        
        # Google Gemini - БЕСПЛАТНО 60 req/min
        if hasattr(Config, 'GOOGLE_API_KEY') and Config.GOOGLE_API_KEY:
            model = Config.LLM_MODEL if (use_custom_model and Config.LLM_PROVIDER == 'google') else default_models["google"]
            provider = GoogleGeminiProvider("Google Gemini", Config.GOOGLE_API_KEY, model)
            if self._test_provider(provider):
                self.providers.append(provider)
        
        # HuggingFace - БЕСПЛАТНО
        if hasattr(Config, 'HUGGINGFACE_API_KEY') and Config.HUGGINGFACE_API_KEY:
            model = Config.LLM_MODEL if (use_custom_model and Config.LLM_PROVIDER == 'huggingface') else default_models["huggingface"]
            provider = HuggingFaceProvider("HuggingFace", Config.HUGGINGFACE_API_KEY, model)
            if self._test_provider(provider):
                self.providers.append(provider)
        
        # DeepSeek - дешево ($0.14/1M), если есть баланс
        if hasattr(Config, 'DEEPSEEK_API_KEY') and Config.DEEPSEEK_API_KEY:
            model = Config.LLM_MODEL if (use_custom_model and Config.LLM_PROVIDER == 'deepseek') else default_models["deepseek"]
            # ИСПРАВЛЕНИЕ: Правильный base_url для DeepSeek (с /v1)
            provider = OpenAIProvider("DeepSeek", Config.DEEPSEEK_API_KEY, model, "https://api.deepseek.com/v1")
            if self._test_provider(provider):
                self.providers.append(provider)
        
        # xAI Grok - платно, если есть баланс
        if hasattr(Config, 'XAI_API_KEY') and Config.XAI_API_KEY:
            model = Config.LLM_MODEL if (use_custom_model and Config.LLM_PROVIDER == 'xai') else default_models["xai"]
            # ИСПРАВЛЕНИЕ: Правильный base_url для xAI
            provider = OpenAIProvider("xAI Grok", Config.XAI_API_KEY, model, "https://api.x.ai/v1")
            if self._test_provider(provider):
                self.providers.append(provider)
    
    def _test_provider(self, provider: LLMProvider) -> bool:
        """Тестирование провайдера простым запросом"""
        try:
            logger.info(f"🧪 Тестирование {provider.name}...")
            test_result = provider.generate(
                "Say 'OK' if you work",
                "",
                0.1,
                10
            )
            if test_result and len(test_result.strip()) > 0:
                logger.info(f"✅ {provider.name}: РАБОТАЕТ")
                return True
            else:
                logger.warning(f"❌ {provider.name}: пустой ответ")
                return False
        except Exception as e:
            logger.warning(f"❌ {provider.name}: не прошел тест ({str(e)[:100]})")
            return False
    
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
        
        system_prompt = "Ты - профессиональный SMM-специалист, который умеет переписывать посты на любые темы, сохраняя смысл, но делая их уникальными и авторскими. Всегда следуй инструкциям точно, шаг за шагом, чтобы результат был предсказуемым даже для простых моделей."
        
        # Вызов с fallback, max_tokens=600 для ограничения длины (Telegram лимит 1024 символа на caption)
        result = self._generate_with_fallback(prompt, system_prompt, temperature=self.temperature, max_tokens=600)
        
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
    # Просто возвращаем слегка измененный текст без CTA
    modified = f"{text}\n\n{Config.YOUR_BRAND_NAME}"
    return modified

def _build_rewrite_prompt_with_links(self, text: str) -> str:
    """Строит промпт для текста со ссылками"""
    return f"""Перепиши этот текст на любую тему так, чтобы он был уникальным, но сохранял весь смысл. Тема может быть любой, включая новости, события или информацию из Telegram.

ОРИГИНАЛЬНЫЙ ТЕКСТ:
{text}

ТРЕБОВАНИЯ (выполняй шаг за шагом):
1. Прочитай текст и пойми основную идею, факты, детали.
2. Замени ВСЕ ссылки (t.me/..., https://..., любые другие) на "{Config.YOUR_LINK}".
3. Перефразируй каждое предложение своими словами, сохраняя все факты, детали, регионы, провайдеры, время, если они есть.
4. Используй стиль: {Config.CHANNEL_STYLE}.
5. Упомяни "{Config.YOUR_BRAND_NAME}" естественно как часть текста, если оно подходит по смыслу.
6. Сделай текст живым и информативным, но не добавляй срочности, если её нет в оригинале.
7. НЕ используй фразы типа "по данным мониторинга" - пиши от своего лица.
8. НЕ добавляй призывы к действию или дополнительные предложения в конце.
9. Сохрани структуру: если есть списки или абзацы, сохрани их.
10. ⚠️ КРИТИЧЕСКИ ВАЖНО: Текст должен быть КОРОТКИМ - максимум 800 символов! Если оригинал длиннее, сократи несущественные части.

ПЕРЕПИСАННЫЙ ТЕКСТ (начни сразу с текста, без введения):"""

def _build_rewrite_prompt_simple(self, text: str) -> str:
    """Строит промпт для текста без ссылок"""
    return f"""Перепиши этот текст на любую тему так, чтобы он был уникальным, но сохранял весь смысл. Тема может быть любой, включая новости, события или информацию из Telegram.

ОРИГИНАЛЬНЫЙ ТЕКСТ:
{text}

ТРЕБОВАНИЯ (выполняй шаг за шагом):
1. Прочитай текст и пойми основную идею, факты, детали.
2. Перефразируй каждое предложение своими словами, сохраняя все факты, детали, регионы, провайдеры, время, если они есть.
3. Слегка измени формулировки для уникальности.
4. Используй стиль: {Config.CHANNEL_STYLE}.
5. Упомяни "{Config.YOUR_BRAND_NAME}" естественно как часть текста, если оно подходит по смыслу.
6. Сделай текст немного более живым и информативным.
7. НЕ добавляй призывы к действию или дополнительные предложения в конце.
8. Сохрани структуру: если есть списки или абзацы, сохрани их.
9. ⚠️ КРИТИЧЕСКИ ВАЖНО: Текст должен быть КОРОТКИМ - максимум 800 символов! Если оригинал длиннее, сократи несущественные части.

ПЕРЕПИСАННЫЙ ТЕКСТ (начни сразу с текста, без введения):"""

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
    Добавляет упоминание бренда если его нет (без CTA)
    
    Args:
        text: Текст поста
        
    Returns:
        Текст с упоминанием
    """
    try:
        prompt = f"""Добавь естественное упоминание "{Config.YOUR_BRAND_NAME}" в этот текст, если оно подходит по смыслу:

ТЕКСТ:
{text}

ТРЕБОВАНИЯ:
1. Упомяни "{Config.YOUR_BRAND_NAME}" только если оно логично вписывается.
2. НЕ добавляй призывы к действию.
3. НЕ добавляй ссылки, если их нет.
4. Максимум 1 предложение изменения.
5. Естественно вписывается в текст.

ТЕКСТ С УПОМИНАНИЕМ:"""
        
        result = self._generate_with_fallback(prompt, "", 0.5, 500)
        
        if result:
            return result
        else:
            # Простое упоминание вручную, если подходит
            return f"{text} (с {Config.YOUR_BRAND_NAME})" if "VPN" in text or "защита" in text else text
        
    except Exception as e:
        logger.error(f"Ошибка при добавлении упоминания: {e}")
        return text

# Singleton instance
_llm_client = None

def get_llm_client() -> LLMClient:
    """Получить глобальный экземпляр LLM клиента"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
