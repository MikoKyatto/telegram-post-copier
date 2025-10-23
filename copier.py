"""
🤖 Telegram Post Copier with AI Agent
Автоматическое копирование и AI-обработка постов из Telegram каналов
"""

import asyncio
import logging
import sys
import re
from io import BytesIO
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.types import InputChannel, MessageMediaPhoto
from telethon.errors import FloodWaitError, SessionPasswordNeededError

from config import Config
from llm_client import get_llm_client
from image_processor import get_image_processor

# Настройка логирования
import os
os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/copier.log')
    ]
)
logger = logging.getLogger(__name__)


class TelegramPostCopier:
    """Основной класс для копирования постов"""
    
    def __init__(self):
        # Валидация конфигурации
        errors = Config.validate()
        if errors:
            for error in errors:
                logger.error(error)
            raise ValueError("Ошибка конфигурации. Проверьте .env файл")
        
        # Инициализация компонентов
        self.client = TelegramClient(
            Config.SESSION_NAME,
            Config.API_ID,
            Config.API_HASH
        )
        self.llm_client = get_llm_client()
        self.image_processor = get_image_processor()
        
        self.source_entity = None
        self.target_entity = None
        self.last_post_id = 0
        self.is_running = False
        
        logger.info("🚀 TelegramPostCopier инициализирован")
    
    async def start(self):
        """Запуск клиента и авторизация"""
        try:
            logger.info("🔐 Подключение к Telegram...")
            await self.client.start()
            
            # Проверка авторизации
            me = await self.client.get_me()
            logger.info(f"✅ Авторизован как: {me.first_name} (@{me.username})")
            
            # Получение сущностей каналов
            await self._init_channels()
            
            logger.info("✨ Система готова к работе!")
            
        except SessionPasswordNeededError:
            logger.error("❌ Требуется двухфакторная аутентификация. Запустите скрипт вручную для ввода пароля.")
            raise
        except Exception as e:
            logger.error(f"❌ Ошибка при запуске: {e}")
            raise
    
    async def _init_channels(self):
        """Инициализация каналов"""
        try:
            # Исходный канал
            logger.info(f"📡 Подключение к исходному каналу: {Config.SOURCE_CHANNEL}")
            self.source_entity = await self.client.get_entity(Config.SOURCE_CHANNEL)
            logger.info(f"✅ Исходный канал: {self.source_entity.title}")
            
            # Целевой канал
            logger.info(f"📢 Подключение к целевому каналу: {Config.TARGET_CHANNEL}")
            self.target_entity = await self.client.get_entity(Config.TARGET_CHANNEL)
            logger.info(f"✅ Целевой канал: {self.target_entity.title}")
            
            # Получение последнего поста для инициализации
            messages = await self.client.get_messages(self.source_entity, limit=1)
            if messages:
                self.last_post_id = messages[0].id
                logger.info(f"📌 Начальная позиция: пост ID {self.last_post_id}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при инициализации каналов: {e}")
            raise
    
    async def check_and_copy_new_posts(self):
        """Проверка новых постов и их копирование"""
        try:
            # Получение последнего поста
            messages = await self.client.get_messages(self.source_entity, limit=5)
            
            # Обработка новых постов (в обратном порядке, чтобы копировать от старых к новым)
            new_messages = [m for m in reversed(messages) if m.id > self.last_post_id]
            
            for message in new_messages:
                await self._process_and_copy_message(message)
                self.last_post_id = message.id
                
                # Задержка между постами для избежания флуда
                await asyncio.sleep(2)
            
            if new_messages:
                logger.info(f"✅ Обработано {len(new_messages)} новых постов")
            
        except FloodWaitError as e:
            logger.warning(f"⏳ Flood wait: ожидание {e.seconds} секунд")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            logger.error(f"❌ Ошибка при проверке постов: {e}")
    
    async def _process_and_copy_message(self, message):
        """
        Обработка и копирование одного сообщения
        
        Args:
            message: Telethon Message объект
        """
        try:
            logger.info(f"🔄 Обработка поста ID {message.id}")
            
            # Извлечение текста
            original_text = message.text or ""
            
            # Проверка наличия ссылок в тексте
            has_links = bool(re.search(r'(t\.me/|https?://)', original_text))
            
            # Переписывание текста с помощью AI
            if original_text:
                logger.info("🧠 AI: Переписывание текста...")
                rewritten_text = self.llm_client.rewrite_text(original_text, has_links)
                
                # Проверка уникальности
                uniqueness = self.llm_client.check_uniqueness(original_text, rewritten_text)
                logger.info(f"📊 Уникальность: {uniqueness:.1f}%")
                
                # Если уникальность низкая, добавляем CTA
                if uniqueness < 30:
                    logger.info("🎯 Добавление CTA для увеличения уникальности...")
                    rewritten_text = self.llm_client.enhance_with_cta(rewritten_text)
            else:
                rewritten_text = ""
            
            # Обработка изображений
            if message.photo:
                await self._copy_message_with_photo(message, rewritten_text)
            else:
                await self._copy_text_message(rewritten_text)
            
            logger.info(f"✅ Пост ID {message.id} успешно скопирован")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при обработке поста ID {message.id}: {e}")
    
    async def _copy_message_with_photo(self, message, text: str):
        """Копирование сообщения с фото"""
        try:
            logger.info("🎨 Обработка изображения...")
            
            # Скачивание фото
            photo_bytes = await message.download_media(bytes)
            
            # Обработка изображения (замена ссылок)
            processed_photo, was_modified = self.image_processor.process_image(photo_bytes)
            
            if was_modified:
                logger.info("✨ Изображение модифицировано (ссылки заменены)")
            else:
                logger.info("ℹ️ Изображение не требует модификации")
            
            # Отправка в целевой канал
            await self.client.send_file(
                self.target_entity,
                processed_photo,
                caption=text,
                file=BytesIO(processed_photo)
            )
            
        except Exception as e:
            logger.error(f"❌ Ошибка при копировании фото: {e}")
            raise
    
    async def _copy_text_message(self, text: str):
        """Копирование текстового сообщения"""
        try:
            if not text or len(text.strip()) < 3:
                logger.warning("⚠️ Текст слишком короткий, пропускаем")
                return
            
            await self.client.send_message(self.target_entity, text)
            
        except Exception as e:
            logger.error(f"❌ Ошибка при копировании текста: {e}")
            raise
    
    async def run_forever(self):
        """Бесконечный цикл мониторинга"""
        self.is_running = True
        retry_count = 0
        
        logger.info(f"🔁 Запуск мониторинга (интервал: {Config.CHECK_INTERVAL}сек)")
        
        while self.is_running:
            try:
                await self.check_and_copy_new_posts()
                retry_count = 0  # Сброс счетчика при успехе
                
                # Ожидание до следующей проверки
                await asyncio.sleep(Config.CHECK_INTERVAL)
                
            except KeyboardInterrupt:
                logger.info("⏹️ Остановка по команде пользователя")
                self.is_running = False
                break
            except Exception as e:
                retry_count += 1
                logger.error(f"❌ Ошибка в цикле мониторинга (попытка {retry_count}/{Config.MAX_RETRIES}): {e}")
                
                if retry_count >= Config.MAX_RETRIES:
                    logger.critical("💥 Превышено количество попыток. Остановка.")
                    self.is_running = False
                    break
                
                # Экспоненциальная задержка при ошибках
                wait_time = min(300, 30 * (2 ** retry_count))
                logger.info(f"⏳ Ожидание {wait_time}сек перед повтором...")
                await asyncio.sleep(wait_time)
    
    async def stop(self):
        """Остановка клиента"""
        logger.info("🛑 Остановка TelegramPostCopier...")
        self.is_running = False
        await self.client.disconnect()
        logger.info("👋 Отключено от Telegram")


async def main():
    """Главная функция"""
    logger.info("=" * 60)
    logger.info("🦄 TELEGRAM POST COPIER WITH AI")
    logger.info("   Unicorn-style automation for your content")
    logger.info("=" * 60)
    logger.info(f"📅 Запуск: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"🤖 LLM Provider: {Config.LLM_PROVIDER}")
    logger.info(f"📡 Source: {Config.SOURCE_CHANNEL}")
    logger.info(f"📢 Target: {Config.TARGET_CHANNEL}")
    logger.info("=" * 60)
    
    copier = TelegramPostCopier()
    
    try:
        await copier.start()
        await copier.run_forever()
    except KeyboardInterrupt:
        logger.info("\n⏹️ Получен сигнал остановки")
    except Exception as e:
        logger.critical(f"💥 Критическая ошибка: {e}", exc_info=True)
        return 1
    finally:
        await copier.stop()
    
    logger.info("✅ Программа завершена")
    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("\n👋 До свидания!")
        sys.exit(0)

