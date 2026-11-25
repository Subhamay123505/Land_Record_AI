# Acceptance Criteria and Reproducible Evaluation

| ID | Metric | Target | Measurement |
|---|---|---:|---|
| AC-01 | Survey number extraction exact accuracy | ≥95% | Correct normalized survey fields / labelled fields |
| AC-02 | Owner matching precision | ≥95% | TP / (TP + FP) |
| AC-03 | Conflict classification macro F1 | ≥0.90 | Macro average across conflict classes |
| AC-04 | Review routing for unresolved cases | 100% | Unresolved cases routed to review / unresolved cases |
| AC-05 | Audit completeness | 100% | Review actions with audit event / all review actions |
| AC-06 | Trusted data mutation | 0 silent changes | Verify trusted CSV hash before/after review |
| AC-07 | Reproducibility | All tests pass | `pytest -q` and evaluation script |

Targets must be tested on a representative, legally authorized, human-labelled dataset. The bundled data is synthetic and only verifies code paths.
