
RECOMMENDATIONS_KB = {
    "hemoglobin": {
        "low": {
            "foods": ["Iron-rich foods: Spinach, red meat, lentils, liver, pumpkin seeds, tofu", "Vitamin C rich foods: Oranges, strawberries, bell peppers (helps iron absorption)"],
            "lifestyle": ["Ensure adequate sleep and rest", "Consider cooking in cast iron cookware"],
            "avoid": ["Drinking tea or coffee immediately with meals (inhibits iron absorption)", "Calcium supplements taken with iron sources"]
        },
        "high": {
            "foods": ["Plenty of water and fluids", "Fresh fruits and vegetables"],
            "lifestyle": ["Quit smoking if applicable (smoking reduces oxygen delivery)", "Regular blood donation (if advised by doctor)"],
            "avoid": ["Iron supplements unless prescribed", "Dehydration"]
        }
    },
    "glucose": {
        "high": {
            "foods": ["Low Glycemic Index (GI) foods: Whole grains, oats, beans, lentils", "Non-starchy vegetables: Broccoli, spinach, green beans", "Nuts and seeds"],
            "lifestyle": ["Regular physical activity (e.g., 30 mins brisk walking daily)", "Weight management", "Stress reduction techniques"],
            "avoid": ["Sugary drinks and sodas", "Refined carbohydrates (white bread, pasta, pastries)", "Processed snacks"]
        },
        "low": {
            "foods": ["Complex carbohydrates for sustained energy", "Small, frequent meals"],
            "lifestyle": ["Monitor blood sugar levels regularly", "Carry emergency snacks"],
            "avoid": ["Skipping meals", "Alcohol on an empty stomach"]
        }
    },
    "cholesterol": {
        "high": {
            "foods": ["Soluble fiber: Oats, barley, apples, pears", "Heart-healthy fats: Avocado, olive oil, nuts", "Fatty fish (Salmon, Mackerel)"],
            "lifestyle": ["Aerobic exercise to boost HDL (good cholesterol)", "Weight loss if overweight"],
            "avoid": ["Trans fats (fried foods, commercially baked goods)", "Excessive red meat and full-fat dairy", "Smoking"]
        },
         "low": { # Generic advice, usually not a primary concern unless very low
            "foods": ["Balanced diet ensuring adequate calorie intake"],
            "lifestyle": ["Treat underlying conditions if any"],
            "avoid": ["Malnutrition"]
        }
    },
    "triglycerides": {
        "high": {
            "foods": ["Omega-3 rich foods: Fatty fish, flaxseeds, walnuts", "Fiber-rich vegetables"],
            "lifestyle": ["Limit alcohol intake", "Regular exercise", "Lose weight if needed"],
            "avoid": ["Sugary foods and drinks", "Refined carbohydrates", "Excessive alcohol"]
        }
    },
    "platelet": {
        "low": {
            "foods": ["Folate-rich foods: Dark leafy greens, beans", "Vitamin B12 sources: Eggs, dairy, meat"],
            "lifestyle": ["Avoid activities with high risk of injury/bruising", "Use a soft toothbrush"],
            "avoid": ["Alcohol", "Blood-thinning medications (unless prescribed)"]
        }
    },
    "tsh": {
        "high": { # Hypothyroidism
            "foods": ["Iodine-rich foods (if deficiency is cause): Dairy, seafood", "Selenium sources: Brazil nuts (in moderation)"],
            "lifestyle": ["Regular exercise to boost metabolism", "Stress management"],
            "avoid": ["Soy products (in excess) near medication time", "Raw goitrogenic vegetables (cabbage, cauliflower) in large amounts"]
        },
        "low": { # Hyperthyroidism
            "foods": ["Calcium and Vitamin D rich foods", "Non-iodized salt (if restricted)"],
            "lifestyle": ["Stress management", "Adequate rest"],
            "avoid": ["Excessive iodine intake", "Caffeine and stimulants"]
        }
    },
    "uric acid": {
        "high": {
            "foods": ["Complex carbs", "Low-fat dairy", "Vitamin C rich foods", "Cherries"],
            "lifestyle": ["Stay well hydrated", "Maintain healthy weight"],
            "avoid": ["High-purine foods: Red meat, organ meats, shellfish", "Sugary drinks (fructose)", "Alcohol (especially beer)"]
        }
    }
}

def get_recommendations(analyzed_data):
    """
    Generates recommendations based on analyzed medical data.
    
    Args:
        analyzed_data (list): List of dicts containing 'test', 'status', etc.
        
    Returns:
        dict: A dictionary where keys are test names and values are dicts of recommendations.
              Only includes abnormal results matching the knowledge base.
    """
    recommendations = {}
    
    for item in analyzed_data:
        test_name = item.get("test", "").lower()
        status = item.get("status", "").lower()
        
        # Only provide recommendations for High or Low results
        if status in ["high", "low"]:
            # Find matching knowledge base entry
            # Simple keyword matching similar to analyzer
            kb_match = None
            for key in RECOMMENDATIONS_KB:
                if key in test_name:
                    kb_match = RECOMMENDATIONS_KB[key]
                    break
            
            if kb_match and status in kb_match:
                rec_data = kb_match[status]
                recommendations[item["test"]] = {
                    "status": status.capitalize(),
                    "foods": rec_data.get("foods", []),
                    "lifestyle": rec_data.get("lifestyle", []),
                    "avoid": rec_data.get("avoid", [])
                }
                
    return recommendations
