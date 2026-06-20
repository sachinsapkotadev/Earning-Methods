"""
SEO CONTENT WRITER TOOL
For: Sachin Sapkota | Nepal
Works on: Fiverr, Upwork, Direct clients
Earning: NPR 12,000-40,000/month
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


class SEOWriter:
    def __init__(self, provider: str = "groq"):
        self.ai = AIEngine(provider)
        self.articles_written = 0

    def seo_article(self, keyword: str, words: int = 2000) -> str:
        console.print(f"[yellow]Writing SEO article: {keyword} ({words} words)...[/yellow]")
        result = self.ai.seo_article(keyword, words)
        self.articles_written += 1
        return result

    def keyword_research(self, niche: str) -> str:
        console.print(f"[yellow]Researching keywords for: {niche}...[/yellow]")
        prompt = f"""Do keyword research for the niche: {niche}

Provide:
- 20 primary keywords (high volume)
- 20 long-tail keywords (low competition)
- 10 question-based keywords (for FAQ sections)
- Search volume estimates
- Competition level (low/medium/high)
- Content type recommendation for each
- Priority ranking (which to target first)
- Nepal-specific keyword variations

Format as structured tables."""

        return self.ai.generate(prompt)

    def meta_tags(self, keyword: str, page_title: str) -> str:
        console.print(f"[yellow]Generating meta tags for: {keyword}...[/yellow]")
        prompt = f"""Generate SEO meta tags:
Target keyword: {keyword}
Page title: {page_title}

Include:
- Title tag (60 chars max) - 3 variations
- Meta description (155 chars max) - 3 variations
- H1 tag suggestion
- URL slug suggestion
- Open Graph tags
- Schema markup suggestions
- Internal linking anchor text suggestions

Optimize for both SEO and click-through rate."""

        return self.ai.generate(prompt)

    def content_plan(self, niche: str, months: int = 3) -> str:
        console.print(f"[yellow]Creating {months}-month content plan for {niche}...[/yellow]")
        prompt = f"""Create a {months}-month SEO content plan for: {niche}

For each month include:
- 8-10 article topics
- Target keyword for each
- Content type (blog/list/howto/comparison)
- Word count target
- Internal linking strategy
- Publishing priority

Also include:
- Content cluster strategy
- Pillar page ideas
- Link building opportunities
- Seasonal content opportunities
- Nepal-specific content angles"""

        return self.ai.generate(prompt)

    def competitor_analysis(self, niche: str) -> str:
        console.print(f"[yellow]Analyzing competitors in: {niche}...[/yellow]")
        prompt = f"""Analyze top SEO competitors in: {niche}

Provide:
- Top 5 ranking factors in this niche
- Content gaps to exploit
- Common keyword opportunities
- Content formats that work
- Average word count for ranking
- Backlink strategies used
- Social signals approach
- Technical SEO requirements
- Nepal-specific SEO considerations
- Action plan to outrank them"""

        return self.ai.generate(prompt)

    def backlink_strategy(self, niche: str) -> str:
        console.print(f"[yellow]Creating backlink strategy for: {niche}...[/yellow]")
        prompt = f"""Create a backlink building strategy for: {niche}

Include:
- Guest posting opportunities (10 sites)
- Directory submissions (Nepal-specific)
- Forum and community participation
- Social bookmarking sites
- Content syndication platforms
- HARO/Quoted opportunities
- Broken link building targets
- Skyscraper technique approach
- Local SEO backlinks (Nepal)
- Monthly link building schedule"""

        return self.ai.generate(prompt)

    def technical_seo_audit(self, website: str) -> str:
        console.print(f"[yellow]Creating technical SEO checklist for {website}...[/yellow]")
        prompt = f"""Create a comprehensive technical SEO audit checklist for: {website}

Include:
- Crawlability and indexing
- Site speed optimization
- Mobile responsiveness
- Core Web Vitals
- Schema markup
- XML sitemap
- Robots.txt
- Canonical tags
- 404 error handling
- Redirect chains
- HTTPS/SSL
- Image optimization
- Internal linking
- Breadcrumbs
- Page experience signals

Provide actionable fix for each issue."""

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
            "[bold cyan]SEO CONTENT WRITER TOOL[/bold cyan]\n"
            "[yellow]NPR 12,000-40,000/month potential[/yellow]\n"
            "[dim]Keywords, articles, meta tags, content plans[/dim]",
            border_style="bright_blue",
        )
    )

    provider = Prompt.ask("AI Provider", default="groq")
    seo = SEOWriter(provider)

    while True:
        console.print()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Tool", style="cyan")
        table.add_column("What it does")
        tools = [
            ("1", "SEO Article", "Write SEO-optimized article"),
            ("2", "Keyword Research", "Find best keywords for niche"),
            ("3", "Meta Tags", "Generate title/description tags"),
            ("4", "Content Plan", "3-month content calendar"),
            ("5", "Competitor Analysis", "Analyze top competitors"),
            ("6", "Backlink Strategy", "Link building plan"),
            ("7", "Technical SEO Audit", "Full site audit checklist"),
            ("8", "Batch Articles", "Write multiple SEO articles"),
            ("9", "Stats", "View stats"),
            ("0", "Exit", "Exit SEO tool"),
        ]
        for num, tool, desc in tools:
            table.add_row(num, tool, desc)
        console.print(table)

        choice = Prompt.ask("\n[green]Select tool[/green]", default="0")

        try:
            if choice == "0":
                console.print(f"[yellow]Articles written: {seo.articles_written} | Keep ranking![/yellow]")
                break
            elif choice == "1":
                keyword = Prompt.ask("Target keyword")
                words = int(Prompt.ask("Word count", default="2000"))
                result = seo.seo_article(keyword, words)
                console.print(Panel(result[:800] + "...", title="Article Preview"))
                if Confirm.ask("Save full article?"):
                    seo.save(result, f"seo_{keyword.replace(' ', '_')}.md")
            elif choice == "2":
                niche = Prompt.ask("Your niche")
                result = seo.keyword_research(niche)
                console.print(Panel(result[:800] + "...", title="Keywords Preview"))
                if Confirm.ask("Save full report?"):
                    seo.save(result, f"keywords_{niche.replace(' ', '_')}.md")
            elif choice == "3":
                keyword = Prompt.ask("Target keyword")
                title = Prompt.ask("Page title")
                result = seo.meta_tags(keyword, title)
                console.print(Panel(result, title="Meta Tags"))
            elif choice == "4":
                niche = Prompt.ask("Your niche")
                months = int(Prompt.ask("Months", default="3"))
                result = seo.content_plan(niche, months)
                console.print(Panel(result[:800] + "...", title="Content Plan Preview"))
                if Confirm.ask("Save full plan?"):
                    seo.save(result, f"content_plan_{niche.replace(' ', '_')}.md")
            elif choice == "5":
                niche = Prompt.ask("Your niche")
                result = seo.competitor_analysis(niche)
                console.print(Panel(result[:800] + "...", title="Competitor Analysis"))
                if Confirm.ask("Save?"):
                    seo.save(result, f"competitors_{niche.replace(' ', '_')}.md")
            elif choice == "6":
                niche = Prompt.ask("Your niche")
                result = seo.backlink_strategy(niche)
                console.print(Panel(result[:800] + "...", title="Backlink Strategy"))
                if Confirm.ask("Save?"):
                    seo.save(result, f"backlinks_{niche.replace(' ', '_')}.md")
            elif choice == "7":
                website = Prompt.ask("Website URL/name")
                result = seo.technical_seo_audit(website)
                console.print(Panel(result[:800] + "...", title="SEO Audit"))
                if Confirm.ask("Save?"):
                    seo.save(result, f"seo_audit_{website.replace('.', '_')}.md")
            elif choice == "8":
                console.print("[dim]Enter keywords one per line. Type 'done' when finished.[/dim]")
                keywords = []
                while True:
                    k = Prompt.ask("Keyword")
                    if k.lower() == "done":
                        break
                    keywords.append(k)
                if keywords:
                    words = int(Prompt.ask("Words per article", default="2000"))
                    for kw in keywords:
                        console.print(f"[yellow]Writing: {kw}...[/yellow]")
                        result = seo.seo_article(kw, words)
                        seo.save(result, f"seo_{kw.replace(' ', '_')}.md")
                    console.print(f"[green]All {len(keywords)} articles saved![/green]")
            elif choice == "9":
                console.print(Panel(
                    f"SEO Articles Written: {seo.articles_written}",
                    title="Stats",
                ))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
