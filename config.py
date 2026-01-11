import os
from dotenv import load_dotenv

load_dotenv()

#
# API Keys
#
COMET_API_KEY = os.getenv("COMET_API_KEY")
COMET_API_BASE_URL = os.getenv("COMET_API_BASE_URL", "https://api.cometapi.com/v1")
COMET_API_MODEL = os.getenv("COMET_API_MODEL", "gpt-4o")

# Google Custom Search API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

#
# Telegram API
#
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

#
# Application Settings
#
POSTS_TO_FETCH = int(os.getenv("POSTS_TO_FETCH", 50))
MAX_CHANNELS_PER_SEARCH = int(os.getenv("MAX_CHANNELS_PER_SEARCH", 20))
SEARCH_QUERIES_COUNT = int(os.getenv("SEARCH_QUERIES_COUNT", 5))
MIN_QUALIFICATION_SCORE = int(os.getenv("MIN_QUALIFICATION_SCORE", 5))


DEFAULT_CONFIG = {
    "search": {
        "queries_per_niche": 5,
        "max_results_per_query": 10,
        "deduplicate": True
    },
    "parser": {
        "posts_limit": 50,
        "include_comments": False,
        "timeout_seconds": 30
    },
    "qualifier": {
        "min_score": 5,
        "include_reasoning": True
    },
    "output": {
        "formats": ["json", "markdown"],
        "include_raw_data": False
    }
}
