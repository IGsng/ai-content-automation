import logging
from pathlib import Path
from typing import Optional
import hashlib

logger = logging.getLogger(__name__)

class VoiceSynthesizer:
    def __init__(self, config):
        self.config = config
        self.provider = config.get('tts_provider', 'silero')
        self.output_dir = Path('output/audio')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def synthesize(self, text: str) -> Optional[Path]:
        try:
            if self.provider == 'silero':
                return await self._silero_tts(text)
            else:
                logger.warning(f'Unknown TTS: {self.provider}')
                return await self._silero_tts(text)
        except Exception as e:
            logger.error(f'TTS error: {e}')
            return None
    
    async def _silero_tts(self, text: str) -> Optional[Path]:
        try:
            import torch
            
            device = torch.device('cpu')
            model, _ = torch.hub.load(
                repo_or_dir='snakers4/silero-models',
                model='silero_tts',
                language='ru',
                speaker='v3_1_ru'
            )
            model.to(device)
            
            audio = model.apply_tts(
                text=text,
                speaker='xenia',
                sample_rate=48000
            )
            
            text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
            output_path = self.output_dir / f'audio_{text_hash}.wav'
            
            import torchaudio
            torchaudio.save(str(output_path), audio.unsqueeze(0), 48000)
            
            logger.info(f'Audio: {output_path}')
            return output_path
        except Exception as e:
            logger.error(f'Silero error: {e}')
            return None