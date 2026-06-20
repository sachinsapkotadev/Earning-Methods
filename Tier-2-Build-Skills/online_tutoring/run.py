"""
ONLINE TUTORING TOOL
For: Sachin Sapkota | Nepal
Works on: MeroSchool, Zoom, Local Facebook groups
Earning: NPR 10,000-30,000/month
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


class TutoringAssistant:
    def __init__(self, provider: str = "groq"):
        self.ai = AIEngine(provider)
        self.lessons_created = 0

    def lesson_plan(self, subject: str, topic: str, grade: str, duration: int = 60) -> str:
        console.print(f"[yellow]Creating lesson plan: {topic}...[/yellow]")
        prompt = f"""Create a detailed lesson plan:

Subject: {subject}
Topic: {topic}
Grade level: {grade}
Duration: {duration} minutes

Include:
- Learning objectives (3-5)
- Prerequisites
- Materials needed
- Lesson structure with timings:
  - Warm-up/Review (5-10 min)
  - Introduction (10 min)
  - Main content (30-40 min)
  - Practice activities (15-20 min)
  - Assessment (5-10 min)
  - Homework/assignment
- Teaching methods
- Differentiation strategies
- Assessment criteria
- Nepal curriculum references (CTEVT/SEE) if applicable"""

        result = self.ai.generate(prompt)
        self.lessons_created += 1
        return result

    def quiz_generator(self, subject: str, topic: str, count: int = 10) -> str:
        console.print(f"[yellow]Generating {count} quiz questions...[/yellow]")
        prompt = f"""Generate {count} quiz questions:

Subject: {subject}
Topic: {topic}

Include a mix of:
- Multiple choice (4 options each)
- Short answer
- True/False
- Problem-solving

For each question provide:
- Question text
- Correct answer
- Explanation
- Difficulty level (easy/medium/hard)
- Marks allotted"""

        return self.ai.generate(prompt)

    def study_material(self, subject: str, topic: str) -> str:
        console.print(f"[yellow]Creating study material: {topic}...[/yellow]")
        prompt = f"""Create comprehensive study material:

Subject: {subject}
Topic: {topic}

Include:
- Key concepts and definitions
- Formulas (if applicable)
- Diagrams descriptions
- Real-life examples (Nepal context)
- Practice problems with solutions
- Summary/cheat sheet
- Common mistakes to avoid
- Further reading resources
- Memory tricks/mnemonics"""

        return self.ai.generate(prompt)

    def exam_prep(self, subject: str, exam_type: str) -> str:
        console.print(f"[yellow]Creating {exam_type} prep for {subject}...[/yellow]")
        prompt = f"""Create exam preparation guide:

Subject: {subject}
Exam type: {exam_type}

Include:
- Important topics to focus on
- Expected question types
- Time management strategy
- Key formulas/concepts
- Practice questions (10)
- Common mistakes
- Last-minute tips
- Nepal exam-specific advice"""

        return self.ai.generate(prompt)

    def course_outline(self, subject: str, duration_weeks: int = 8) -> str:
        console.print(f"[yellow]Creating {duration_weeks}-week course outline...[/yellow]")
        prompt = f"""Create a {duration_weeks}-week course outline:

Subject: {subject}

For each week include:
- Topics covered
- Learning objectives
- Assignments
- Assessments
- Resources needed

Also include:
- Course description
- Prerequisites
- Grading criteria
- Required materials
- Contact information placeholder"""

        return self.ai.generate(prompt)

    def student_feedback(self, student_name: str, performance: str) -> str:
        console.print(f"[yellow]Writing feedback for {student_name}...[/yellow]")
        prompt = f"""Write constructive student feedback:

Student: {student_name}
Performance: {performance}

Include:
- Positive observations
- Areas for improvement
- Specific suggestions
- Goals for next period
- Encouragement
- Parent communication notes

Keep professional, supportive tone."""

        return self.ai.generate(prompt)

    def pricing_strategy(self) -> str:
        prompt = """Create a tutoring pricing strategy for Nepal (2026):

Include:
- Hourly rates by subject and grade
- Package deals (monthly, quarterly)
- Group class pricing
- Online vs in-person rates
- Exam prep special packages
- Competitive analysis
- Value-added services
- Payment methods that work in Nepal

Recommend starting rates and scaling strategy."""

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
            "[bold cyan]ONLINE TUTORING TOOL[/bold cyan]\n"
            "[yellow]NPR 10,000-30,000/month potential[/yellow]\n"
            "[dim]Lesson plans, quizzes, study materials[/dim]",
            border_style="bright_yellow",
        )
    )

    provider = Prompt.ask("AI Provider", default="groq")
    tutor = TutoringAssistant(provider)

    while True:
        console.print()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Tool", style="cyan")
        table.add_column("What it does")
        tools = [
            ("1", "Lesson Plan", "Create detailed lesson plans"),
            ("2", "Quiz Generator", "Generate quiz questions"),
            ("3", "Study Material", "Create study notes and guides"),
            ("4", "Exam Prep", "Exam preparation guides"),
            ("5", "Course Outline", "Multi-week course structure"),
            ("6", "Student Feedback", "Write constructive feedback"),
            ("7", "Pricing Strategy", "Nepal tutoring pricing guide"),
            ("8", "Stats", "View stats"),
            ("0", "Exit", "Exit tutoring tool"),
        ]
        for num, tool, desc in tools:
            table.add_row(num, tool, desc)
        console.print(table)

        choice = Prompt.ask("\n[green]Select tool[/green]", default="0")

        try:
            if choice == "0":
                console.print(f"[yellow]Lessons created: {tutor.lessons_created} | Keep teaching![/yellow]")
                break
            elif choice == "1":
                subject = Prompt.ask("Subject")
                topic = Prompt.ask("Topic")
                grade = Prompt.ask("Grade level")
                duration = int(Prompt.ask("Duration (minutes)", default="60"))
                result = tutor.lesson_plan(subject, topic, grade, duration)
                console.print(Panel(result[:800] + "...", title="Lesson Plan"))
                if Confirm.ask("Save?"):
                    tutor.save(result, f"lesson_{topic[:20].replace(' ', '_')}.md")
            elif choice == "2":
                subject = Prompt.ask("Subject")
                topic = Prompt.ask("Topic")
                count = int(Prompt.ask("Number of questions", default="10"))
                result = tutor.quiz_generator(subject, topic, count)
                console.print(Panel(result[:800] + "...", title="Quiz"))
                if Confirm.ask("Save?"):
                    tutor.save(result, f"quiz_{topic[:20].replace(' ', '_')}.md")
            elif choice == "3":
                subject = Prompt.ask("Subject")
                topic = Prompt.ask("Topic")
                result = tutor.study_material(subject, topic)
                console.print(Panel(result[:800] + "...", title="Study Material"))
                if Confirm.ask("Save?"):
                    tutor.save(result, f"notes_{topic[:20].replace(' ', '_')}.md")
            elif choice == "4":
                subject = Prompt.ask("Subject")
                exam = Prompt.ask("Exam type (SEE/CTEVT/entrance/competitive)")
                result = tutor.exam_prep(subject, exam)
                console.print(Panel(result[:800] + "...", title="Exam Prep"))
                if Confirm.ask("Save?"):
                    tutor.save(result, f"prep_{exam}_{subject.replace(' ', '_')}.md")
            elif choice == "5":
                subject = Prompt.ask("Subject")
                weeks = int(Prompt.ask("Duration (weeks)", default="8"))
                result = tutor.course_outline(subject, weeks)
                console.print(Panel(result[:800] + "...", title="Course Outline"))
                if Confirm.ask("Save?"):
                    tutor.save(result, f"course_{subject.replace(' ', '_')}.md")
            elif choice == "6":
                name = Prompt.ask("Student name")
                perf = Prompt.ask("Performance description")
                result = tutor.student_feedback(name, perf)
                console.print(Panel(result, title="Student Feedback"))
            elif choice == "7":
                result = tutor.pricing_strategy()
                console.print(Panel(result, title="Pricing Strategy"))
                if Confirm.ask("Save?"):
                    tutor.save(result, "pricing_strategy.md")
            elif choice == "8":
                console.print(Panel(
                    f"Lessons Created: {tutor.lessons_created}",
                    title="Stats",
                ))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
