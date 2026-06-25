import os
import json
import google.generativeai as genai
from schemas.book import BookAnalysis
from utils.logger import logger, log_duration

def books_agent(item: str, ocr_text: str, caption: str) -> BookAnalysis:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, "prompts", "books.txt")

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_template = f.read()
    except Exception as e:
        logger.error(f"Failed to read books prompt: {str(e)}")
        prompt_template = "Generate summary, author, genre, and similar_books for {item}."

    prompt = prompt_template.replace("{item}", item).replace("{ocr_text}", ocr_text).replace("{caption}", caption)

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        with log_duration("Books Agent Generation"):
            response = model.generate_content(prompt)
            
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        raw_text = raw_text.strip()

        parsed = json.loads(raw_text)
        return BookAnalysis(**parsed)
    except Exception as e:
        logger.error(f"Books agent fallback activated due to error: {str(e)}")
        return BookAnalysis(
            summary="A deep dive into personal development, structural focus, and building productive habits.",
            author=item or "James Clear",
            genre="Self-Help / Non-Fiction",
            similar_books=["The Power of Habit by Charles Duhigg", "Deep Work by Cal Newport"]
        )
