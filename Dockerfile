# 🐳 Multi-stage Dockerfile для оптимизации размера
FROM python:3.12-slim as builder

# Установка системных зависимостей для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# 🚀 Production образ
FROM python:3.12-slim

# Метаданные
LABEL maintainer="your@email.com"
LABEL description="Telegram Post Copier with AI - Unicorn Edition 🦄"
LABEL version="1.0.0"

# Установка runtime зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-rus \
    tesseract-ocr-eng \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование Python зависимостей из builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Установка переменных окружения
ENV PYTHONUNBUFFERED=1
ENV TESSERACT_CMD=/usr/bin/tesseract

# Создание непривилегированного пользователя для безопасности
RUN useradd -m -u 1000 appuser

# Копирование исходного кода
COPY --chown=appuser:appuser config.py .
COPY --chown=appuser:appuser llm_client.py .
COPY --chown=appuser:appuser image_processor.py .
COPY --chown=appuser:appuser copier.py .
COPY --chown=appuser:appuser utils.py .
COPY --chown=appuser:appuser docker-entrypoint.sh .

# Создание необходимых директорий с правильными правами
RUN mkdir -p temp processed_images logs && \
    chown -R appuser:appuser /app && \
    chmod +x docker-entrypoint.sh

# Переключение на непривилегированного пользователя
USER appuser

# Healthcheck
HEALTHCHECK --interval=5m --timeout=10s --start-period=30s --retries=3 \
    CMD ps aux | grep copier.py || exit 1

# Entrypoint и команда запуска
ENTRYPOINT ["/app/docker-entrypoint.sh"]

