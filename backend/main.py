from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from backend.routers import ocr, pdf_tools, converter, image_tools, scan_id

app = FastAPI(
    title="DocPro API",
    description="All-in-One Document & Image Processing API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(ocr.router)
app.include_router(pdf_tools.router)
app.include_router(converter.router)
app.include_router(image_tools.router)
app.include_router(scan_id.router)

# Serve frontend static files
frontend_dir = Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
