from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from modules.ocr import extract_text_from_image
from modules.pdf_processor import extract_text_from_pdf
from modules.nlp_processor import extract_medical_data
from modules.analyzer import analyze_medical_data
from modules.recommender import get_recommendations
from modules.translator import translate_text, LANGUAGES
from modules.validator import validate_medical_report
from utils.file_handler import save_uploaded_file, delete_file
from utils.feedback_manager import save_feedback

# --- Application Setup ---
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for React/Frontend

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Routes ---

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "healthy", "service": "SmartMed AI Backend"}), 200

@app.route('/analyze', methods=['POST'])
def analyze_report():
    """
    Main analysis endpoint.
    Expects a file in the multipart-form data with key 'file'.
    Optional param: 'language' (default: 'en')
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
        
    file = request.files['file']
    language = request.form.get('language', 'en')
    print("LANGUAGE RECEIVED FROM FRONTEND:", language)
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
        
    if file and allowed_file(file.filename):
        # 1. Save File
        file_path = save_uploaded_file(file, UPLOAD_FOLDER)
        if not file_path:
             return jsonify({"error": "Failed to save file"}), 500
        
        try:
            # 2. Extract Text
            extracted_text = ""
            if file.filename.lower().endswith('.pdf'):
                extracted_text = extract_text_from_pdf(file_path)
            else:
                extracted_text = extract_text_from_image(file_path)
            
            if not extracted_text:
                return jsonify({"error": "Unreadable document. Please upload a clearer image or PDF."}), 422

            # 3. Validate
            is_valid, score, details = validate_medical_report(extracted_text)
            if not is_valid:
                error_msg = "The document does not appear to be a valid lab report."
                details_msg = "Invalid medical report."
                
                if language != 'en':
                    error_msg = translate_text(error_msg, language)
                    details_msg = translate_text(details_msg, language)

                return jsonify({
                    "error": details_msg,
                    "details": details,
                    "message": error_msg
                }), 400

            # 4. Extract Data (NLP)
            medical_data = extract_medical_data(extracted_text)
            if not medical_data:
                return jsonify({"message": "No structured data found in report.", "data": []}), 200

            # 5. Analyze Data
            analyzed_results = analyze_medical_data(medical_data)

            # 6. Generate Recommendations
            recommendations = get_recommendations(analyzed_results)

            # 7. Translate (if needed)
            # Translate 'interpretation' in analyzed_results
            # Translate recommendations
            if language != 'en':
                # Translate Results
                for item in analyzed_results:
                    item['interpretation'] = translate_text(item['interpretation'], language)
                
                # Translate Recommendations
                translated_recs = {}
                for key, rec_group in recommendations.items():
                    translated_recs[key] = {
                        "status": rec_group['status'], # Keep status logic (High/Low) in English or translate? Usually status logic tokens stay, display translates.
                        "foods": [translate_text(f, language) for f in rec_group['foods']],
                        "lifestyle": [translate_text(l, language) for l in rec_group['lifestyle']],
                        "avoid": [translate_text(a, language) for a in rec_group['avoid']]
                    }
                recommendations = translated_recs

            # 8. Cleanup (Optional: Delete file after processing)
            # delete_file(file_path) 
            # Commented out for debugging, uncomment in production

            return jsonify({
                "status": "success",
                "language": language,
                "results": analyzed_results,
                "recommendations": recommendations,
                "metadata": details
            }), 200

        except Exception as e:
            logger.error(f"Error processing file: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500
            
    else:
        return jsonify({"error": "File type not allowed. Use PDF, JPG, PNG."}), 400



@app.route('/languages', methods=['GET'])
def get_languages():
    """Return supported languages."""
    return jsonify(LANGUAGES), 200

if __name__ == '__main__':
    # Run Flask Server
    print("🚀 Starting SmartMed AI Backend...")
    app.run(host='0.0.0.0', port=5000, debug=True)
