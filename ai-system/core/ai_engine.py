import json
import time
from typing import Optional
from openai import OpenAI
from config.settings import AI_PROVIDERS, DEFAULT_PROVIDER, get_api_key


class AIEngine:
    def __init__(self, provider: str = None):
        self.provider = provider or DEFAULT_PROVIDER
        self.config = AI_PROVIDERS[self.provider]
        api_key = get_api_key(self.provider)

        if self.provider == "gemini":
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            )
        else:
            self.client = OpenAI(
                api_key=api_key or "ollama",
                base_url=self.config["base_url"],
            )
        self.model = self.config["model"]
        self.history = []

    def generate(
        self,
        prompt: str,
        system: str = "You are a professional content writer and freelancer assistant.",
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            result = response.choices[0].message.content
            self.history.append({"prompt": prompt, "result": result})
            return result
        except Exception as e:
            return f"[AI Error] {str(e)}"

    def generate_batch(
        self,
        prompts: list[dict],
        system: str = "You are a professional content writer and freelancer assistant.",
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> list[str]:
        results = []
        for item in prompts:
            prompt = item if isinstance(item, str) else item.get("prompt", "")
            result = self.generate(prompt, system, temperature, max_tokens)
            results.append(result)
            time.sleep(0.5)
        return results

    def blog_post(self, topic: str, words: int = 1500, seo_keyword: str = "") -> str:
        seo = f"Optimize for SEO keyword: {seo_keyword}" if seo_keyword else ""
        prompt = f"""Write a professional blog post about: {topic}
Word count: approximately {words} words
{seo}

Requirements:
- Engaging title
- Introduction hook
- Well-structured headings (H2, H3)
- Practical tips and examples
- Call to action conclusion
- Write in natural, human tone

Return the full blog post in markdown format."""

        return self.generate(
            prompt,
            system="You are an expert blog writer who creates SEO-optimized, engaging content. Write in natural human tone.",
        )

    def social_media_posts(
        self, brand: str, platform: str, count: int = 5, niche: str = ""
    ) -> str:
        prompt = f"""Create {count} social media posts for: {brand}
Platform: {platform}
Niche: {niche}

Requirements:
- Each post should be unique
- Include relevant hashtags
- Include call-to-action where appropriate
- Vary between educational, promotional, engaging, and motivational
- Make them platform-appropriate length

Return each post separated by "---POST---" """

        return self.generate(
            prompt,
            system="You are a social media expert who creates viral, engaging content that drives engagement.",
        )

    def seo_article(self, keyword: str, word_count: int = 2000) -> str:
        prompt = f"""Write a comprehensive SEO article targeting the keyword: {keyword}
Word count: {word_count} words

Requirements:
- SEO-optimized title with keyword
- Meta description (155 characters)
- Introduction with keyword in first paragraph
- Multiple H2 and H3 headings
- Keyword density 1-2%
- Internal linking suggestions
- FAQ section at the end
- Conclusion with CTA

Return in markdown format with front matter (title, description, keywords)."""

        return self.generate(
            prompt,
            system="You are an SEO content specialist. Write articles that rank on Google while providing genuine value to readers.",
        )

    def product_description(self, product: str, features: list = None) -> str:
        features_text = "\n".join(f"- {f}" for f in (features or []))
        prompt = f"""Write a compelling product description for: {product}

Features:
{features_text}

Requirements:
- Attention-grabbing headline
- Benefit-focused description (not just features)
- Social proof elements
- Urgency/scarcity elements
- Clear CTA
- Write for e-commerce (Amazon/Daraz style)"""

        return self.generate(
            prompt,
            system="You are an e-commerce copywriter who writes descriptions that convert browsers into buyers.",
        )

    def email_sequence(self, topic: str, emails: int = 5) -> str:
        prompt = f"""Create an email sequence for: {topic}
Number of emails: {emails}

For each email provide:
- Subject line (with A/B test variant)
- Preview text
- Full email body
- CTA button text

Return each email separated by "---EMAIL---" """

        return self.generate(
            prompt,
            system="You are an email marketing expert who writes sequences that get high open rates and conversions.",
        )

    def proposal(self, client: str, project: str, budget: str, timeline: str) -> str:
        from config.settings import USER_INFO
        prompt = f"""Write a professional freelance proposal:

Client: {client}
Project: {project}
Budget: {budget}
Timeline: {timeline}
Freelancer: {USER_INFO['name']}
Location: {USER_INFO['country']}

Requirements:
- Professional greeting
- Understanding of the project
- Why I'm the right fit
- Relevant experience/skills
- Proposed approach/milestones
- Timeline breakdown
- Call to action
- Professional closing

Keep it concise (300-400 words). Write in first person."""

        return self.generate(
            prompt,
            system="You are a professional freelancer who writes winning proposals that land clients on Upwork and Fiverr.",
        )

    def invoice(self, client: str, items: list, invoice_no: str = "INV-001") -> str:
        items_text = ""
        total = 0
        for item in items:
            desc = item.get("description", "")
            qty = item.get("quantity", 1)
            rate = item.get("rate", 0)
            amount = qty * rate
            total += amount
            items_text += f"| {desc} | {qty} | NPR {rate:,.0f} | NPR {amount:,.0f} |\n"

        from config.settings import USER_INFO
        prompt = f"""Create a professional invoice:

Invoice Number: {invoice_no}
From: {USER_INFO['name']} ({USER_INFO['country']})
To: {client}

Items:
| Description | Qty | Rate | Amount |
|---|---|---|---|
{items_text}
| **Total** | | | **NPR {total:,.0f}** |

Requirements:
- Professional layout
- Payment terms
- Bank/Payoneer details placeholder
- Thank you note
- Return in markdown format"""

        return self.generate(
            prompt,
            system="You are a professional accountant who creates clean, clear invoices.",
        )

    def autoCAD_help(self, question: str) -> str:
        prompt = f"""AutoCAD/Civil Engineering question: {question}

Provide:
- Clear explanation
- Step-by-step commands if applicable
- Tips and shortcuts
- Common mistakes to avoid"""

        return self.generate(
            prompt,
            system="You are a senior civil engineer and AutoCAD expert. Provide practical, accurate technical answers.",
            temperature=0.3,
        )

    def code_review(self, code: str, language: str = "python") -> str:
        prompt = f"""Review this {language} code and suggest improvements:

```
{code}
```

Provide:
- Issues found
- Performance improvements
- Best practices
- Fixed code example"""

        return self.generate(
            prompt,
            system="You are a senior software developer. Review code thoroughly and suggest practical improvements.",
            temperature=0.3,
        )
