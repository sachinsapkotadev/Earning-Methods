"""
ONLINE COURSE CREATOR TOOL
For: Sachin Sapkota | Nepal
Earning: NPR 10,000-50,000+/month
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


class CourseCreator:
    def __init__(self, provider: str = "groq"):
        self.ai = AIEngine(provider)
        self.courses_created = 0

    def full_curriculum(self, topic: str, lessons: int = 20) -> str:
        console.print(f"[yellow]Creating course curriculum: {topic}...[/yellow]")
        prompt = f"""Create a complete online course curriculum:

Topic: {topic}
Lessons: {lessons}

For each lesson:
- Lesson title
- Learning objective (1 sentence)
- Video script outline (key talking points)
- Text content/supporting material
- Assignment/exercise
- Downloadable resource idea
- Estimated duration

Include:
- Course title (3 options)
- Course description (for landing page)
- Prerequisites
- What students will learn (10 bullet points)
- Target audience
- Course level (beginner/intermediate/advanced)
- Total estimated duration
- Certificate template idea"""

        result = self.ai.generate(prompt)
        self.courses_created += 1
        return result

    def lesson_script(self, topic: str, duration: int = 15) -> str:
        console.print(f"[yellow]Writing lesson script...[/yellow]")
        prompt = f"""Write a detailed lesson script:

Topic: {topic}
Duration: {duration} minutes

Include:
- Opening hook (30 seconds)
- Recap of previous lesson (1 minute)
- Today's agenda (1 minute)
- Main content sections with timestamps
- Code examples/demonstrations if applicable
- Practice exercise
- Key takeaways
- Next lesson preview
- Engagement questions throughout

Write in conversational, teaching tone.
Include [SLIDE: description] markers."""

        return self.ai.generate(prompt)

    def course_landing_page(self, topic: str, price: str) -> str:
        console.print(f"[yellow]Writing landing page copy...[/yellow]")
        prompt = f"""Write a high-converting course landing page:

Course: {topic}
Price: {price}

Include:
- Headline (attention-grabbing)
- Subheadline
- Video placeholder text
- What you'll learn (10 points)
- Course curriculum preview (modules)
- Instructor bio template (Sachin Sapkota, Nepal)
- Student testimonials template
- Price anchoring
- Money-back guarantee
- FAQ section (10 questions)
- CTA buttons
- Social proof elements
- Urgency/scarcity elements"""

        return self.ai.generate(prompt)

    def quiz_assessment(self, topic: str, questions: int = 20) -> str:
        console.print(f"[yellow]Creating assessments for {topic}...[/yellow]")
        prompt = f"""Create course assessments for: {topic}

Include {questions} questions:
- Multiple choice (10)
- Short answer (5)
- Practical exercises (3)
- True/False (2)

For each question:
- Question text
- Correct answer
- Explanation
- Points value
- Difficulty level

Also create:
- Final exam structure
- Grading criteria
- Pass/fail requirements
- Certificate requirements"""

        return self.ai.generate(prompt)

    def marketing_plan(self, topic: str, platform: str) -> str:
        console.print(f"[yellow]Creating marketing plan...[/yellow]")
        prompt = f"""Create a course marketing plan:

Course: {topic}
Platform: {platform}

Include:
- Pre-launch strategy (4 weeks)
- Launch day plan
- Post-launch ongoing marketing
- Social media strategy
- Email marketing sequence
- Free content funnel
- SEO strategy for course page
- Paid ads strategy (if applicable)
- Affiliate/referral program
- Nepal-specific marketing channels
- Pricing strategy
- Discount/coupon strategy
- Upsell/cross-sell opportunities"""

        return self.ai.generate(prompt)

    def module_content(self, module_name: str, lessons: int = 5) -> str:
        console.print(f"[yellow]Creating module: {module_name}...[/yellow]")
        prompt = f"""Create detailed module content:

Module: {module_name}
Lessons: {lessons}

For each lesson:
- Title
- Video script outline
- Text lesson content (1000+ words)
- Hands-on exercise
- Quiz questions (5)
- Resources/links

Include:
- Module overview
- Learning objectives
- Prerequisites
- Module assignment
- Module quiz
- Completion criteria"""

        return self.ai.generate(prompt)

    def udemy_listing(self, topic: str) -> str:
        console.print(f"[yellow]Creating Udemy listing...[/yellow]")
        prompt = f"""Create a Udemy course listing:

Course topic: {topic}

Include:
- Course title (optimized for Udemy search)
- Course description (SEO optimized)
- What you'll learn (bullet points)
- Requirements
- Target audience
- Course content (modules and lectures)
- Instructor profile (Sachin Sapkota)
- 4 lectures preview descriptions
- Pricing recommendation
- Tags (20)
- Coupon strategy"""

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
            "[bold cyan]ONLINE COURSE CREATOR[/bold cyan]\n"
            "[yellow]NPR 10,000-50,000+/month potential[/yellow]\n"
            "[dim]Curriculum, scripts, landing pages, marketing[/dim]",
            border_style="bright_yellow",
        )
    )

    provider = Prompt.ask("AI Provider", default="groq")
    cc = CourseCreator(provider)

    while True:
        console.print()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Tool", style="cyan")
        table.add_column("What it does")
        tools = [
            ("1", "Full Curriculum", "Complete course structure"),
            ("2", "Lesson Script", "Write video lesson scripts"),
            ("3", "Landing Page", "Course sales page copy"),
            ("4", "Quiz/Assessment", "Create course assessments"),
            ("5", "Marketing Plan", "Course marketing strategy"),
            ("6", "Module Content", "Detailed module lessons"),
            ("7", "Udemy Listing", "Udemy-specific listing"),
            ("8", "Stats", "View stats"),
            ("0", "Exit", "Exit course tool"),
        ]
        for num, tool, desc in tools:
            table.add_row(num, tool, desc)
        console.print(table)

        choice = Prompt.ask("\n[green]Select tool[/green]", default="0")

        try:
            if choice == "0":
                console.print(f"[yellow]Courses created: {cc.courses_created} | Keep teaching![/yellow]")
                break
            elif choice == "1":
                topic = Prompt.ask("Course topic")
                lessons = int(Prompt.ask("Number of lessons", default="20"))
                result = cc.full_curriculum(topic, lessons)
                console.print(Panel(result[:800] + "...", title="Curriculum Preview"))
                if Confirm.ask("Save?"):
                    cc.save(result, f"curriculum_{topic[:20].replace(' ', '_')}.md")
            elif choice == "2":
                topic = Prompt.ask("Lesson topic")
                duration = int(Prompt.ask("Duration (minutes)", default="15"))
                result = cc.lesson_script(topic, duration)
                console.print(Panel(result[:500] + "...", title="Script Preview"))
                if Confirm.ask("Save?"):
                    cc.save(result, f"script_{topic[:20].replace(' ', '_')}.md")
            elif choice == "3":
                topic = Prompt.ask("Course topic")
                price = Prompt.ask("Price")
                result = cc.course_landing_page(topic, price)
                console.print(Panel(result[:800] + "...", title="Landing Page"))
                if Confirm.ask("Save?"):
                    cc.save(result, f"landing_{topic[:20].replace(' ', '_')}.md")
            elif choice == "4":
                topic = Prompt.ask("Course topic")
                count = int(Prompt.ask("Number of questions", default="20"))
                result = cc.quiz_assessment(topic, count)
                console.print(Panel(result[:800] + "...", title="Assessment"))
                if Confirm.ask("Save?"):
                    cc.save(result, f"quiz_{topic[:20].replace(' ', '_')}.md")
            elif choice == "5":
                topic = Prompt.ask("Course topic")
                platform = Prompt.ask("Platform (Udemy/Teachable/Own)")
                result = cc.marketing_plan(topic, platform)
                console.print(Panel(result[:800] + "...", title="Marketing Plan"))
                if Confirm.ask("Save?"):
                    cc.save(result, f"marketing_{topic[:20].replace(' ', '_')}.md")
            elif choice == "6":
                module = Prompt.ask("Module name")
                lessons = int(Prompt.ask("Lessons in module", default="5"))
                result = cc.module_content(module, lessons)
                console.print(Panel(result[:800] + "...", title="Module Content"))
                if Confirm.ask("Save?"):
                    cc.save(result, f"module_{module[:20].replace(' ', '_')}.md")
            elif choice == "7":
                topic = Prompt.ask("Course topic")
                result = cc.udemy_listing(topic)
                console.print(Panel(result[:800] + "...", title="Udemy Listing"))
                if Confirm.ask("Save?"):
                    cc.save(result, f"udemy_{topic[:20].replace(' ', '_')}.md")
            elif choice == "8":
                console.print(Panel(
                    f"Courses Created: {cc.courses_created}",
                    title="Stats",
                ))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
