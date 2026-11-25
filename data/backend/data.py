import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRUSTED_PATH = ROOT / "data" / "trusted_records.csv"

def load_trusted_records(path=TRUSTED_PATH):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def load_cases(path=None):
    path = path or ROOT / "data" / "evaluation_cases.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)
