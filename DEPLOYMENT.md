# 🚀 Deployment Guide: SmartMed AI

This guide covers how to deploy the **Flask Backend** (with Tesseract OCR) and the **React Frontend** to the cloud.

---

## 🏗️ 1. Backend Deployment (Render)

We use **Docker** to easily install Tesseract OCR and Python dependencies.

1.  **Push your code to GitHub/GitLab.**
2.  **Sign up/Login to [Render.com](https://render.com).**
3.  Click **"New +"** → **"Web Service"**.
4.  Connect your repository.
5.  **Configuration:**
    *   **Runtime:** `Docker` (Render detects the `Dockerfile` automatically).
    *   **Region:** Choose closest to you (e.g., Singapore, Frankfurt, Oregon).
    *   **Env Variables:**
        *   `FLASK_ENV`: `production`
        *   `PORT`: `5000`
6.  Click **"Create Web Service"**.
7.  Wait for the build to finish. Render will give you a public URL (e.g., `https://smartmed-backend.onrender.com`).
    *   *Copy this URL, you need it for the frontend.*

---

## 🎨 2. Frontend Deployment (Vercel)

1.  **Sign up/Login to [Vercel.com](https://vercel.com).**
2.  Click **"Add New..."** → **"Project"**.
3.  Import your repository.
4.  **Project Settings:**
    *   **Framework Preset:** Vite (Should be auto-detected).
    *   **Root Directory:** Click "Edit" and select `frontend`.
5.  **Environment Variables:**
    *   Add a new variable:
        *   **Name:** `VITE_API_URL`
        *   **Value:** Your backend URL from Step 1 (e.g., `https://smartmed-backend.onrender.com`).
          *   *Note: Do NOT add a trailing slash `/`.*
6.  Click **"Deploy"**.
7.  Vercel will build your site and give you a live domain (e.g., `https://smartmed-ai.vercel.app`).

---

## 🧪 3. Verification

1.  Open your Vercel URL.
2.  The app should load with the particle background.
3.  Open Developer Tools (F12) → Console.
4.  **Check Health:** If you see no red connection errors, the frontend successfully contacted the backend.
5.  **Try it:** Upload a sample medical PDF.

---

## 🛠️ Troubleshooting

### ❌ "Server is unavailable"
*   **Check Vercel Env Var:** Did you set `VITE_API_URL` correctly? Did you rebuild/redeploy after setting it?
*   **Check Render Logs:** Go to Render Dashboard → Logs. Is the backend crashing? Is Tesseract installed? (Our Dockerfile handles this).
*   **CORS Issues:** Access the Backend URL directly in a browser (`/health`). If it loads, the backend is up.

### ❌ "Invalid medical report" on valid files
*   **OCR Issues:** Ensure the image contains readable text.
*   **Language:** The current OCR is optimized for English (`tesseract-ocr-eng`). Support for other languages requires updating the Dockerfile.

---

## 💻 Local Development

To run everything locally:

1.  **Backend:**
    ```bash
    pip install -r requirements.txt
    python app.py
    ```
2.  **Frontend:**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
3.  **Env:**
    *   Ensure `frontend/.env` has `VITE_API_URL=http://127.0.0.1:5000`.

---
*Created by SmartMed DevOps Team*
