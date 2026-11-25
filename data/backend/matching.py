from rapidfuzz import fuzz
from .schemas import normalize_owner, normalize_survey

def similarity(a: str, b: str) -> float:
    a, b = normalize_owner(a), normalize_owner(b)
    if not a or not b:
        return 0.0
    return max(fuzz.ratio(a, b), fuzz.token_sort_ratio(a, b), fuzz.token_set_ratio(a, b)) / 100.0

def survey_similarity(a: str, b: str) -> float:
    a, b = normalize_survey(a), normalize_survey(b)
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    return fuzz.ratio(a, b) / 100.0

def rank_candidates(extracted: dict, trusted_rows: list[dict], limit=5):
    ranked = []
    for row in trusted_rows:
        owner = similarity(extracted.get("owner_name", ""), row.get("owner_name", ""))
        survey = survey_similarity(extracted.get("survey_number", ""), row.get("survey_number", ""))
        # Survey number is a strong key; owner similarity helps tolerate OCR/spelling variation.
        score = 0.55 * survey + 0.45 * owner
        ranked.append({**row, "owner_similarity": round(owner, 4),
                       "survey_similarity": round(survey, 4),
                       "candidate_score": round(score, 4)})
    return sorted(ranked, key=lambda x: x["candidate_score"], reverse=True)[:limit]
