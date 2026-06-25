import os
from fastapi import UploadFile, HTTPException
from utils.logger import logger

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}
ALLOWED_MIME_TYPES = {"image/png", "image/jpeg", "image/jpg"}
MAX_FILE_SIZE = 10 * 1024 * 1024

async def validate_image(file: UploadFile) -> bytes:
    filename = file.filename or ""
    ext = os.path.splitext(filename.lower())[1]
    
    if ext not in ALLOWED_EXTENSIONS:
        logger.warning(f"Validation failed: extension '{ext}' not allowed.")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension: {ext}. Only PNG, JPG, and JPEG are supported."
        )

    if file.content_type not in ALLOWED_MIME_TYPES:
        logger.warning(f"Validation failed: content type '{file.content_type}' not allowed.")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid content type: {file.content_type}. Only PNG, JPG, and JPEG are supported."
        )

    contents = await file.read()
    size = len(contents)
    
    await file.seek(0)

    if size > MAX_FILE_SIZE:
        logger.warning(f"Validation failed: file size {size} bytes exceeds 10MB limit.")
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds maximum size limit of 10MB (Uploaded: {size / (1024*1024):.2f}MB)."
        )

    return contents
