import os
import csv
import datetime
import logging

FEEDBACK_FILE = "user_feedback.csv"
logger = logging.getLogger(__name__)

def save_feedback(helpful, comment):
    """
    Saves anonymous user feedback to a local CSV file.
    helpful: str ("Yes" / "No")
    comment: str (Optional text)
    """
    file_exists = os.path.isfile(FEEDBACK_FILE)
    
    try:
        with open(FEEDBACK_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write header if file is new
            if not file_exists:
                writer.writerow(["Timestamp", "Helpful", "Comment"])
                
            # Write data
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Sanitize content slightly to prevent CSV injection issues if opened in Excel
            clean_comment = comment.replace("=", "").replace("@", "").strip() if comment else ""
            
            writer.writerow([timestamp, helpful, clean_comment])
            return True
    except Exception as e:
        logger.error(f"Failed to save feedback: {e}")
        return False
