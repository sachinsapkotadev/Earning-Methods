"""
BLOGGING AUTOMATION TOOL
For: Sachin Sapkota | Nepal
Earning: NPR 5,000-30,000+/month (ads + affiliate)
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


class BlogAutomation:
    def __init__(self, provider: str = "groq"):
        self.ai = AIEngine(provider)
        self.posts_written = 0

    def blog_post(self, topic: str, words: int = 1500, keyword: str = "") -> str:
        console.print(f"[yellow]Writing blog post: {topic}...[/yellow]")
        result = self.ai.blog_post(topic, words, keyword)
        self.posts_written += 1
        return result

    def niche_research(self, interest: str) -> str:
        console.print(f"[yellow]Researching niches for: {interest}...[/yellow]")
        prompt = f"""Research profitable blog niches related to: {interest}

Include:
- 5 niche ideas with analysis
- Monthly search volume estimates
- Competition level
- Monetization potential
- Ad revenue estimates (RPM)
- Affiliate program availability
- Nepal-specific angles
- Content difficulty level
- Time to first income estimate
- Recommended niche (with reasoning)"""

        return self.ai.generate(prompt)

    def blog_plan(self, niche: str, months: int = 3) -> str:
        console.print(f"[yellow]Creating {months}-month blog plan...[/yellow]")
        prompt = f"""Create a {months}-month blogging plan:

Niche: {niche}

For each month:
- 8-12 post topics
- Target keyword for each
- Content type (how-to/list/review/guide)
- Word count target
- Internal linking strategy
- Monetization approach

Also include:
- Domain name suggestions
- WordPress setup guide
- Essential plugins
- Theme recommendations
- Google AdSense application tips
- Affiliate program signups
- Social media promotion strategy"""

        return self.ai.generate(prompt)

    def affiliate_content(self, product: str, platform: str) -> str:
        console.print(f"[yellow]Writing affiliate content for {product}...[/yellow]")
        prompt = f"""Write affiliate marketing content:

Product: {product}
Platform: {platform}

Include:
- Honest product review (1000+ words)
- Pros and cons
- Personal experience angle (Nepal context)
- Comparison with alternatives
- Affiliate link placement suggestions
- Call-to-action buttons
- FAQ section
- Star rating
- Buy now recommendations
- Disclosure statement"""

        return self.ai.generate(prompt)

    def seo_optimize(self, post: str, keyword: str) -> str:
        console.print(f"[yellow]Optimizing post for SEO...[/yellow]")
        prompt = f"""Optimize this blog post for SEO:

Keyword: {keyword}

Post content:
{post[:2000]}

Provide:
- Optimized title
- Meta description
- URL slug
- Header tags (H1, H2, H3)
- Keyword placement suggestions
- Internal link suggestions
- Image alt text recommendations
- Schema markup
- Readability improvements"""

        return self.ai.generate(prompt)

    def email_newsletter(self, topic: str) -> str:
        console.print(f"[yellow]Writing newsletter: {topic}...[/yellow]")
        prompt = f"""Write a blog email newsletter:

Topic: {topic}

Include:
- Subject line (3 variations)
- Preview text
- Engaging opening
- Main content (3 sections)
- Personal story/angle
- Blog post links
- CTA to read more
- Social sharing prompt
- P.S. with teaser for next email"""

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
            "[bold cyan]BLOGGING AUTOMATION TOOL[/bold cyan]\n"
            "[yellow]NPR 5,000-30,000+/month potential[/yellow]\n"
            "[dim]Posts, SEO, affiliate content, newsletters[/dim]",
            border_style="bright_green",
        )
    )

    provider = Prompt.ask("AI Provider", default="groq")
    blog = BlogAutomation(provider)

    while True:
        console.print()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Tool", style="cyan")
        table.add_column("What it does")
        tools = [
            ("1", "Blog Post", "Write full blog posts"),
            ("2", "Niche Research", "Find profitable blog niches"),
            ("3", "Blog Plan", "3-month content strategy"),
            ("4", "Affiliate Content", "Write product reviews"),
            ("5", "SEO Optimize", "Optimize posts for Google"),
            ("6", "Newsletter", "Write email newsletters"),
            ("7", "Batch Posts", "Write multiple posts at once"),
            ("8", "Stats", "View stats"),
            ("0", "Exit", "Exit blogging tool"),
        ]
        for num, tool, desc in tools:
            table.add_row(num, tool, desc)
        console.print(table)

        choice = Prompt.ask("\n[green]Select tool[/green]", default="0")

        try:
            if choice == "0":
                console.print(f"[yellow]Posts written: {blog.posts_written} | Keep blogging![/yellow]")
                break
            elif choice == "1":
                topic = Prompt.ask("Blog topic")
                words = int(Prompt.ask("Word count", default="1500"))
                keyword = Prompt.ask("SEO keyword (optional)", default="")
                result = blog.blog_post(topic, words, keyword)
                console.print(Panel(result[:500] + "...", title="Blog Preview"))
                if Confirm.ask("Save full post?"):
                    blog.save(result, f"blog_{topic[:30].replace(' ', '_')}.md")
            elif choice == "2":
                interest = Prompt.ask("Your interest/field")
                result = blog.niche_research(interest)
                console.print(Panel(result[:800] + "...", title="Niche Research"))
                if Confirm.ask("Save?"):
                    blog.save(result, f"niche_{interest.replace(' ', '_')}.md")
            elif choice == "3":
                niche = Prompt.ask("Your niche")
                months = int(Prompt.ask("Months", default="3"))
                result = blog.blog_plan(niche, months)
                console.print(Panel(result[:800] + "...", title="Blog Plan"))
                if Confirm.ask("Save?"):
                    blog.save(result, f"plan_{niche.replace(' ', '_')}.md")
            elif choice == "4":
                product = Prompt.ask("Product name")
                platform = Prompt.ask("Affiliate platform (Amazon/Daraz/Other)")
                result = blog.affiliate_content(product, platform)
                console.print(Panel(result[:800] + "...", title="Affiliate Content"))
                if Confirm.ask("Save?"):
                    blog.save(result, f"affiliate_{product.replace(' ', '_')}.md")
            elif choice == "5":
                console.print("[dim]Paste your blog post (press Enter twice when done):[/dim]")
                lines = []
                while True:
                    line = input()
                    if line == "" and lines and lines[-1] == "":
                        break
                    lines.append(line)
                post = "\n".join(lines)
                keyword = Prompt.ask("Target keyword")
                result = blog.seo_optimize(post, keyword)
                console.print(Panel(result, title="SEO Optimization"))
            elif choice == "6":
                topic = Prompt.ask("Newsletter topic")
                result = blog.email_newsletter(topic)
                console.print(Panel(result, title="Newsletter"))
            elif choice == "7":
                console.print("[dim]Enter topics one per line. Type 'done' when finished.[/dim]")
                topics = []
                while True:
                    t = Prompt.ask("Topic")
                    if t.lower() == "done":
                        break
                    topics.append(t)
                if topics:
                    for topic in topics:
                        console.print(f"[yellow]Writing: {topic}...[/yellow]")
                        result = blog.blog_post(topic)
                        blog.save(result, f"blog_{topic[:30].replace(' ', '_')}.md")
                    console.print(f"[green]All {len(topics)} posts saved![/green]")
            elif choice == "8":
                console.print(Panel(
                    f"Posts Written: {blog.posts_written}",
                    title="Stats",
                ))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
