from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from pathlib import Path
from PyPDF2 import PdfReader
import logging

UPLOAD_DIR = Path("uploads/menus")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter()

@router.get("/health")
def menu_health():
    return {"status": "ok", "message": "Menu router is alive"}

@router.post("/test-upload")
async def test_upload(file: UploadFile = File(...)):
    # Just echo back the filename and size for debugging
    try:
        content = await file.read()
        return {"filename": file.filename, "size": len(content)}
    except Exception as e:
        logging.exception("Test upload failed")
        raise HTTPException(status_code=500, detail=f"Test upload failed: {e}")

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    try:
        # Save the uploaded file
        save_path = UPLOAD_DIR / file.filename
        try:
            with open(save_path, "wb") as f:
                content = await file.read()
                f.write(content)
        except Exception as e:
            logging.exception("Failed to save uploaded PDF")
            raise HTTPException(status_code=500, detail=f"Failed to save PDF: {e}")
        # Extract text from PDF
        try:
            reader = PdfReader(str(save_path))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            logging.exception("Failed to extract text from PDF")
            raise HTTPException(status_code=500, detail=f"Failed to extract text: {e}")
        return JSONResponse({
            "filename": file.filename,
            "text": text.strip() or "No text found in PDF. (Scanned image? Try OCR.)"
        })
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Unexpected error in upload_pdf")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}") 