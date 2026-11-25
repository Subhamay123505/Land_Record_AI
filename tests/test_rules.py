from backend.rules import compare_records
from backend.engine import analyze_record

TRUSTED = {"record_id":"LR-001","owner_name":"Rahul Kumar","survey_number":"125/2",
           "parcel_area":"2.50 acres","record_status":"Active"}

def test_clean_record_consistent():
    uploaded = {"owner_name":"Rahul Kumar","survey_number":"125/2",
                "parcel_area":"2.50 acres","record_status":"Active"}
    assert compare_records(uploaded, TRUSTED)["consistent"]

def test_noisy_owner_and_status_normalized():
    uploaded = {"owner_name":"Rahul Kurnar","survey_number":"125 / 2",
                "parcel_area":"2.50 acres","record_status":"Current"}
    result = compare_records(uploaded, TRUSTED)
    assert result["checks"]["owner_name"]["match"]
    assert result["checks"]["survey_number"]["match"]
    assert result["checks"]["record_status"]["match"]
    assert result["consistent"]

def test_area_conflict_detected():
    uploaded = {"owner_name":"Rahul Kumar","survey_number":"125/2",
                "parcel_area":"3.50 acres","record_status":"Active"}
    result = compare_records(uploaded, TRUSTED)
    assert "PARCEL_AREA_MISMATCH" in result["conflicts"]

def test_missing_field_detected():
    uploaded = {"owner_name":"Rahul Kumar","survey_number":"125/2",
                "parcel_area":"","record_status":"Active"}
    result = compare_records(uploaded, TRUSTED)
    assert "MISSING_PARCEL_AREA" in result["conflicts"]

def test_engine_does_not_auto_accept_conflict():
    uploaded = {"owner_name":"Rahul Kumar","survey_number":"125/2",
                "parcel_area":"3.50 acres","record_status":"Active"}
    result = analyze_record(uploaded, [TRUSTED])
    assert result["decision"] == "REVIEW_REQUIRED"
