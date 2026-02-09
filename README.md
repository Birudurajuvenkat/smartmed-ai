# SmartMed AI – Multilingual Medical Report Analyzer

## Project Overview
SmartMed AI is a full-stack web application designed to analyze medical laboratory reports and present easy-to-understand health insights for users. The system extracts data from PDF and image-based reports using OCR and NLP techniques, evaluates medical parameters, and provides recommendations based on standard reference ranges.

This project aims to make medical report interpretation accessible to non-technical users through a simple and multilingual interface
## Key Features

- Upload and analyze medical reports in PDF and image formats
- Optical Character Recognition (OCR) using Tesseract for scanned documents
- NLP-based extraction of medical parameters
- Automated classification of results as Low, Normal, or High
- Health and lifestyle recommendations based on analysis
- Multilingual support (English, Telugu, Hindi, Tamil)
- Responsive and user-friendly web interface
- Cloud deployment with frontend and backend separation
- Error handling and server wake-up retry mechanism

## System Workflow

-User uploads a medical report through the web interface.
- The frontend sends the file to the backend using REST APIs.
- The backend processes the file using OCR and NLP pipelines.
- Extracted data is validated and analyzed against reference ranges.
- Health status and recommendations are generated.
- Results are returned to the frontend and displayed to the user.

## Technologies Used

Frontend
- React.js
- HTML, CSS, JavaScript
Backend
- Python
- Flask (REST API)
AI / Data Processing
- OCR (Tesseract)
- NLP (Natural Language Processing using Regular Expressions)
- Data Validation and Parsing
Cloud
- Vercel (Frontend Hosting)
- Render (Backend Hosting)
- Docker
- Environment Variables
Tools
- Git, GitHub
- VS Code

## Live Application
https://smartmed-ai-web.vercel.app/

## Deployment

Backend
- Deployed on Render using Docker
Frontend
- Deployed on Vercel with automatic CI/CD from GitHub
Every push to the main branch triggers automatic redeployment.

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
- Integration of machine learning models for health risk prediction
- User profile and report history
- Mobile application support
- Advanced medical analytics
- Secure database integration
