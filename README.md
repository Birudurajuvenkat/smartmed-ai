# SmartMed AI – Multilingual Medical Report Analyzer

## Project Overview

- SmartMed AI is an AI-powered web application developed to analyze medical reports and generate simplified, patient-friendly summaries.
- The system is designed to be free, easy to use, and accessible without user login.
- It supports multiple languages including English, Telugu, Hindi, and Tamil.
- The application focuses on improving healthcare awareness using artificial intelligence technologies.

## Key Features

- Supports upload of medical reports in PDF and image formats.
- Uses Optical Character Recognition (OCR) with Tesseract to extract text from scanned documents.
- Implements Natural Language Processing (NLP) for text preprocessing and medical entity extraction.
- Automatically identifies medical parameters such as Hemoglobin, Blood Sugar, and Cholesterol.
- Classifies health values into Low, Normal, and High categories using reference ranges.
- Generates personalized diet and lifestyle recommendations.
- Includes document validation to prevent non-medical and irrelevant file uploads.
- Provides multilingual output through translation mechanisms.
- Offers a clean and user-friendly web interface built with Streamlit.
- Allows anonymous feedback submission without collecting personal data.

## System Workflow

- User uploads a medical report through the web interface.
- The system validates the uploaded file format and content.
- OCR is applied to extract text from scanned documents.
- Extracted text is cleaned and processed using NLP techniques.
- Medical values and parameters are identified and structured.
- Values are analyzed and compared with standard reference ranges.
- Health status is classified into appropriate categories.
- Recommendations are generated based on analysis.
- Results are displayed in real time.
- Uploaded files are deleted automatically after processing.

## Technologies Used

- Python for backend development and data processing.
- Streamlit for web application development.
- Tesseract OCR and pytesseract for text extraction.
- Natural Language Processing techniques for text analysis.
- Machine Learning and rule-based algorithms for classification.
- Git and GitHub for version control.
- Streamlit Cloud for application deployment.

## Deployment

- The application is deployed on Streamlit Cloud.
- The system is publicly accessible without authentication.
- Continuous deployment is managed through GitHub integration.
- Live application URL:
  https://smartmed-ai-birurajuvenkat.streamlit.app/

## Data Privacy and Security

- Uploaded documents are stored temporarily during processing.
- Files are automatically deleted after analysis.
- No personal or medical records are permanently stored.
- Feedback is collected anonymously.
- The system follows basic privacy and ethical guidelines.

## Limitations

- The application does not replace professional medical consultation.
- Accuracy depends on document quality and OCR performance.
- Some complex or poorly scanned reports may not be processed correctly.
- Reference ranges may differ across laboratories.

## Future Enhancements

- Integration with external databases for persistent storage.
- Advanced deep learning-based NLP models.
- Admin dashboard for system monitoring.
- Mobile application development.
- Cloud-based analytics and reporting.
- Research-level validation and optimization.
