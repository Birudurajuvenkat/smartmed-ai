import pytesseract
from PIL import Image
import os
import logging

# Configure logger for this module
logger = logging.getLogger(__name__)

def extract_text_from_image(image_path):
    """
    Extracts text from an image file using OCR.
    Returns None if extraction fails.
    """
    if not os.path.exists(image_path):
        logger.error(f"File not found: {image_path}")
        return None

    try:
        with Image.open(image_path) as image:
            # Tesseract can fail on very small or corrupt images
            text = pytesseract.image_to_string(image)
            if not text.strip():
                logger.warning(f"OCR returned empty text for {image_path}")
            return text.strip()
    except Exception as e:
        logger.error(f"OCR failed for {image_path}: {e}", exc_info=True)
        return None
