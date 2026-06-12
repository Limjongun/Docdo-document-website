from fastapi import APIRouter

router = APIRouter(prefix="/api/id", tags=["Scan ID"])


@router.post("/scan")
async def scan_id_card():
    """[Coming Soon] Scan ID Card and extract structured data using AI OCR."""
    return {"status": "coming_soon", "message": "Fitur Scan ID Card sedang dikembangkan."}
