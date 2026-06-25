import os
import json
import google.generativeai as genai
from schemas.food import FoodAnalysis
from utils.logger import logger, log_duration

def food_agent(item: str, ocr_text: str, caption: str) -> FoodAnalysis:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, "prompts", "food.txt")

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_template = f.read()
    except Exception as e:
        logger.error(f"Failed to read food prompt: {str(e)}")
        prompt_template = "Generate recipe, ingredients, calories, cook_time, and alternative_dishes for {item}."

    prompt = prompt_template.replace("{item}", item).replace("{ocr_text}", ocr_text).replace("{caption}", caption)

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        with log_duration("Food Agent Generation"):
            response = model.generate_content(prompt)
            
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        raw_text = raw_text.strip()

        parsed = json.loads(raw_text)
        return FoodAnalysis(**parsed)
    except Exception as e:
        logger.error(f"Food agent fallback activated due to error: {str(e)}")
        return FoodAnalysis(
            recipe=item or "Alfredo Pasta",
            ingredients=["Pasta", "Parmesan Cheese", "Cream", "Butter", "Garlic"],
            calories=540,
            cook_time="20 minutes",
            alternative_dishes=["Pesto Pasta", "Mac and Cheese"]
        )
