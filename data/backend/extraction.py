import csv, io, re
from pathlib import Path
from .schemas import LandRecord

FIELD_PATTERNS = {
    "owner_name": [r"(?:owner(?:'s)? name|owner|khatedar)\s*[:\-]\s*(.+)",
                   r"(?:name of landholder)\s*[:\-]\s*(.+)"],
    "survey_number": [r"(?:survey(?:\s+no\.?|\s+number)?|khasra(?:\s+no\.?)?|plot(?:\s+no\.?)?)\s*[:\-]\s*([A-Za-z0-9./-]+)"],
    "parcel_area": [r"(?:parcel\s+area|area|extent)\s*[:\-]\s*([0-9.,]+\s*(?:acres?|ha|hectares?|sqm|sq\.?\s*m|m2|bigha)?)"],
    "record_status": [r"(?:record\s+status|status)\s*[:\-]\s*([A-Za-z ]+)"],
}

def parse_record_text(text: str, source_name: str = "") -> LandRecord:
    result = LandRecord(source_name=source_name)
    # Normalize newline variations and escaped newlines
    normalized_text = text.replace("\r\n", "\n").replace("\\r\\n", "\n").replace("\\n", "\n")
    for field, patterns in FIELD_PATTERNS.items():
        for pattern in patterns:
            match = re.search(pattern, normalized_text, flags=re.IGNORECASE)
            if match:
                setattr(result, field, match.group(1).strip().splitlines()[0][:160])
                break
    return result

def extract_from_upload(filename: str, raw: bytes) -> tuple[str, LandRecord]:
    suffix = Path(filename).suffix.lower()
    text = ""
    if suffix in (".txt", ".md", ".csv"):
        text = raw.decode("utf-8", errors="replace")
        if suffix == ".csv":
            try:
                rows = list(csv.DictReader(io.StringIO(text)))
                if rows:
                    row = rows[0]
                    record = LandRecord(
                        owner_name=row.get("owner_name", row.get("owner", "")),
                        survey_number=row.get("survey_number", row.get("survey_no", "")),
                        parcel_area=row.get("parcel_area", row.get("area", "")),
                        record_status=row.get("record_status", row.get("status", "")),
                        source_name=filename)
                    return text, record
            except Exception:
                pass
    elif suffix == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(raw))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:
            text = f"PDF text extraction failed: {exc}"
    elif suffix == ".docx":
        try:
            import docx
            doc = docx.Document(io.BytesIO(raw))
            text = "\n".join(p.text for p in doc.paragraphs if p.text)
        except Exception as exc:
            text = f"DOCX text extraction failed: {exc}"
    elif suffix in (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"):
        try:
            from PIL import Image
            import pytesseract
            text = pytesseract.image_to_string(Image.open(io.BytesIO(raw)))
        except Exception as exc:
            text = f"OCR unavailable or failed: {exc}. Install Tesseract OCR and pytesseract."
    else:
        text = raw.decode("utf-8", errors="replace")
    return text, parse_record_text(text, filename)

def extract_from_text(text: str, source_name="manual-entry") -> LandRecord:
    return parse_record_text(text, source_name)
