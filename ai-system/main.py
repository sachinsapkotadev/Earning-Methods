import sys
import os
import json
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import print as rprint
from dotenv import load_dotenv

load_dotenv()

from core.ai_engine import AIEngine
from core.batch_processor import BatchProcessor
from modules.project_manager import ProjectManager
from modules.content_generator import ContentGenerator
from modules.client_manager import ClientManager
from config.settings import load_config, save_config, OUTPUT_DIR, PROJECT_STATUSES, TASK_TYPES

console = Console()


def banner():
    console.print(
        Panel.fit(
            "[bold cyan]AI FREELANCING AUTOMATION SYSTEM[/bold cyan]\n"
            "[green]Powered by Python + AI[/green]\n"
            "[yellow]For: Sachin Sapkota | Nepal[/yellow]\n\n"
            "[dim]Handle 10-20 projects simultaneously[/dim]",
            border_style="bright_blue",
        )
    )


def menu():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Command", style="cyan")
    table.add_column("Description")

    commands = [
        ("1", "generate", "Generate content (blog, social, SEO, etc.)"),
        ("2", "batch", "Batch generate multiple contents at once"),
        ("3", "project", "Create/manage projects"),
        ("4", "client", "Add/manage clients"),
        ("5", "proposal", "Generate a freelance proposal"),
        ("6", "invoice", "Generate an invoice"),
        ("7", "fiverr", "Generate Fiverr gig description"),
        ("8", "upwork", "Generate Upwork proposal"),
        ("9", "youtube", "Generate YouTube script"),
        ("10", "cad", "AutoCAD / Civil Engineering help"),
        ("11", "custom", "Custom AI prompt"),
        ("12", "stats", "View earnings & project stats"),
        ("13", "config", "Setup your profile"),
        ("14", "status", "Check project statuses"),
        ("15", "multi", "Multi-project dashboard (10-20 projects)"),
        ("0", "exit", "Exit the system"),
    ]

    for num, cmd, desc in commands:
        table.add_row(num, cmd, desc)

    console.print(table)


def cmd_generate():
    console.print("\n[bold cyan]CONTENT GENERATOR[/bold cyan]")
    types = [
        "blog_post", "social_media", "seo_article",
        "product_description", "email_sequence", "youtube_script",
    ]
    for i, t in enumerate(types, 1):
        console.print(f"  {i}. {t}")
    choice = Prompt.ask("Select type", choices=[str(i) for i in range(1, len(types) + 1)])
    content_type = types[int(choice) - 1]

    provider = Prompt.ask("AI Provider", default="groq")
    gen = ContentGenerator(provider)

    if content_type == "blog_post":
        topic = Prompt.ask("Blog topic")
        words = int(Prompt.ask("Word count", default="1500"))
        keyword = Prompt.ask("SEO keyword (optional)", default="")
        console.print("\n[yellow]Generating blog post...[/yellow]")
        result = gen.blog_post(topic, words, keyword)
    elif content_type == "social_media":
        brand = Prompt.ask("Brand/business name")
        platform = Prompt.ask("Platform (Instagram/Facebook/Twitter/TikTok)")
        count = int(Prompt.ask("Number of posts", default="5"))
        console.print("\n[yellow]Generating social media posts...[/yellow]")
        result = gen.social_media_posts(brand, platform, count)
    elif content_type == "seo_article":
        keyword = Prompt.ask("Target keyword")
        words = int(Prompt.ask("Word count", default="2000"))
        console.print("\n[yellow]Generating SEO article...[/yellow]")
        result = gen.seo_article(keyword, words)
    elif content_type == "product_description":
        product = Prompt.ask("Product name")
        features = Prompt.ask("Features (comma-separated)").split(",")
        console.print("\n[yellow]Generating product description...[/yellow]")
        result = gen.product_description(product, [f.strip() for f in features])
    elif content_type == "email_sequence":
        topic = Prompt.ask("Email sequence topic")
        count = int(Prompt.ask("Number of emails", default="5"))
        console.print("\n[yellow]Generating email sequence...[/yellow]")
        result = gen.email_sequence(topic, count)
    elif content_type == "youtube_script":
        topic = Prompt.ask("Video topic")
        duration = int(Prompt.ask("Duration (minutes)", default="10"))
        console.print("\n[yellow]Generating YouTube script...[/yellow]")
        result = gen.youtube_script(topic, duration)

    save = Confirm.ask("Save to file?", default=True)
    if save:
        out_dir = OUTPUT_DIR / "content"
        out_dir.mkdir(exist_ok=True)
        filename = f"{content_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = out_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(result)
        console.print(f"[green]Saved to {filepath}[/green]")
    else:
        console.print(Panel(result, title="Generated Content"))


def cmd_batch():
    console.print("\n[bold cyan]BATCH GENERATOR (10-20 projects at once)[/bold cyan]")
    console.print("  1. Batch blog posts")
    console.print("  2. Batch social media posts")
    console.print("  3. Batch SEO articles")
    console.print("  4. Mixed batch (custom)")

    choice = Prompt.ask("Select", choices=["1", "2", "3", "4"])
    provider = Prompt.ask("AI Provider", default="groq")
    batch = BatchProcessor(max_workers=5, provider=provider)

    if choice == "1":
        console.print("[dim]Enter topics one per line. Type 'done' when finished.[/dim]")
        topics = []
        while True:
            t = Prompt.ask("Topic")
            if t.lower() == "done":
                break
            topics.append(t)
        words = int(Prompt.ask("Words per post", default="1500"))
        tasks = [
            {"type": "blog_post", "topic": t, "words": words, "name": f"blog_{i+1}"}
            for i, t in enumerate(topics)
        ]
    elif choice == "2":
        brand = Prompt.ask("Brand name")
        console.print("[dim]Enter platforms one per line. Type 'done' when finished.[/dim]")
        platforms = []
        while True:
            p = Prompt.ask("Platform")
            if p.lower() == "done":
                break
            platforms.append(p)
        count = int(Prompt.ask("Posts per platform", default="5"))
        tasks = [
            {"type": "social_media", "brand": brand, "platform": p, "count": count, "name": f"social_{p}"}
            for p in platforms
        ]
    elif choice == "3":
        console.print("[dim]Enter keywords one per line. Type 'done' when finished.[/dim]")
        keywords = []
        while True:
            k = Prompt.ask("Keyword")
            if k.lower() == "done":
                break
            keywords.append(k)
        words = int(Prompt.ask("Words per article", default="2000"))
        tasks = [
            {"type": "seo_article", "keyword": k, "words": words, "name": f"seo_{i+1}"}
            for i, k in enumerate(keywords)
        ]
    elif choice == "4":
        console.print("[dim]Enter custom prompts one per line. Type 'done' when finished.[/dim]")
        tasks = []
        i = 1
        while True:
            p = Prompt.ask(f"Prompt {i}")
            if p.lower() == "done":
                break
            tasks.append({"type": "custom", "prompt": p, "name": f"custom_{i}"})
            i += 1

    if not tasks:
        console.print("[red]No tasks entered.[/red]")
        return

    console.print(f"\n[yellow]Processing {len(tasks)} tasks with {batch.max_workers} workers...[/yellow]")
    results = batch.process_tasks(tasks)

    project_name = Prompt.ask("Project name for saving", default="batch_output")
    saved_dir = batch.save_results(project_name)
    console.print(f"\n[green]All done! Results saved to {saved_dir}[/green]")
    console.print(f"[green]Completed: {batch.get_summary()['completed']}/{batch.get_summary()['total']}[/green]")


def cmd_project():
    console.print("\n[bold cyan]PROJECT MANAGER[/bold cyan]")
    pm = ProjectManager()

    console.print("  1. Create project")
    console.print("  2. List projects")
    console.print("  3. Update status")
    console.print("  4. View stats")
    console.print("  5. Add task to project")
    console.print("  6. Delete project")

    choice = Prompt.ask("Select", choices=[str(i) for i in range(1, 7)])

    if choice == "1":
        name = Prompt.ask("Project name")
        client = Prompt.ask("Client name")
        console.print(f"Types: {', '.join(TASK_TYPES)}")
        task_type = Prompt.ask("Task type")
        budget = float(Prompt.ask("Budget (NPR)", default="0"))
        deadline = Prompt.ask("Deadline (YYYY-MM-DD)", default="")
        desc = Prompt.ask("Description", default="")
        project = pm.create_project(name, client, task_type, budget, deadline, desc)
        console.print(f"[green]Project created: {project['name']} (ID: {project['id']})[/green]")

    elif choice == "2":
        status_filter = Prompt.ask("Filter by status (or 'all')", default="all")
        projects = pm.list_projects(status=status_filter if status_filter != "all" else None)
        if not projects:
            console.print("[yellow]No projects found.[/yellow]")
            return
        table = Table(title="Projects")
        table.add_column("ID", style="dim")
        table.add_column("Name", style="cyan")
        table.add_column("Client")
        table.add_column("Type")
        table.add_column("Status", style="yellow")
        table.add_column("Budget")
        table.add_column("Earned")
        for p in projects:
            table.add_row(
                str(p["id"]), p["name"], p["client"], p["task_type"],
                p["status"], f"NPR {p['budget']:,.0f}", f"NPR {p.get('earnings', 0):,.0f}"
            )
        console.print(table)

    elif choice == "3":
        pid = int(Prompt.ask("Project ID"))
        console.print(f"Statuses: {', '.join(PROJECT_STATUSES)}")
        status = Prompt.ask("New status")
        if pm.update_status(pid, status):
            console.print("[green]Status updated![/green]")
        else:
            console.print("[red]Invalid status or project not found.[/red]")

    elif choice == "4":
        stats = pm.get_stats()
        console.print(Panel(
            f"Total Projects: {stats['total_projects']}\n"
            f"Active: {stats['active']}\n"
            f"Completed: {stats['completed']}\n"
            f"Total Earnings: NPR {stats['total_earnings']:,.0f}",
            title="Project Statistics",
        ))

    elif choice == "5":
        pid = int(Prompt.ask("Project ID"))
        task_name = Prompt.ask("Task name")
        task = {"name": task_name}
        if pm.add_task(pid, task):
            console.print("[green]Task added![/green]")
        else:
            console.print("[red]Project not found.[/red]")

    elif choice == "6":
        pid = int(Prompt.ask("Project ID to delete"))
        if Confirm.ask("Are you sure?"):
            if pm.delete_project(pid):
                console.print("[green]Deleted![/green]")


def cmd_client():
    console.print("\n[bold cyan]CLIENT MANAGER[/bold cyan]")
    cm = ClientManager()

    console.print("  1. Add client")
    console.print("  2. List clients")
    console.print("  3. View client")
    console.print("  4. Stats")

    choice = Prompt.ask("Select", choices=["1", "2", "3", "4"])

    if choice == "1":
        name = Prompt.ask("Client name")
        email = Prompt.ask("Email (optional)", default="")
        platform = Prompt.ask("Platform (Upwork/Fiverr/Local)", default="")
        notes = Prompt.ask("Notes (optional)", default="")
        client = cm.add_client(name, email, platform, notes)
        console.print(f"[green]Client added: {client['name']} (ID: {client['id']})[/green]")

    elif choice == "2":
        clients = cm.list_clients()
        if not clients:
            console.print("[yellow]No clients yet.[/yellow]")
            return
        table = Table(title="Clients")
        table.add_column("ID")
        table.add_column("Name", style="cyan")
        table.add_column("Platform")
        table.add_column("Projects")
        table.add_column("Earnings")
        for c in clients:
            table.add_row(
                str(c["id"]), c["name"], c["platform"],
                str(c["total_projects"]), f"NPR {c['total_earnings']:,.0f}"
            )
        console.print(table)

    elif choice == "3":
        name = Prompt.ask("Client name to search")
        client = cm.find_client(name)
        if client:
            console.print(Panel(
                f"Name: {client['name']}\n"
                f"Email: {client['email']}\n"
                f"Platform: {client['platform']}\n"
                f"Projects: {client['total_projects']}\n"
                f"Earnings: NPR {client['total_earnings']:,.0f}\n"
                f"Notes: {client['notes']}",
                title=f"Client: {client['name']}",
            ))
        else:
            console.print("[red]Client not found.[/red]")

    elif choice == "4":
        stats = cm.get_stats()
        console.print(Panel(
            f"Total Clients: {stats['total_clients']}\n"
            f"Total Earnings: NPR {stats['total_earnings']:,.0f}",
            title="Client Statistics",
        ))


def cmd_proposal():
    provider = Prompt.ask("AI Provider", default="groq")
    ai = AIEngine(provider)
    client = Prompt.ask("Client name")
    project = Prompt.ask("Project description")
    budget = Prompt.ask("Budget", default="")
    timeline = Prompt.ask("Timeline", default="")
    console.print("\n[yellow]Generating proposal...[/yellow]")
    result = ai.proposal(client, project, budget, timeline)
    console.print(Panel(result, title="Your Proposal"))


def cmd_invoice():
    provider = Prompt.ask("AI Provider", default="groq")
    ai = AIEngine(provider)
    client = Prompt.ask("Client name")
    invoice_no = Prompt.ask("Invoice number", default=f"INV-{datetime.now().strftime('%Y%m%d')}")
    items = []
    console.print("[dim]Add items. Type 'done' when finished.[/dim]")
    while True:
        desc = Prompt.ask("Item description (or 'done')")
        if desc.lower() == "done":
            break
        qty = int(Prompt.ask("Quantity", default="1"))
        rate = float(Prompt.ask("Rate (NPR)"))
        items.append({"description": desc, "quantity": qty, "rate": rate})
    if items:
        result = ai.invoice(client, items, invoice_no)
        console.print(Panel(result, title="Invoice"))


def cmd_fiverr():
    provider = Prompt.ask("AI Provider", default="groq")
    gen = ContentGenerator(provider)
    service = Prompt.ask("Service/gig name")
    skills = Prompt.ask("Skills (comma-separated)").split(",")
    console.print("\n[yellow]Generating Fiverr gig...[/yellow]")
    result = gen.fiverr_gig_description(service, [s.strip() for s in skills])
    console.print(Panel(result, title="Fiverr Gig"))


def cmd_upwork():
    provider = Prompt.ask("AI Provider", default="groq")
    gen = ContentGenerator(provider)
    client = Prompt.ask("Client name")
    project = Prompt.ask("Project description")
    budget = Prompt.ask("Budget", default="")
    timeline = Prompt.ask("Timeline", default="")
    console.print("\n[yellow]Generating Upwork proposal...[/yellow]")
    result = gen.upwork_proposal(client, project, budget, timeline)
    console.print(Panel(result, title="Upwork Proposal"))


def cmd_youtube():
    provider = Prompt.ask("AI Provider", default="groq")
    gen = ContentGenerator(provider)
    topic = Prompt.ask("Video topic")
    duration = int(Prompt.ask("Duration (minutes)", default="10"))
    console.print("\n[yellow]Generating YouTube script...[/yellow]")
    result = gen.youtube_script(topic, duration)
    console.print(Panel(result, title="YouTube Script"))


def cmd_cad():
    provider = Prompt.ask("AI Provider", default="groq")
    ai = AIEngine(provider)
    question = Prompt.ask("Your AutoCAD / Civil Engineering question")
    console.print("\n[yellow]Generating answer...[/yellow]")
    result = ai.autoCAD_help(question)
    console.print(Panel(result, title="Engineering Answer"))


def cmd_custom():
    provider = Prompt.ask("AI Provider", default="groq")
    ai = AIEngine(provider)
    prompt = Prompt.ask("Your prompt")
    console.print("\n[yellow]Generating...[/yellow]")
    result = ai.generate(prompt)
    console.print(Panel(result, title="AI Response"))


def cmd_stats():
    pm = ProjectManager()
    cm = ClientManager()
    ps = pm.get_stats()
    cs = cm.get_stats()
    console.print(Panel(
        f"[bold]Projects:[/bold]\n"
        f"  Total: {ps['total_projects']}\n"
        f"  Active: {ps['active']}\n"
        f"  Completed: {ps['completed']}\n"
        f"  Earnings: NPR {ps['total_earnings']:,.0f}\n\n"
        f"[bold]Clients:[/bold]\n"
        f"  Total: {cs['total_clients']}\n"
        f"  Earnings: NPR {cs['total_earnings']:,.0f}\n\n"
        f"[bold]This Month:[/bold]\n"
        f"  Projects: {ps['total_projects']}\n"
        f"  Revenue: NPR {ps['total_earnings']:,.0f}",
        title="Earnings Dashboard",
    ))


def cmd_config():
    console.print("\n[bold cyan]PROFILE SETUP[/bold cyan]")
    config = load_config()
    console.print(f"Current: {config['name']} | {config['country']}")

    name = Prompt.ask("Your name", default=config["name"])
    email = Prompt.ask("Email", default=config.get("email", ""))
    phone = Prompt.ask("Phone", default=config.get("phone", ""))
    upwork = Prompt.ask("Upwork username", default=config.get("upwork", ""))
    fiverr = Prompt.ask("Fiverr username", default=config.get("fiverr", ""))
    payoneer = Prompt.ask("Payoneer email", default=config.get("payoneer", ""))

    save_config({
        "name": name, "email": email, "phone": phone,
        "upwork": upwork, "fiverr": fiverr, "payoneer": payoneer,
    })
    console.print("[green]Profile saved![/green]")


def cmd_status():
    pm = ProjectManager()
    projects = pm.list_projects()
    if not projects:
        console.print("[yellow]No projects yet. Create one first![/yellow]")
        return

    table = Table(title="Project Status Board")
    table.add_column("ID", style="dim")
    table.add_column("Name", style="cyan")
    table.add_column("Client")
    table.add_column("Status")
    table.add_column("Tasks")
    table.add_column("Deadline")
    table.add_column("Earned")

    status_colors = {
        "pending": "dim",
        "in_progress": "yellow",
        "review": "blue",
        "revision": "red",
        "completed": "green",
        "delivered": "bright_green",
        "paid": "bright_cyan",
    }

    for p in projects:
        tasks_done = sum(1 for t in p.get("tasks", []) if t.get("done", False))
        tasks_total = len(p.get("tasks", []))
        status = p["status"]
        color = status_colors.get(status, "white")
        table.add_row(
            str(p["id"]), p["name"], p["client"],
            f"[{color}]{status}[/{color}]",
            f"{tasks_done}/{tasks_total}",
            p.get("deadline", "-"),
            f"NPR {p.get('earnings', 0):,.0f}",
        )
    console.print(table)


def cmd_multi():
    console.print(
        Panel.fit(
            "[bold cyan]MULTI-PROJECT DASHBOARD[/bold cyan]\n"
            "[dim]Manage 10-20 projects simultaneously[/dim]",
            border_style="bright_blue",
        )
    )
    pm = ProjectManager()
    batch = BatchProcessor(max_workers=5)

    console.print("  1. View all active projects")
    console.print("  2. Batch generate content for multiple projects")
    console.print("  3. Mass update project statuses")
    console.print("  4. Revenue overview")

    choice = Prompt.ask("Select", choices=["1", "2", "3", "4"])

    if choice == "1":
        projects = pm.list_projects(status="in_progress")
        if not projects:
            console.print("[yellow]No active projects. Create some first![/yellow]")
            return
        for p in projects:
            tasks_done = sum(1 for t in p.get("tasks", []) if t.get("done", False))
            console.print(
                f"  [{p['id']}] {p['name']} | {p['client']} | "
                f"Tasks: {tasks_done}/{len(p.get('tasks', []))} | "
                f"NPR {p.get('earnings', 0):,.0f}"
            )

    elif choice == "2":
        console.print("[dim]For each project, enter the content needed.[/dim]")
        console.print("[dim]Type 'done' when finished with all projects.[/dim]")
        all_tasks = []
        i = 1
        while True:
            project_name = Prompt.ask(f"Project {i} name (or 'done')")
            if project_name.lower() == "done":
                break
            content_type = Prompt.ask(f"  Content type (blog/social/seo/custom)")
            prompt = Prompt.ask(f"  Topic/Prompt")
            all_tasks.append({
                "type": "custom" if content_type == "custom" else content_type,
                "prompt": prompt,
                "topic": prompt,
                "keyword": prompt,
                "name": f"{project_name}_{content_type}",
            })
            i += 1

        if all_tasks:
            console.print(f"\n[yellow]Processing {len(all_tasks)} tasks across projects...[/yellow]")
            results = batch.process_tasks(all_tasks)
            saved_dir = batch.save_results("multi_project")
            console.print(f"[green]Results saved to {saved_dir}[/green]")
            console.print(f"[green]{batch.get_summary()['completed']}/{batch.get_summary()['total']} completed[/green]")

    elif choice == "3":
        projects = pm.list_projects()
        for p in projects:
            console.print(f"  [{p['id']}] {p['name']} - current: {p['status']}")
        pid = int(Prompt.ask("Project ID to update"))
        console.print(f"Statuses: {', '.join(PROJECT_STATUSES)}")
        status = Prompt.ask("New status")
        if pm.update_status(pid, status):
            console.print("[green]Updated![/green]")

    elif choice == "4":
        stats = pm.get_stats()
        console.print(Panel(
            f"Total Projects: {stats['total_projects']}\n"
            f"Active: {stats['active']}\n"
            f"Completed: {stats['completed']}\n"
            f"Total Revenue: NPR {stats['total_earnings']:,.0f}\n\n"
            f"[bold yellow]Monthly Target: NPR 50,000[/bold yellow]\n"
            f"Progress: {'=' * int(stats['total_earnings'] / 50000 * 20)}{'░' * (20 - int(stats['total_earnings'] / 50000 * 20))}",
            title="Revenue Overview",
        ))


def main():
    banner()
    load_config()

    if not os.getenv("GROQ_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        console.print(
            "[yellow]WARNING: No AI API key found![/yellow]\n"
            "[dim]Set GROQ_API_KEY or OPENAI_API_KEY in .env file[/dim]\n"
            "[dim]Get free Groq key at: https://console.groq.com[/dim]\n"
        )

    while True:
        console.print()
        menu()
        choice = Prompt.ask("\n[bold green]Enter command[/bold green]", default="0")

        try:
            if choice == "0":
                console.print("[yellow]Goodbye, Sachin! Keep earning![/yellow]")
                break
            elif choice == "1":
                cmd_generate()
            elif choice == "2":
                cmd_batch()
            elif choice == "3":
                cmd_project()
            elif choice == "4":
                cmd_client()
            elif choice == "5":
                cmd_proposal()
            elif choice == "6":
                cmd_invoice()
            elif choice == "7":
                cmd_fiverr()
            elif choice == "8":
                cmd_upwork()
            elif choice == "9":
                cmd_youtube()
            elif choice == "10":
                cmd_cad()
            elif choice == "11":
                cmd_custom()
            elif choice == "12":
                cmd_stats()
            elif choice == "13":
                cmd_config()
            elif choice == "14":
                cmd_status()
            elif choice == "15":
                cmd_multi()
            else:
                console.print("[red]Invalid command.[/red]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Returning to menu...[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
