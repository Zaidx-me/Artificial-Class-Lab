"""Central configuration (reads .env)."""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # dotenv is optional
    pass

BASE_DIR = Path(__file__).parent
DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "data" / "recruitment.db"))
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
INBOX_DIR = BASE_DIR / "assets" / "inbox"        # fallback "inbox" of .eml files
DOWNLOAD_DIR = BASE_DIR / "data" / "downloads"   # attachments saved here
UPLOAD_DIR = BASE_DIR / "data" / "uploads"       # resumes uploaded through the UI

LLM_API_KEY = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL") or None
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "0") == "1"

# Reasoning models (e.g. NVIDIA Nemotron) "think" before replying: slow, and can return empty
# text because reasoning tokens count against max_tokens. Blank = auto-disable on NVIDIA
# endpoints; set LLM_DISABLE_THINKING=1/0 to force it on or off.
_thinking_env = os.getenv("LLM_DISABLE_THINKING")
LLM_DISABLE_THINKING = (
    _thinking_env.strip() == "1"
    if _thinking_env is not None
    else "nvidia" in (LLM_BASE_URL or "").lower()
)

IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
EMAIL_USER = os.getenv("EMAIL_USER", "")
EMAIL_PASS = os.getenv("EMAIL_PASS", "")

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))

MAX_AGENT_STEPS = 80

# How many candidate evaluations run concurrently in process_new_applications.
LLM_EVAL_WORKERS = int(os.getenv("LLM_EVAL_WORKERS", "4"))
