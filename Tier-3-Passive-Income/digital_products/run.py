"""
DIGITAL PRODUCTS CREATOR TOOL
For: Sachin Sapkota | Nepal
Earning: NPR 5,000-25,000+/month (sell once, earn forever)
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


class DigitalProducts:
    def __init__(self, provider: str = "groq"):
        self.ai = AIEngine(provider)
        self.products_created = 0

    def ebook(self, topic: str, chapters: int = 10) -> str:
        console.print(f"[yellow]Creating e-book: {topic} ({chapters} chapters)...[/yellow]")
        prompt = f"""Create a complete e-book outline and content:

Topic: {topic}
Chapters: {chapters}

For each chapter provide:
- Chapter title
- Chapter summary (200-300 words)
- Key points
- Practical examples
- Action items
- Chapter conclusion

Also include:
- Book title (3 options)
- Subtitle
- Book description (for Gumroad/Amazon)
- Target audience
- Unique selling points
- Introduction draft
- Conclusion draft
- Call to action (follow author, visit website)"""

        result = self.ai.generate(prompt)
        self.products_created += 1
        return result

    def template_pack(self, template_type: str, count: int = 10) -> str:
        console.print(f"[yellow]Creating {count} {template_type} templates...[/yellow]")
        prompt = f"""Create a pack of {count} {template_type} templates:

For each template:
- Template name
- Description
- Content/structure
- Customization instructions
- Use case examples

Also include:
- Bundle title
- Product description
- Pricing suggestion
- Preview descriptions
- What's included list
- How to use guide
- File format recommendations"""

        result = self.ai.generate(prompt)
        self.products_created += 1
        return result

    def notion_template(self, purpose: str) -> str:
        console.print(f"[yellow]Creating Notion template: {purpose}...[/yellow]")
        prompt = f"""Design a Notion template for: {purpose}

Include:
- Template name and description
- Database structure
- Properties and types
- Views to create
- Formulas needed
- Relations between databases
- Sample data
- Setup instructions
- Customization tips
- Pricing suggestion
- Marketing description"""

        return self.ai.generate(prompt)

    def course_curriculum(self, topic: str, lessons: int = 20) -> str:
        console.print(f"[yellow]Creating course curriculum...[/yellow]")
        prompt = f"""Create a complete online course curriculum:

Topic: {topic}
Lessons: {lessons}

For each lesson:
- Lesson title
- Learning objective
- Content outline
- Assignment/exercise
- Resources needed
- Estimated duration

Also include:
- Course title
- Course description
- Prerequisites
- What students will learn
- Target audience
- Pricing strategy
- Platform recommendations
- Marketing plan"""

        result = self.ai.generate(prompt)
        self.products_created += 1
        return result

    def canva_templates(self, template_type: str, count: int = 5) -> str:
        console.print(f"[yellow]Designing {count} Canva templates...[/yellow]")
        prompt = f"""Create specifications for {count} Canva {template_type} templates:

For each template:
- Template name
- Dimensions
- Color palette (hex codes)
- Font recommendations
- Layout description
- Element placement
- Text content
- Design tips
- Customization instructions

Also include:
- Bundle name
- Product description
- Preview mockup ideas
- How to use guide
- Pricing suggestion"""

        return self.ai.generate(prompt)

    def printables(self, product_type: str) -> str:
        console.print(f"[yellow]Creating printable product...[/yellow]")
        prompt = f"""Design a printable product: {product_type}

Include:
- Product name and description
- Pages count
- Page-by-page content layout
- Design specifications
- Print settings (size, bleed, margins)
- File format recommendations
- Preview image descriptions
- Marketing copy
- Etsy/Daraz listing description
- Pricing suggestion"""

        return self.ai.generate(prompt)

    def product_listing(self, product: str, platform: str) -> str:
        console.print(f"[yellow]Writing listing for {platform}...[/yellow]")
        prompt = f"""Write a product listing for:

Product: {product}
Platform: {platform}

Include:
- Title (SEO optimized)
- Description (2000+ words)
- Features list
- What's included
- How to use
- FAQ section
- Tags/keywords (10-15)
- Pricing recommendation
- Refund policy
- Social proof elements"""

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
            "[bold cyan]DIGITAL PRODUCTS CREATOR[/bold cyan]\n"
            "[yellow]NPR 5,000-25,000+/month potential[/yellow]\n"
            "[dim]E-books, templates, courses, printables[/dim]",
            border_style="bright_cyan",
        )
    )

    provider = Prompt.ask("AI Provider", default="groq")
    dp = DigitalProducts(provider)

    while True:
        console.print()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Tool", style="cyan")
        table.add_column("What it does")
        tools = [
            ("1", "E-Book", "Create complete e-book content"),
            ("2", "Template Pack", "Create template bundles"),
            ("3", "Notion Template", "Design Notion templates"),
            ("4", "Course Curriculum", "Create online course outline"),
            ("5", "Canva Templates", "Design Canva template specs"),
            ("6", "Printables", "Create printable products"),
            ("7", "Product Listing", "Write marketplace listing"),
            ("8", "Stats", "View stats"),
            ("0", "Exit", "Exit products tool"),
        ]
        for num, tool, desc in tools:
            table.add_row(num, tool, desc)
        console.print(table)

        choice = Prompt.ask("\n[green]Select tool[/green]", default="0")

        try:
            if choice == "0":
                console.print(f"[yellow]Products created: {dp.products_created} | Keep creating![/yellow]")
                break
            elif choice == "1":
                topic = Prompt.ask("E-book topic")
                chapters = int(Prompt.ask("Number of chapters", default="10"))
                result = dp.ebook(topic, chapters)
                console.print(Panel(result[:800] + "...", title="E-Book Preview"))
                if Confirm.ask("Save?"):
                    dp.save(result, f"ebook_{topic[:20].replace(' ', '_')}.md")
            elif choice == "2":
                ttype = Prompt.ask("Template type (resume/invoice/social/business)")
                count = int(Prompt.ask("Number of templates", default="10"))
                result = dp.template_pack(ttype, count)
                console.print(Panel(result[:800] + "...", title="Template Pack"))
                if Confirm.ask("Save?"):
                    dp.save(result, f"templates_{ttype.replace(' ', '_')}.md")
            elif choice == "3":
                purpose = Prompt.ask("Template purpose")
                result = dp.notion_template(purpose)
                console.print(Panel(result[:800] + "...", title="Notion Template"))
                if Confirm.ask("Save?"):
                    dp.save(result, f"notion_{purpose.replace(' ', '_')}.md")
            elif choice == "4":
                topic = Prompt.ask("Course topic")
                lessons = int(Prompt.ask("Number of lessons", default="20"))
                result = dp.course_curriculum(topic, lessons)
                console.print(Panel(result[:800] + "...", title="Course Curriculum"))
                if Confirm.ask("Save?"):
                    dp.save(result, f"course_{topic[:20].replace(' ', '_')}.md")
            elif choice == "5":
                ttype = Prompt.ask("Template type (social/business/marketing)")
                count = int(Prompt.ask("Number of templates", default="5"))
                result = dp.canva_templates(ttype, count)
                console.print(Panel(result[:800] + "...", title="Canva Templates"))
                if Confirm.ask("Save?"):
                    dp.save(result, f"canva_{ttype.replace(' ', '_')}.md")
            elif choice == "6":
                ptype = Prompt.ask("Product type (planner/checklist/journal)")
                result = dp.printables(ptype)
                console.print(Panel(result[:800] + "...", title="Printable"))
                if Confirm.ask("Save?"):
                    dp.save(result, f"printable_{ptype.replace(' ', '_')}.md")
            elif choice == "7":
                product = Prompt.ask("Product name")
                platform = Prompt.ask("Platform (Gumroad/Etsy/Daraz)")
                result = dp.product_listing(product, platform)
                console.print(Panel(result[:500] + "...", title="Listing"))
                if Confirm.ask("Save?"):
                    dp.save(result, f"listing_{product.replace(' ', '_')}.md")
            elif choice == "8":
                console.print(Panel(
                    f"Products Created: {dp.products_created}",
                    title="Stats",
                ))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
