# SmartMed AI 🩺

SmartMed AI is an intelligent medical report analyzer application built with Streamlit. It helps users make sense of their lab reports by extracting data, analyzing results against standard reference ranges, and providing personalized lifestyle recommendations.

## 🌟 Features

*   **Document Parsing**:
    *   **OCR Integration**: Extracts text from images (JPG, PNG) using Tesseract OCR.
    *   **PDF Support**: Extracts text from native PDF medical reports.
*   **Intelligent Analysis**:
    *   **Validator**: Validates if the uploaded document is a medical report.
    *   **NLP Engine**: Structured extraction of test names, values, units, and ranges using Regex and Pattern Matching.
    *   **Analyzer**: Compares results against lab-provided ranges (if found) or internal standard medical ranges.
*   **Personalization**:
    *   **Recommender System**: Provides food and lifestyle suggestions for abnormal results (High/Low).
    *   **Multi-language Support**: Interface and results available in English, Hindi, Telugu, and Tamil.
*   **User Feedback**: Collects anonymous user feedback to improve the system.

## 🚀 Deployment

This project is ready for deployment on **Streamlit Cloud** or **Docker**.

👉 **[Read the Deployment Guide](DEPLOYMENT.md)** for step-by-step instructions.

## 🛠️ Project Structure

*   `app.py`: Main Streamlit application entry point.
*   `modules/`:
    *   `ocr.py`: Image text extraction.
    *   `pdf_processor.py`: PDF text extraction.
    *   `nlp_processor.py`: Medical data parsing logic.
    *   `analyzer.py`: Logic to interpret results (Low/Normal/High).
    *   `recommender.py`: Rule-based recommendation engine.
    *   `validator.py`: Document validation logic.
    *   `translator.py`: Translation services.
*   `utils/`: Helper functions for file handling and feedback.
*   `uploads/`: Temporary storage for uploaded files.

## 📦 Local Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/smartmed-ai.git
    cd smartmed-ai
    ```

2.  **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Tesseract OCR**:
    *   **Windows**: [Download installer](https://github.com/UB-Mannheim/tesseract/wiki) and add to PATH.
    *   **Linux (Ubuntu/Debian)**: `sudo apt-get install tesseract-ocr`
    *   **Mac**: `brew install tesseract`

4.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## 📝 Disclaimer

*   **Not a Medical Device**: This application is for informational purposes only. Always consult a qualified healthcare provider for medical advice, diagnosis, or treatment.
*   **Data Privacy**: Uploaded files are processed in-memory or temporarily stored and can be deleted by the user. On ephemeral deployments (like Streamlit Cloud), files are wiped on restart.

---
SmartMed AI © 2026
