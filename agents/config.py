import os
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent

logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(BASE_DIR / "logs" / "system.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("config")

API_KEYS = {
    "deepseek": os.getenv("DEEPSEEK_API_KEY"),
    "claude": os.getenv("CLAUDE_API_KEY"),
    "elevenlabs": os.getenv("ELEVENLABS_API_KEY"),
    "buttondown": os.getenv("BUTTONDOWN_API_KEY"),
    "youtube": os.getenv("YOUTUBE_API_KEY"),
}

HAS_GEN_AI = any(k for name, k in API_KEYS.items() if name != "buttondown" and k and not k.startswith("your_") and k != "placeholder")
HAS_BUTTONDOWN = bool(API_KEYS.get("buttondown"))

LOCAL_MODE = not HAS_GEN_AI
if LOCAL_MODE:
    logger.info("Local mode — all content generation uses embedded templates (no external AI APIs)")

BRAND = {
    "name": os.getenv("NEWSLETTER_NAME", "Business Digest"),
    "tagline": os.getenv("NEWSLETTER_TAGLINE", "Three moves. Every Saturday. Zero noise."),
    "domain": os.getenv("DOMAIN", "businessdigest.com"),
}
