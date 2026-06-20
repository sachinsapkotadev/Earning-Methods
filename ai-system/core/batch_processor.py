import concurrent.futures
import json
import time
from pathlib import Path
from datetime import datetime
from core.ai_engine import AIEngine
from config.settings import PROJECTS_DIR, OUTPUT_DIR


class BatchProcessor:
    def __init__(self, max_workers: int = 5, provider: str = None):
        self.max_workers = max_workers
        self.provider = provider
        self.results = []
        self.errors = []

    def process_tasks(self, tasks: list[dict]) -> list[dict]:
        results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_task = {}
            for task in tasks:
                ai = AIEngine(self.provider)
                future = executor.submit(self._run_task, ai, task)
                future_to_task[future] = task

            for future in concurrent.futures.as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)
                    print(f"  Done: {task.get('name', 'unnamed')}")
                except Exception as e:
                    error_result = {
                        "task": task,
                        "status": "error",
                        "error": str(e),
                        "timestamp": datetime.now().isoformat(),
                    }
                    results.append(error_result)
                    self.errors.append(error_result)
                    print(f"  Error: {task.get('name', 'unnamed')} - {e}")

        self.results = results
        return results

    def _run_task(self, ai: AIEngine, task: dict) -> dict:
        task_type = task.get("type", "custom")
        start_time = time.time()

        if task_type == "blog_post":
            content = ai.blog_post(
                topic=task["topic"],
                words=task.get("words", 1500),
                seo_keyword=task.get("keyword", ""),
            )
        elif task_type == "social_media":
            content = ai.social_media_posts(
                brand=task["brand"],
                platform=task["platform"],
                count=task.get("count", 5),
                niche=task.get("niche", ""),
            )
        elif task_type == "seo_article":
            content = ai.seo_article(
                keyword=task["keyword"],
                word_count=task.get("words", 2000),
            )
        elif task_type == "product_description":
            content = ai.product_description(
                product=task["product"],
                features=task.get("features", []),
            )
        elif task_type == "email_sequence":
            content = ai.email_sequence(
                topic=task["topic"],
                emails=task.get("emails", 5),
            )
        elif task_type == "proposal":
            content = ai.proposal(
                client=task["client"],
                project=task["project"],
                budget=task.get("budget", ""),
                timeline=task.get("timeline", ""),
            )
        elif task_type == "invoice":
            content = ai.invoice(
                client=task["client"],
                items=task.get("items", []),
                invoice_no=task.get("invoice_no", "INV-001"),
            )
        elif task_type == "custom":
            content = ai.generate(
                prompt=task["prompt"],
                system=task.get("system", "You are a professional assistant."),
            )
        else:
            content = ai.generate(prompt=task.get("prompt", ""))

        elapsed = round(time.time() - start_time, 2)

        return {
            "task": task,
            "status": "completed",
            "content": content,
            "elapsed": elapsed,
            "timestamp": datetime.now().isoformat(),
        }

    def save_results(self, project_name: str) -> Path:
        project_dir = OUTPUT_DIR / project_name
        project_dir.mkdir(exist_ok=True)

        for i, result in enumerate(self.results):
            if result["status"] == "completed":
                task = result["task"]
                task_type = task.get("type", "custom")
                name = task.get("name", f"output_{i+1}")
                filename = f"{name}.md"

                filepath = project_dir / filename
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"# {name}\n\n")
                    f.write(f"**Type:** {task_type}\n")
                    f.write(f"**Generated:** {result['timestamp']}\n")
                    f.write(f"**Time:** {result['elapsed']}s\n\n---\n\n")
                    f.write(result["content"])

        summary_path = project_dir / "_summary.json"
        summary = {
            "project": project_name,
            "total_tasks": len(self.results),
            "completed": sum(1 for r in self.results if r["status"] == "completed"),
            "errors": len(self.errors),
            "total_time": sum(r.get("elapsed", 0) for r in self.results if r["status"] == "completed"),
            "timestamp": datetime.now().isoformat(),
        }
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)

        return project_dir

    def get_summary(self) -> dict:
        return {
            "total": len(self.results),
            "completed": sum(1 for r in self.results if r["status"] == "completed"),
            "errors": len(self.errors),
            "total_time": sum(r.get("elapsed", 0) for r in self.results),
        }


def quick_batch(prompt_list: list[str], provider: str = None) -> list[str]:
    tasks = [{"type": "custom", "prompt": p, "name": f"task_{i+1}"} for i, p in enumerate(prompt_list)]
    processor = BatchProcessor(max_workers=3, provider=provider)
    results = processor.process_tasks(tasks)
    return [r.get("content", "") for r in results if r["status"] == "completed"]


def batch_blog_posts(topics: list[str], words: int = 1500, provider: str = None) -> list[dict]:
    tasks = [
        {"type": "blog_post", "topic": t, "words": words, "name": f"blog_{i+1}"}
        for i, t in enumerate(topics)
    ]
    processor = BatchProcessor(max_workers=3, provider=provider)
    return processor.process_tasks(tasks)


def batch_social_posts(
    brand: str, platforms: list[str], count: int = 5, provider: str = None
) -> list[dict]:
    tasks = [
        {"type": "social_media", "brand": brand, "platform": p, "count": count, "name": f"social_{p}"}
        for p in platforms
    ]
    processor = BatchProcessor(max_workers=3, provider=provider)
    return processor.process_tasks(tasks)
