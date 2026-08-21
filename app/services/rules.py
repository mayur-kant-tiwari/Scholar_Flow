"""Deterministic eligibility rule engine — judgment stays in code, not the AI.

These thresholds are placeholders for your college's actual policy document.
"""
from dataclasses import dataclass

from app.services.extraction import ExtractedFields

INCOME_CEILING = {
    "General": 250_000,
    "OBC": 300_000,
    "SC": 350_000,
    "ST": 350_000,
}
BORDERLINE_BAND = 20_000  # within this much of the ceiling => human review
MIN_MARKS = 60.0


@dataclass
class Decision:
    status: str  # "eligible" | "not_eligible" | "borderline"
    reason: str


def evaluate_eligibility(fields: ExtractedFields) -> Decision:
    ceiling = INCOME_CEILING.get(fields.category, INCOME_CEILING["General"])

    if fields.marks_percentage < MIN_MARKS:
        return Decision("not_eligible", f"Marks {fields.marks_percentage}% below the {MIN_MARKS}% minimum.")

    if fields.annual_income <= ceiling - BORDERLINE_BAND:
        return Decision("eligible", f"Income within the {fields.category} ceiling of ₹{ceiling:,}.")

    if fields.annual_income <= ceiling + BORDERLINE_BAND:
        return Decision("borderline", f"Income within ₹{BORDERLINE_BAND:,} of the {fields.category} ceiling — needs a human call.")

    return Decision("not_eligible", f"Income exceeds the {fields.category} ceiling of ₹{ceiling:,}.")
