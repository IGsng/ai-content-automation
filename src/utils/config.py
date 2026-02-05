import os
from pathlib import Path
from typing import Any, Dict
import yaml
from dotenv import load_dotenv

load_dotenv()

def load_config() -> Dict[str, Any]:
    config = {}
    
    settings_path = Path('config/settings.yaml')
    if settings_path.exists():
        with open(settings_path) as f:
            config.update(yaml.safe_load(f) or {})
    
    config.update({
        'ollama_host': os.getenv('OLLAMA_HOST', 'http://localhost:11434'),
        'ollama_model': os.getenv('OLLAMA_MODEL', 'qwen2.5:32b'),
        'ollama_temperature': float(os.getenv('OLLAMA_TEMPERATURE', '0.7')),
        
        'video_api_provider': os.getenv('VIDEO_API_PROVIDER', 'replicate'),
        'replicate_api_token': os.getenv('REPLICATE_API_TOKEN'),
        
        'tts_provider': os.getenv('TTS_PROVIDER', 'silero'),
        'elevenlabs_api_key': os.getenv('ELEVENLABS_API_KEY'),
        
        'blotato_api_key': os.getenv('BLOTATO_API_KEY'),
        'publish_to_tiktok': os.getenv('PUBLISH_TO_TIKTOK', 'true').lower() == 'true',
        'publish_to_instagram': os.getenv('PUBLISH_TO_INSTAGRAM', 'true').lower() == 'true',
        'publish_to_youtube': os.getenv('PUBLISH_TO_YOUTUBE', 'true').lower() == 'true',
        
        'videos_per_day': int(os.getenv('VIDEOS_PER_DAY', '3')),
        'generation_hours': os.getenv('GENERATION_HOURS', '09:00,15:00,21:00').split(','),
        
        'default_duration': int(os.getenv('DEFAULT_DURATION', '45')),
        'default_style': os.getenv('DEFAULT_STYLE', 'energetic'),
        'default_topics': os.getenv('DEFAULT_TOPICS', 'космос,наука,технологии').split(','),
        
        'auto_publish': os.getenv('AUTO_PUBLISH', 'false').lower() == 'true',
        'cache_enabled': os.getenv('CACHE_ENABLED', 'true').lower() == 'true',
        'debug': os.getenv('DEBUG', 'false').lower() == 'true',
    })
    
    return config