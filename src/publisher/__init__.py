import logging
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)

class ContentPublisher:
    def __init__(self, config):
        self.config = config
        self.blotato_api_key = config.get('blotato_api_key')
    
    async def publish(
        self,
        video_path: Path,
        platforms: Optional[List[str]] = None
    ) -> bool:
        if platforms is None:
            platforms = []
            if self.config.get('publish_to_tiktok'):
                platforms.append('tiktok')
            if self.config.get('publish_to_instagram'):
                platforms.append('instagram')
            if self.config.get('publish_to_youtube'):
                platforms.append('youtube')
        
        if not platforms:
            logger.warning('No platforms enabled')
            return False
        
        try:
            success_count = 0
            
            for platform in platforms:
                if await self._publish_to_platform(video_path, platform):
                    success_count += 1
            
            return success_count > 0
        except Exception as e:
            logger.error(f'Publishing error: {e}')
            return False
    
    async def _publish_to_platform(self, video_path: Path, platform: str) -> bool:
        try:
            if not self.blotato_api_key:
                logger.warning(f'No API key for {platform}, skipping')
                return False
            
            import httpx
            
            logger.info(f'Publishing to {platform}')
            
            # Blotato API
            async with httpx.AsyncClient(timeout=120.0) as client:
                with open(video_path, 'rb') as video_file:
                    files = {'video': video_file}
                    data = {
                        'title': 'Интересный факт! 🤯',
                        'platform': platform
                    }
                    headers = {'Authorization': f'Bearer {self.blotato_api_key}'}
                    
                    response = await client.post(
                        'https://api.blotato.com/v1/upload',
                        files=files,
                        data=data,
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        logger.info(f'✅ Published to {platform}')
                        return True
                    else:
                        logger.error(f'{platform} error: {response.status_code}')
                        return False
        except Exception as e:
            logger.error(f'{platform} publish error: {e}')
            return False