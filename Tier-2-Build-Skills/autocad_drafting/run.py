"""
AUTOCAD & CIVIL ENGINEERING TOOL
For: Sachin Sapkota | Nepal
Your unique advantage as a Civil Engineering student
Works on: Upwork, Fiverr, Local architects/contractors
Earning: NPR 15,000-50,000/month
"""
import os
import sys
import json
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


class AutoCADAssistant:
    def __init__(self, provider: str = "groq"):
        self.ai = AIEngine(provider)
        self.queries_answered = 0

    def cad_command_help(self, command: str) -> str:
        console.print(f"[yellow]Explaining AutoCAD command: {command}...[/yellow]")
        prompt = f"""Explain this AutoCAD command in detail: {command}

Include:
- What the command does
- Step-by-step usage
- All options/parameters
- Keyboard shortcuts
- Common use cases in civil engineering
- Tips and tricks
- Common mistakes to avoid
- Related commands
- Practice exercise"""

        result = self.ai.autoCAD_help(prompt)
        self.queries_answered += 1
        return result

    def drawing_guide(self, drawing_type: str) -> str:
        console.print(f"[yellow]Creating guide for: {drawing_type}...[/yellow]")
        prompt = f"""Create a complete AutoCAD drawing guide for: {drawing_type}

Include:
- Drawing standards and conventions
- Layer setup and naming
- Dimension styles
- Text styles
- Plot settings
- Step-by-step drawing process
- Key measurements and scales
- Common symbols and annotations
- Quality checklist
- Nepal building code references if applicable"""

        return self.ai.autoCAD_help(prompt)

    def structural_calculation(self, problem: str) -> str:
        console.print(f"[yellow]Calculating: {problem}...[/yellow]")
        prompt = f"""Solve this structural engineering problem:

{problem}

Include:
- Given data
- Formula used
- Step-by-step calculation
- Final answer with units
- Safety factors considered
- Relevant code references (NBC/Nepal standards)
- Practical implications
- Diagram description if needed"""

        return self.ai.autoCAD_help(prompt)

    def bill_of_quantities(self, project: str) -> str:
        console.print(f"[yellow]Creating BOQ for: {project}...[/yellow]")
        prompt = f"""Create a Bill of Quantities (BOQ) for:

Project: {project}

Include:
- Item description
- Unit of measurement
- Quantity
- Rate (NPR)
- Amount
- Subtotals
- Contingency (5%)
- Grand total

Format as a professional BOQ table.
Use Nepal market rates (2026 estimates)."""

        return self.ai.autoCAD_help(prompt)

    def estimation(self, project_type: str, area: str) -> str:
        console.print(f"[yellow]Estimating cost for {project_type}...[/yellow]")
        prompt = f"""Create a construction cost estimation:

Project type: {project_type}
Area: {area}

Include:
- Material costs (cement, sand, aggregate, steel, bricks, etc.)
- Labor costs
- Equipment costs
- Foundation costs
- Structural costs
- Finishing costs
- Plumbing estimates
- Electrical estimates
- Total estimated cost
- Cost per sq ft/sq m
- Nepal-specific rates (2026)
- Contingency recommendation"""

        return self.ai.autoCAD_help(prompt)

    def project_report(self, project: str, stage: str) -> str:
        console.print(f"[yellow]Creating project report...[/yellow]")
        prompt = f"""Create a civil engineering project progress report:

Project: {project}
Current stage: {stage}

Include:
- Project overview
- Progress summary
- Work completed
- Work in progress
- Upcoming activities
- Issues/challenges
- Safety report
- Quality control measures
- Timeline status
- Recommendations
- Photos placeholder sections"""

        return self.ai.autoCAD_help(prompt)

    def autocad_shortcuts(self, category: str = "all") -> str:
        console.print(f"[yellow]Generating AutoCAD shortcuts...[/yellow]")
        prompt = f"""List all important AutoCAD shortcuts for civil engineering:
Category: {category}

Organize by:
- Drawing commands
- Modification commands
- Dimensioning
- Layer management
- View controls
- Object snap
- Selection
- Navigation
- Custom shortcuts to set up

Include keyboard shortcuts and their functions."""

        return self.ai.autoCAD_help(prompt)

    def revit_vs_autocad(self, task: str) -> str:
        console.print(f"[yellow]Comparing Revit vs AutoCAD for: {task}...[/yellow]")
        prompt = f"""Compare Revit and AutoCAD for this task: {task}

Include:
- Which is better and why
- Workflow in each software
- Time comparison
- Quality comparison
- When to use which
- Hybrid approach recommendation
- Learning resources for both"""

        return self.ai.autoCAD_help(prompt)

    def save(self, content: str, filename: str) -> str:
        filepath = OUTPUT_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        console.print(f"[green]Saved -> {filepath}[/green]")
        return str(filepath)


def main():
    console.print(
        Panel.fit(
            "[bold cyan]AUTOCAD & CIVIL ENGINEERING TOOL[/bold cyan]\n"
            "[yellow]NPR 15,000-50,000/month potential[/yellow]\n"
            "[dim]Your engineering advantage — use it![/dim]",
            border_style="bright_cyan",
        )
    )

    provider = Prompt.ask("AI Provider", default="groq")
    acad = AutoCADAssistant(provider)

    while True:
        console.print()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Tool", style="cyan")
        table.add_column("What it does")
        tools = [
            ("1", "CAD Command Help", "Explain any AutoCAD command"),
            ("2", "Drawing Guide", "Step-by-step drawing guides"),
            ("3", "Structural Calc", "Structural calculations"),
            ("4", "Bill of Quantities", "Create BOQ for projects"),
            ("5", "Cost Estimation", "Construction cost estimates"),
            ("6", "Project Report", "Engineering progress reports"),
            ("7", "AutoCAD Shortcuts", "Complete shortcut reference"),
            ("8", "Revit vs AutoCAD", "Software comparison"),
            ("9", "Stats", "View stats"),
            ("0", "Exit", "Exit engineering tool"),
        ]
        for num, tool, desc in tools:
            table.add_row(num, tool, desc)
        console.print(table)

        choice = Prompt.ask("\n[green]Select tool[/green]", default="0")

        try:
            if choice == "0":
                console.print(f"[yellow]Queries answered: {acad.queries_answered} | Keep learning![/yellow]")
                break
            elif choice == "1":
                cmd = Prompt.ask("AutoCAD command")
                result = acad.cad_command_help(cmd)
                console.print(Panel(result, title=f"Command: {cmd}"))
            elif choice == "2":
                dtype = Prompt.ask("Drawing type (floor_plan/elevation/section/site_plan)")
                result = acad.drawing_guide(dtype)
                console.print(Panel(result[:800] + "...", title="Drawing Guide"))
                if Confirm.ask("Save?"):
                    acad.save(result, f"guide_{dtype.replace(' ', '_')}.md")
            elif choice == "3":
                problem = Prompt.ask("Describe your structural problem")
                result = acad.structural_calculation(problem)
                console.print(Panel(result, title="Structural Calculation"))
                if Confirm.ask("Save?"):
                    acad.save(result, f"calc_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
            elif choice == "4":
                project = Prompt.ask("Project description")
                result = acad.bill_of_quantities(project)
                console.print(Panel(result[:800] + "...", title="BOQ Preview"))
                if Confirm.ask("Save full BOQ?"):
                    acad.save(result, f"boq_{project[:20].replace(' ', '_')}.md")
            elif choice == "5":
                ptype = Prompt.ask("Project type (residential/commercial/road/bridge)")
                area = Prompt.ask("Area/size")
                result = acad.estimation(ptype, area)
                console.print(Panel(result[:800] + "...", title="Cost Estimation"))
                if Confirm.ask("Save?"):
                    acad.save(result, f"estimate_{ptype}_{datetime.now().strftime('%Y%m%d')}.md")
            elif choice == "6":
                project = Prompt.ask("Project name")
                stage = Prompt.ask("Current stage")
                result = acad.project_report(project, stage)
                console.print(Panel(result[:800] + "...", title="Project Report"))
                if Confirm.ask("Save?"):
                    acad.save(result, f"report_{project[:20].replace(' ', '_')}.md")
            elif choice == "7":
                result = acad.autocad_shortcuts()
                console.print(Panel(result[:800] + "...", title="Shortcuts Preview"))
                if Confirm.ask("Save full list?"):
                    acad.save(result, "autocad_shortcuts.md")
            elif choice == "8":
                task = Prompt.ask("What task do you need to compare?")
                result = acad.revit_vs_autocad(task)
                console.print(Panel(result, title="Revit vs AutoCAD"))
            elif choice == "9":
                console.print(Panel(
                    f"Queries Answered: {acad.queries_answered}",
                    title="Stats",
                ))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
