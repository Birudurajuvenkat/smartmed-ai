from deep_translator import GoogleTranslator
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

# Language mapping
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta"
}

@lru_cache(maxsize=128)
def translate_text(text, target_lang):
    """
    Translates text dynamically using Deep Translator.
    Cached to avoid repeated API calls for same text.
    Returns original text if translation fails.
    """
    if target_lang == "en" or not text:
        return text
        
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated if translated else text
    except Exception as e:
        logger.warning(f"DeepTranslator failed for '{text[:20]}...': {e}")
        return text 
