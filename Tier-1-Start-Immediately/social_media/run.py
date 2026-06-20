"""
SOCIAL MEDIA MANAGEMENT TOOL
For: Sachin Sapkota | Nepal
Works on: Fiverr, Upwork, Local businesses
Earning: NPR 10,000-40,000/month
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
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
SCHEDULE_DIR = Path(__file__).parent / "schedule"
SCHEDULE_DIR.mkdir(exist_ok=True)


class SocialMediaManager:
    def __init__(self, provider: str = "groq"):
        self.ai = AIEngine(provider)
        self.posts_generated = 0

    def generate_posts(self, brand: str, platform: str, count: int = 5, niche: str = "") -> list:
        console.print(f"[yellow]Generating {count} {platform} posts for {brand}...[/yellow]")
        result = self.ai.social_media_posts(brand, platform, count, niche)
        posts = [p.strip() for p in result.split("---POST---") if p.strip()]
        self.posts_generated += len(posts)
        return posts

    def generate_content_calendar(self, brand: str, niche: str, days: int = 30) -> str:
        console.print(f"[yellow]Generating {days}-day content calendar for {brand}...[/yellow]")
        prompt = f"""Create a {days}-day social media content calendar for: {brand}
Niche: {niche}

For each day include:
- Day number and date
- Platform (mix of Instagram, Facebook, TikTok)
- Content type (image/reel/story/post)
- Caption
- Hashtags (5-10 relevant)
- Best posting time for Nepal audience

Format as a structured calendar. Mix between:
- Educational content (30%)
- Engaging/fun content (30%)
- Promotional content (20%)
- User-generated content (20%)"""

        return self.ai.generate(prompt)

    def generate_hashtag_sets(self, niche: str, count: int = 5) -> str:
        console.print(f"[yellow]Generating hashtag sets for {niche}...[/yellow]")
        prompt = f"""Generate {count} sets of hashtags for: {niche}

Each set should have:
- 15-20 hashtags
- Mix of popular (1M+), medium (100K-1M), and niche (<100K)
- Nepal-specific hashtags included
- Instagram, TikTok, and Facebook relevant

Label each set (Set 1, Set 2, etc.) and include estimated reach."""

        return self.ai.generate(prompt)

    def generate_bio(self, brand: str, platform: str) -> str:
        console.print(f"[yellow]Generating {platform} bio for {brand}...[/yellow]")
        prompt = f"""Create 3 bio options for a {platform} account:
Brand: {brand}

For each bio include:
- Main headline
- Description
- CTA
- Emoji usage (strategic, not excessive)
- Link suggestion

Keep within platform character limits.
Make it professional and engaging for Nepal audience."""

        return self.ai.generate(prompt)

    def generate_ad_copy(self, product: str, platform: str, budget: str) -> str:
        console.print(f"[yellow]Generating ad copy...[/yellow]")
        prompt = f"""Write ad copy for:
Product: {product}
Platform: {platform}
Budget: {budget}

Include:
- Primary text (125 chars for FB)
- Headline (40 chars)
- Description (30 chars)
- CTA button text
- 3 variations to A/B test
- Target audience suggestion for Nepal"""

        return self.ai.generate(prompt)

    def create_post(self, content: str, platform: str, schedule_time: str = "") -> dict:
        post = {
            "content": content,
            "platform": platform,
            "scheduled_time": schedule_time,
            "status": "scheduled" if schedule_time else "draft",
            "created_at": datetime.now().isoformat(),
        }
        return post

    def save_calendar(self, calendar: str, brand: str) -> str:
        filename = f"calendar_{brand.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md"
        filepath = OUTPUT_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(calendar)
        console.print(f"[green]Calendar saved -> {filepath}[/green]")
        return str(filepath)

    def save_posts(self, posts: list, brand: str, platform: str) -> str:
        filename = f"posts_{brand.replace(' ', '_')}_{platform}_{datetime.now().strftime('%Y%m%d')}.md"
        filepath = OUTPUT_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# Social Media Posts\n\n")
            f.write(f"**Brand:** {brand}\n")
            f.write(f"**Platform:** {platform}\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n\n")
            for i, post in enumerate(posts, 1):
                f.write(f"## Post {i}\n\n{post}\n\n---\n\n")
        console.print(f"[green]Posts saved -> {filepath}[/green]")
        return str(filepath)


def main():
    console.print(
        Panel.fit(
            "[bold cyan]SOCIAL MEDIA MANAGEMENT TOOL[/bold cyan]\n"
            "[yellow]NPR 10,000-40,000/month potential[/yellow]\n"
            "[dim]Manage multiple client pages simultaneously[/dim]",
            border_style="bright_magenta",
        )
    )

    provider = Prompt.ask("AI Provider", default="groq")
    smm = SocialMediaManager(provider)

    while True:
        console.print()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Tool", style="cyan")
        table.add_column("What it does")
        tools = [
            ("1", "Generate Posts", "Create posts for any platform"),
            ("2", "Content Calendar", "30-day content plan"),
            ("3", "Hashtag Sets", "Generate hashtag collections"),
            ("4", "Bio Generator", "Create platform bio"),
            ("5", "Ad Copy", "Write social media ad copy"),
            ("6", "Batch Posts", "Generate posts for multiple brands"),
            ("7", "Stats", "View generation stats"),
            ("0", "Exit", "Exit social media tool"),
        ]
        for num, tool, desc in tools:
            table.add_row(num, tool, desc)
        console.print(table)

        choice = Prompt.ask("\n[green]Select tool[/green]", default="0")

        try:
            if choice == "0":
                console.print(f"[yellow]Posts generated: {smm.posts_generated} | Keep going![/yellow]")
                break
            elif choice == "1":
                brand = Prompt.ask("Brand/business name")
                platform = Prompt.ask("Platform (Instagram/Facebook/Twitter/TikTok)")
                count = int(Prompt.ask("Number of posts", default="5"))
                niche = Prompt.ask("Niche (optional)", default="")
                posts = smm.generate_posts(brand, platform, count, niche)
                for i, post in enumerate(posts, 1):
                    console.print(f"\n[bold]Post {i}:[/bold]")
                    console.print(post)
                if Confirm.ask("Save all posts?"):
                    smm.save_posts(posts, brand, platform)
            elif choice == "2":
                brand = Prompt.ask("Brand/business name")
                niche = Prompt.ask("Niche/industry")
                days = int(Prompt.ask("Days", default="30"))
                calendar = smm.generate_content_calendar(brand, niche, days)
                console.print(Panel(calendar[:800] + "...", title="Content Calendar Preview"))
                if Confirm.ask("Save full calendar?"):
                    smm.save_calendar(calendar, brand)
            elif choice == "3":
                niche = Prompt.ask("Niche/industry")
                count = int(Prompt.ask("Number of sets", default="5"))
                result = smm.generate_hashtag_sets(niche, count)
                console.print(Panel(result, title="Hashtag Sets"))
            elif choice == "4":
                brand = Prompt.ask("Brand name")
                platform = Prompt.ask("Platform")
                result = smm.generate_bio(brand, platform)
                console.print(Panel(result, title="Bio Options"))
            elif choice == "5":
                product = Prompt.ask("Product/service")
                platform = Prompt.ask("Platform")
                budget = Prompt.ask("Ad budget")
                result = smm.generate_ad_copy(product, platform, budget)
                console.print(Panel(result, title="Ad Copy"))
            elif choice == "6":
                console.print("[dim]Enter brands one per line. Type 'done' when finished.[/dim]")
                brands = []
                while True:
                    b = Prompt.ask("Brand name")
                    if b.lower() == "done":
                        break
                    brands.append(b)
                if brands:
                    platform = Prompt.ask("Platform")
                    for brand in posts:
                        posts = smm.generate_posts(brand, platform, 3)
                        smm.save_posts(posts, brand, platform)
                    console.print(f"[green]Generated posts for {len(brands)} brands![/green]")
            elif choice == "7":
                console.print(Panel(
                    f"Posts Generated: {smm.posts_generated}\n"
                    f"Target: 20-30 posts/day for all clients",
                    title="Stats",
                ))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
