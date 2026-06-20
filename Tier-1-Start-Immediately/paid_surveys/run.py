"""
PAID SURVEYS & MICRO-TASK TRACKER
For: Sachin Sapkota | Nepal
Works on: TGM Panel, Remotasks, Appen
Earning: NPR 2,000-5,000/month
"""
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
DATA_FILE = OUTPUT_DIR / "survey_tracker.json"


class SurveyTracker:
    def __init__(self):
        self.data = self._load()

    def _load(self) -> dict:
        if DATA_FILE.exists():
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        return {"surveys": [], "micro_tasks": [], "earnings": [], "stats": {"total_earned": 0, "total_surveys": 0}}

    def _save(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def add_survey(self, platform: str, topic: str, payment: float, time_mins: int):
        survey = {
            "platform": platform,
            "topic": topic,
            "payment": payment,
            "time_mins": time_mins,
            "date": datetime.now().isoformat(),
            "hourly_rate": round(payment / (time_mins / 60), 2) if time_mins > 0 else 0,
        }
        self.data["surveys"].append(survey)
        self.data["stats"]["total_earned"] += payment
        self.data["stats"]["total_surveys"] += 1
        self._save()
        return survey

    def add_task(self, platform: str, task_type: str, payment: float, time_mins: int):
        task = {
            "platform": platform,
            "task_type": task_type,
            "payment": payment,
            "time_mins": time_mins,
            "date": datetime.now().isoformat(),
            "hourly_rate": round(payment / (time_mins / 60), 2) if time_mins > 0 else 0,
        }
        self.data["micro_tasks"].append(task)
        self.data["stats"]["total_earned"] += payment
        self._save()
        return task

    def get_daily_summary(self, date: str = None) -> dict:
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        today_surveys = [s for s in self.data["surveys"] if s["date"].startswith(date)]
        today_tasks = [t for t in self.data["micro_tasks"] if t["date"].startswith(date)]
        return {
            "date": date,
            "surveys_done": len(today_surveys),
            "tasks_done": len(today_tasks),
            "earned_today": sum(s["payment"] for s in today_surveys) + sum(t["payment"] for t in today_tasks),
            "time_spent": sum(s["time_mins"] for s in today_surveys) + sum(t["time_mins"] for t in today_tasks),
        }

    def get_weekly_summary(self) -> dict:
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        weekly_surveys = [
            s for s in self.data["surveys"]
            if datetime.fromisoformat(s["date"]) >= week_start
        ]
        weekly_tasks = [
            t for t in self.data["micro_tasks"]
            if datetime.fromisoformat(t["date"]) >= week_start
        ]
        return {
            "surveys": len(weekly_surveys),
            "tasks": len(weekly_tasks),
            "earned": sum(s["payment"] for s in weekly_surveys) + sum(t["payment"] for t in weekly_tasks),
        }

    def get_platform_stats(self) -> dict:
        platforms = {}
        for s in self.data["surveys"]:
            p = s["platform"]
            if p not in platforms:
                platforms[p] = {"count": 0, "earned": 0}
            platforms[p]["count"] += 1
            platforms[p]["earned"] += s["payment"]
        for t in self.data["micro_tasks"]:
            p = t["platform"]
            if p not in platforms:
                platforms[p] = {"count": 0, "earned": 0}
            platforms[p]["count"] += 1
            platforms[p]["earned"] += t["payment"]
        return platforms

    def get_best_platforms(self) -> list:
        stats = self.get_platform_stats()
        return sorted(stats.items(), key=lambda x: x[1]["earned"], reverse=True)


def show_platforms():
    console.print(Panel(
        "[bold]Available Platforms in Nepal (2026):[/bold]\n\n"
        "[cyan]Surveys:[/cyan]\n"
        "  - TGM Panel (tgmpanel.com) - Best for Nepal\n"
        "  - Swagbucks\n"
        "  - Survey Junkie\n\n"
        "[cyan]Micro-Tasks:[/cyan]\n"
        "  - Remotasks (remotasks.com) - AI training tasks\n"
        "  - Appen Connect\n"
        "  - TELUS International AI\n"
        "  - Clickworker\n\n"
        "[cyan]Tips:[/cyan]\n"
        "  - Start with TGM Panel (verified working in Nepal)\n"
        "  - Do Remotasks training for higher-paying tasks\n"
        "  - Track everything to find best-paying platforms",
        title="Survey & Task Platforms",
    ))


def main():
    console.print(
        Panel.fit(
            "[bold cyan]PAID SURVEYS & MICRO-TASKS TRACKER[/bold cyan]\n"
            "[yellow]NPR 2,000-5,000/month potential[/yellow]\n"
            "[dim]Easy start, no skills required[/dim]",
            border_style="bright_green",
        )
    )

    tracker = SurveyTracker()

    while True:
        console.print()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Option", style="cyan")
        table.add_column("What it does")
        tools = [
            ("1", "Log Survey", "Record a completed survey"),
            ("2", "Log Micro-Task", "Record a completed micro-task"),
            ("3", "Today's Summary", "View today's earnings"),
            ("4", "Weekly Summary", "View this week's earnings"),
            ("5", "Platform Stats", "See which platform pays best"),
            ("6", "Platforms List", "View available platforms"),
            ("7", "Hourly Rate", "Calculate your hourly rate"),
            ("0", "Exit", "Exit tracker"),
        ]
        for num, tool, desc in tools:
            table.add_row(num, tool, desc)
        console.print(table)

        choice = Prompt.ask("\n[green]Select option[/green]", default="0")

        try:
            if choice == "0":
                summary = tracker.get_daily_summary()
                console.print(f"[yellow]Today: {summary['surveys_done']} surveys, NPR {summary['earned_today']:.0f} earned[/yellow]")
                break
            elif choice == "1":
                platform = Prompt.ask("Platform", default="TGM Panel")
                topic = Prompt.ask("Survey topic")
                payment = float(Prompt.ask("Payment (NPR)"))
                time_mins = int(Prompt.ask("Time spent (minutes)"))
                tracker.add_survey(platform, topic, payment, time_mins)
                console.print(f"[green]Logged! +NPR {payment:.0f}[/green]")
            elif choice == "2":
                platform = Prompt.ask("Platform", default="Remotasks")
                task_type = Prompt.ask("Task type")
                payment = float(Prompt.ask("Payment (NPR)"))
                time_mins = int(Prompt.ask("Time spent (minutes)"))
                tracker.add_task(platform, task_type, payment, time_mins)
                console.print(f"[green]Logged! +NPR {payment:.0f}[/green]")
            elif choice == "3":
                summary = tracker.get_daily_summary()
                console.print(Panel(
                    f"Date: {summary['date']}\n"
                    f"Surveys Done: {summary['surveys_done']}\n"
                    f"Tasks Done: {summary['tasks_done']}\n"
                    f"Total Time: {summary['time_spent']} mins\n"
                    f"[bold green]Earned: NPR {summary['earned_today']:.0f}[/bold green]",
                    title="Today's Summary",
                ))
            elif choice == "4":
                summary = tracker.get_weekly_summary()
                console.print(Panel(
                    f"Surveys: {summary['surveys']}\n"
                    f"Tasks: {summary['tasks']}\n"
                    f"[bold green]Total Earned: NPR {summary['earned']:.0f}[/bold green]",
                    title="Weekly Summary",
                ))
            elif choice == "5":
                platforms = tracker.get_best_platforms()
                if platforms:
                    table = Table(title="Platform Performance")
                    table.add_column("Platform")
                    table.add_column("Count")
                    table.add_column("Earned")
                    for name, stats in platforms:
                        table.add_row(name, str(stats["count"]), f"NPR {stats['earned']:.0f}")
                    console.print(table)
                else:
                    console.print("[yellow]No data yet. Start logging![/yellow]")
            elif choice == "6":
                show_platforms()
            elif choice == "7":
                earned = float(Prompt.ask("Total earned (NPR)"))
                hours = float(Prompt.ask("Total hours worked"))
                if hours > 0:
                    rate = earned / hours
                    console.print(f"[green]Your hourly rate: NPR {rate:.0f}/hour[/green]")
                    console.print(f"[dim]Target: NPR 200-500/hour for surveys[/dim]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
