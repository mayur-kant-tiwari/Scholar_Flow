# Architecture

```
Input → Process → Output, with Notion at the center
```

| Stage          | What happens                                                        |
|----------------|----------------------------------------------------------------------|
| Input          | Student submits a form (Google Form or hosted HTML form) → webhook  |
| AI Extraction  | Reads scanned income / category / marks certificates                |
| Rule Engine    | Plain Python code applies eligibility criteria                      |
| Notion         | Interface + Run Log — where humans see and approve borderline cases |

## Notion schema

### `Cases` database
| Property             | Type       |
|-----------------------|------------|
| Student                | Title      |
| Email                   | Email      |
| Category                | Select (General / OBC / SC / ST) |
| Income (extracted)       | Number     |
| Eligibility               | Select (eligible / not_eligible / borderline) |
| Status                     | Select (Auto-Resolved / Needs Review) |
| Resolved By                  | Rich text  |

### `Run Log` database
| Property     | Type              |
|---------------|-------------------|
| Case           | Relation → Cases  |
| Outcome         | Select            |
| Auto             | Checkbox          |
| Reason            | Rich text         |
| Timestamp          | Date              |

## Design decisions

- **Judgment stays human.** The rule engine only ever produces `eligible`,
  `not_eligible`, or `borderline` — it never auto-approves a borderline case.
- **Notion is the interface, not the whole system.** The FastAPI backend and
  rule engine are real code with tests; Notion is where humans look and act.
- **Every run is logged**, whether it was resolved automatically or by a
  human, so "what's the status?" always has an answer.
