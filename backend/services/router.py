import os
import uuid
from typing import Optional
from fastapi import APIRouter, File, UploadFile, Form, HTTPException

from config.settings import settings
from schemas.analysis import AnalysisResponse
from utils.validator import validate_image
from utils.cache import image_cache
from utils.logger import logger, log_duration
from services.ocr import OCRService
from services.vision import VisionService
from services.classifier import route_category_agent

router = APIRouter()

os.makedirs(settings.UPLOADS_DIR, exist_ok=True)

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_screenshot(
    file: UploadFile = File(...),
    caption: Optional[str] = Form(None)
):
    caption_text = caption or ""

    image_bytes = await validate_image(file)

    cached_response = image_cache.get(image_bytes)
    if cached_response:
        logger.info("Serving analysis response from cache memory.")
        return cached_response

    file_ext = os.path.splitext(file.filename or "")[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    save_path = os.path.join(settings.UPLOADS_DIR, unique_filename)
    
    try:
        with open(save_path, "wb") as f:
            f.write(image_bytes)
        logger.info(f"Uploaded file saved successfully at: {save_path}")
    except Exception as e:
        logger.error(f"Failed to write image file to uploads storage: {str(e)}")

    ocr_text = OCRService.extract_text(image_bytes)

    vision_data = VisionService.analyze_screenshot(image_bytes, ocr_text, caption_text)
    
    category = vision_data.get("category", "tech")
    item = vision_data.get("item", "Screenshot item")
    confidence = vision_data.get("confidence", 70)
    objects = vision_data.get("objects", [])
    description = vision_data.get("description", "No description generated.")

    if item == "Rate Limit Exceeded":
        agent_analysis = {
            "device": "API Rate Limit",
            "specifications": ["Please wait 30 seconds for quota to reset"],
            "estimated_price": "N/A",
            "alternatives": []
        }
    else:
        agent_analysis = route_category_agent(
            category=category,
            item=item,
            ocr_text=ocr_text,
            caption=caption_text
        )

    response = AnalysisResponse(
        category=category,
        confidence=confidence,
        detected_objects=objects,
        ocr_text=ocr_text,
        description=description,
        analysis=agent_analysis
    )

    image_cache.set(image_bytes, response)

    return response
