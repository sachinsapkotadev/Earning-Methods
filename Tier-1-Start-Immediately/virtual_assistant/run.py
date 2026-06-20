"""
VIRTUAL ASSISTANT AUTOMATION TOOL
For: Sachin Sapkota | Nepal
Works on: Upwork, Fiverr, Direct Clients
Earning: NPR 8,000-20,000/month
"""
import os
import sys
import json
import csv
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


class VirtualAssistant:
    def __init__(self, provider: str = "groq"):
        self.ai = AIEngine(provider)
        self.tasks_done = 0

    def email_drafter(self, purpose: str, recipient: str, tone: str = "professional") -> str:
        console.print(f"[yellow]Drafting email to {recipient}...[/yellow]")
        prompt = f"""Draft an email:
To: {recipient}
Purpose: {purpose}
Tone: {tone}

Include:
- Subject line
- Greeting
- Body (clear and concise)
- Call to action
- Professional closing

Keep it under 200 words. Write naturally."""

        return self.ai.generate(prompt)

    def email_responder(self, original_email: str, response_intent: str) -> str:
        console.print("[yellow]Drafting email response...[/yellow]")
        prompt = f"""Original email:
{original_email}

My response intent: {response_intent}

Write a professional reply that:
- Addresses their points
- Matches the tone
- Is clear and actionable
- Includes next steps"""

        return self.ai.generate(prompt)

    def meeting_notes(self, transcript: str) -> str:
        console.print("[yellow]Summarizing meeting notes...[/yellow]")
        prompt = f"""Convert this meeting transcript into structured notes:

{transcript}

Include:
- Meeting summary (2-3 sentences)
- Key decisions made
- Action items with owners
- Deadlines mentioned
- Follow-up items
- Next meeting date (if mentioned)"""

        return self.ai.generate(prompt)

    def data_research(self, topic: str) -> str:
        console.print(f"[yellow]Researching: {topic}...[/yellow]")
        prompt = f"""Research this topic and provide a structured report: {topic}

Include:
- Overview/summary
- Key facts and statistics
- Top 5 relevant sources/links
- Key takeaways
- Recommendations
- Sources to explore further

Be thorough and cite where possible."""

        return self.ai.generate(prompt)

    def spreadsheet_helper(self, task: str) -> str:
        console.print(f"[yellow]Creating spreadsheet formula/template...[/yellow]")
        prompt = f"""Help with this spreadsheet task: {task}

Provide:
- Formula (if applicable)
- Step-by-step instructions
- Example with sample data
- Tips for efficiency
- Common errors to avoid"""

        return self.ai.generate(prompt)

    def presentation_outline(self, topic: str, slides: int = 10) -> str:
        console.print(f"[yellow]Creating presentation outline...[/yellow]")
        prompt = f"""Create a presentation outline for: {topic}
Number of slides: {slides}

For each slide provide:
- Slide title
- Key points (3-5 bullet points)
- Speaker notes
- Suggested visuals/images
- Transition to next slide

Make it professional and engaging."""

        return self.ai.generate(prompt)

    def social_calendar(self, brand: str, days: int = 7) -> str:
        console.print(f"[yellow]Creating social media schedule...[/yellow]")
        prompt = f"""Create a {days}-day social media posting schedule for: {brand}

For each day include:
- Platform
- Post type
- Content brief
- Best posting time (Nepal time)
- Hashtag suggestions

Mix between educational, promotional, and engagement posts."""

        return self.ai.generate(prompt)

    def template_generator(self, template_type: str) -> str:
        console.print(f"[yellow]Generating {template_type} template...[/yellow]")
        prompt = f"""Create a professional template for: {template_type}

Include:
- Full template with placeholders
- Instructions for customization
- Example filled-in version
- Tips for best results"""

        return self.ai.generate(prompt)

    def save(self, content: str, filename: str) -> str:
        filepath = OUTPUT_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        console.print(f"[green]Saved -> {filepath}[/green]")
        return str(filepath)


def main():
    console.print(
        Panel.fit(
            "[bold cyan]VIRTUAL ASSISTANT TOOL[/bold cyan]\n"
            "[yellow]NPR 8,000-20,000/month potential[/yellow]\n"
            "[dim]Admin, emails, research, scheduling[/dim]",
            border_style="bright_yellow",
        )
    )

    provider = Prompt.ask("AI Provider", default="groq")
    va = VirtualAssistant(provider)

    while True:
        console.print()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Tool", style="cyan")
        table.add_column("What it does")
        tools = [
            ("1", "Draft Email", "Write professional emails"),
            ("2", "Reply to Email", "Draft email responses"),
            ("3", "Meeting Notes", "Summarize meeting transcripts"),
            ("4", "Research", "Research any topic"),
            ("5", "Spreadsheet Help", "Formulas and templates"),
            ("6", "Presentation", "Create slide outlines"),
            ("7", "Social Schedule", "Weekly posting schedule"),
            ("8", "Templates", "Generate business templates"),
            ("9", "Stats", "View task stats"),
            ("0", "Exit", "Exit VA tool"),
        ]
        for num, tool, desc in tools:
            table.add_row(num, tool, desc)
        console.print(table)

        choice = Prompt.ask("\n[green]Select tool[/green]", default="0")

        try:
            if choice == "0":
                console.print(f"[yellow]Tasks done: {va.tasks_done} | Great work![/yellow]")
                break
            elif choice == "1":
                purpose = Prompt.ask("Email purpose")
                recipient = Prompt.ask("Recipient")
                tone = Prompt.ask("Tone (professional/casual/formal)", default="professional")
                result = va.email_drafter(purpose, recipient, tone)
                console.print(Panel(result, title="Email Draft"))
                if Confirm.ask("Save?"):
                    va.save(result, f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
            elif choice == "2":
                console.print("[dim]Paste the email you received (press Enter twice when done):[/dim]")
                lines = []
                while True:
                    line = input()
                    if line == "" and lines and lines[-1] == "":
                        break
                    lines.append(line)
                original = "\n".join(lines)
                intent = Prompt.ask("Your response intent")
                result = va.email_responder(original, intent)
                console.print(Panel(result, title="Email Response"))
            elif choice == "3":
                console.print("[dim]Paste meeting transcript (press Enter twice when done):[/dim]")
                lines = []
                while True:
                    line = input()
                    if line == "" and lines and lines[-1] == "":
                        break
                    lines.append(line)
                transcript = "\n".join(lines)
                result = va.meeting_notes(transcript)
                console.print(Panel(result, title="Meeting Notes"))
                if Confirm.ask("Save?"):
                    va.save(result, f"meeting_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
            elif choice == "4":
                topic = Prompt.ask("Research topic")
                result = va.data_research(topic)
                console.print(Panel(result[:800] + "...", title="Research Preview"))
                if Confirm.ask("Save full report?"):
                    va.save(result, f"research_{topic[:20].replace(' ', '_')}.md")
            elif choice == "5":
                task = Prompt.ask("What do you need help with?")
                result = va.spreadsheet_helper(task)
                console.print(Panel(result, title="Spreadsheet Help"))
            elif choice == "6":
                topic = Prompt.ask("Presentation topic")
                slides = int(Prompt.ask("Number of slides", default="10"))
                result = va.presentation_outline(topic, slides)
                console.print(Panel(result[:800] + "...", title="Presentation Outline"))
                if Confirm.ask("Save?"):
                    va.save(result, f"presentation_{topic[:20].replace(' ', '_')}.md")
            elif choice == "7":
                brand = Prompt.ask("Brand name")
                days = int(Prompt.ask("Days", default="7"))
                result = va.social_calendar(brand, days)
                console.print(Panel(result, title="Social Schedule"))
            elif choice == "8":
                template = Prompt.ask("Template type (invoice/proposal/contract/report)")
                result = va.template_generator(template)
                console.print(Panel(result, title="Template"))
                if Confirm.ask("Save?"):
                    va.save(result, f"template_{template}_{datetime.now().strftime('%Y%m%d')}.md")
            elif choice == "9":
                console.print(Panel(
                    f"Tasks Completed: {va.tasks_done}\n"
                    f"Target: 10-15 tasks/day",
                    title="Stats",
                ))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
