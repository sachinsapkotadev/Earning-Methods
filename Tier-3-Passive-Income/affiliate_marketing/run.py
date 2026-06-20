"""
AFFILIATE MARKETING TOOL
For: Sachin Sapkota | Nepal
Earning: NPR 5,000-25,000+/month
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


class AffiliateMarketing:
    def __init__(self, provider: str = "groq"):
        self.ai = AIEngine(provider)
        self.content_created = 0

    def product_review(self, product: str, platform: str = "Amazon") -> str:
        console.print(f"[yellow]Writing review for: {product}...[/yellow]")
        prompt = f"""Write a detailed affiliate product review:

Product: {product}
Affiliate platform: {platform}

Include:
- Attention-grabbing headline
- Product overview
- Key features and specs
- Pros and cons (be honest)
- Personal experience angle (Nepal context)
- Price comparison
- Who should buy this
- Alternative products
- Final verdict with rating
- Buy now CTA with affiliate link placeholder
- FAQ section (5 questions)
- Disclosure statement

Write 1500+ words. Be genuine and helpful."""

        result = self.ai.generate(prompt)
        self.content_created += 1
        return result

    def comparison_post(self, product_a: str, product_b: str) -> str:
        console.print(f"[yellow]Writing comparison: {product_a} vs {product_b}...[/yellow]")
        prompt = f"""Write a detailed comparison post:

Product A: {product_a}
Product B: {product_b}

Include:
- Quick verdict (winner at top)
- Detailed comparison table
- Feature-by-feature breakdown
- Price comparison (NPR if possible)
- Performance comparison
- Pros and cons of each
- Which one to buy and why
- Nepal-specific availability
- Final recommendation
- Affiliate links for both products"""

        result = self.ai.generate(prompt)
        self.content_created += 1
        return result

    def best_of_list(self, category: str, count: int = 10) -> str:
        console.print(f"[yellow]Writing best {category} list...[/yellow]")
        prompt = f"""Write a "Best {count} {category}" affiliate article:

Include for each product:
- Product name and image placeholder
- Key specs
- Why it's on this list
- Price (estimate)
- Pros and cons
- Rating (out of 5)
- Buy now link placeholder

Also include:
- Buying guide section
- How we chose these products
- FAQ section
- Comparison table
- Winner highlight

Write 2000+ words. Target SEO keyword: "best {category.lower()} Nepal" """

        result = self.ai.generate(prompt)
        self.content_created += 1
        return result

    def landing_page_copy(self, product: str) -> str:
        console.print(f"[yellow]Writing landing page copy...[/yellow]")
        prompt = f"""Write high-converting affiliate landing page copy:

Product: {product}

Include:
- Headline (attention-grabbing)
- Subheadline
- Problem statement
- Solution introduction
- Features with benefits
- Social proof section
- Testimonials (template)
- Price anchoring
- Urgency elements
- CTA buttons text
- Money-back guarantee mention
- FAQ section
- Final CTA
- P.S. line

Write in persuasive, conversion-focused style."""

        result = self.ai.generate(prompt)
        self.content_created += 1
        return result

    def email_sequence(self, product: str, emails: int = 5) -> str:
        console.print(f"[yellow]Writing {emails}-email sequence...[/yellow]")
        result = self.ai.email_sequence(f"promote {product}", emails)
        self.content_created += 1
        return result

    def social_promo(self, product: str, platform: str) -> str:
        console.print(f"[yellow]Writing {platform} promo content...[/yellow]")
        prompt = f"""Create promotional content for {platform}:

Product: {product}

Include:
- 5 posts with affiliate angle
- Each with hook, value, CTA
- Relevant hashtags
- Link placement suggestions
- Disclosure (#ad or #affiliate)
- Engagement boosters
- Story/reel ideas

Make them engaging, not salesy."""

        result = self.ai.generate(prompt)
        self.content_created += 1
        return result

    def niche_finder(self, interest: str) -> str:
        console.print(f"[yellow]Finding affiliate niches...[/yellow]")
        prompt = f"""Find profitable affiliate marketing niches related to: {interest}

Include:
- 5 niche ideas
- Commission rates for each
- Available affiliate programs
- Competition analysis
- Content strategy for each
- Nepal-specific opportunities
- Monthly income potential
- Recommended starting niche

Focus on programs that work in Nepal."""

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
            "[bold cyan]AFFILIATE MARKETING TOOL[/bold cyan]\n"
            "[yellow]NPR 5,000-25,000+/month potential[/yellow]\n"
            "[dim]Reviews, comparisons, landing pages, promotions[/dim]",
            border_style="bright_magenta",
        )
    )

    provider = Prompt.ask("AI Provider", default="groq")
    aff = AffiliateMarketing(provider)

    while True:
        console.print()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Tool", style="cyan")
        table.add_column("What it does")
        tools = [
            ("1", "Product Review", "Write detailed product review"),
            ("2", "Comparison Post", "Compare two products"),
            ("3", "Best Of List", "Write top 10 product list"),
            ("4", "Landing Page", "Write conversion copy"),
            ("5", "Email Sequence", "Write promo email sequence"),
            ("6", "Social Promo", "Write social media promo posts"),
            ("7", "Niche Finder", "Find profitable niches"),
            ("8", "Stats", "View stats"),
            ("0", "Exit", "Exit affiliate tool"),
        ]
        for num, tool, desc in tools:
            table.add_row(num, tool, desc)
        console.print(table)

        choice = Prompt.ask("\n[green]Select tool[/green]", default="0")

        try:
            if choice == "0":
                console.print(f"[yellow]Content created: {aff.content_created} | Keep promoting![/yellow]")
                break
            elif choice == "1":
                product = Prompt.ask("Product name")
                platform = Prompt.ask("Platform (Amazon/Daraz/Other)", default="Amazon")
                result = aff.product_review(product, platform)
                console.print(Panel(result[:500] + "...", title="Review Preview"))
                if Confirm.ask("Save full review?"):
                    aff.save(result, f"review_{product.replace(' ', '_')}.md")
            elif choice == "2":
                a = Prompt.ask("Product A")
                b = Prompt.ask("Product B")
                result = aff.comparison_post(a, b)
                console.print(Panel(result[:500] + "...", title="Comparison Preview"))
                if Confirm.ask("Save?"):
                    aff.save(result, f"vs_{a.replace(' ', '_')}_vs_{b.replace(' ', '_')}.md")
            elif choice == "3":
                category = Prompt.ask("Category (e.g., laptops, phones, cameras)")
                count = int(Prompt.ask("How many products?", default="10"))
                result = aff.best_of_list(category, count)
                console.print(Panel(result[:500] + "...", title="List Preview"))
                if Confirm.ask("Save?"):
                    aff.save(result, f"best_{category.replace(' ', '_')}.md")
            elif choice == "4":
                product = Prompt.ask("Product name")
                result = aff.landing_page_copy(product)
                console.print(Panel(result[:500] + "...", title="Landing Page"))
                if Confirm.ask("Save?"):
                    aff.save(result, f"landing_{product.replace(' ', '_')}.md")
            elif choice == "5":
                product = Prompt.ask("Product name")
                count = int(Prompt.ask("Number of emails", default="5"))
                result = aff.email_sequence(product, count)
                console.print(Panel(result[:500] + "...", title="Email Sequence"))
                if Confirm.ask("Save?"):
                    aff.save(result, f"emails_{product.replace(' ', '_')}.md")
            elif choice == "6":
                product = Prompt.ask("Product name")
                platform = Prompt.ask("Platform (Instagram/Facebook/TikTok)")
                result = aff.social_promo(product, platform)
                console.print(Panel(result[:500] + "...", title="Social Promo"))
                if Confirm.ask("Save?"):
                    aff.save(result, f"promo_{platform}_{product.replace(' ', '_')}.md")
            elif choice == "7":
                interest = Prompt.ask("Your interest")
                result = aff.niche_finder(interest)
                console.print(Panel(result[:800] + "...", title="Niche Ideas"))
                if Confirm.ask("Save?"):
                    aff.save(result, f"niches_{interest.replace(' ', '_')}.md")
            elif choice == "8":
                console.print(Panel(
                    f"Content Created: {aff.content_created}",
                    title="Stats",
                ))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
