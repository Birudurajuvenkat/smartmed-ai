# Deployment Guide for SmartMed AI

This guide covers how to deploy the **SmartMed AI** application to **Streamlit Cloud** and **Docker** platforms.

## Prerequisites

Ensure all files are committed to a GitHub repository.

## Option 1: Streamlit Cloud (Recommended)

Streamlit Cloud is the easiest way to deploy Streamlit apps.

1.  **Push your code to GitHub.**
2.  Login to [Streamlit Cloud](https://streamlit.io/cloud).
3.  Click **"New app"**.
4.  Select your repository, branch, and set the main file path to `app.py`.
5.  **Advanced Settings**:
    *   Streamlit Cloud automatically detects `requirements.txt` and installs Python dependencies.
    *   It also detects `packages.txt` and installs system dependencies (we have already included `tesseract-ocr` in this file).
6.  Click **"Deploy!"**.

**Note on Persistence**: The `user_feedback.csv` file will store feedback only temporarily in the current session's container. If the app restarts, this data may be lost. For production persistence, consider using a database or Google Sheets.

## Option 2: Docker / Container Deployment

If you want to deploy to platforms like **Fly.io**, **Google Cloud Run**, or **Hugging Face Spaces**, you can use the included `Dockerfile`.

### Build the Image
```bash
docker build -t smartmed-ai .
```

### Run the Container
```bash
docker run -p 8501:8501 smartmed-ai
```

Access the app at `http://localhost:8501`.

## Option 3: Hugging Face Spaces

1.  Create a new Space on [Hugging Face](https://huggingface.co/spaces).
2.  Select **Docker** as the SDK.
3.  Upload your files (including the `Dockerfile`) to the Space.
4.  It will build and run automatically.

## Troubleshooting

*   **OCR Errors**: If you see errors related to Tesseract not being found, ensure `packages.txt` (Streamlit Cloud) or the `apt-get install tesseract-ocr` command (Docker) was executed successfully.
*   **Memory Issues**: OCR and detailed logging can consume memory. If the app crashes, consider resizing images before processing.
