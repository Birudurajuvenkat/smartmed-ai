import re
import logging

logger = logging.getLogger(__name__)

# Keywords that strongly suggest a medical lab report
MEDICAL_KEYWORDS = {
    'hemoglobin', 'platelet', 'blood', 'glucose', 'cholesterol', 'triglycerides',
    'leukocyte', 'erythrocyte', 'neutrophils', 'lymphocytes', 'monocytes',
    'eosinophils', 'basophils', 'hematocrit', 'mcv', 'mch', 'mchc', 'rdw',
    'bilirubin', 'protein', 'albumin', 'globulin', 'phosphatase', 'sgot', 'sgpt',
    'urea', 'creatinine', 'calcium', 'sodium', 'potassium', 'chloride', 
    'thyroid', 'tsh', 't3', 't4', 'hba1c', 'vitamin', 'urine', 'analysis'
}

# Structural keywords found in report headers/tables
REPORT_STRUCTURE_KEYWORDS = {
    'test name', 'investigation', 'observed value', 'result', 'unit', 
    'reference range', 'biological reference', 'interval', 'method', 'specimen',
    'sample', 'collected', 'received', 'reported', 'patient', 'doctor', 'lab'
}

# Medical units regex patterns
UNIT_PATTERNS = [
    r'mg/dl', r'g/dl', r'mmol/l', r'iu/l', r'u/l', r'\b%\b', 
    r'ng/ml', r'pg/ml', r'ug/ml', r'fl', r'cells/cumm', 
    r'10\^6/ul', r'10\^3/ul', r'micromol/l'
]

def validate_medical_report(text):
    """
    Analyzes text to determine if it is a valid medical laboratory report.
    Returns (is_valid, confidence_score, details).
    """
    if not text:
        return False, 0.0, "Empty text"

    text_lower = text.lower()
    
    # 1. Keyword Score
    found_keywords = [kw for kw in MEDICAL_KEYWORDS if kw in text_lower]
    keyword_score = len(found_keywords) * 2
    
    # 2. Structure Score (Higher weight as these define the format)
    found_structure = [kw for kw in REPORT_STRUCTURE_KEYWORDS if kw in text_lower]
    structure_score = len(found_structure) * 3
    
    # 3. Units Score (Regex matching)
    found_units = 0
    for pattern in UNIT_PATTERNS:
        matches = re.findall(pattern, text_lower)
        found_units += len(matches)
    unit_score = found_units * 4
    
    # Total Score
    total_score = keyword_score + structure_score + unit_score
    
    # Thresholding
    # A typical report has at least one test (kw), some structure (result/range), and units.
    # A score of 15 allows for small/partial reports but filters out generic text.
    THRESHOLD = 15
    
    # CRITICAL CHECK: If almost no medical keywords are found, it's likely a resume or random doc.
    if len(found_keywords) < 2:
        logger.warning("Validation Failed: Too few medical keywords found.")
        return False, total_score, {"error": "Not enough medical terms found."}

    is_valid = total_score >= THRESHOLD
    
    logger.info(f"Validator Details -> Score: {total_score} (Threshold: {THRESHOLD}). Valid: {is_valid}")
    logger.info(f"Breakdown -> Keywords: {len(found_keywords)} ({found_keywords}), Structure: {len(found_structure)}, Units: {found_units}")
    
    details = {
        "score": total_score,
        "keywords_found": len(found_keywords),
        "structure_found": len(found_structure),
        "units_found": found_units
    }
    
    return is_valid, total_score, details
