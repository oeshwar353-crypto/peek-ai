import io
import json
import os
from PIL import Image
import google.generativeai as genai
from config.settings import settings
from utils.logger import logger, log_duration

class VisionService:
    _configured = False

    @classmethod
    def _initialize_sdk(cls):
        if not cls._configured:
            api_key = settings.GEMINI_API_KEY
            if not api_key:
                logger.error("GEMINI_API_KEY settings value is empty. Please set it in backend/.env")
            genai.configure(api_key=api_key)
            cls._configured = True

    @classmethod
    def analyze_screenshot(cls, image_bytes: bytes, ocr_text: str, caption: str) -> dict:
        cls._initialize_sdk()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompt_path = os.path.join(base_dir, "prompts", "vision.txt")

        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt_template = f.read()
        except Exception as e:
            logger.error(f"Failed to read vision prompt file: {str(e)}")
            prompt_template = "You are Peek AI. Analyze screenshot. OCR: {ocr_text}, Caption: {caption}"

        prompt = prompt_template.replace("{ocr_text}", ocr_text).replace("{caption}", caption)

        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            model = genai.GenerativeModel("gemini-2.5-flash")

            with log_duration("Gemini Vision Model Call"):
                response = model.generate_content([image, prompt])

            raw_text = response.text.strip()
            
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()

            parsed_data = json.loads(raw_text)
            if "description" not in parsed_data:
                parsed_data["description"] = f"This is a {parsed_data.get('category', 'screenshot')} showing {parsed_data.get('item', 'an item')}."
            logger.info("Screenshot successfully classified by Gemini Vision.")
            return parsed_data
            
        except Exception as e:
            logger.error(f"Failed to execute Gemini Vision API call: {str(e)}")
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                return {
                    "category": "tech",
                    "item": "Rate Limit Exceeded",
                    "confidence": 100,
                    "objects": ["Quota", "Rate Limit"],
                    "description": "API Quota Exceeded (Rate Limit 429): You are using the Gemini API Free Tier, which is limited to 5 requests per minute. Please wait 30 seconds before trying again!"
                }
            return {
                "category": "tech",
                "item": "Tech Device",
                "confidence": 60,
                "objects": ["Device", "Screen", "Interface"],
                "description": "We couldn't analyze the screenshot with Gemini because of an API connection issue. Please double check that your API key is correct and valid."
            }
