"""Email notifications — Mailtrap (demo-safe sandbox) or Resend for production."""
import os

import httpx

PROVIDER = os.getenv("EMAIL_PROVIDER", "mailtrap")  # "mailtrap" | "resend"
API_KEY = os.getenv("EMAIL_API_KEY", "")
FROM_ADDRESS = os.getenv("EMAIL_FROM", "noreply@scholarflow.example")


def send_decision_email(to: str, student_name: str, decision) -> None:
    subject, body = _compose(student_name, decision)

    if PROVIDER == "mailtrap":
        _send_via_mailtrap(to, subject, body)
    else:
        _send_via_resend(to, subject, body)


def _compose(student_name: str, decision) -> tuple[str, str]:
    if decision.status == "eligible":
        subject = "Your scholarship application has been approved"
        body = f"Hi {student_name},\n\nYour application has been approved. {decision.reason}\n\n— ScholarFlow"
    else:
        subject = "Update on your scholarship application"
        body = f"Hi {student_name},\n\nYour application was not approved. {decision.reason}\n\n— ScholarFlow"
    return subject, body


def _send_via_mailtrap(to: str, subject: str, body: str) -> None:
    httpx.post(
        "https://send.api.mailtrap.io/api/send",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "from": {"email": FROM_ADDRESS},
            "to": [{"email": to}],
            "subject": subject,
            "text": body,
        },
    )


def _send_via_resend(to: str, subject: str, body: str) -> None:
    httpx.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"from": FROM_ADDRESS, "to": [to], "subject": subject, "text": body},
    )
