import sqlite3, json
from pathlib import Path
DB_PATH = Path(__file__).resolve().parents[1] / "review_audit.sqlite3"

def init_db(path=DB_PATH):
    with sqlite3.connect(path) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS review_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            source_name TEXT, decision TEXT NOT NULL, confidence REAL,
            trusted_record_id TEXT, extracted_json TEXT, corrected_json TEXT,
            reviewer_note TEXT
        )""")
        con.commit()

def add_review_event(source_name, decision, confidence, trusted_record_id,
                     extracted, corrected=None, reviewer_note="", path=DB_PATH):
    with sqlite3.connect(path) as con:
        con.execute("""INSERT INTO review_events
        (source_name, decision, confidence, trusted_record_id, extracted_json, corrected_json, reviewer_note)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (source_name, decision, confidence, trusted_record_id,
         json.dumps(extracted, ensure_ascii=False),
         json.dumps(corrected, ensure_ascii=False) if corrected else None, reviewer_note))
        con.commit()

def get_review_events(path=DB_PATH):
    with sqlite3.connect(path) as con:
        con.row_factory = sqlite3.Row
        return [dict(r) for r in con.execute("SELECT * FROM review_events ORDER BY id DESC").fetchall()]
