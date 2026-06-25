import io
import numpy as np
from PIL import Image
import easyocr
from utils.logger import logger, log_duration

class OCRService:
    _reader = None

    @classmethod
    def _initialize_reader(cls):
        if cls._reader is None:
            with log_duration("EasyOCR Model Load"):
                cls._reader = easyocr.Reader(['en'], gpu=False)

    @classmethod
    def extract_text(cls, image_bytes: bytes) -> str:
        cls._initialize_reader()
        
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image.convert("RGB"))
            
            with log_duration("EasyOCR Parsing"):
                results = cls._reader.readtext(image_np)
            
            words = [item[1] for item in results]
            extracted_text = " ".join(words)
            
            logger.info(f"OCR parsing completed successfully. Extracted {len(words)} words.")
            return extracted_text
        except Exception as e:
            logger.error(f"Error during EasyOCR parsing: {str(e)}")
            return ""
