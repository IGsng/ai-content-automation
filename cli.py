#!/usr/bin/env python3
"""CLI interface for AI Content Automation"""

import asyncio
import click
from pathlib import Path
from rich.console import Console

console = Console()

@click.group()
def cli():
    """🤖 AI Content Automation CLI"""
    pass

@cli.command()
@click.option('--topic', '-t', default='интересные факты', help='Topic')
@click.option('--duration', '-d', default=45, type=int, help='Duration')
def generate(topic, duration):
    """Generate a single video"""
    console.print(f"[cyan]🎬 Generating video: {topic}[/cyan]")
    
    async def run():
        from src.pipeline import ContentPipeline
        from src.utils.config import load_config
        
        config = load_config()
        pipeline = ContentPipeline(config)
        
        video_path = await pipeline.generate_video(
            topic=topic,
            duration=duration
        )
        
        if video_path:
            console.print(f"[green]✅ Video: {video_path}[/green]")
        else:
            console.print("[red]❌ Failed[/red]")
    
    asyncio.run(run())

@cli.command()
def init():
    """Initialize project"""
    console.print("[cyan]🚀 Initializing...[/cyan]")
    
    dirs = ['output', 'logs', 'models', 'cache', 'temp', 'config']
    for d in dirs:
        Path(d).mkdir(exist_ok=True)
    
    if not Path('.env').exists():
        import shutil
        shutil.copy('.env.example', '.env')
        console.print("[green]✅ Created .env[/green]")
    
    console.print("[green]✅ Done![/green]")

if __name__ == '__main__':
    cli()