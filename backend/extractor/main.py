from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .parsers.excel_parser import parse_excel
from .parsers.pdf_parser import parse_pdf

logger = logging.getLogger("extractor")
logging.basicConfig(level=logging.INFO)

ALLOWED_EXTENSIONS = {
    ".pdf": "application/pdf",
    ".xls": "application/vnd.ms-excel",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".csv": "text/csv",
}

app = FastAPI(
    title="Iterum File Extraction Service",
    description="Backend service that converts PDFs and spreadsheets into structured recipe/menu data.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def detect_extension(upload: UploadFile) -> str:
    suffix = Path(upload.filename or "").suffix.lower()
    if suffix in ALLOWED_EXTENSIONS:
        return suffix
    content_type = upload.content_type or ""
    for ext, mime in ALLOWED_EXTENSIONS.items():
        if content_type.startswith(mime):
            return ext
    return suffix


async def read_file(upload: UploadFile) -> bytes:
    content = await upload.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    return content


def normalize_response(
    *,
    recipes: Optional[list[dict[str, Any]]] = None,
    menu_items: Optional[list[dict[str, Any]]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    warnings: Optional[list[str]] = None,
) -> Dict[str, Any]:
    return {
        "recipes": recipes or [],
        "menu_items": menu_items or [],
        "metadata": metadata or {},
        "warnings": warnings or [],
    }


@app.get("/health", tags=["system"])
async def health_check() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/extract", response_class=JSONResponse, tags=["extraction"])
async def extract_file(
    file: UploadFile = File(..., description="Recipe or menu document"),
) -> JSONResponse:
    extension = detect_extension(file)
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{extension or file.content_type}'. "
            f"Supported: {', '.join(ALLOWED_EXTENSIONS.keys())}",
        )

    payload = await read_file(file)
    logger.info("Processing upload '%s' (%s)", file.filename, extension)

    try:
        if extension == ".pdf":
            result = await asyncio.get_event_loop().run_in_executor(
                None, parse_pdf, payload, file.filename
            )
        elif extension in {".xls", ".xlsx", ".csv"}:
            result = await asyncio.get_event_loop().run_in_executor(
                None, parse_excel, payload, file.filename, extension
            )
        else:
            raise HTTPException(status_code=415, detail="Unsupported file type.")
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        logger.exception("Extraction failed for '%s'", file.filename)
        raise HTTPException(
            status_code=500,
            detail=f"Extraction failed: {exc}",
        ) from exc

    response = normalize_response(
        recipes=result.get("recipes"),
        menu_items=result.get("menu_items"),
        metadata=result.get("metadata"),
        warnings=result.get("warnings"),
    )
    return JSONResponse(content=response)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.extractor.main:app", host="0.0.0.0", port=8081, reload=True)


