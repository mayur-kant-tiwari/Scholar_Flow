# ScholarFlow

**Automated scholarship & fee-concession eligibility, with Notion as the operations hub.**

ScholarFlow replaces the manual loop of *scan → forward → retype → decide* with a
pipeline that reads a student's documents, applies your college's actual eligibility
rules in code, and only asks a human to step in when a case is genuinely borderline.
Every run — automatic or human-approved — is logged.

```
Student submits form
        │
        ▼
  AI Extraction  ──────►  pulls income, category, marks from scanned certificates
        │
        ▼
  Rule Engine     ──────►  plain Python logic decides eligibility
        │
        ├── Clear case  ──────►  auto-resolved + student notified by email
        │
        └── Borderline  ──────►  pauses in Notion for human approval
                                          │
                                          ▼
                                  Run Log (Notion) — full audit trail
```

## Why

Every college runs a scholarship / fee-concession process where students submit
scanned income certificates, category certificates, and marksheets, and an admin
office member manually retypes each one into a spreadsheet to check eligibility.
It's slow, error-prone, and nobody can answer "what's the status?" ScholarFlow
keeps a human in the loop for judgment calls, but removes the retyping entirely.

## Tech stack

| Layer               | Technology                                            |
|---------------------|--------------------------------------------------------|
| Frontend / trigger   | Google Form or hosted HTML form → webhook              |
| Backend              | Python + FastAPI, deployed on Render / Railway          |
| AI extraction        | Claude / GPT-4o — reads scanned certificates, extracts fields |
| Rule engine           | Plain Python logic applying eligibility criteria        |
| Interface & DB        | Notion API — `Cases` database + `Run Log` database      |
| Notifications          | Mailtrap (demo-safe) or Resend for production email     |

## Project structure

```
scholarflow/
├── app/
│   ├── main.py                 # FastAPI app, webhook entrypoint
│   ├── routers/
│   │   └── submissions.py      # POST /submissions — intake from the form
│   ├── services/
│   │   ├── extraction.py       # AI document extraction (Claude/GPT-4o)
│   │   ├── rules.py            # Deterministic eligibility rule engine
│   │   ├── notion.py           # Notion API: Cases + Run Log
│   │   └── notifications.py    # Mailtrap / Resend email sending
│   └── config.py                # Environment / settings
├── docs/
│   └── architecture.md
├── tests/
├── .env.example
├── requirements.txt
└── .github/workflows/ci.yml
```

## Getting started

```bash
git clone https://github.com/<your-org>/scholarflow.git
cd scholarflow
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in NOTION_API_KEY, ANTHROPIC_API_KEY, MAILTRAP creds
uvicorn app.main:app --reload
```

Point your Google Form / hosted form webhook at `POST /submissions`, and create
two Notion databases — `Cases` and `Run Log` — matching the schema in
[`docs/architecture.md`](docs/architecture.md).

## Status

Hackathon prototype. Runs entirely on free tiers (Notion free plan,
Render/Railway free hosting, Mailtrap sandbox) — near-zero cost to demo or adopt.

## License

MIT
