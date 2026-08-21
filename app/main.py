"""ScholarFlow — FastAPI entrypoint.

Input -> Process -> Output, with Notion at the center.
"""
from fastapi import FastAPI

from app.routers import submissions

app = FastAPI(
    title="ScholarFlow",
    description="Automated scholarship eligibility, with Notion as the operations hub.",
    version="0.1.0",
)

app.include_router(submissions.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "scholarflow"}
