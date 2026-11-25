from dataclasses import dataclass, asdict
from typing import Optional
import re
import unicodedata

@dataclass
class LandRecord:
    owner_name: str = ""
    survey_number: str = ""
    parcel_area: str = ""
    record_status: str = ""
    source_name: str = ""

    def to_dict(self):
        return asdict(self)

def normalize_text(value: Optional[str]) -> str:
    if value is None:
        return ""
    value = unicodedata.normalize("NFKC", str(value)).strip().lower()
    value = re.sub(r"\s+", " ", value)
    return value

def normalize_owner(value: str) -> str:
    value = normalize_text(value)
    value = re.sub(r"\b(s/o|d/o|w/o|shri|smt|mr|mrs)\b", " ", value)
    value = re.sub(r"[^a-z0-9 ]", " ", value)
    value = re.sub(r"\b(s\s*o|d\s*o|w\s*o)\b", " ", value)
    return re.sub(r"\s+", " ", value).strip()

def normalize_survey(value: str) -> str:
    value = normalize_text(value).replace(" ", "")
    value = value.replace("\\", "/")
    value = re.sub(r"[^a-z0-9/.-]", "", value)
    return value

def parse_area(value: str):
    """Return (numeric value, normalized unit); unknown formats return (None, '')."""
    value = normalize_text(value).replace(",", "")
    match = re.search(r"(-?\d+(?:\.\d+)?)\s*(acres?|acre|ha|hectares?|sqm|sq\.?\s*m|m2|bigha)?", value)
    if not match:
        return None, ""
    number = float(match.group(1))
    unit = (match.group(2) or "").replace(" ", "")
    if unit in ("acre", "acres"):
        unit = "acre"
    elif unit in ("ha", "hectare", "hectares"):
        unit = "hectare"
    elif unit in ("sqm", "sq.m", "m2"):
        unit = "sqm"
    elif unit == "bigha":
        unit = "bigha"
    return number, unit

def normalize_status(value: str) -> str:
    v = normalize_text(value)
    aliases = {"current": "active", "valid": "active", "live": "active",
               "inactive": "inactive", "closed": "closed", "cancelled": "cancelled",
               "canceled": "cancelled", "active": "active", "pending": "pending"}
    return aliases.get(v, v)
