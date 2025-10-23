"""
🧪 Скрипт для тестирования конфигурации
Запустите перед первым запуском бота
"""

import sys
import os
from colorama import init, Fore, Style

# Инициализация colorama для Windows
init()

def print_success(msg):
    print(f"{Fore.GREEN}✅ {msg}{Style.RESET_ALL}")

def print_error(msg):
    print(f"{Fore.RED}❌ {msg}{Style.RESET_ALL}")

def print_warning(msg):
    print(f"{Fore.YELLOW}⚠️  {msg}{Style.RESET_ALL}")

def print_info(msg):
    print(f"{Fore.CYAN}ℹ️  {msg}{Style.RESET_ALL}")

def check_env_file():
    """Проверка наличия .env файла"""
    if not os.path.exists('.env'):
        print_error(".env файл не найден")
        print_info("Создайте его: cp env.example .env")
        return False
    print_success(".env файл существует")
    return True

def check_config():
    """Проверка конфигурации"""
    try:
        from config import Config
        
        errors = Config.validate()
        
        if errors:
            print_error("Ошибки конфигурации:")
            for error in errors:
                print(f"  {error}")
            return False
        
        print_success("Конфигурация валидна")
        
        # Показываем текущие настройки (без секретов)
        print("\n" + "=" * 50)
        print(f"{Fore.CYAN}📋 Текущие настройки:{Style.RESET_ALL}")
        print("=" * 50)
        print(f"API ID: {Config.API_ID}")
        print(f"Source Channel: {Config.SOURCE_CHANNEL}")
        print(f"Target Channel: {Config.TARGET_CHANNEL}")
        print(f"LLM Provider: {Config.LLM_PROVIDER}")
        print(f"LLM Model: {Config.LLM_MODEL}")
        print(f"Your Link: {Config.YOUR_LINK}")
        print(f"Brand Name: {Config.YOUR_BRAND_NAME}")
        print(f"Check Interval: {Config.CHECK_INTERVAL}s")
        print("=" * 50 + "\n")
        
        return True
        
    except ImportError as e:
        print_error(f"Ошибка импорта: {e}")
        return False
    except Exception as e:
        print_error(f"Ошибка: {e}")
        return False

def check_dependencies():
    """Проверка установленных зависимостей"""
    print(f"\n{Fore.CYAN}📦 Проверка зависимостей...{Style.RESET_ALL}")
    
    required_packages = [
        'telethon',
        'opencv-python',
        'pytesseract',
        'PIL',
        'openai',
        'requests',
        'dotenv'
    ]
    
    all_installed = True
    
    for package in required_packages:
        try:
            if package == 'opencv-python':
                import cv2
            elif package == 'PIL':
                from PIL import Image
            elif package == 'dotenv':
                from dotenv import load_dotenv
            else:
                __import__(package)
            print_success(f"{package} установлен")
        except ImportError:
            print_error(f"{package} не установлен")
            all_installed = False
    
    if not all_installed:
        print_warning("Установите зависимости: pip install -r requirements.txt")
        return False
    
    return True

def check_tesseract():
    """Проверка Tesseract OCR"""
    print(f"\n{Fore.CYAN}🔍 Проверка Tesseract OCR...{Style.RESET_ALL}")
    
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print_success(f"Tesseract установлен: {version}")
        return True
    except Exception as e:
        print_error(f"Tesseract не найден: {e}")
        print_info("macOS: brew install tesseract tesseract-lang")
        print_info("Linux: sudo apt install tesseract-ocr tesseract-ocr-rus")
        print_info("Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        return False

def check_llm_api():
    """Проверка LLM API ключа"""
    print(f"\n{Fore.CYAN}🧠 Проверка LLM API...{Style.RESET_ALL}")
    
    try:
        from config import Config
        
        if Config.LLM_PROVIDER == 'deepseek' and Config.DEEPSEEK_API_KEY:
            print_success(f"DeepSeek API ключ установлен (начинается с: {Config.DEEPSEEK_API_KEY[:10]}...)")
        elif Config.LLM_PROVIDER == 'openai' and Config.OPENAI_API_KEY:
            print_success(f"OpenAI API ключ установлен (начинается с: {Config.OPENAI_API_KEY[:10]}...)")
        elif Config.LLM_PROVIDER == 'xai' and Config.XAI_API_KEY:
            print_success(f"xAI API ключ установлен")
        else:
            print_error(f"API ключ для {Config.LLM_PROVIDER} не установлен")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Ошибка проверки LLM API: {e}")
        return False

def main():
    """Главная функция"""
    print(f"\n{Fore.MAGENTA}{'=' * 50}")
    print(f"🦄 Проверка конфигурации Telegram Post Copier")
    print(f"{'=' * 50}{Style.RESET_ALL}\n")
    
    results = []
    
    # Проверки
    results.append(("Файл .env", check_env_file()))
    
    if results[-1][1]:  # Если .env существует
        results.append(("Конфигурация", check_config()))
    
    results.append(("Зависимости Python", check_dependencies()))
    results.append(("Tesseract OCR", check_tesseract()))
    
    if results[1][1]:  # Если конфигурация валидна
        results.append(("LLM API", check_llm_api()))
    
    # Итоги
    print(f"\n{Fore.MAGENTA}{'=' * 50}")
    print("📊 Результаты проверки:")
    print(f"{'=' * 50}{Style.RESET_ALL}\n")
    
    for name, status in results:
        if status:
            print_success(f"{name}")
        else:
            print_error(f"{name}")
    
    # Финальный вердикт
    all_passed = all(status for _, status in results)
    
    print(f"\n{Fore.MAGENTA}{'=' * 50}{Style.RESET_ALL}")
    
    if all_passed:
        print_success("Все проверки пройдены! Можно запускать бота 🚀")
        print_info("Запуск: python copier.py")
        return 0
    else:
        print_error("Некоторые проверки не пройдены")
        print_info("Исправьте ошибки и запустите снова: python test_config.py")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Прервано пользователем{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Неожиданная ошибка: {e}")
        sys.exit(1)

