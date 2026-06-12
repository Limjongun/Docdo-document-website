from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import Response, JSONResponse
from backend.services import ocr_service

router = APIRouter(prefix="/api/ocr", tags=["OCR"])


@router.post("/scan-document")
async def scan_document(
    file: UploadFile = File(...),
    lang: str = Form("ind+eng"),
):
    """Extract all text from a document image via Tesseract OCR."""
    image_bytes = await file.read()
    text = ocr_service.extract_text_from_image(image_bytes, lang=lang)
    return JSONResponse({"text": text})
