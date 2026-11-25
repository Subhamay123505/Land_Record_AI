# Antigravity Agent Handoff — LandRecordAI

You are the implementation agent for this SIH 2026 prototype. Work inside this repository only.

## Mission
Deliver a reliable, explainable human-in-the-loop prototype for individual land-record extraction and consistency reasoning. Preserve the core safety invariant: **never silently modify trusted reference records**.

## Before changing code
1. Read `README.md`, `docs/PROJECT_REPORT.md`, and `docs/ACCEPTANCE_CRITERIA.md`.
2. Inspect the full repository and run `pytest -q`.
3. Run `python scripts/run_evaluation.py`.
4. Record baseline results before making changes.

## Engineering requirements
- Keep extraction, normalization, matching, rules, confidence, database/audit, UI, and evaluation as separate modules.
- Keep synthetic sample data synthetic. Do not introduce real personal land data.
- Do not claim that heuristic confidence is a probability.
- Do not claim target metrics have been achieved unless a reproducible labelled evaluation proves it.
- Any new rule must have unit tests and a documented explanation.
- Preserve original source text and provenance where feasible.
- Keep reviewer approval/rejection/correction as audit events; never overwrite the trusted CSV from the UI.
- Handle missing values and OCR failures explicitly. Do not silently convert missing values into valid data.
- Prefer deterministic behaviour and fixed test fixtures.
- Keep dependencies minimal and pin compatible version ranges.

## Suggested next improvements
1. Add a dedicated conflict taxonomy with per-class precision/recall/F1.
2. Add duplicate trusted-record detection and candidate ambiguity warnings.
3. Add area-unit conversion only after documenting jurisdiction-specific conversion rules.
4. Add language selection and OCR language-pack checks.
5. Add authentication and role-based access only for a secured deployment; do not invent reviewer identities.
6. Add audit integrity checks and tests proving the trusted register is unchanged after all review actions.
7. Add upload size/type validation and robust error messages.
8. Add a sample PDF fixture generated from synthetic data.
9. Add accessibility and responsive layout checks to the Streamlit UI.

## Completion protocol
For every change:
- Explain the problem addressed.
- Make the smallest coherent change.
- Add/update tests.
- Run `pytest -q` and `python scripts/run_evaluation.py`.
- Update docs and screenshots if the user-facing flow changes.
- Summarize changed files, test results, limitations, and any manual steps still required.

## Local run commands (Windows PowerShell)
```powershell
py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```
