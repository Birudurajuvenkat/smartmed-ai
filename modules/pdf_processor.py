import pdfplumber
import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    Returns None if extraction fails.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if not pdf.pages:
                logger.warning(f"PDF has no pages: {pdf_path}")
                return None
                
            for i, page in enumerate(pdf.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                except Exception as e:
                     logger.warning(f"Failed to extract text from page {i} of {pdf_path}: {e}")
                     continue # Try next page
        
        if not text.strip():
            logger.warning(f"PDF extraction resulted in empty text: {pdf_path}")
            
        return text
    except Exception as e:
        logger.error(f"Critical PDF processing failure for {pdf_path}: {e}", exc_info=True)
        return None
