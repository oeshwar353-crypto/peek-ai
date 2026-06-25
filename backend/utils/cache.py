import hashlib
from typing import Optional, Any
from utils.logger import logger

class ResponseCache:
    def __init__(self):
        self._store = {}

    def _get_hash(self, content_bytes: bytes) -> str:
        return hashlib.sha256(content_bytes).hexdigest()

    def get(self, content_bytes: bytes) -> Optional[Any]:
        img_hash = self._get_hash(content_bytes)
        if img_hash in self._store:
            logger.info(f"[CACHE HIT] Found cached response for image hash: {img_hash[:12]}...")
            return self._store[img_hash]
        return None

    def set(self, content_bytes: bytes, response_data: Any) -> None:
        img_hash = self._get_hash(content_bytes)
        logger.info(f"[CACHE SET] Storing response under image hash: {img_hash[:12]}...")
        self._store[img_hash] = response_data

image_cache = ResponseCache()
