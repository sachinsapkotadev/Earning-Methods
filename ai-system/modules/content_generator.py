from datetime import datetime
from core.ai_engine import AIEngine
from core.batch_processor import BatchProcessor
from config.settings import CONTENT_TYPES


class ContentGenerator:
    def __init__(self, provider: str = None):
        self.ai = AIEngine(provider)
        self.batch = BatchProcessor(max_workers=5, provider=provider)

    def blog_post(self, topic: str, words: int = 1500, keyword: str = "") -> str:
        return self.ai.blog_post(topic, words, keyword)

    def batch_blog_posts(self, topics: list[str], words: int = 1500) -> list[dict]:
        tasks = [
            {"type": "blog_post", "topic": t, "words": words, "name": f"blog_{i+1}"}
            for i, t in enumerate(topics)
        ]
        return self.batch.process_tasks(tasks)

    def social_media_posts(
        self, brand: str, platform: str, count: int = 5, niche: str = ""
    ) -> str:
        return self.ai.social_media_posts(brand, platform, count, niche)

    def batch_social_posts(
        self, brand: str, platforms: list[str], count: int = 5
    ) -> list[dict]:
        tasks = [
            {"type": "social_media", "brand": brand, "platform": p, "count": count, "name": f"social_{p}"}
            for p in platforms
        ]
        return self.batch.process_tasks(tasks)

    def seo_article(self, keyword: str, words: int = 2000) -> str:
        return self.ai.seo_article(keyword, words)

    def batch_seo_articles(self, keywords: list[str], words: int = 2000) -> list[dict]:
        tasks = [
            {"type": "seo_article", "keyword": k, "words": words, "name": f"seo_{i+1}"}
            for i, k in enumerate(keywords)
        ]
        return self.batch.process_tasks(tasks)

    def product_description(self, product: str, features: list = None) -> str:
        return self.ai.product_description(product, features)

    def batch_product_descriptions(self, products: list[dict]) -> list[dict]:
        tasks = [
            {
                "type": "product_description",
                "product": p["name"],
                "features": p.get("features", []),
                "name": f"product_{i+1}",
            }
            for i, p in enumerate(products)
        ]
        return self.batch.process_tasks(tasks)

    def email_sequence(self, topic: str, emails: int = 5) -> str:
        return self.ai.email_sequence(topic, emails)

    def youtube_script(self, topic: str, duration_min: int = 10) -> str:
        prompt = f"""Write a YouTube video script about: {topic}
Target duration: {duration_min} minutes (approx {duration_min * 150} words)

Include:
- Hook (first 10 seconds)
- Introduction
- Main content with timestamps
- B-roll suggestions [B-roll: description]
- Call to action
- Outro

Format with timestamps like [00:00], [01:30], etc."""

        return self.ai.generate(
            prompt,
            system="You are a YouTube content strategist who writes scripts that keep viewers watching.",
        )

    def fiverr_gig_description(self, service: str, skills: list = None) -> str:
        skills_text = ", ".join(skills or [])
        prompt = f"""Write a Fiverr gig description for: {service}
Skills: {skills_text}

Include:
- Attention-grabbing title (60 chars max)
- Gig description (structured, engaging)
- 3 packages: Basic, Standard, Premium with prices
- FAQ section (5 questions)
- Requirements from buyer

Make it professional and conversion-focused."""

        return self.ai.generate(
            prompt,
            system="You are a Fiverr optimization expert who writes gig descriptions that rank and convert.",
        )

    def upwork_proposal(self, client: str, project: str, budget: str = "", timeline: str = "") -> str:
        return self.ai.proposal(client, project, budget, timeline)

    def client_report(self, project: str, tasks_done: list, next_steps: list) -> str:
        tasks_text = "\n".join(f"- [x] {t}" for t in tasks_done)
        steps_text = "\n".join(f"- [ ] {s}" for s in next_steps)
        prompt = f"""Write a professional client progress report:

Project: {project}
Completed Tasks:
{tasks_text}

Next Steps:
{steps_text}

Include:
- Professional greeting
- Summary of progress
- What was delivered
- What's coming next
- Any questions/concerns
- Professional closing"""

        return self.ai.generate(
            prompt,
            system="You are a professional freelancer who writes clear, impressive client reports.",
        )
