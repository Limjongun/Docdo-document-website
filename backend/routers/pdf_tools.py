import io
import zipfile
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import Response, JSONResponse
from backend.services import pdf_service

router = APIRouter(prefix="/api/pdf", tags=["PDF"])


@router.post("/to-word")
async def pdf_to_word(file: UploadFile = File(...)):
    """Convert a PDF to .docx."""
    pdf_bytes = await file.read()
    docx_bytes = pdf_service.pdf_to_word(pdf_bytes)
    return Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="converted.docx"'},
    )


@router.post("/watermark")
async def add_watermark(
    file: UploadFile = File(...),
    text: str = Form("CONFIDENTIAL"),
):
    """Add a watermark to a PDF."""
    pdf_bytes = await file.read()
    result = pdf_service.add_watermark(pdf_bytes, text)
    return Response(
        content=result,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="watermarked.pdf"'},
    )


@router.post("/set-password")
async def set_password(
    file: UploadFile = File(...),
    password: str = Form(...),
):
    """Encrypt a PDF with a password."""
    pdf_bytes = await file.read()
    result = pdf_service.set_pdf_password(pdf_bytes, password)
    return Response(
        content=result,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="protected.pdf"'},
    )


@router.post("/remove-password")
async def remove_password(
    file: UploadFile = File(...),
    password: str = Form(...),
):
    """Remove password from a PDF."""
    pdf_bytes = await file.read()
    result = pdf_service.remove_pdf_password(pdf_bytes, password)
    return Response(
        content=result,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="unlocked.pdf"'},
    )


@router.post("/rotate")
async def rotate_pdf(
    file: UploadFile = File(...),
    degrees: int = Form(90),
):
    """Rotate all pages in a PDF."""
    pdf_bytes = await file.read()
    result = pdf_service.rotate_pdf(pdf_bytes, degrees)
    return Response(
        content=result,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="rotated.pdf"'},
    )


@router.post("/to-images")
async def pdf_to_images(
    file: UploadFile = File(...),
    fmt: str = Form("png"),
):
    """Convert PDF pages to images, returned as a ZIP archive."""
    pdf_bytes = await file.read()
    images = pdf_service.pdf_to_images(pdf_bytes, fmt)

    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w") as zf:
        for i, img_bytes in enumerate(images, start=1):
            zf.writestr(f"page_{i}.{fmt}", img_bytes)

    return Response(
        content=zip_buf.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="pdf_images.zip"'},
    )


@router.post("/embed-signature")
async def embed_signature(
    pdf_file: UploadFile = File(...),
    sig_file: UploadFile = File(...),
    page_num: int = Form(0),
):
    """Embed a signature image onto a PDF page."""
    pdf_bytes = await pdf_file.read()
    sig_bytes = await sig_file.read()
    result = pdf_service.embed_signature(pdf_bytes, sig_bytes, page_num)
    return Response(
        content=result,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="signed.pdf"'},
    )
