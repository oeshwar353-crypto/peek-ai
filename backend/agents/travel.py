import os
import json
import google.generativeai as genai
from schemas.travel import TravelAnalysis
from utils.logger import logger, log_duration

def travel_agent(item: str, ocr_text: str, caption: str) -> TravelAnalysis:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, "prompts", "travel.txt")

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_template = f.read()
    except Exception as e:
        logger.error(f"Failed to read travel prompt: {str(e)}")
        prompt_template = "Generate destination, hotels, budget, and things_to_do for {item}."

    prompt = prompt_template.replace("{item}", item).replace("{ocr_text}", ocr_text).replace("{caption}", caption)

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        with log_duration("Travel Agent Generation"):
            response = model.generate_content(prompt)
            
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        raw_text = raw_text.strip()

        parsed = json.loads(raw_text)
        return TravelAnalysis(**parsed)
    except Exception as e:
        logger.error(f"Travel agent fallback activated due to error: {str(e)}")
        return TravelAnalysis(
            destination=item or "Amalfi Coast, Italy",
            hotels=["Hotel Santa Caterina", "Le Sirenuse", "Villa d'Este"],
            budget="$$$$",
            things_to_do=["Take a boat tour around the coast", "Visit the Cathedral of Amalfi", "Hike the Path of the Gods"]
        )
