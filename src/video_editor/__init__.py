import logging
from pathlib import Path
from typing import Optional
import hashlib
from datetime import datetime

logger = logging.getLogger(__name__)

class VideoEditor:
    def __init__(self, config):
        self.config = config
        self.output_dir = Path('output/final')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def compose(
        self,
        video_path: Optional[Path],
        audio_path: Optional[Path],
        script: str,
        duration: int = 45
    ) -> Optional[Path]:
        try:
            import ffmpeg
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = self.output_dir / f'video_{timestamp}.mp4'
            
            if not video_path or not video_path.exists():
                logger.error('Video path invalid')
                return None
            
            if audio_path and audio_path.exists():
                logger.info('Merging video + audio')
                
                video_input = ffmpeg.input(str(video_path))
                audio_input = ffmpeg.input(str(audio_path))
                
                stream = ffmpeg.output(
                    video_input,
                    audio_input,
                    str(output_path),
                    vcodec='libx264',
                    acodec='aac',
                    video_bitrate='5000k',
                    audio_bitrate='192k',
                    preset='fast'
                )
                
                ffmpeg.run(stream, overwrite_output=True, quiet=True)
            else:
                logger.info('Video only (no audio)')
                import shutil
                shutil.copy(video_path, output_path)
            
            logger.info(f'Final video: {output_path}')
            return output_path
        except Exception as e:
            logger.error(f'Compose error: {e}')
            return None
    
    async def add_subtitles(self, video_path: Path, script: str) -> Optional[Path]:
        try:
            srt_path = video_path.with_suffix('.srt')
            
            words = script.split()
            words_per_segment = 10
            duration_per_segment = 3
            
            with open(srt_path, 'w', encoding='utf-8') as f:
                for i, chunk_start in enumerate(range(0, len(words), words_per_segment)):
                    chunk = ' '.join(words[chunk_start:chunk_start + words_per_segment])
                    start_time = i * duration_per_segment
                    end_time = start_time + duration_per_segment
                    
                    f.write(f'{i+1}\n')
                    f.write(f'{self._format_time(start_time)} --> {self._format_time(end_time)}\n')
                    f.write(f'{chunk}\n\n')
            
            logger.info(f'Subtitles: {srt_path}')
            return srt_path
        except Exception as e:
            logger.error(f'Subtitles error: {e}')
            return None
    
    def _format_time(self, seconds: int) -> str:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f'{hours:02d}:{minutes:02d}:{secs:02d},000'