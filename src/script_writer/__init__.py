import logging
from typing import Optional

logger = logging.getLogger(__name__)

class ScriptWriter:
    def __init__(self, config):
        self.config = config
        self.ollama_host = config.get('ollama_host')
        self.model = config.get('ollama_model')
    
    async def write(self, fact: str, duration: int, style: str = 'energetic') -> Optional[str]:
        try:
            import httpx
            
            word_count = int(duration * 2.5)
            
            prompt = f"""Создай сценарий для короткого видео ({duration} сек):

Факт: {fact}

Структура:
1. Хук (3 сек) - зацепить внимание
2. Основная часть - раскрыть факт
3. Призыв к действию

Стиль: {style}, разговорный
Длина: ~{word_count} слов

Только текст сценария, без комментариев."""
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f'{self.ollama_host}/api/generate',
                    json={'model': self.model, 'prompt': prompt, 'stream': False}
                )
                
                if response.status_code == 200:
                    script = response.json().get('response', '').strip()
                    logger.info(f'Script: {len(script.split())} words')
                    return script
                return None
        except Exception as e:
            logger.error(f'Script error: {e}')
            return None