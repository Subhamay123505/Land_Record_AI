from .matching import rank_candidates
from .rules import compare_records, confidence_score

def analyze_record(extracted: dict, trusted_rows: list[dict]):
    if not trusted_rows:
        return {"decision": "REVIEW_REQUIRED", "reason": "Trusted reference register is empty",
                "candidate": None, "comparison": None, "confidence": 0.0}
    candidates = rank_candidates(extracted, trusted_rows)
    best = candidates[0]
    comparison = compare_records(extracted, best)
    confidence = confidence_score(extracted, best, comparison)
    if best["survey_similarity"] < 0.70:
        decision = "NO_RELIABLE_MATCH"
    elif comparison["consistent"] and confidence >= 85:
        decision = "CONSISTENT_CANDIDATE"
    else:
        decision = "REVIEW_REQUIRED"
    return {"decision": decision, "candidate": best, "candidates": candidates,
            "comparison": comparison, "confidence": confidence,
            "explanation": build_explanation(best, comparison, confidence)}

def build_explanation(candidate, comparison, confidence):
    matched = [k for k,v in comparison["checks"].items() if v.get("match")]
    failed = [k for k,v in comparison["checks"].items() if not v.get("match")]
    return {
        "matched_fields": matched,
        "failed_fields": failed,
        "conflicts": comparison["conflicts"],
        "summary": ("All checked fields are consistent with the top candidate."
                    if comparison["consistent"] else
                    "One or more consistency rules failed. Human review is required."),
        "confidence_note": f"{confidence:.1f}/100 heuristic confidence; not a probability."
    }
