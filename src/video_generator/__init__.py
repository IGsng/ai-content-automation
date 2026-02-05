import logging
from pathlib import Path
from typing import Optional
import hashlib

logger = logging.getLogger(__name__)

class VideoGenerator:
    def __init__(self, config):
        self.config = config
        self.provider = config.get('video_api_provider', 'replicate')
        self.output_dir = Path('output/video')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def generate(self, prompt: str, duration: int, style: str = 'energetic') -> Optional[Path]:
        try:
            if self.provider == 'replicate':
                return await self._replicate_generate(prompt, duration)
            else:
                return await self._placeholder_generate(prompt)
        except Exception as e:
            logger.error(f'Video gen error: {e}')
            return None
    
    async def _replicate_generate(self, prompt: str, duration: int) -> Optional[Path]:
        try:
            import replicate
            
            api_token = self.config.get('replicate_api_token')
            if not api_token:
                logger.warning('No Replicate API token, using placeholder')
                return await self._placeholder_generate(prompt)
            
            output = replicate.run(
                "wan-ai/wan2.2:latest",
                input={"prompt": prompt, "duration": duration}
            )
            
            prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
            output_path = self.output_dir / f'video_{prompt_hash}.mp4'
            
            import requests
            response = requests.get(output)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f'Video generated: {output_path}')
            return output_path
        except Exception as e:
            logger.error(f'Replicate error: {e}')
            return await self._placeholder_generate(prompt)
    
    async def _placeholder_generate(self, prompt: str) -> Optional[Path]:
        try:
            import cv2
            import numpy as np
            
            prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
            output_path = self.output_dir / f'placeholder_{prompt_hash}.mp4'
            
            width, height = 1080, 1920
            fps = 30
            duration = 10
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
            
            for i in range(fps * duration):
                frame = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
                color = (50 + i % 200, 100, 150)
                cv2.rectangle(frame, (100, 100), (width-100, height-100), color, -1)
                
                text = f'AI Video: {prompt[:30]}...'
                cv2.putText(frame, text, (150, height//2), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
                
                out.write(frame)
            
            out.release()
            logger.info(f'Placeholder video: {output_path}')
            return output_path
        except Exception as e:
            logger.error(f'Placeholder error: {e}')
            return None