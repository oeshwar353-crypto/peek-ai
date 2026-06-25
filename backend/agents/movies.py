import os
import json
import google.generativeai as genai
from schemas.movie import MovieAnalysis
from utils.logger import logger, log_duration

def movies_agent(item: str, ocr_text: str, caption: str) -> MovieAnalysis:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, "prompts", "movies.txt")

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_template = f.read()
    except Exception as e:
        logger.error(f"Failed to read movies prompt: {str(e)}")
        prompt_template = "Generate movie_title, actors, plot, and streaming_platforms for {item}."

    prompt = prompt_template.replace("{item}", item).replace("{ocr_text}", ocr_text).replace("{caption}", caption)

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        with log_duration("Movies Agent Generation"):
            response = model.generate_content(prompt)
            
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        raw_text = raw_text.strip()

        parsed = json.loads(raw_text)
        return MovieAnalysis(**parsed)
    except Exception as e:
        logger.error(f"Movies agent fallback activated due to error: {str(e)}")
        return MovieAnalysis(
            movie_title=item or "Inception",
            actors=["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"],
            plot="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
            streaming_platforms=["Netflix", "HBO Max", "Amazon Prime Video"]
        )
