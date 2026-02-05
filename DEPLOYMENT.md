# 🚀 Инструкция по развертыванию

## Вариант 1: Автоматическая установка (рекомендуется)

```bash
# Клонируй репозиторий
git clone https://github.com/IGsng/ai-content-automation.git
cd ai-content-automation

# Запусти скрипт установки
chmod +x setup.sh
./setup.sh
```

Скрипт автоматически:
- Проверит Docker
- Создаст необходимые директории
- Создаст .env файл
- Запустит контейнеры
- Скачает LLM модель

## Вариант 2: Ручная установка

### Шаг 1: Требования

**Обязательно:**
- Docker 20.10+
- Docker Compose 2.0+
- 20 GB свободного места

**Опционально (для GPU):**
- NVIDIA GPU с 8+ GB VRAM
- NVIDIA Docker Runtime

### Шаг 2: Настройка окружения

```bash
# Создай .env
cp .env.example .env

# Отредактируй .env
nano .env
```

**Минимальные настройки:**
```env
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=qwen2.5:7b
VIDEO_API_PROVIDER=replicate
REPLICATE_API_TOKEN=r8_your_token_here
TTS_PROVIDER=silero
```

### Шаг 3: Запуск

**С GPU:**
```bash
docker-compose up -d
```

**Без GPU (CPU only):**
```bash
docker-compose -f docker-compose.cpu.yml up -d
```

### Шаг 4: Скачать LLM модель

```bash
# Легкая модель (7B параметров)
docker exec ai-content-ollama ollama pull qwen2.5:7b

# Или более мощная (32B параметров)
docker exec ai-content-ollama ollama pull qwen2.5:32b
```

### Шаг 5: Проверка

```bash
# Статус контейнеров
docker-compose ps

# Логи
docker-compose logs -f app

# Проверка Ollama
curl http://localhost:11434/api/tags
```

## Вариант 3: Локально без Docker

### Требования
- Python 3.10+
- FFmpeg
- 16+ GB RAM

### Установка

```bash
# Установи зависимости
pip install -r requirements.txt

# Установи Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:7b

# Запусти Ollama сервер
ollama serve &

# Инициализация
python cli.py init

# Генерация видео
python cli.py generate --topic "космос"
```

## Получение API ключей

### Replicate (для видео генерации)
1. Регистрация: https://replicate.com/
2. Получи токен: https://replicate.com/account/api-tokens
3. Добавь в .env: `REPLICATE_API_TOKEN=r8_...`

### ElevenLabs (опционально, для качественной озвучки)
1. Регистрация: https://elevenlabs.io/
2. Получи API ключ: https://elevenlabs.io/app/settings/api-keys
3. Добавь в .env: `ELEVENLABS_API_KEY=...`

### Blotato (для публикации)
1. Регистрация: https://blotato.com/
2. Получи API ключ
3. Добавь в .env: `BLOTATO_API_KEY=...`

## Тестирование

```bash
# Быстрый тест
chmod +x quick-start.sh
./quick-start.sh

# Или вручную
python cli.py generate --topic "интересные факты" --duration 30

# Проверь результат
ls -lh output/final/
```

## Решение проблем

### Контейнеры не запускаются
```bash
docker-compose down
docker-compose up -d
docker-compose logs -f
```

### Ollama не скачивает модель
```bash
# Зайди в контейнер
docker exec -it ai-content-ollama bash

# Скачай вручную
ollama pull qwen2.5:7b
```

### Ошибки с CUDA/GPU
```bash
# Используй CPU версию
docker-compose -f docker-compose.cpu.yml up -d
```

### Не хватает памяти
```bash
# Используй более легкую модель
docker exec ai-content-ollama ollama pull qwen2.5:7b

# В .env поменяй
OLLAMA_MODEL=qwen2.5:7b
```

## Мониторинг

```bash
# Статус сервисов
python cli.py status

# Статистика
python cli.py stats --last-days 7

# Логи приложения
tail -f logs/app.log

# Логи Docker
docker-compose logs -f --tail=100
```

## Производительность

| Конфигурация | Время генерации 1 видео |
|--------------|-------------------------|
| CPU only | 10-15 минут |
| RTX 3060 12GB | 3-5 минут |
| RTX 4090 24GB | 1-2 минуты |
| A100 80GB | 30-60 секунд |

## Масштабирование

### Несколько воркеров
```bash
docker-compose up -d --scale app=3
```

### Разные модели на разных серверах
```env
OLLAMA_HOST=http://remote-server:11434
```

## Автоматизация

### Расписание через cron
```bash
crontab -e

# Каждый день в 9:00, 15:00, 21:00
0 9,15,21 * * * cd /path/to/project && python cli.py generate
```

### Через n8n
1. Открой http://localhost:5678
2. Логин: admin / admin123
3. Импортируй workflow из `workflows/n8n/`

## Обновление

```bash
git pull
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Остановка

```bash
# Остановить
docker-compose stop

# Удалить контейнеры
docker-compose down

# Удалить всё (включая данные)
docker-compose down -v
```

## Поддержка

- Issues: https://github.com/IGsng/ai-content-automation/issues
- Документация: https://github.com/IGsng/ai-content-automation
