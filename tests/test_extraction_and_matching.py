from backend.extraction import parse_record_text, extract_from_upload
from backend.schemas import normalize_owner, normalize_survey, parse_area, normalize_status
from backend.matching import similarity, survey_similarity, rank_candidates

def test_parse_record_text_multiline_and_escaped():
    raw_text = "Owner Name: Rahul Kumar\nSurvey Number: 125/2\nParcel Area: 2.50 acres\nRecord Status: Active"
    rec = parse_record_text(raw_text)
    assert rec.owner_name == "Rahul Kumar"
    assert rec.survey_number == "125/2"
    assert rec.parcel_area == "2.50 acres"
    assert rec.record_status == "Active"

    escaped_text = "Owner Name: Priya Das\\nSurvey Number: 19/7\\nParcel Area: 0.80 hectare\\nRecord Status: Active"
    rec2 = parse_record_text(escaped_text)
    assert rec2.owner_name == "Priya Das"
    assert rec2.survey_number == "19/7"
    assert rec2.parcel_area == "0.80 hectare"
    assert rec2.record_status == "Active"

def test_normalization():
    assert normalize_owner("Shri Rahul Kumar s/o Ramesh") == "rahul kumar ramesh"
    assert normalize_survey(" 125 / 2 ") == "125/2"
    assert normalize_survey("125\\2") == "125/2"
    assert normalize_status("Current") == "active"
    assert normalize_status("Live") == "active"
    assert normalize_status("Canceled") == "cancelled"

    val, unit = parse_area("2.50 acres")
    assert val == 2.50 and unit == "acre"

    val_ha, unit_ha = parse_area("0.80 ha")
    assert val_ha == 0.80 and unit_ha == "hectare"

    val_sqm, unit_sqm = parse_area("1,200 sq.m")
    assert val_sqm == 1200.0 and unit_sqm == "sqm"

def test_matching_and_ranking():
    sim = similarity("Rahul Kumar", "Rahul Kurnar")
    assert sim >= 0.85

    survey_exact = survey_similarity("125/2", "125 / 2")
    assert survey_exact == 1.0

    trusted_mock = [
        {"record_id": "1", "owner_name": "Anita Sharma", "survey_number": "88/1"},
        {"record_id": "2", "owner_name": "Rahul Kumar", "survey_number": "125/2"},
    ]
    extracted = {"owner_name": "Rahul Kumar", "survey_number": "125/2"}
    ranked = rank_candidates(extracted, trusted_mock)
    assert ranked[0]["record_id"] == "2"
    assert ranked[0]["candidate_score"] > 0.95
