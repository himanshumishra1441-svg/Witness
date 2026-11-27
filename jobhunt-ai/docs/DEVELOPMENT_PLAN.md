# JobHunt AI — Development Plan v1.0 (Frozen)

## Goal
Discover vacancies, rank fit transparently, prepare application material, and track progress. Human approval is mandatory for external applications/messages.

## Phases
0. Requirements and architecture freeze.
1. Foundation: FastAPI, settings, PostgreSQL connectivity, SQLAlchemy, Alembic, health endpoint, tests.
2. Candidate intelligence: validated profile and read API.
3. Discovery: public Greenhouse and Lever job feeds, normalized records, deduplication and provenance.
4. Intelligence: required/preferred skill extraction and explainable scoring.
5. Resume intelligence: backend, applied AI, technical solutions CV tracks; never invent candidate facts.
6. Application preparation: drafts and human approval.
7. Recruiter intelligence: permitted public contact information, draft outreach and duplicate prevention.
8. Tracking: status lifecycle, activity history, follow-up reminders.
9. Streamlit dashboard and three daily discovery windows; prioritize jobs posted in last 7 days.
10. Testing, security review, deployment and documentation.

## Frozen scoring
Skills 30; experience 20; project relevance 20; salary 15; location/availability 10; freshness 5. Shortlist >=65; high priority >=80. Unknown salary remains unknown.

## Stack
Python 3.12, FastAPI, Streamlit, PostgreSQL, SQLAlchemy, Alembic, Pydantic, httpx, pytest. LLMs/LangGraph only where useful; initial scoring deterministic.

## Acceptance
No duplicate jobs; every score explains its component results; source and apply URL retained; no message/application without approval; secrets only in environment; missing facts are never fabricated.
