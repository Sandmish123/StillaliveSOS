from fastapi import APIRouter, HTTPException
from pathlib import Path

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
LEGAL_DIR = BASE_DIR / "legal_content"

def read_file(filename: str):
    file_path = LEGAL_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Document not found")
    return file_path.read_text(encoding="utf-8")

@router.get("/terms")
def get_terms():
    return {
        "title": "Terms and Conditions",
        "effectiveDate": "March 1, 2025",
        "content": read_file("terms.md")
    }

@router.get("/privacy")
def get_privacy():
    return {
        "title": "Privacy Policy",
        "effectiveDate": "March 1, 2025",
        "content": read_file("privacy.md")
    }

@router.get("/data-retention")
def get_data_retention():
    return {
        "title": "Data Retention Policy",
        "effectiveDate": "March 1, 2025",
        "content": read_file("data_retention.md")
    }

@router.get("/emergency-disclosure")
def get_emergency_disclosure():
    return {
        "title": "Emergency Contact Disclosure Notice",
        "effectiveDate": "March 1, 2025",
        "content": read_file("emergency.md")
    }

@router.get("/cookies")
def get_cookies():
    return {
        "title": "Cookie & Tracking Notice",
        "effectiveDate": "March 1, 2025",
        "content": read_file("cookies.md")
    }