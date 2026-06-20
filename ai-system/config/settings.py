import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
PROJECTS_DIR = BASE_DIR / "projects"
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "templates"

for d in [CONFIG_DIR, PROJECTS_DIR, OUTPUT_DIR, TEMPLATES_DIR]:
    d.mkdir(exist_ok=True)

AI_PROVIDERS = {
    "openai": {
        "api_key_env": "OPENAI_API_KEY",
        "model": "gpt-4o-mini",
        "base_url": "https://api.openai.com/v1",
    },
    "groq": {
        "api_key_env": "GROQ_API_KEY",
        "model": "llama-3.3-70b-versatile",
        "base_url": "https://api.groq.com/openai/v1",
    },
    "gemini": {
        "api_key_env": "GEMINI_API_KEY",
        "model": "gemini-2.0-flash",
        "base_url": "https://generativelanguage.googleapis.com/v1beta",
    },
    "ollama": {
        "api_key_env": "",
        "model": "llama3.2",
        "base_url": "http://localhost:11434/v1",
    },
}

DEFAULT_PROVIDER = "groq"

PROJECT_STATUSES = [
    "pending",
    "in_progress",
    "review",
    "revision",
    "completed",
    "delivered",
    "paid",
]

CONTENT_TYPES = [
    "blog_post",
    "article",
    "social_media_post",
    "email_copy",
    "product_description",
    "seo_content",
    "technical_writing",
    "resume",
    "proposal",
]

TASK_TYPES = [
    "content_writing",
    "graphic_design",
    "video_editing",
    "data_entry",
    "social_media_management",
    "seo_work",
    "web_development",
    "autoCAD_drafting",
    "tutoring",
    "virtual_assistant",
]

CURRENCY = "NPR"

USER_INFO = {
    "name": "Sachin Sapkota",
    "country": "Nepal",
    "email": "",
    "phone": "",
    "upwork": "",
    "fiverr": "",
    "payoneer": "",
}


def load_config():
    config_file = CONFIG_DIR / "user_config.json"
    if config_file.exists():
        with open(config_file, "r") as f:
            saved = json.load(f)
            USER_INFO.update(saved)
    return USER_INFO


def save_config(info: dict):
    USER_INFO.update(info)
    config_file = CONFIG_DIR / "user_config.json"
    with open(config_file, "w") as f:
        json.dump(USER_INFO, f, indent=2)


def get_api_key(provider: str = None) -> str:
    provider = provider or DEFAULT_PROVIDER
    env_key = AI_PROVIDERS[provider]["api_key_env"]
    if env_key:
        return os.getenv(env_key, "")
    return ""
