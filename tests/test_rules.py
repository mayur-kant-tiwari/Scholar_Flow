from app.services.extraction import ExtractedFields
from app.services.rules import evaluate_eligibility


def test_clearly_eligible():
    fields = ExtractedFields(annual_income=150_000, category="General", marks_percentage=75)
    decision = evaluate_eligibility(fields)
    assert decision.status == "eligible"


def test_clearly_not_eligible_income():
    fields = ExtractedFields(annual_income=500_000, category="General", marks_percentage=75)
    decision = evaluate_eligibility(fields)
    assert decision.status == "not_eligible"


def test_low_marks_not_eligible():
    fields = ExtractedFields(annual_income=100_000, category="General", marks_percentage=40)
    decision = evaluate_eligibility(fields)
    assert decision.status == "not_eligible"


def test_borderline_income():
    fields = ExtractedFields(annual_income=245_000, category="General", marks_percentage=75)
    decision = evaluate_eligibility(fields)
    assert decision.status == "borderline"
