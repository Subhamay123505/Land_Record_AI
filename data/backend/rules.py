from .schemas import normalize_owner, normalize_survey, normalize_status, parse_area
from .matching import similarity, survey_similarity

def compare_records(extracted: dict, trusted: dict, area_tolerance=0.01):
    conflicts, evidence = [], []
    checks = {}
    fields = ("owner_name", "survey_number", "parcel_area", "record_status")
    for field in fields:
        if not str(extracted.get(field, "")).strip():
            conflicts.append("MISSING_" + field.upper())
            checks[field] = {"match": False, "reason": "Missing in uploaded record"}
            continue
        if not str(trusted.get(field, "")).strip():
            conflicts.append("TRUSTED_FIELD_MISSING_" + field.upper())
            checks[field] = {"match": False, "reason": "Missing in trusted reference"}
            continue

        if field == "owner_name":
            score = similarity(extracted[field], trusted[field])
            ok = score >= 0.85
            reason = f"Normalized name similarity = {score:.2f}; threshold = 0.85 (allows limited OCR spelling noise)"
        elif field == "survey_number":
            score = survey_similarity(extracted[field], trusted[field])
            ok = score == 1.0
            reason = f"Normalized survey similarity = {score:.2f}; exact normalized match required"
        elif field == "parcel_area":
            a, ua = parse_area(extracted[field])
            b, ub = parse_area(trusted[field])
            ok = a is not None and b is not None and ua == ub and abs(a-b) <= area_tolerance
            reason = (f"Uploaded={a} {ua or '(unit unknown)'}, trusted={b} {ub or '(unit unknown)'}, "
                      f"absolute tolerance={area_tolerance}; units must match")
            score = 1.0 if ok else 0.0
        else:
            a, b = normalize_status(extracted[field]), normalize_status(trusted[field])
            ok = a == b
            reason = f"Normalized status: uploaded='{a}', trusted='{b}'"
            score = 1.0 if ok else 0.0
        checks[field] = {"match": bool(ok), "score": round(float(score), 4), "reason": reason}
        if not ok:
            conflicts.append(field.upper() + "_MISMATCH")
        else:
            evidence.append(field + " matched")

    return {"consistent": len(conflicts) == 0, "conflicts": conflicts,
            "checks": checks, "evidence": evidence}

def confidence_score(extracted: dict, candidate: dict, comparison: dict) -> float:
    """Transparent heuristic score (0..100), not a calibrated probability."""
    key_score = 0.55 * candidate.get("survey_similarity", 0) + 0.45 * candidate.get("owner_similarity", 0)
    populated = sum(bool(str(extracted.get(k, "")).strip()) for k in
                     ("owner_name", "survey_number", "parcel_area", "record_status")) / 4
    rule_ratio = sum(1 for v in comparison["checks"].values() if v.get("match")) / 4
    score = 100 * (0.45 * key_score + 0.20 * populated + 0.35 * rule_ratio)
    return round(max(0.0, min(100.0, score)), 1)
