"""
GRAPHIC DESIGN ASSISTANT TOOL
For: Sachin Sapkota | Nepal
Works on: Fiverr, Upwork, Local businesses
Earning: NPR 15,000-60,000/month
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


class GraphicDesignAssistant:
    def __init__(self, provider: str = "groq"):
        self.ai = AIEngine(provider)
        self.designs_ideas = 0

    def logo_brief(self, brand: str, industry: str, style: str = "modern") -> str:
        console.print(f"[yellow]Creating logo brief for {brand}...[/yellow]")
        prompt = f"""Create a detailed logo design brief:

Brand: {brand}
Industry: {industry}
Preferred style: {style}

Include:
- 3 logo concept descriptions
- Color palette suggestions (with hex codes)
- Typography recommendations
- Layout variations (icon, wordmark, combination)
- Usage guidelines
- File format recommendations
- Design do's and don'ts
- Competitor analysis notes"""

        return self.ai.generate(prompt)

    def social_media_template(self, brand: str, platform: str, post_type: str) -> str:
        console.print(f"[yellow]Creating {platform} template design guide...[/yellow]")
        prompt = f"""Create a detailed design template guide:

Brand: {brand}
Platform: {platform}
Post type: {post_type}

Include:
- Exact dimensions for the platform
- Layout grid structure
- Color placement
- Text hierarchy
- Font sizes and styles
- Image placement zones
- Branding elements placement
- Call-to-action positioning
- Design variations (3 versions)
- Step-by-step creation instructions for Canva/Photoshop"""

        return self.ai.generate(prompt)

    def canva_guide(self, design_type: str) -> str:
        console.print(f"[yellow]Creating Canva guide for {design_type}...[/yellow]")
        prompt = f"""Create a step-by-step Canva tutorial for creating: {design_type}

Include:
- Search terms for templates
- Recommended template to start with
- Step-by-step customization
- Color and font recommendations
- Download settings
- Pro tips for professional results
- Time estimate
- Difficulty level (beginner/intermediate)"""

        return self.ai.generate(prompt)

    def brand_guidelines(self, brand: str, industry: str) -> str:
        console.print(f"[yellow]Creating brand guidelines for {brand}...[/yellow]")
        prompt = f"""Create comprehensive brand guidelines for:

Brand: {brand}
Industry: {industry}

Include:
- Brand story and values
- Logo usage rules
- Color palette (primary, secondary, accent with hex codes)
- Typography (headings, body, accent fonts)
- Imagery style
- Voice and tone
- Social media templates
- Business card design
- Letterhead design
- Do's and Don'ts
- File naming conventions"""

        return self.ai.generate(prompt)

    def design_description(self, design_type: str, client_needs: str) -> str:
        console.print(f"[yellow]Writing design description...[/yellow]")
        prompt = f"""Write a compelling design deliverable description:

Design type: {design_type}
Client needs: {client_needs}

Include:
- What's included in the delivery
- Number of revisions
- Timeline
- File formats provided
- Copyright/usage rights
- Professional formatting for Fiverr/Upwork gig"""

        return self.ai.generate(prompt)

    def portfolio_description(self, project: str) -> str:
        console.print(f"[yellow]Writing portfolio description...[/yellow]")
        prompt = f"""Write a portfolio case study description for:

Project: {project}

Include:
- Project overview
- Challenge/problem
- Solution/design approach
- Tools used
- Results/impact
- Client testimonial placeholder
- Visual description

Write in first person, professional tone, 150-200 words."""

        return self.ai.generate(prompt)

    def batch_social_templates(self, brand: str, platforms: list) -> str:
        results = []
        for platform in platforms:
            for post_type in ["promo", "educational", "engagement"]:
                result = self.social_media_template(brand, platform, post_type)
                results.append(f"## {platform} - {post_type}\n\n{result}\n\n---\n")
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
            "[bold cyan]GRAPHIC DESIGN ASSISTANT[/bold cyan]\n"
            "[yellow]NPR 15,000-60,000/month potential[/yellow]\n"
            "[dim]Templates, briefs, Canva guides, brand kits[/dim]",
            border_style="bright_magenta",
        )
    )

    provider = Prompt.ask("AI Provider", default="groq")
    gda = GraphicDesignAssistant(provider)

    while True:
        console.print()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Tool", style="cyan")
        table.add_column("What it does")
        tools = [
            ("1", "Logo Brief", "Create detailed logo design brief"),
            ("2", "Social Template", "Design template guide for posts"),
            ("3", "Canva Guide", "Step-by-step Canva tutorial"),
            ("4", "Brand Guidelines", "Full brand kit document"),
            ("5", "Design Description", "Write gig/deliverable descriptions"),
            ("6", "Portfolio Case", "Write portfolio project descriptions"),
            ("7", "Batch Templates", "Templates for multiple platforms"),
            ("8", "Stats", "View stats"),
            ("0", "Exit", "Exit design tool"),
        ]
        for num, tool, desc in tools:
            table.add_row(num, tool, desc)
        console.print(table)

        choice = Prompt.ask("\n[green]Select tool[/green]", default="0")

        try:
            if choice == "0":
                console.print(f"[yellow]Design ideas generated: {gda.designs_ideas} | Keep designing![/yellow]")
                break
            elif choice == "1":
                brand = Prompt.ask("Brand name")
                industry = Prompt.ask("Industry")
                style = Prompt.ask("Style (modern/minimal/classic/playful)", default="modern")
                result = gda.logo_brief(brand, industry, style)
                console.print(Panel(result[:800] + "...", title="Logo Brief Preview"))
                if Confirm.ask("Save?"):
                    gda.save(result, f"logo_brief_{brand.replace(' ', '_')}.md")
            elif choice == "2":
                brand = Prompt.ask("Brand name")
                platform = Prompt.ask("Platform (Instagram/Facebook/TikTok)")
                post_type = Prompt.ask("Post type (promo/educational/engagement/story)")
                result = gda.social_media_template(brand, platform, post_type)
                console.print(Panel(result[:800] + "...", title="Template Guide"))
                if Confirm.ask("Save?"):
                    gda.save(result, f"template_{platform}_{post_type}.md")
            elif choice == "3":
                design = Prompt.ask("Design type (logo/post/banner/thumbnail/flyer)")
                result = gda.canva_guide(design)
                console.print(Panel(result, title="Canva Guide"))
                if Confirm.ask("Save?"):
                    gda.save(result, f"canva_{design.replace(' ', '_')}.md")
            elif choice == "4":
                brand = Prompt.ask("Brand name")
                industry = Prompt.ask("Industry")
                result = gda.brand_guidelines(brand, industry)
                console.print(Panel(result[:800] + "...", title="Brand Guidelines Preview"))
                if Confirm.ask("Save full guidelines?"):
                    gda.save(result, f"brand_{brand.replace(' ', '_')}.md")
            elif choice == "5":
                dtype = Prompt.ask("Design type")
                needs = Prompt.ask("Client needs")
                result = gda.design_description(dtype, needs)
                console.print(Panel(result, title="Design Description"))
            elif choice == "6":
                project = Prompt.ask("Project name/description")
                result = gda.portfolio_description(project)
                console.print(Panel(result, title="Portfolio Description"))
            elif choice == "7":
                brand = Prompt.ask("Brand name")
                platforms = Prompt.ask("Platforms (comma-separated)").split(",")
                result = gda.batch_social_templates(brand, [p.strip() for p in platforms])
                if Confirm.ask("Save all templates?"):
                    gda.save(result, f"all_templates_{brand.replace(' ', '_')}.md")
            elif choice == "8":
                console.print(Panel(
                    f"Design Ideas Generated: {gda.designs_ideas}",
                    title="Stats",
                ))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
