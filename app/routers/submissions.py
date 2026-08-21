"""Intake endpoint — receives a form webhook, runs the full pipeline."""
from fastapi import APIRouter
from pydantic import BaseModel

from app.services import extraction, notifications, notion, rules

router = APIRouter()


class SubmissionPayload(BaseModel):
    student_name: str
    student_email: str
    income_certificate_url: str
    category_certificate_url: str
    marksheet_url: str


@router.post("/submissions")
def handle_submission(payload: SubmissionPayload):
    """
    Runs the ScholarFlow pipeline for one student submission:
      1. AI extraction of income / category / marks from scanned docs
      2. Deterministic eligibility rule check
      3. Clear cases: auto-resolve + notify. Borderline: pause in Notion for approval.
      4. Every outcome is written to the Run Log.
    """
    extracted = extraction.extract_fields(
        income_doc=payload.income_certificate_url,
        category_doc=payload.category_certificate_url,
        marksheet=payload.marksheet_url,
    )

    decision = rules.evaluate_eligibility(extracted)

    case_id = notion.create_case(
        student_name=payload.student_name,
        student_email=payload.student_email,
        extracted=extracted,
        decision=decision,
    )

    if decision.status == "eligible" or decision.status == "not_eligible":
        notifications.send_decision_email(
            to=payload.student_email,
            student_name=payload.student_name,
            decision=decision,
        )
        notion.close_case(case_id, resolved_by="system")
    else:
        # Borderline — leaves the case open in Notion for a human reviewer.
        pass

    notion.log_run(case_id=case_id, decision=decision, auto=decision.status != "borderline")

    return {"case_id": case_id, "status": decision.status}
