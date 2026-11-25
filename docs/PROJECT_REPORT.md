# SIH 2026 Project Report — LandRecordAI

## 1. Abstract
LandRecordAI is a human-in-the-loop decision-support prototype for extracting key entities from land-record documents and checking them against a trusted reference register. It combines structured knowledge representation, semantic/fuzzy entity matching, deterministic production rules, transparent confidence scoring, and an auditable review workflow. The system highlights evidence and exceptions; it does not autonomously change authoritative records.

## 2. Problem statement
Land records may be scanned, noisy, incomplete, inconsistently formatted, or contain conflicting values. Manual comparison can be slow and difficult to reproduce. The prototype aims to standardize extraction and comparison while keeping the final decision with an authorized official.

## 3. Objectives
1. Define a structured schema for owner, survey number, parcel area, unit, and record status.
2. Prepare reproducible clean, noisy, missing-field, and conflicting cases.
3. Extract fields from supported documents.
4. Rank candidate trusted records using explainable similarity signals.
5. Apply production rules to classify inconsistencies.
6. Present evidence, rule outcomes, and a heuristic confidence score.
7. Record human decisions without mutating trusted records.

## 4. Scope and assumptions
- Prototype uses synthetic data only.
- Trusted records are supplied as a read-only CSV.
- Survey number is treated as a strong identifier; exact normalized equality is required by the current rule.
- Owner-name matching tolerates minor spelling/format differences.
- Parcel area comparison requires equal normalized units; no jurisdiction-specific unit conversion is assumed.
- The confidence score is a transparent heuristic, not a probability.
- OCR depends on scan quality and installed language packs.
- No live government registry, cadastral map, ownership transfer, or legal title verification is implemented.

## 5. Structured schema
`LandRecord`: `owner_name` (string), `survey_number` (string), `parcel_area` (string with numeric value and unit), `record_status` (controlled string where possible), `source_name` (string). Trusted rows additionally include `record_id`.

## 6. System architecture
Upload → text/OCR extraction → normalization → candidate ranking → production-rule comparison → conflict classification → confidence/evidence → human review → append-only audit event.

## 7. Matching and reasoning
Candidate rank = 0.55 × survey similarity + 0.45 × owner-name similarity. The best candidate is checked field-by-field. Rules classify missing uploaded values, missing trusted values, owner mismatch, survey mismatch, parcel-area mismatch, and status mismatch. A candidate is labelled consistent only if all configured rules pass and the heuristic confidence is at least 85/100. Otherwise it is routed to review. No candidate with weak survey similarity is treated as a reliable match.

## 8. Confidence
The current score combines key-field similarity (45%), field completeness (20%), and consistency-rule pass ratio (35%). It is intended to prioritize review, not estimate a statistically calibrated chance of correctness. Thresholds require validation on a representative, authorized, human-labelled dataset.

## 9. Data quality checks
- Required fields checked for missing/blank values.
- Survey identifiers normalized for whitespace and separators.
- Owner names normalized for case, punctuation, and common honorifics.
- Area values parsed into number and unit; units must match.
- Status aliases normalized (e.g., Current/Valid → Active).
- Duplicate candidate detection and cross-record uniqueness checks are recommended for the next iteration.
- Source provenance and reviewer notes are retained in the audit event.

## 10. Acceptance criteria (targets)
- ≥95% survey-number extraction accuracy on a representative labelled test set.
- ≥95% owner-name match precision at the selected threshold.
- ≥0.90 macro F1 for conflict classification on a balanced labelled benchmark.
- 100% of unresolved/low-confidence records sent to human review.
- 100% of review actions captured in audit history.
- 0 silent updates to trusted reference records.
- Reproducible test and evaluation commands documented.

These are targets, not measured results. Populate the results table only after running evaluation on an appropriately sized labelled dataset.

## 11. Test strategy
Unit tests cover normalized clean/noisy cases, area conflicts, missing fields, and human-review routing. The bundled synthetic benchmark is a smoke test and not a representative accuracy study. Add stratified test sets by document type, scan quality, language, and conflict class before deployment.

## 12. Privacy, security, and governance
Use synthetic data in this demo. Real deployments require legal authorization, data minimization, encryption in transit/at rest, role-based access, authenticated reviewer identities, retention schedules, backups, monitoring, and security review. A correction must be recorded as a proposal with provenance; authoritative records must be updated only through approved official workflows.

## 13. Limitations and future work
Add multilingual OCR, layout-aware extraction, calibrated embedding-based matching, jurisdiction-specific unit conversion, duplicate detection, role-based authentication, secure API integration, and larger adjudicated datasets. Validate against state-specific land-record terminology and legal procedures.

## 14. Reproducibility
Install `requirements.txt`, run `streamlit run app.py`, then execute `python scripts/run_evaluation.py` and `pytest -q`. Dataset and acceptance assumptions are version-controlled with the code.
