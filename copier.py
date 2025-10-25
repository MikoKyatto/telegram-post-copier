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

# Настройка логирования с ротацией
import os
from logging.handlers import RotatingFileHandler

os.makedirs('logs', exist_ok=True)

# Ротация логов: максимум 10MB на файл, хранить 5 файлов
file_handler = RotatingFileHandler(
    'logs/copier.log',
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5,  # Хранить 5 файлов
    encoding='utf-8'
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        file_handler
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
        self.groups = {}  # Буфер для группировки медиа по grouped_id
        self.group_timers = {}  # Таймеры для flush групп
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
            
            # Регистрация event handler для новых сообщений
            self.client.add_event_handler(
                self._new_message_handler,
                events.NewMessage(chats=self.source_entity)
            )
            logger.info("📡 Event-based мониторинг зарегистрирован")
            
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
            
        except Exception as e:
            logger.error(f"❌ Ошибка при инициализации каналов: {e}")
            raise
    
    async def _new_message_handler(self, event):
        """Обработчик новых сообщений (event-based)"""
        try:
            msg = event.message
            group_id = msg.grouped_id
            
            logger.info(f"🔔 Новое сообщение ID {msg.id} (grouped_id: {group_id or 'None'})")
            
            if group_id:
                # Сообщение является частью альбома
                if group_id not in self.groups:
                    self.groups[group_id] = []
                
                self.groups[group_id].append(msg)
                
                # Отменяем старый таймер если был
                if group_id in self.group_timers:
                    self.group_timers[group_id].cancel()
                
                # Создаем новый таймер для flush группы через 2 секунды
                # (чтобы собрать все сообщения альбома)
                timer = asyncio.create_task(self._flush_group_after_delay(group_id, delay=2.0))
                self.group_timers[group_id] = timer
            else:
                # Одиночное сообщение - обрабатываем сразу
                await self._process_and_copy_group([msg])
                await asyncio.sleep(2)  # Антифлуд
            
        except Exception as e:
            logger.error(f"❌ Ошибка в обработчике события: {e}", exc_info=True)
    
    async def _flush_group_after_delay(self, group_id, delay: float):
        """Отложенная обработка группы (после сбора всех сообщений альбома)"""
        try:
            await asyncio.sleep(delay)
            
            if group_id in self.groups:
                msgs = self.groups.pop(group_id)
                self.group_timers.pop(group_id, None)
                
                # Сортируем по ID для правильного порядка
                msgs.sort(key=lambda m: m.id)
                
                logger.info(f"📦 Flush группы {group_id}: собрано {len(msgs)} сообщений")
                
                await self._process_and_copy_group(msgs)
                await asyncio.sleep(2)  # Антифлуд
                
        except asyncio.CancelledError:
            # Таймер был отменен (пришло еще сообщение в группу)
            pass
        except Exception as e:
            logger.error(f"❌ Ошибка при flush группы {group_id}: {e}", exc_info=True)
    
    async def _process_and_copy_group(self, messages: list):
        """
        Обработка и копирование группы сообщений (альбом или одиночное)
        
        Args:
            messages: List of Telethon Message objects (может быть 1 или несколько)
        """
        try:
            if not messages:
                return
            
            first_msg = messages[0]
            group_id = first_msg.grouped_id
            
            if len(messages) > 1:
                logger.info(f"🔄 Обработка альбома ID {group_id} ({len(messages)} медиа)")
            else:
                logger.info(f"🔄 Обработка поста ID {first_msg.id}")
            
            # Текст обычно в первом сообщении
            original_text = first_msg.text or ""
            
            # Проверка ссылок в тексте
            has_links = bool(re.search(r'(t\.me/|https?://)', original_text))
            
            # Переписывание текста с помощью AI
            if original_text:
                logger.info("🧠 AI: Переписывание текста...")
                rewritten_text = self.llm_client.rewrite_text(original_text, has_links)
                
                uniqueness = self.llm_client.check_uniqueness(original_text, rewritten_text)
                logger.info(f"📊 Уникальность: {uniqueness:.1f}%")
                
                # Если уникальность низкая, добавляем упоминание бренда
                if uniqueness < 30:
                    logger.info("🎯 Добавление упоминания бренда...")
                    rewritten_text = self.llm_client.enhance_with_cta(rewritten_text)
            else:
                rewritten_text = ""
            
            # Telegram лимит для подписи к фото/альбому: 1024 символа
            MAX_CAPTION_LENGTH = 1024
            if len(rewritten_text) > MAX_CAPTION_LENGTH:
                logger.warning(f"⚠️ Текст обрезан до {MAX_CAPTION_LENGTH} символов (было {len(rewritten_text)})")
                rewritten_text = rewritten_text[:MAX_CAPTION_LENGTH-3] + "..."
            
            # Сбор и обработка всех медиа из группы
            media_list = []
            for msg in messages:
                if msg.photo or (msg.media and hasattr(msg.media, 'photo')):
                    logger.info(f"🎨 Обработка изображения из сообщения ID {msg.id}...")
                    
                    # Скачиваем как bytes
                    photo_bytes = await msg.download_media(bytes)
                    
                    # Обрабатываем (замена ссылок)
                    processed_photo, was_modified = self.image_processor.process_image(photo_bytes)
                    
                    if was_modified:
                        logger.info("✨ Изображение модифицировано (ссылки заменены)")
                    
                    media_list.append(processed_photo)
            
            # Отправка в зависимости от типа контента
            if media_list:
                if len(media_list) > 1:
                    # Альбом (несколько изображений)
                    await self._copy_media_album(media_list, rewritten_text)
                else:
                    # Одно изображение
                    await self._copy_single_photo(media_list[0], rewritten_text)
            elif rewritten_text:
                # Только текст
                await self._copy_text_message(rewritten_text)
            else:
                logger.warning("⚠️ Нет контента для копирования")
                return
            
            if len(messages) > 1:
                logger.info(f"✅ Альбом успешно скопирован ({len(messages)} медиа)")
            else:
                logger.info(f"✅ Пост ID {first_msg.id} успешно скопирован")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при обработке группы: {e}", exc_info=True)
    
    async def _copy_single_photo(self, photo_bytes: bytes, text: str):
        """Копирование одного изображения с подписью"""
        try:
            logger.info("📤 Отправка изображения...")
            
            # Создаем BytesIO с правильным именем файла и расширением
            bio = BytesIO(photo_bytes)
            bio.name = "photo.jpg"  # ВАЖНО: добавляем имя с расширением!
            bio.seek(0)  # Позиционируемся в начало
            
            await self.client.send_file(
                self.target_entity,
                bio,
                caption=text if text else None
            )
            
        except FloodWaitError as e:
            logger.warning(f"⏳ Flood wait: ожидание {e.seconds} секунд")
            await asyncio.sleep(e.seconds)
            await self._copy_single_photo(photo_bytes, text)  # Retry
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке изображения: {e}", exc_info=True)
            raise
    
    async def _copy_media_album(self, media_list: list, text: str):
        """
        Копирование альбома (несколько изображений одним сообщением)
        
        Args:
            media_list: List[bytes] - список байтов изображений
            text: str - подпись к альбому
        """
        try:
            logger.info(f"📤 Отправка альбома ({len(media_list)} изображений)...")
            
            # Подготавливаем файлы с правильными именами и расширениями
            files = []
            for idx, photo_bytes in enumerate(media_list):
                bio = BytesIO(photo_bytes)
                bio.name = f"photo_{idx + 1}.jpg"  # ВАЖНО: имя с расширением!
                bio.seek(0)  # Позиционируемся в начало
                files.append(bio)
            
            # Отправляем как альбом (один вызов send_file с массивом)
            await self.client.send_file(
                self.target_entity,
                files,
                caption=text if text else None
            )
            
            logger.info(f"✅ Альбом отправлен ({len(media_list)} фото)")
            
        except FloodWaitError as e:
            logger.warning(f"⏳ Flood wait: ожидание {e.seconds} секунд")
            await asyncio.sleep(e.seconds)
            await self._copy_media_album(media_list, text)  # Retry
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке альбома: {e}", exc_info=True)
            raise
    
    async def _copy_text_message(self, text: str):
        """Копирование текстового сообщения"""
        try:
            if not text or len(text.strip()) < 3:
                logger.warning("⚠️ Текст слишком короткий, пропускаем")
                return
            
            logger.info("📤 Отправка текста...")
            
            await self.client.send_message(self.target_entity, text)
            
        except FloodWaitError as e:
            logger.warning(f"⏳ Flood wait: ожидание {e.seconds} секунд")
            await asyncio.sleep(e.seconds)
            await self._copy_text_message(text)  # Retry
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке текста: {e}", exc_info=True)
            raise
    
    async def run_forever(self):
        """Запуск event-based мониторинга (работает бесконечно)"""
        self.is_running = True
        
        logger.info("🔁 Запуск event-based мониторинга (слушаем новые сообщения)")
        logger.info("💡 Бот будет автоматически обрабатывать новые посты в реальном времени")
        
        try:
            # Запускаем клиент до отключения
            await self.client.run_until_disconnected()
        except KeyboardInterrupt:
            logger.info("⏹️ Остановка по команде пользователя")
        finally:
            self.is_running = False
    
    async def stop(self):
        """Остановка клиента"""
        logger.info("🛑 Остановка TelegramPostCopier...")
        self.is_running = False
        
        # Отменяем все активные таймеры
        for timer in self.group_timers.values():
            timer.cancel()
        
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
