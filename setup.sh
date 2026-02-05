#!/bin/bash
# Скрипт быстрой установки AI Content Automation

set -e

echo "🚀 AI Content Automation - Setup Script"
echo "=========================================="
echo ""

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    echo "Установи Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен!"
    echo "Установи Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker установлен"

# Создание директорий
echo "📁 Создание директорий..."
mkdir -p output logs models cache temp config
echo "✅ Директории созданы"

# Копирование .env
if [ ! -f .env ]; then
    echo "📝 Создание .env файла..."
    cp .env.example .env
    echo "✅ Создан .env файл"
    echo "⚠️  ВАЖНО: Отредактируй .env и добавь API ключи!"
    echo ""
else
    echo "✅ .env уже существует"
fi

# Выбор режима запуска
echo ""
echo "Выбери режим запуска:"
echo "1) С GPU (требуется NVIDIA GPU + nvidia-docker)"
echo "2) CPU only (медленнее, но работает везде)"
read -p "Выбор [1/2]: " choice

if [ "$choice" = "1" ]; then
    COMPOSE_FILE="docker-compose.yml"
    echo "✅ Режим: GPU"
else
    COMPOSE_FILE="docker-compose.cpu.yml"
    echo "✅ Режим: CPU"
fi

# Запуск Docker Compose
echo ""
echo "🐳 Запуск Docker контейнеров..."
docker-compose -f $COMPOSE_FILE up -d

echo ""
echo "⏳ Ожидание запуска сервисов (30 сек)..."
sleep 30

# Скачивание LLM модели
echo ""
echo "📦 Скачивание LLM модели (это может занять время)..."
docker exec ai-content-ollama ollama pull qwen2.5:7b || echo "⚠️ Ошибка загрузки модели"

echo ""
echo "✅ Установка завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Отредактируй .env файл: nano .env"
echo "2. Добавь API ключи (Replicate, ElevenLabs и др.)"
echo "3. Перезапусти: docker-compose restart"
echo "4. Проверь статус: docker-compose ps"
echo "5. Генерация видео: python cli.py generate --topic 'космос'"
echo ""
echo "🌐 Веб-интерфейсы:"
echo "  - n8n: http://localhost:5678 (admin/admin123)"
echo "  - Ollama: http://localhost:11434"
echo ""
echo "📚 Документация: https://github.com/IGsng/ai-content-automation"
echo ""