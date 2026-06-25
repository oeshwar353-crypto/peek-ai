import os
import json
import google.generativeai as genai
from schemas.fashion import FashionAnalysis
from utils.logger import logger, log_duration

def fashion_agent(item: str, ocr_text: str, caption: str) -> FashionAnalysis:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, "prompts", "fashion.txt")

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_template = f.read()
    except Exception as e:
        logger.error(f"Failed to read fashion prompt: {str(e)}")
        prompt_template = "Generate estimated_style, brand, price_range, and matching_outfits for {item}."

    prompt = prompt_template.replace("{item}", item).replace("{ocr_text}", ocr_text).replace("{caption}", caption)

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        with log_duration("Fashion Agent Generation"):
            response = model.generate_content(prompt)
            
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        raw_text = raw_text.strip()

        parsed = json.loads(raw_text)
        return FashionAnalysis(**parsed)
    except Exception as e:
        logger.error(f"Fashion agent fallback activated due to error: {str(e)}")
        return FashionAnalysis(
            estimated_style="Casual Streetwear",
            brand=item or "Urban Outfitters",
            price_range="$45 - $120",
            matching_outfits=["White leather sneakers", "Black slim-fit denim", "Canvas tote bag"]
        )
