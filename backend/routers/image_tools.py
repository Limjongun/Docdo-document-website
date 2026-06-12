from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import Response
from backend.services import image_service

router = APIRouter(prefix="/api/image", tags=["Image"])


@router.post("/sharpen")
async def sharpen_document(file: UploadFile = File(...)):
    """Sharpen and denoise a document image."""
    image_bytes = await file.read()
    result = image_service.sharpen_image(image_bytes)
    return Response(content=result, media_type="image/png")


@router.post("/signature")
async def extract_signature(file: UploadFile = File(...)):
    """Extract and isolate a signature from an image."""
    image_bytes = await file.read()
    result = image_service.extract_signature(image_bytes)
    return Response(content=result, media_type="image/png")
