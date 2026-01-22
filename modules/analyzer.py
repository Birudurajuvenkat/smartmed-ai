import re

# Standard Reference Ranges Dictionary
# Format: "keyword" : {"min": val, "max": val, "unit": "unit"}
STANDARD_RANGES = {
    "hemoglobin": {"min": 13.0, "max": 17.0, "unit_type": "g/dL"},
    "glucose": {"min": 70.0, "max": 140.0, "unit_type": "mg/dL"}, # Broad random/fasting mix
    "cholesterol": {"min": 0, "max": 200.0, "unit_type": "mg/dL"},
    "hdl": {"min": 40.0, "max": 100.0, "unit_type": "mg/dL"},
    "ldl": {"min": 0, "max": 100.0, "unit_type": "mg/dL"},
    "triglycerides": {"min": 0, "max": 150.0, "unit_type": "mg/dL"},
    "platelet": {"min": 150000, "max": 450000, "unit_type": "/uL"},
    "wbc": {"min": 4000, "max": 11000, "unit_type": "/uL"},
    "rbc": {"min": 4.5, "max": 5.9, "unit_type": "million/uL"},
    "tsh": {"min": 0.4, "max": 4.0, "unit_type": "mIU/L"},
    "creatinine": {"min": 0.7, "max": 1.3, "unit_type": "mg/dL"},
    "calcium": {"min": 8.5, "max": 10.2, "unit_type": "mg/dL"},
    "sodium": {"min": 135, "max": 145, "unit_type": "mmol/L"},
    "potassium": {"min": 3.5, "max": 5.0, "unit_type": "mmol/L"},
    "sgot": {"min": 0, "max": 40, "unit_type": "U/L"},
    "sgpt": {"min": 0, "max": 40, "unit_type": "U/L"}
}

TEST_KNOWLEDGE = {
    "hemoglobin": {
        "low": "Low hemoglobin (Anemia) can cause fatigue and weakness.",
        "high": "High hemoglobin can be caused by dehydration or other conditions."
    },
    "glucose": {
        "low": "Low blood sugar (Hypoglycemia) requires immediate attention.",
        "high": "High blood sugar may indicate frequent fluctuations or diabetes risk."
    },
    "hba1c": {
        "low": "Unusually low HbA1c is rare.",
        "high": "High HbA1c indicates poor long-term blood sugar control."
    },
    "cholesterol": {
        "low": "Low cholesterol is generally good but extremely low levels can be an issue.",
        "high": "High cholesterol increases the risk of heart disease."
    },
    "platelet": {
        "low": "Low platelet count can increase risk of bleeding.",
        "high": "High platelet count can lead to blood clots."
    }
}

def parse_range(range_str):
    """
    Parses a reference range string into min and max values.
    Supported formats: "10-20", "10 - 20", "< 5", "> 10"
    """
    if not range_str:
        return None, None
        
    range_str = range_str.strip().lower()
    
    try:
        if range_str.startswith("<"):
            max_val = float(re.findall(r"[\d\.]+", range_str)[0])
            return -1, max_val
            
        if range_str.startswith(">"):
            min_val = float(re.findall(r"[\d\.]+", range_str)[0])
            return min_val, float('inf')
            
        numbers = re.findall(r"[\d\.]+", range_str)
        if len(numbers) >= 2:
            return float(numbers[0]), float(numbers[1])
            
    except Exception:
        return None, None

    return None, None

def get_standard_range(test_name):
    """
    Retrieves the standard range for a test if available.
    """
    test_name = test_name.lower()
    for key, data in STANDARD_RANGES.items():
        if key in test_name: # Simple keyword matching
            return data["min"], data["max"]
    return None, None

def analyze_medical_data(data):
    """
    Analyzes medical test results using both lab-provided and standard reference ranges.
    """
    analyzed_results = []
    
    for item in data:
        result = item.copy()
        test_name = result.get("test", "Unknown")
        value = result.get("value")
        ref_range = result.get("range", "")
        
        status = "Unknown"
        interpretation = "Range not available."
        range_source = "N/A"
        
        # 1. Try to parse Lab Range first
        min_val, max_val = parse_range(ref_range)
        
        if min_val is not None:
             range_source = "Lab Report"
        else:
            # 2. Fallback to Standard Range
            min_val, max_val = get_standard_range(test_name)
            if min_val is not None:
                range_source = "Standard DB"
                # Update the range field for display clarity if it was original empty
                if not ref_range:
                    result["range"] = f"{min_val} - {max_val} (Std)"

        # 3. Analyze if we have valid ranges
        if min_val is not None and max_val is not None and isinstance(value, (int, float)):
            if value < min_val:
                status = "Low"
            elif value > max_val:
                status = "High"
            else:
                status = "Normal"
                
            # Generate Interpretation
            if status == "Normal":
                interpretation = "Within normal limits."
            else:
                found_key = None
                for key in TEST_KNOWLEDGE:
                    if key in test_name.lower():
                        found_key = key
                        break
                
                if found_key:
                    interpretation = TEST_KNOWLEDGE[found_key].get(status.lower(), f"Result is {status}.")
                else:
                    interpretation = f"The result is {status}."
                    
        result["status"] = status
        result["interpretation"] = interpretation
        result["range_source"] = range_source
        analyzed_results.append(result)
        
    return analyzed_results
