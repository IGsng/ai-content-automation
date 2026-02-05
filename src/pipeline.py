import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class ContentPipeline:
    def __init__(self, config):
        self.config = config
        logger.info('Pipeline initialized')
    
    async def generate_video(self, topic: str, duration: int = 45) -> Optional[Path]:
        try:
            logger.info(f'Generating: {topic}')
            
            from .fact_generator import FactGenerator
            from .script_writer import ScriptWriter  
            from .voice_synthesis import VoiceSynthesizer
            from .video_generator import VideoGenerator
            from .video_editor import VideoEditor
            
            fact_gen = FactGenerator(self.config)
            script_writer = ScriptWriter(self.config)
            voice_synth = VoiceSynthesizer(self.config)
            video_gen = VideoGenerator(self.config)
            editor = VideoEditor(self.config)
            
            fact = await fact_gen.generate(topic)
            if not fact:
                return None
            
            script = await script_writer.write(fact, duration)
            if not script:
                return None
            
            audio_path = await voice_synth.synthesize(script)
            video_path = await video_gen.generate(fact, duration)
            
            final = await editor.compose(video_path, audio_path, script)
            
            logger.info(f'Done: {final}')
            return final
        except Exception as e:
            logger.error(f'Error: {e}')
            return None
    
    async def publish(self, video_path, platforms=None):
        from .publisher import ContentPublisher
        publisher = ContentPublisher(self.config)
        return await publisher.publish(video_path, platforms)