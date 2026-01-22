import re

# Vocabulary and Filter Lists
IGNORED_TERMS = {
    "page", "date", "time", "report", "sample", "id", "lab", "reference", 
    "interval", "technology", "method", "authorized", "signature", "end of report",
    "sex", "age", "referred", "registered", "collected", "received", "printed",
    "doctor", "physician", "hospital", "patient", "mr.", "mrs.", "dr.", "dept",
    "unit", "observed", "value", "investigation", "bill", "address"
}

COMMON_MEDICAL_TESTS = {
    "hemoglobin", "glucose", "cholesterol", "triglycerides", "hdl", "ldl", 
    "vldl", "platelet", "wbc", "rbc", "hematocrit", "mcv", "mch", "mchc", 
    "neutrophils", "lymphocytes", "monocytes", "eosinophils", "basophils", 
    "tsh", "t3", "t4", "urea", "creatinine", "uric acid", "calcium", 
    "sodium", "potassium", "chloride", "bilirubin", "protein", "albumin",
    "globulin", "alkaline phosphatase", "sgot", "sgpt", "ggt", "esr", "pcr"
}

def clean_test_name(name):
    """
    Cleans the test name by removing non-alphanumeric characters (except valid ones)
    and trimming whitespace.
    """
    # Remove special chars at start/end but allow brackets inside
    name = re.sub(r"^[^a-zA-Z0-9(]+|[^a-zA-Z0-9)]+$", "", name.strip())
    return name

def calculate_confidence(test_name, unit, ref_range):
    """
    Calculates a confidence score for the extracted item.
    """
    score = 0
    test_name_lower = test_name.lower()
    
    # 1. Matches common medical test vocabulary
    if any(med_test in test_name_lower for med_test in COMMON_MEDICAL_TESTS):
        score += 3
        
    # 2. Has a valid unit
    if unit:
        score += 2
        
    # 3. Has a valid range
    if ref_range:
        score += 1
        
    # 4. Length check (too short or too long is suspicious)
    if 3 < len(test_name) < 50:
        score += 1
        
    return score

def extract_medical_data(text):
    """
    Extracts medical test information from raw text using intelligent filtering.
    """
    results_dict = {} # Use dict for deduplication
    lines = text.split('\n')
    
    # Expanded Unit List
    units = [
        "mg/dL", "g/dL", "ng/mL", "ug/dL", "mEq/L", "U/L", "IU/L", 
        "mmol/L", "µmol/L", "/uL", "count/uL", "million/uL", "x10^3/uL", 
        "x10^6/uL", "fl", "pg", "L", "mL", "%", "g/L", "IU/mL", "mOsm/kg"
    ]
    # Sorted by length descending to match longer units first (e.g., mg/dL vs L)
    units.sort(key=len, reverse=True)
    unit_regex_part = "|".join([re.escape(u) for u in units])
    
    # Relaxed Regex to capture potential lines
    # Structure: Name ... Value ... Unit ... (Range)?
    name_pattern = r"(?P<name>[a-zA-Z][a-zA-Z0-9\s\(\)\-\,\.\:%]+?)"
    value_pattern = r"(?P<value>\d{1,5}(\.\d{1,3})?)"
    unit_pattern = fr"(?P<unit>{unit_regex_part})" # Make unit mandatory for regex matching initially? No, pattern matching first.
    range_pattern = r"(?P<range>(\d+(\.\d+)?\s*[\-–]\s*\d+(\.\d+)?)|([<>]\s*\d+(\.\d+)?)|(\(\d+(\.\d+)?\s*[\-–]\s*\d+(\.\d+)?\)))?"

    full_pattern = re.compile(
        fr"^\s*{name_pattern}\s+{value_pattern}\s*{unit_pattern}\s*{range_pattern}.*$",
        re.IGNORECASE | re.MULTILINE
    )

    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
            
        # 1. Immediate keyword filtering (Noise Reduction)
        if any(ignore in line_clean.lower() for ignore in IGNORED_TERMS):
            continue

        match = full_pattern.match(line_clean)
        
        if match:
            item = match.groupdict()
            
            raw_name = item['name']
            value_str = item['value']
            unit = item['unit']
            ref_range = item['range'] if item['range'] else ""

            # 2. Strict Unit Check (User Requirement 3)
            # If no unit captured by regex, ignore line? 
            # Yes, user said "Ignore rows without valid medical units"
            if not unit:
                continue

            # 3. Post-Processing & Validation
            test_name = clean_test_name(raw_name)
            
            # Filter out headers that might look like tests
            if test_name.lower() in IGNORED_TERMS or len(test_name) < 2:
                continue

            try:
                value = float(value_str)
            except ValueError:
                continue
                
            # 4. Confidence Scoring
            confidence = calculate_confidence(test_name, unit, ref_range)
            
            # Threshold for acceptance
            if confidence >= 2: # At least Unit matches (score 2) or Name+Range(3+1)
                
                # Fix range formatting
                if ref_range:
                    ref_range = ref_range.strip("()")

                result_entry = {
                    "test": test_name,
                    "value": value,
                    "unit": unit.strip(),
                    "range": ref_range.strip()
                }
                
                # Deduplication logic: 
                # If test exists, keep the one with higher confidence or more complete info
                # Simple heuristic: overwriting usually works for finding the "result" vs "range" line
                if test_name not in results_dict:
                    results_dict[test_name] = result_entry
                else:
                    # Optional: Could compare if new one has range and old one didn't
                    if not results_dict[test_name]['range'] and ref_range:
                        results_dict[test_name] = result_entry
    
    return list(results_dict.values())
