import asyncio
import logging
from datetime import datetime
from typing import Dict
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)

class ContentScheduler:
    def __init__(self, pipeline, config: Dict):
        self.pipeline = pipeline
        self.config = config
        self.scheduler = AsyncIOScheduler()
        
        self.videos_per_day = config.get('videos_per_day', 3)
        self.generation_hours = config.get('generation_hours', ['09:00', '15:00', '21:00'])
        self.topics = config.get('default_topics', ['космос', 'наука'])
        self.current_topic_index = 0
        
        logger.info(f'Scheduler: {self.videos_per_day} videos/day')
    
    def _get_next_topic(self) -> str:
        topic = self.topics[self.current_topic_index]
        self.current_topic_index = (self.current_topic_index + 1) % len(self.topics)
        return topic
    
    async def generate_and_publish(self):
        try:
            topic = self._get_next_topic()
            logger.info(f'Scheduled: {topic}')
            
            video_path = await self.pipeline.generate_video(
                topic=topic,
                duration=self.config.get('default_duration', 45)
            )
            
            if video_path and self.config.get('auto_publish'):
                await self.pipeline.publish(video_path)
                logger.info(f'✅ Complete: {topic}')
        except Exception as e:
            logger.error(f'Scheduled task error: {e}')
    
    async def start(self):
        logger.info('Starting scheduler...')
        
        for hour_str in self.generation_hours:
            hour, minute = map(int, hour_str.split(':'))
            self.scheduler.add_job(
                self.generate_and_publish,
                CronTrigger(hour=hour, minute=minute),
                id=f'gen_{hour}_{minute}'
            )
            logger.info(f'Scheduled: {hour_str}')
        
        self.scheduler.start()
        logger.info('✅ Scheduler running')
        
        try:
            while True:
                await asyncio.sleep(60)
        except KeyboardInterrupt:
            self.scheduler.shutdown()