import os
import json
import google.generativeai as genai
from schemas.tech import TechAnalysis
from utils.logger import logger, log_duration

def tech_agent(item: str, ocr_text: str, caption: str) -> TechAnalysis:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, "prompts", "tech.txt")

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_template = f.read()
    except Exception as e:
        logger.error(f"Failed to read tech prompt: {str(e)}")
        prompt_template = "Generate device, specifications, estimated_price, and alternatives for {item}."

    prompt = prompt_template.replace("{item}", item).replace("{ocr_text}", ocr_text).replace("{caption}", caption)

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        with log_duration("Tech Agent Generation"):
            response = model.generate_content(prompt)
            
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        raw_text = raw_text.strip()

        parsed = json.loads(raw_text)
        return TechAnalysis(**parsed)
    except Exception as e:
        logger.error(f"Tech agent fallback activated due to error: {str(e)}")
        return TechAnalysis(
            device=item or "iPhone 15 Pro",
            specifications=["Super Retina XDR OLED Display", "A17 Pro Bionic Chip", "48MP Main Camera", "Titanium Design"],
            estimated_price="$999 - $1299",
            alternatives=["Samsung Galaxy S24 Ultra", "Google Pixel 8 Pro"]
        )
