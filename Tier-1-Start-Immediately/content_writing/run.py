"""
CONTENT WRITING AUTOMATION SYSTEM
For: Sachin Sapkota | Nepal
Works on: Fiverr, Upwork, Medium
Earning: NPR 8,000-25,000/month
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


class ContentWriter:
    def __init__(self, provider: str = "groq"):
        self.ai = AIEngine(provider)
        self.articles_written = 0

    def write_blog(self, topic: str, words: int = 1500, keyword: str = "") -> str:
        console.print(f"[yellow]Writing blog: {topic} ({words} words)...[/yellow]")
        result = self.ai.blog_post(topic, words, keyword)
        self.articles_written += 1
        return result

    def write_article(self, topic: str, words: int = 2000) -> str:
        console.print(f"[yellow]Writing article: {topic}...[/yellow]")
        prompt = f"""Write a well-researched article about: {topic}
Word count: {words} words
Include:
- Catchy headline
- Engaging introduction
- Subheadings (H2, H3)
- Examples and data
- Conclusion with key takeaways
- Write in professional but accessible tone"""

        result = self.ai.generate(prompt)
        self.articles_written += 1
        return result

    def write_product_description(self, product: str, features: list = None) -> str:
        console.print(f"[yellow]Writing product description: {product}...[/yellow]")
        return self.ai.product_description(product, features)

    def write_email_copy(self, purpose: str, audience: str) -> str:
        console.print(f"[yellow]Writing email copy...[/yellow]")
        prompt = f"""Write email copy:
Purpose: {purpose}
Target audience: {audience}

Include:
- Subject line (with A/B variant)
- Preview text
- Body copy
- CTA button text
- P.S. line

Write in a natural, conversational tone that converts."""

        return self.ai.generate(prompt)

    def rewrite_content(self, original: str, style: str = "professional") -> str:
        console.print(f"[yellow]Rewriting content ({style} style)...[/yellow]")
        prompt = f"""Rewrite this content in {style} style while keeping the core message:

{original}

Requirements:
- Maintain key information
- Improve flow and readability
- {style.title()} tone
- Fix any grammar issues"""

        return self.ai.generate(prompt)

    def proofread(self, text: str) -> str:
        console.print("[yellow]Proofreading...[/yellow]")
        prompt = f"""Proofread this text and fix all errors:

{text}

Return:
1. Corrected text
2. List of changes made
3. Writing score (1-10)"""

        return self.ai.generate(prompt)

    def batch_write(self, topics: list) -> list:
        results = []
        for topic in topics:
            content = self.write_blog(topic)
            results.append({"topic": topic, "content": content})
        return results

    def save(self, content: str, filename: str = None) -> str:
        if not filename:
            filename = f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = OUTPUT_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        console.print(f"[green]Saved -> {filepath}[/green]")
        return str(filepath)


def main():
    console.print(
        Panel.fit(
            "[bold cyan]CONTENT WRITING TOOL[/bold cyan]\n"
            "[yellow]NPR 8,000-25,000/month potential[/yellow]\n"
            "[dim]AI-powered content creation[/dim]",
            border_style="bright_green",
        )
    )

    provider = Prompt.ask("AI Provider", default="groq")
    writer = ContentWriter(provider)

    while True:
        console.print()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Tool", style="cyan")
        table.add_column("What it does")
        tools = [
            ("1", "Blog Post", "Write SEO blog post on any topic"),
            ("2", "Article", "Write long-form article"),
            ("3", "Product Description", "Write e-commerce product description"),
            ("4", "Email Copy", "Write marketing email copy"),
            ("5", "Rewrite", "Rewrite content in different style"),
            ("6", "Proofread", "Check and fix grammar/style"),
            ("7", "Batch Write", "Write multiple articles at once"),
            ("8", "Stats", "View writing stats"),
            ("0", "Exit", "Exit content writer"),
        ]
        for num, tool, desc in tools:
            table.add_row(num, tool, desc)
        console.print(table)

        choice = Prompt.ask("\n[green]Select tool[/green]", default="0")

        try:
            if choice == "0":
                console.print(f"[yellow]Articles written: {writer.articles_written} | Keep writing![/yellow]")
                break
            elif choice == "1":
                topic = Prompt.ask("Blog topic")
                words = int(Prompt.ask("Word count", default="1500"))
                keyword = Prompt.ask("SEO keyword (optional)", default="")
                result = writer.write_blog(topic, words, keyword)
                console.print(Panel(result[:500] + "...", title="Blog Post Preview"))
                if Confirm.ask("Save full article?"):
                    writer.save(result, f"blog_{topic[:30].replace(' ', '_')}.md")
            elif choice == "2":
                topic = Prompt.ask("Article topic")
                words = int(Prompt.ask("Word count", default="2000"))
                result = writer.write_article(topic, words)
                console.print(Panel(result[:500] + "...", title="Article Preview"))
                if Confirm.ask("Save full article?"):
                    writer.save(result, f"article_{topic[:30].replace(' ', '_')}.md")
            elif choice == "3":
                product = Prompt.ask("Product name")
                features = Prompt.ask("Features (comma-separated)").split(",")
                result = writer.write_product_description(product, [f.strip() for f in features])
                console.print(Panel(result, title="Product Description"))
            elif choice == "4":
                purpose = Prompt.ask("Email purpose")
                audience = Prompt.ask("Target audience")
                result = writer.write_email_copy(purpose, audience)
                console.print(Panel(result, title="Email Copy"))
            elif choice == "5":
                console.print("[dim]Paste your content (press Enter twice when done):[/dim]")
                lines = []
                while True:
                    line = input()
                    if line == "" and lines and lines[-1] == "":
                        break
                    lines.append(line)
                original = "\n".join(lines)
                style = Prompt.ask("Style (professional/casual/formal/engaging)", default="professional")
                result = writer.rewrite_content(original, style)
                console.print(Panel(result, title="Rewritten Content"))
            elif choice == "6":
                console.print("[dim]Paste content to proofread (press Enter twice when done):[/dim]")
                lines = []
                while True:
                    line = input()
                    if line == "" and lines and lines[-1] == "":
                        break
                    lines.append(line)
                text = "\n".join(lines)
                result = writer.proofread(text)
                console.print(Panel(result, title="Proofread Result"))
            elif choice == "7":
                console.print("[dim]Enter topics one per line. Type 'done' when finished.[/dim]")
                topics = []
                while True:
                    t = Prompt.ask("Topic")
                    if t.lower() == "done":
                        break
                    topics.append(t)
                if topics:
                    console.print(f"[yellow]Writing {len(topics)} articles...[/yellow]")
                    results = writer.batch_write(topics)
                    for r in results:
                        writer.save(r["content"], f"blog_{r['topic'][:30].replace(' ', '_')}.md")
                    console.print(f"[green]All {len(results)} articles saved![/green]")
            elif choice == "8":
                console.print(Panel(
                    f"Articles Written: {writer.articles_written}\n"
                    f"Keep going! Target: 3-5 articles/day",
                    title="Writing Stats",
                ))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
