"""Central place to read environment settings, so nothing else calls os.getenv directly."""
import os

NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")
NOTION_CASES_DB_ID = os.getenv("NOTION_CASES_DB_ID", "")
NOTION_RUN_LOG_DB_ID = os.getenv("NOTION_RUN_LOG_DB_ID", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "mailtrap")
EMAIL_API_KEY = os.getenv("EMAIL_API_KEY", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@scholarflow.example")
