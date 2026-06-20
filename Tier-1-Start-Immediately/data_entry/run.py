"""
DATA ENTRY AUTOMATION SYSTEM
For: Sachin Sapkota | Nepal
Works on: Fiverr, Upwork, OnlineKaam
Earning: NPR 5,000-15,000/month
"""
import os
import csv
import json
import re
import time
import sys
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


class DataEntryAutomation:
    def __init__(self):
        self.tasks_completed = 0
        self.earnings = 0

    def csv_cleaner(self, input_file: str) -> str:
        console.print("[yellow]Processing CSV...[/yellow]")
        cleaned_rows = []
        with open(input_file, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            for row in reader:
                cleaned = {}
                for key, value in row.items():
                    if value:
                        value = value.strip()
                        value = re.sub(r'\s+', ' ', value)
                        if key and any(w in key.lower() for w in ["email", "mail"]):
                            value = value.lower()
                        if key and any(w in key.lower() for w in ["phone", "mobile", "tel"]):
                            value = re.sub(r'[^\d+\-\(\)\s]', '', value)
                        if key and any(w in key.lower() for w in ["name", "first", "last"]):
                            value = value.title()
                cleaned[key] = value
                cleaned_rows.append(cleaned)

        output_file = OUTPUT_DIR / f"cleaned_{Path(input_file).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(cleaned_rows)

        self.tasks_completed += 1
        console.print(f"[green]Cleaned {len(cleaned_rows)} rows -> {output_file}[/green]")
        return str(output_file)

    def csv_merger(self, files: list) -> str:
        console.print(f"[yellow]Merging {len(files)} CSV files...[/yellow]")
        all_data = []
        headers = None
        for f in files:
            with open(f, "r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                if headers is None:
                    headers = reader.fieldnames
                for row in reader:
                    all_data.append(row)

        output_file = OUTPUT_DIR / f"merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(all_data)

        self.tasks_completed += 1
        console.print(f"[green]Merged {len(all_data)} rows -> {output_file}[/green]")
        return str(output_file)

    def data_formatter(self, input_file: str, output_format: str = "csv") -> str:
        console.print(f"[yellow]Converting to {output_format}...[/yellow]")
        data = []
        with open(input_file, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(dict(row))

        if output_format == "json":
            output_file = OUTPUT_DIR / f"formatted_{Path(input_file).stem}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        elif output_format == "markdown":
            output_file = OUTPUT_DIR / f"formatted_{Path(input_file).stem}_{datetime.now().strftime('%Y%m%d')}.md"
            if data:
                headers = list(data[0].keys())
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(f"# Data Export\n\n")
                    f.write("| " + " | ".join(headers) + " |\n")
                    f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
                    for row in data:
                        vals = [str(row.get(h, "")) for h in headers]
                        f.write("| " + " | ".join(vals) + " |\n")
        elif output_format == "excel":
            output_file = OUTPUT_DIR / f"formatted_{Path(input_file).stem}_{datetime.now().strftime('%Y%m%d')}.csv"
            with open(output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

        self.tasks_completed += 1
        console.print(f"[green]Formatted -> {output_file}[/green]")
        return str(output_file)

    def email_extractor(self, text_file: str) -> str:
        console.print("[yellow]Extracting emails from text...[/yellow]")
        with open(text_file, "r", encoding="utf-8") as f:
            text = f.read()

        emails = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)))

        output_file = OUTPUT_DIR / f"emails_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(output_file, "w") as f:
            for email in emails:
                f.write(email + "\n")

        self.tasks_completed += 1
        console.print(f"[green]Found {len(emails)} emails -> {output_file}[/green]")
        return str(output_file)

    def phone_formatter(self, input_file: str) -> str:
        console.print("[yellow]Formatting phone numbers...[/yellow]")
        formatted = []
        with open(input_file, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            for row in reader:
                for key in row:
                    if key and any(w in key.lower() for w in ["phone", "mobile", "tel", "contact"]):
                        if row[key]:
                            nums = re.findall(r'[\d]+', row[key])
                            if nums:
                                row[key] = " ".join(nums)
                formatted.append(row)

        output_file = OUTPUT_DIR / f"phones_{Path(input_file).stem}_{datetime.now().strftime('%Y%m%d')}.csv"
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(formatted)

        self.tasks_completed += 1
        console.print(f"[green]Formatted phones -> {output_file}[/green]")
        return str(output_file)

    def duplicate_remover(self, input_file: str, key_column: str = None) -> str:
        console.print("[yellow]Removing duplicates...[/yellow]")
        seen = set()
        unique = []
        total = 0
        with open(input_file, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            for row in reader:
                total += 1
                if key_column:
                    key = row.get(key_column, "").strip().lower()
                else:
                    key = json.dumps(row, sort_keys=True)
                if key not in seen:
                    seen.add(key)
                    unique.append(row)

        output_file = OUTPUT_DIR / f"unique_{Path(input_file).stem}_{datetime.now().strftime('%Y%m%d')}.csv"
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(unique)

        removed = total - len(unique)
        self.tasks_completed += 1
        console.print(f"[green]Removed {removed} duplicates. {len(unique)} unique rows -> {output_file}[/green]")
        return str(output_file)

    def batch_rename(self, folder: str, pattern: str = "file_{n}"):
        console.print(f"[yellow]Batch renaming files in {folder}...[/yellow]")
        files = sorted(Path(folder).iterdir())
        count = 0
        for i, f in enumerate(files, 1):
            if f.is_file():
                ext = f.suffix
                new_name = pattern.replace("{n}", str(i)) + ext
                new_path = f.parent / new_name
                f.rename(new_path)
                count += 1
        self.tasks_completed += 1
        console.print(f"[green]Renamed {count} files.[/green]")

    def generate_sample_csv(self) -> str:
        output_file = OUTPUT_DIR / "sample_data.csv"
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Email", "Phone", "Address", "City"])
            for i in range(1, 21):
                writer.writerow([
                    f"Person {i}",
                    f"person{i}@example.com",
                    f"984{i:07d}",
                    f"Street {i}, Ward {i}",
                    ["Kathmandu", "Pokhara", "Chitwan", "Lalitpur", "Bhaktapur"][i % 5],
                ])
        console.print(f"[green]Sample CSV created -> {output_file}[/green]")
        return str(output_file)

    def get_stats(self) -> dict:
        return {
            "tasks_completed": self.tasks_completed,
            "earnings": self.earnings,
        }


def main():
    console.print(
        Panel.fit(
            "[bold cyan]DATA ENTRY AUTOMATION TOOL[/bold cyan]\n"
            "[yellow]NPR 5,000-15,000/month potential[/yellow]\n"
            "[dim]Fast, accurate, automated[/dim]",
            border_style="bright_blue",
        )
    )

    auto = DataEntryAutomation()

    while True:
        console.print()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Tool", style="cyan")
        table.add_column("What it does")
        tools = [
            ("1", "CSV Cleaner", "Clean and format messy CSV data"),
            ("2", "CSV Merger", "Merge multiple CSV files into one"),
            ("3", "Data Formatter", "Convert CSV to JSON/Markdown/Excel"),
            ("4", "Email Extractor", "Extract emails from any text file"),
            ("5", "Phone Formatter", "Clean and format phone numbers"),
            ("6", "Duplicate Remover", "Remove duplicate rows from CSV"),
            ("7", "Batch Rename", "Rename multiple files at once"),
            ("8", "Sample Data", "Generate sample CSV for practice"),
            ("9", "Stats", "View your work stats"),
            ("0", "Exit", "Exit data entry tool"),
        ]
        for num, tool, desc in tools:
            table.add_row(num, tool, desc)
        console.print(table)

        choice = Prompt.ask("\n[green]Select tool[/green]", default="0")

        try:
            if choice == "0":
                stats = auto.get_stats()
                console.print(f"[yellow]Tasks done: {stats['tasks_completed']} | Keep going![/yellow]")
                break
            elif choice == "1":
                path = Prompt.ask("CSV file path")
                if os.path.exists(path):
                    auto.csv_cleaner(path)
                else:
                    console.print("[red]File not found![/red]")
            elif choice == "2":
                console.print("[dim]Enter file paths one by one. Type 'done' when finished.[/dim]")
                files = []
                while True:
                    f = Prompt.ask("File path")
                    if f.lower() == "done":
                        break
                    if os.path.exists(f):
                        files.append(f)
                if files:
                    auto.csv_merger(files)
            elif choice == "3":
                path = Prompt.ask("CSV file path")
                fmt = Prompt.ask("Output format (csv/json/markdown)", default="json")
                if os.path.exists(path):
                    auto.data_formatter(path, fmt)
                else:
                    console.print("[red]File not found![/red]")
            elif choice == "4":
                path = Prompt.ask("Text file path")
                if os.path.exists(path):
                    auto.email_extractor(path)
                else:
                    console.print("[red]File not found![/red]")
            elif choice == "5":
                path = Prompt.ask("CSV file path")
                if os.path.exists(path):
                    auto.phone_formatter(path)
                else:
                    console.print("[red]File not found![/red]")
            elif choice == "6":
                path = Prompt.ask("CSV file path")
                key = Prompt.ask("Key column for dedup (or leave blank for all)", default="")
                if os.path.exists(path):
                    auto.duplicate_remover(path, key if key else None)
                else:
                    console.print("[red]File not found![/red]")
            elif choice == "7":
                folder = Prompt.ask("Folder path")
                pattern = Prompt.ask("Pattern (use {n} for number)", default="file_{n}")
                if os.path.isdir(folder):
                    auto.batch_rename(folder, pattern)
                else:
                    console.print("[red]Folder not found![/red]")
            elif choice == "8":
                auto.generate_sample_csv()
            elif choice == "9":
                stats = auto.get_stats()
                console.print(Panel(
                    f"Tasks Completed: {stats['tasks_completed']}\n"
                    f"Earnings: NPR {stats['earnings']:,.0f}",
                    title="Your Stats",
                ))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
