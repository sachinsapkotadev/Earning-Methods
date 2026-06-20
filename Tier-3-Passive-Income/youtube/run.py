"""
YOUTUBE CHANNEL AUTOMATION TOOL
For: Sachin Sapkota | Nepal
Earning: NPR 5,000-50,000+/month (ads + sponsorships)
"""
import os
import sys
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "ai-system"))
from core.ai_engine import AIEngine

load_dotenv(Path(__file__).parent.parent.parent / "ai-system" / ".env")

console = Console()
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


class YouTubeAutomation:
    def __init__(self, provider: str = "groq"):
        self.ai = AIEngine(provider)
        self.scripts_written = 0

    def video_script(self, topic: str, duration: int = 10) -> str:
        console.print(f"[yellow]Writing script: {topic} ({duration} min)...[/yellow]")
        result = self.ai.youtube_script(topic, duration)
        self.scripts_written += 1
        return result

    def channel_idea(self, niche: str) -> str:
        console.print(f"[yellow]Generating channel ideas for {niche}...[/yellow]")
        prompt = f"""Create YouTube channel strategy for niche: {niche}

Include:
- 5 channel name ideas
- Channel description/bio
- Content pillars (3-5 topics)
- 30 video ideas (mix of trending + evergreen)
- Upload schedule recommendation
- Thumbnail style guide
- SEO strategy for YouTube
- Growth milestones (1K, 10K, 50K subs)
- Monetization roadmap
- Nepal audience specific tips
- Equipment recommendations (budget-friendly)
- Editing workflow"""

        result = self.ai.generate(prompt)
        return result

    def seo_optimize(self, title: str) -> str:
        console.print(f"[yellow]Optimizing video SEO...[/yellow]")
        prompt = f"""Optimize this YouTube video for SEO:

Video title: {title}

Provide:
- Optimized title (60 chars max)
- Description (5000 chars with keywords)
- 30 relevant tags
- Hashtags (3-5)
- Timestamps/chapters
- Pinned comment suggestion
- End screen strategy
- Card suggestions
- Playlist placement
- Related video suggestions"""

        return self.ai.generate(prompt)

    def thumbnail_ideas(self, title: str, count: int = 3) -> str:
        console.print(f"[yellow]Creating thumbnail concepts...[/yellow]")
        prompt = f"""Create {count} thumbnail concepts for video:
Title: {title}

For each concept:
- Main visual element
- Text overlay (max 4 words)
- Color scheme
- Face expression suggestion
- Background idea
- Contrast tips
- Mobile readability check
- A/B testing recommendation"""

        return self.ai.generate(prompt)

    def title_variations(self, topic: str, count: int = 10) -> str:
        console.print(f"[yellow]Generating {count} title variations...[/yellow]")
        prompt = f"""Generate {count} YouTube title variations for: {topic}

Include mix of:
- How-to titles
- List titles
- Question titles
- Comparison titles
- Numbers/stats titles
- Emotional hook titles
- Nepal-specific titles

Each title should be:
- Under 60 characters
- Include primary keyword
- Click-worthy but not clickbait
- SEO optimized"""

        return self.ai.generate(prompt)

    def content_calendar(self, niche: str, weeks: int = 4) -> str:
        console.print(f"[yellow]Creating {weeks}-week content calendar...[/yellow]")
        prompt = f"""Create a {weeks}-week YouTube content calendar for: {niche}

For each week include:
- 2-3 video ideas
- Script outline for each
- Upload day and time (Nepal time)
- Thumbnail concept
- SEO keywords
- Cross-promotion strategy
- Community post ideas

Mix between:
- Tutorial/educational (40%)
- Trending/topical (20%)
- Evergreen content (30%)
- Community/engagement (10%)"""

        return self.ai.generate(prompt)

    def sponsor_pitch(self, channel: str, subscribers: str) -> str:
        console.print(f"[yellow]Creating sponsor pitch for {channel}...[/yellow]")
        prompt = f"""Write a YouTube sponsorship pitch:

Channel: {channel}
Subscribers: {subscribers}
Niche: (will be filled)

Include:
- Professional introduction
- Channel stats and reach
- Audience demographics (Nepal focus)
- Why this brand fits
- Content integration ideas
- Previous brand collaborations (placeholder)
- Rate card structure
- Call to action
- Contact information template"""

        return self.ai.generate(prompt)

    def batch_scripts(self, topics: list, duration: int = 10) -> str:
        results = []
        for topic in topics:
            script = self.video_script(topic, duration)
            results.append(f"# {topic}\n\n{script}\n\n---\n")
        return "\n".join(results)

    def save(self, content: str, filename: str) -> str:
        filepath = OUTPUT_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        console.print(f"[green]Saved -> {filepath}[/green]")
        return str(filepath)


def main():
    console.print(
        Panel.fit(
            "[bold cyan]YOUTUBE CHANNEL AUTOMATION[/bold cyan]\n"
            "[yellow]NPR 5,000-50,000+/month potential[/yellow]\n"
            "[dim]Scripts, SEO, thumbnails, channel growth[/dim]",
            border_style="bright_red",
        )
    )

    provider = Prompt.ask("AI Provider", default="groq")
    yt = YouTubeAutomation(provider)

    while True:
        console.print()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Tool", style="cyan")
        table.add_column("What it does")
        tools = [
            ("1", "Video Script", "Write full video scripts"),
            ("2", "Channel Idea", "Complete channel strategy"),
            ("3", "SEO Optimize", "Optimize video for search"),
            ("4", "Thumbnail Ideas", "Design thumbnail concepts"),
            ("5", "Title Ideas", "Generate video title variations"),
            ("6", "Content Calendar", "Weekly upload schedule"),
            ("7", "Sponsor Pitch", "Write brand partnership pitches"),
            ("8", "Batch Scripts", "Write multiple scripts at once"),
            ("9", "Stats", "View stats"),
            ("0", "Exit", "Exit YouTube tool"),
        ]
        for num, tool, desc in tools:
            table.add_row(num, tool, desc)
        console.print(table)

        choice = Prompt.ask("\n[green]Select tool[/green]", default="0")

        try:
            if choice == "0":
                console.print(f"[yellow]Scripts written: {yt.scripts_written} | Keep creating![/yellow]")
                break
            elif choice == "1":
                topic = Prompt.ask("Video topic")
                duration = int(Prompt.ask("Duration (minutes)", default="10"))
                result = yt.video_script(topic, duration)
                console.print(Panel(result[:800] + "...", title="Script Preview"))
                if Confirm.ask("Save full script?"):
                    yt.save(result, f"yt_{topic[:30].replace(' ', '_')}.md")
            elif choice == "2":
                niche = Prompt.ask("Your niche")
                result = yt.channel_idea(niche)
                console.print(Panel(result[:800] + "...", title="Channel Strategy"))
                if Confirm.ask("Save?"):
                    yt.save(result, f"channel_{niche.replace(' ', '_')}.md")
            elif choice == "3":
                title = Prompt.ask("Video title")
                result = yt.seo_optimize(title)
                console.print(Panel(result, title="SEO Optimization"))
            elif choice == "4":
                title = Prompt.ask("Video title")
                result = yt.thumbnail_ideas(title)
                console.print(Panel(result, title="Thumbnail Concepts"))
            elif choice == "5":
                topic = Prompt.ask("Video topic")
                result = yt.title_variations(topic)
                console.print(Panel(result, title="Title Variations"))
            elif choice == "6":
                niche = Prompt.ask("Your niche")
                weeks = int(Prompt.ask("Weeks", default="4"))
                result = yt.content_calendar(niche, weeks)
                console.print(Panel(result[:800] + "...", title="Content Calendar"))
                if Confirm.ask("Save?"):
                    yt.save(result, f"calendar_{niche.replace(' ', '_')}.md")
            elif choice == "7":
                channel = Prompt.ask("Channel name")
                subs = Prompt.ask("Subscriber count")
                result = yt.sponsor_pitch(channel, subs)
                console.print(Panel(result, title="Sponsor Pitch"))
            elif choice == "8":
                console.print("[dim]Enter topics one per line. Type 'done' when finished.[/dim]")
                topics = []
                while True:
                    t = Prompt.ask("Topic")
                    if t.lower() == "done":
                        break
                    topics.append(t)
                if topics:
                    duration = int(Prompt.ask("Duration per video (minutes)", default="10"))
                    result = yt.batch_scripts(topics, duration)
                    if Confirm.ask("Save all scripts?"):
                        yt.save(result, f"batch_{datetime.now().strftime('%Y%m%d')}.md")
            elif choice == "9":
                console.print(Panel(
                    f"Scripts Written: {yt.scripts_written}",
                    title="Stats",
                ))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
