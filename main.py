#!/usr/bin/env python3
"""
AI Content Automation System - Main Entry Point

Автоматическая система генерации видеоконтента.
"""

import asyncio
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler

from src.pipeline import ContentPipeline
from src.scheduler import ContentScheduler
from src.utils.config import load_config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("ai_content")
console = Console()


def setup_environment():
    """Инициализация окружения."""
    # Load environment variables
    load_dotenv()
    
    # Create necessary directories
    directories = ['output', 'logs', 'models', 'cache', 'temp']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    logger.info("✅ Environment initialized")


def check_dependencies():
    """Проверка установленных зависимостей."""
    try:
        import torch
        import ffmpeg
        logger.info(f"✅ PyTorch: {torch.__version__}")
        logger.info(f"✅ FFmpeg: installed")
        
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            logger.info(f"🎮 GPU detected: {gpu_name}")
        else:
            logger.warning("⚠️  No GPU detected, using CPU (slower)")
            
    except ImportError as e:
        logger.error(f"❌ Missing dependency: {e}")
        sys.exit(1)


async def main():
    """Основная функция запуска."""
    console.print("[bold cyan]🤖 AI Content Automation System[/bold cyan]")
    console.print("[dim]Starting up...[/dim]\n")
    
    # Setup
    setup_environment()
    check_dependencies()
    
    # Load configuration
    config = load_config()
    
    # Initialize pipeline
    pipeline = ContentPipeline(config)
    
    # Check if scheduling is enabled
    if config.get('scheduling', {}).get('enabled', False):
        logger.info("📅 Starting scheduled content generation...")
        scheduler = ContentScheduler(pipeline, config)
        await scheduler.start()
    else:
        logger.info("🎬 Running single video generation...")
        
        # Generate one video
        video_path = await pipeline.generate_video(
            topic=config.get('default_topic', 'интересные факты'),
            duration=config.get('default_duration', 45)
        )
        
        if video_path:
            console.print(f"\n[green]✅ Video generated: {video_path}[/green]")
            
            # Publish if enabled
            if config.get('auto_publish', False):
                await pipeline.publish(video_path)
                console.print("[green]✅ Published to social media[/green]")
        else:
            console.print("[red]❌ Video generation failed[/red]")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        logger.exception("Fatal error")
        sys.exit(1)