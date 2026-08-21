"""Notion API integration — Cases database + Run Log database.

Notion is the interface, not the whole system: this module is the only place
that talks to Notion, so the rest of the app stays testable without it.
"""
import os
from datetime import datetime, timezone

import httpx

NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")
CASES_DB_ID = os.getenv("NOTION_CASES_DB_ID", "")
RUN_LOG_DB_ID = os.getenv("NOTION_RUN_LOG_DB_ID", "")

_HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


def create_case(student_name: str, student_email: str, extracted, decision) -> str:
    """Creates a row in the Cases database. Returns the Notion page id."""
    payload = {
        "parent": {"database_id": CASES_DB_ID},
        "properties": {
            "Student": {"title": [{"text": {"content": student_name}}]},
            "Email": {"email": student_email},
            "Category": {"select": {"name": extracted.category}},
            "Income (extracted)": {"number": extracted.annual_income},
            "Eligibility": {"select": {"name": decision.status}},
            "Status": {
                "select": {"name": "Auto-Resolved" if decision.status != "borderline" else "Needs Review"}
            },
        },
    }
    resp = httpx.post("https://api.notion.com/v1/pages", headers=_HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json()["id"]


def close_case(case_id: str, resolved_by: str) -> None:
    payload = {"properties": {"Resolved By": {"rich_text": [{"text": {"content": resolved_by}}]}}}
    httpx.patch(f"https://api.notion.com/v1/pages/{case_id}", headers=_HEADERS, json=payload)


def log_run(case_id: str, decision, auto: bool) -> None:
    payload = {
        "parent": {"database_id": RUN_LOG_DB_ID},
        "properties": {
            "Case": {"relation": [{"id": case_id}]},
            "Outcome": {"select": {"name": decision.status}},
            "Auto": {"checkbox": auto},
            "Reason": {"rich_text": [{"text": {"content": decision.reason}}]},
            "Timestamp": {"date": {"start": datetime.now(timezone.utc).isoformat()}},
        },
    }
    httpx.post("https://api.notion.com/v1/pages", headers=_HEADERS, json=payload)
