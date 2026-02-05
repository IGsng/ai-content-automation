import logging
import json
from typing import Optional

logger = logging.getLogger(__name__)

class FactGenerator:
    def __init__(self, config):
        self.config = config
        self.ollama_host = config.get('ollama_host', 'http://localhost:11434')
        self.model = config.get('ollama_model', 'qwen2.5:32b')
    
    async def generate(self, topic: str) -> Optional[str]:
        try:
            import httpx
            
            prompt = f"""Найди интересный, малоизвестный и проверенный факт на тему: {topic}

Критерии:
- Удивительный
- Можно объяснить за 30-60 секунд
- Проверенная информация
- Подходит для визуализации

Ответ дай кратко, 2-3 предложения."""
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f'{self.ollama_host}/api/generate',
                    json={'model': self.model, 'prompt': prompt, 'stream': False}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    fact = result.get('response', '').strip()
                    logger.info(f'Fact generated: {len(fact)} chars')
                    return fact
                else:
                    logger.error(f'Ollama error: {response.status_code}')
                    return None
        except Exception as e:
            logger.error(f'Generation error: {e}')
            return None