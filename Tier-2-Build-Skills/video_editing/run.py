"""
VIDEO EDITING ASSISTANT TOOL
For: Sachin Sapkota | Nepal
Works on: Fiverr, Upwork, YouTube clients
Earning: NPR 20,000-70,000/month
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


class VideoEditorAssistant:
    def __init__(self, provider: str = "groq"):
        self.ai = AIEngine(provider)
        self.scripts_written = 0

    def youtube_script(self, topic: str, duration: int = 10) -> str:
        console.print(f"[yellow]Writing YouTube script: {topic} ({duration} min)...[/yellow]")
        prompt = f"""Write a YouTube video script:
Topic: {topic}
Duration: {duration} minutes (approx {duration * 150} words)

Include:
- Hook (first 10 seconds - MUST grab attention)
- Intro (channel branding, topic overview)
- Main content with timestamps [00:00]
- B-roll suggestions [B-roll: description]
- Visual transition notes
- Sound effect suggestions
- Key points to emphasize
- Call to action (subscribe, like, comment)
- Outro

Format with timestamps. Make it engaging and conversational."""

        result = self.ai.generate(prompt)
        self.scripts_written += 1
        return result

    def reel_script(self, topic: str, platform: str = "Instagram") -> str:
        console.print(f"[yellow]Writing {platform} Reel script...[/yellow]")
        prompt = f"""Write a {platform} Reel/Short script:
Topic: {topic}
Duration: 30-60 seconds

Include:
- Hook (first 3 seconds)
- Main message (clear, concise)
- Visual directions [VISUAL: description]
- Text overlay suggestions
- Audio/music suggestions
- Trending hashtags
- Caption

Make it viral-worthy and attention-grabbing."""

        return self.ai.generate(prompt)

    def editing_brief(self, video_type: str, client_needs: str) -> str:
        console.print(f"[yellow]Creating editing brief...[/yellow]")
        prompt = f"""Create a video editing brief:

Video type: {video_type}
Client needs: {client_needs}

Include:
- Editing style and tone
- Color grading direction
- Music style recommendations
- Transition types
- Text/animation requirements
- Export settings
- Timeline estimate
- Revision policy
- Deliverable formats"""

        return self.ai.generate(prompt)

    def capcut_tutorial(self, effect: str) -> str:
        console.print(f"[yellow]Creating CapCut tutorial: {effect}...[/yellow]")
        prompt = f"""Create a step-by-step CapCut tutorial for: {effect}

Include:
- What this effect does
- Step-by-step instructions with screenshots description
- Timing recommendations
- Pro tips
- Common mistakes
- Alternative approaches
- Best for what type of content
- Time to implement (beginner/intermediate/advanced)"""

        return self.ai.generate(prompt)

    def thumbnail_concept(self, title: str, style: str = "clickbait") -> str:
        console.print(f"[yellow]Creating thumbnail concepts...[/yellow]")
        prompt = f"""Create thumbnail design concepts for:
Video title: {title}
Style: {style}

Include:
- 3 thumbnail concept descriptions
- Color scheme for each
- Text placement and font
- Image/face placement
- Background ideas
- Contrast and readability tips
- A/B testing recommendations
- Size and format specs (1280x720)"""

        return self.ai.generate(prompt)

    def client_script(self, project: str, deliverables: list) -> str:
        console.print(f"[yellow]Writing client script...[/yellow]")
        deliverables_text = "\n".join(f"- {d}" for d in deliverables)
        prompt = f"""Write a professional video editing client communication:

Project: {project}
Deliverables:
{deliverables_text}

Include:
- Project understanding summary
- Timeline and milestones
- What I'll deliver
- What I need from client
- Revision policy
- Payment terms
- Professional tone"""

        return self.ai.generate(prompt)

    def batch_scripts(self, topics: list, duration: int = 10) -> str:
        results = []
        for topic in topics:
            script = self.youtube_script(topic, duration)
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
            "[bold cyan]VIDEO EDITING ASSISTANT[/bold cyan]\n"
            "[yellow]NPR 20,000-70,000/month potential[/yellow]\n"
            "[dim]Scripts, thumbnails, editing guides, CapCut[/dim]",
            border_style="bright_red",
        )
    )

    provider = Prompt.ask("AI Provider", default="groq")
    vea = VideoEditorAssistant(provider)

    while True:
        console.print()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Tool", style="cyan")
        table.add_column("What it does")
        tools = [
            ("1", "YouTube Script", "Write full video scripts"),
            ("2", "Reel/Short Script", "Write short-form video scripts"),
            ("3", "Editing Brief", "Create editing project briefs"),
            ("4", "CapCut Tutorial", "Step-by-step CapCut effects"),
            ("5", "Thumbnail Concepts", "Design thumbnail ideas"),
            ("6", "Client Script", "Write client communications"),
            ("7", "Batch Scripts", "Write multiple scripts at once"),
            ("8", "Stats", "View stats"),
            ("0", "Exit", "Exit video tool"),
        ]
        for num, tool, desc in tools:
            table.add_row(num, tool, desc)
        console.print(table)

        choice = Prompt.ask("\n[green]Select tool[/green]", default="0")

        try:
            if choice == "0":
                console.print(f"[yellow]Scripts written: {vea.scripts_written} | Keep creating![/yellow]")
                break
            elif choice == "1":
                topic = Prompt.ask("Video topic")
                duration = int(Prompt.ask("Duration (minutes)", default="10"))
                result = vea.youtube_script(topic, duration)
                console.print(Panel(result[:800] + "...", title="Script Preview"))
                if Confirm.ask("Save full script?"):
                    vea.save(result, f"yt_{topic[:30].replace(' ', '_')}.md")
            elif choice == "2":
                topic = Prompt.ask("Reel topic")
                platform = Prompt.ask("Platform (Instagram/TikTok/YouTube Shorts)", default="Instagram")
                result = vea.reel_script(topic, platform)
                console.print(Panel(result, title="Reel Script"))
            elif choice == "3":
                vtype = Prompt.ask("Video type (youtube/reel/documentary/ad)")
                needs = Prompt.ask("Client needs")
                result = vea.editing_brief(vtype, needs)
                console.print(Panel(result, title="Editing Brief"))
            elif choice == "4":
                effect = Prompt.ask("CapCut effect/technique")
                result = vea.capcut_tutorial(effect)
                console.print(Panel(result, title="CapCut Tutorial"))
                if Confirm.ask("Save?"):
                    vea.save(result, f"capcut_{effect.replace(' ', '_')}.md")
            elif choice == "5":
                title = Prompt.ask("Video title")
                style = Prompt.ask("Style (clickbait/clean/dramatic)", default="clickbait")
                result = vea.thumbnail_concept(title, style)
                console.print(Panel(result, title="Thumbnail Concepts"))
            elif choice == "6":
                project = Prompt.ask("Project name")
                deliverables = Prompt.ask("Deliverables (comma-separated)").split(",")
                result = vea.client_script(project, [d.strip() for d in deliverables])
                console.print(Panel(result, title="Client Script"))
            elif choice == "7":
                console.print("[dim]Enter topics one per line. Type 'done' when finished.[/dim]")
                topics = []
                while True:
                    t = Prompt.ask("Topic")
                    if t.lower() == "done":
                        break
                    topics.append(t)
                if topics:
                    duration = int(Prompt.ask("Duration per video (minutes)", default="10"))
                    result = vea.batch_scripts(topics, duration)
                    if Confirm.ask("Save all scripts?"):
                        vea.save(result, f"batch_scripts_{datetime.now().strftime('%Y%m%d')}.md")
            elif choice == "8":
                console.print(Panel(
                    f"Scripts Written: {vea.scripts_written}",
                    title="Stats",
                ))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
