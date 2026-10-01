import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_BASE_URL = os.getenv("AI_BASE_URL", "")
AI_MODEL = os.getenv("AI_MODEL", "")
PREMIUM_LINK = os.getenv("PREMIUM_LINK", "https://t.me/your_bot")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
FREE_LIMIT = int(os.getenv("FREE_LIMIT", "3"))
PREMIUM_PRICE = int(os.getenv("PREMIUM_PRICE", "990"))
REFERRAL_DISCOUNT_PERCENT = 10
MAX_REFERRALS = 3
