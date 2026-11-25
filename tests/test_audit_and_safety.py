import hashlib
import tempfile
from pathlib import Path
from backend.db import init_db, add_review_event, get_review_events
from backend.engine import analyze_record
from backend.data import TRUSTED_PATH, load_trusted_records

def test_trusted_data_never_modified_by_review(tmp_path):
    """Safety Invariant: Trusted register hash must remain identical after review events."""
    with open(TRUSTED_PATH, "rb") as f:
        hash_before = hashlib.sha256(f.read()).hexdigest()
    
    db_path = tmp_path / "review_test.sqlite3"
    init_db(db_path)
    
    extracted = {"owner_name": "Rahul Kumar", "survey_number": "125/2", "parcel_area": "2.50 acres", "record_status": "Active"}
    corrected = {"owner_name": "Rahul Kumar", "survey_number": "125/2", "parcel_area": "2.50 acres", "record_status": "Active"}
    
    add_review_event("test_file.txt", "APPROVED_BY_REVIEWER", 95.0, "LR-001", extracted, corrected, "Test approval", path=db_path)
    events = get_review_events(path=db_path)
    assert len(events) == 1
    assert events[0]["decision"] == "APPROVED_BY_REVIEWER"
    assert events[0]["trusted_record_id"] == "LR-001"
    
    with open(TRUSTED_PATH, "rb") as f:
        hash_after = hashlib.sha256(f.read()).hexdigest()
    
    assert hash_before == hash_after

def test_empty_trusted_records_handled():
    extracted = {"owner_name": "Rahul Kumar", "survey_number": "125/2"}
    result = analyze_record(extracted, [])
    assert result["decision"] == "REVIEW_REQUIRED"
    assert result["candidate"] is None

def test_no_reliable_match():
    trusted = load_trusted_records()
    # A completely unrelated survey and owner
    extracted = {"owner_name": "Xavier Nonexistent", "survey_number": "99999/ZZZ", "parcel_area": "1 acre", "record_status": "Active"}
    result = analyze_record(extracted, trusted)
    assert result["decision"] == "NO_RELIABLE_MATCH"
