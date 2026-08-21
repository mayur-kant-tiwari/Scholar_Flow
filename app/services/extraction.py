"""AI document extraction — reads scanned certificates, pulls structured fields.

Swap `_call_model` for a real Claude / GPT-4o vision call. Kept as a thin,
mockable seam so the rest of the pipeline never has to know which model is used.
"""
from dataclasses import dataclass


@dataclass
class ExtractedFields:
    annual_income: float
    category: str  # "General" | "OBC" | "SC" | "ST"
    marks_percentage: float


def extract_fields(income_doc: str, category_doc: str, marksheet: str) -> ExtractedFields:
    income = _call_model(income_doc, field="annual_income")
    category = _call_model(category_doc, field="category")
    marks = _call_model(marksheet, field="marks_percentage")

    return ExtractedFields(
        annual_income=float(income),
        category=str(category),
        marks_percentage=float(marks),
    )


def _call_model(document_url: str, field: str):
    """Placeholder for the real vision-model call (Claude / GPT-4o).

    Replace with something like:

        response = anthropic_client.messages.create(
            model="claude-sonnet-4-6",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "url", "url": document_url}},
                    {"type": "text", "text": f"Extract the {field} from this certificate."},
                ],
            }],
        )
    """
    raise NotImplementedError("Wire up your AI extraction call here.")
