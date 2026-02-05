import pytesseract
from PIL import Image
import os
import logging

# Configure logger for this module
logger = logging.getLogger(__name__)

import shutil

# Cross-platform Tesseract Configuration
# Priority:
# 1. Environment variable TESSERACT_CMD
# 2. System PATH (works for Linux/Render and correctly installed Windows)
# 3. Fallback hardcoded Windows path

tesseract_cmd = os.environ.get("TESSERACT_CMD")
if not tesseract_cmd:
    tesseract_cmd = shutil.which("tesseract")
    
if not tesseract_cmd and os.name == 'nt':
    # Common default installation path on Windows
    possible_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    if os.path.exists(possible_path):
        tesseract_cmd = possible_path

if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
else:
    logger.warning("Tesseract binary not found in PATH or standard locations. OCR may fail.")

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
