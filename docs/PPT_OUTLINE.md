# SIH 2026 Presentation — Slide Outline

1. **Title:** LandRecordAI — Individual Land Record Extraction and Consistency Reasoning System.
2. **Problem:** Noisy, incomplete, inconsistent land records make manual comparison difficult.
3. **Proposed solution:** Extract → match → reason → explain → human review.
4. **System architecture:** Upload/OCR, schema, semantic matching, production rules, confidence, audit.
5. **Knowledge representation:** Owner, survey number, parcel area/unit, status, provenance.
6. **Semantic matching:** Owner-name similarity + survey-number similarity; candidate ranking.
7. **Production rules:** Missing values, owner/survey/area/status conflicts, unit validation.
8. **Explainable review:** Candidate, evidence, failed rules, heuristic confidence, approve/reject/correct.
9. **Evaluation plan:** Clean/noisy/conflicting dataset, precision, recall, macro F1, latency, audit completeness.
10. **Demo and impact:** Show clean and conflicting cases; emphasize human oversight and no silent overwrite.
11. **Limitations and roadmap:** Synthetic data, OCR language support, official integration, security.
12. **Conclusion:** Reproducible, explainable decision support for authorized officials.

Do not report synthetic smoke-test values as real-world accuracy. Replace evaluation placeholders with measured results from a labelled benchmark.
