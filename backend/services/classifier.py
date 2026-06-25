from utils.logger import logger
from agents.food import food_agent
from agents.fashion import fashion_agent
from agents.books import books_agent
from agents.travel import travel_agent
from agents.movies import movies_agent
from agents.tech import tech_agent

AGENTS = {
    "food": food_agent,
    "fashion": fashion_agent,
    "books": books_agent,
    "travel": travel_agent,
    "movies": movies_agent,
    "tech": tech_agent
}

def route_category_agent(category: str, item: str, ocr_text: str, caption: str):
    norm_category = category.lower().strip()
    
    if norm_category not in AGENTS:
        logger.warning(f"Unrecognized category '{category}'. Defaulting to 'tech' agent routing.")
        norm_category = "tech"

    agent_function = AGENTS[norm_category]
    logger.info(f"Routing request dynamically to the '{norm_category}' agent.")
    
    return agent_function(item, ocr_text, caption)
