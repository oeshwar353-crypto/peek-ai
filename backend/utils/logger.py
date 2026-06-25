import logging
import time
from contextlib import contextmanager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("PeekAI")

@contextmanager
def log_duration(activity_name: str):
    start_time = time.time()
    logger.info(f"Starting {activity_name}...")
    try:
        yield
    finally:
        duration = time.time() - start_time
        logger.info(f"Finished {activity_name} in {duration:.3f} seconds")
