from fastapi import APIRouter, UploadFile, File
from fastapi.responses import Response
from backend.services import converter_service

router = APIRouter(prefix="/api/convert", tags=["Converter"])


@router.post("/images-to-pdf")
async def images_to_pdf(files: list[UploadFile] = File(...)):
    """Merge multiple images into one PDF."""
    image_bytes_list = [await f.read() for f in files]
    result = converter_service.images_to_pdf(image_bytes_list)
    return Response(
        content=result,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="merged.pdf"'},
    )


@router.post("/pdf-to-excel")
async def pdf_to_excel(file: UploadFile = File(...)):
    """Extract tables from PDF to Excel (.xlsx)."""
    pdf_bytes = await file.read()
    result = converter_service.pdf_to_excel(pdf_bytes)
    return Response(
        content=result,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="extracted.xlsx"'},
    )


@router.post("/excel-to-pdf")
async def excel_to_pdf(file: UploadFile = File(...)):
    """Convert Excel spreadsheet to PDF."""
    excel_bytes = await file.read()
    result = converter_service.excel_to_pdf(excel_bytes)
    return Response(
        content=result,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="converted.pdf"'},
    )
