"""
🎨 Image Processor - Обработка изображений с OCR и заменой текста
Работа с изображениями из постов Telegram
"""

import cv2
import pytesseract
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import re
import logging
from typing import Optional, Tuple
from config import Config

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Обработчик изображений для замены текста/ссылок"""
    
    def __init__(self):
        self.old_link_pattern = Config.OLD_LINK_PATTERN
        self.new_link = Config.YOUR_LINK
        self.ocr_language = Config.OCR_LANGUAGE
        
        # Настройка Tesseract (путь может отличаться)
        try:
            pytesseract.get_tesseract_version()
        except Exception:
            # Попытка установить стандартные пути
            possible_paths = [
                '/usr/bin/tesseract',
                '/usr/local/bin/tesseract',
                'C:\\Program Files\\Tesseract-OCR\\tesseract.exe',
                '/opt/homebrew/bin/tesseract'
            ]
            for path in possible_paths:
                try:
                    pytesseract.pytesseract.tesseract_cmd = path
                    pytesseract.get_tesseract_version()
                    break
                except:
                    continue
    
    def process_image(self, image_bytes: bytes) -> Tuple[bytes, bool]:
        """
        Обрабатывает изображение: ищет старые ссылки и заменяет на новые
        
        Args:
            image_bytes: Байты изображения
            
        Returns:
            Tuple[bytes, bool]: (обработанное изображение, был ли изменен)
        """
        try:
            # Конвертация в OpenCV формат
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                logger.error("Не удалось декодировать изображение")
                return image_bytes, False
            
            # Поиск текста на изображении
            found_links = self._find_links_in_image(img)
            
            if not found_links:
                logger.info("Ссылки не найдены на изображении")
                return image_bytes, False
            
            # Замена найденных ссылок
            modified_img = self._replace_links_in_image(img, found_links)
            
            # Конвертация обратно в байты
            success, buffer = cv2.imencode('.png', modified_img)
            if not success:
                logger.error("Не удалось закодировать изображение")
                return image_bytes, False
            
            return buffer.tobytes(), True
            
        except Exception as e:
            logger.error(f"Ошибка при обработке изображения: {e}")
            return image_bytes, False
    
    def _find_links_in_image(self, img: np.ndarray) -> list:
        """
        Находит ссылки на изображении с помощью OCR
        
        Returns:
            List of dicts with link info: {'text': str, 'x': int, 'y': int, 'w': int, 'h': int}
        """
        try:
            # Конвертация в grayscale для лучшего OCR
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Улучшение контраста
            gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=30)
            
            # OCR
            data = pytesseract.image_to_data(
                gray,
                lang=self.ocr_language,
                output_type=pytesseract.Output.DICT
            )
            
            found_links = []
            n_boxes = len(data['text'])
            
            for i in range(n_boxes):
                text = data['text'][i].strip()
                
                # Проверка на наличие паттерна ссылки
                if re.search(self.old_link_pattern, text, re.IGNORECASE):
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    
                    # Фильтруем слишком маленькие области
                    if w > 10 and h > 5:
                        found_links.append({
                            'text': text,
                            'x': x,
                            'y': y,
                            'w': w,
                            'h': h
                        })
                        logger.info(f"Найдена ссылка: {text} на позиции ({x}, {y})")
            
            return found_links
            
        except Exception as e:
            logger.error(f"Ошибка OCR: {e}")
            return []
    
    def _replace_links_in_image(self, img: np.ndarray, links: list) -> np.ndarray:
        """
        Заменяет найденные ссылки на новые
        
        Args:
            img: OpenCV изображение
            links: Список найденных ссылок с координатами
            
        Returns:
            Модифицированное изображение
        """
        try:
            result_img = img.copy()
            
            for link in links:
                x, y, w, h = link['x'], link['y'], link['w'], link['h']
                
                # Увеличиваем область для лучшего покрытия
                padding = 5
                x = max(0, x - padding)
                y = max(0, y - padding)
                w = w + 2 * padding
                h = h + 2 * padding
                
                # Создаем маску для inpainting
                mask = np.zeros(result_img.shape[:2], np.uint8)
                cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
                
                # Inpainting - удаление старого текста
                result_img = cv2.inpaint(result_img, mask, 3, cv2.INPAINT_TELEA)
                
                # Добавление нового текста с Pillow
                result_img = self._add_text_to_image(result_img, self.new_link, x, y, h)
            
            return result_img
            
        except Exception as e:
            logger.error(f"Ошибка при замене ссылок: {e}")
            return img
    
    def _add_text_to_image(
        self,
        img: np.ndarray,
        text: str,
        x: int,
        y: int,
        height: int
    ) -> np.ndarray:
        """
        Добавляет текст на изображение
        
        Args:
            img: OpenCV изображение
            text: Текст для добавления
            x, y: Координаты
            height: Высота текста (для выбора размера шрифта)
            
        Returns:
            Изображение с текстом
        """
        try:
            # Конвертация в PIL
            pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil_img)
            
            # Выбор размера шрифта пропорционально высоте
            font_size = max(12, int(height * 0.7))
            
            try:
                # Попытка использовать разные шрифты
                font = None
                font_paths = [
                    '/System/Library/Fonts/Helvetica.ttc',  # macOS
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Linux
                    'C:\\Windows\\Fonts\\arial.ttf',  # Windows
                    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'  # Linux alt
                ]
                
                for font_path in font_paths:
                    try:
                        font = ImageFont.truetype(font_path, font_size)
                        break
                    except:
                        continue
                
                if font is None:
                    font = ImageFont.load_default()
                    
            except Exception as e:
                logger.warning(f"Не удалось загрузить шрифт: {e}")
                font = ImageFont.load_default()
            
            # Рисуем текст (белый с черной обводкой для читаемости)
            # Обводка
            for offset_x in [-1, 0, 1]:
                for offset_y in [-1, 0, 1]:
                    draw.text((x + offset_x, y + offset_y), text, fill=(0, 0, 0), font=font)
            
            # Основной текст
            draw.text((x, y), text, fill=(255, 255, 255), font=font)
            
            # Конвертация обратно в OpenCV
            return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            
        except Exception as e:
            logger.error(f"Ошибка при добавлении текста: {e}")
            return img
    
    def has_text(self, image_bytes: bytes) -> bool:
        """
        Проверяет, есть ли текст на изображении
        
        Args:
            image_bytes: Байты изображения
            
        Returns:
            True если текст найден
        """
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return False
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray, lang=self.ocr_language)
            
            return len(text.strip()) > 5
            
        except Exception as e:
            logger.error(f"Ошибка при проверке текста: {e}")
            return False


# Singleton instance
_image_processor = None

def get_image_processor() -> ImageProcessor:
    """Получить глобальный экземпляр обработчика изображений"""
    global _image_processor
    if _image_processor is None:
        _image_processor = ImageProcessor()
    return _image_processor

