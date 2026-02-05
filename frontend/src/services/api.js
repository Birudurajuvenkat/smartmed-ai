import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL ||
    (import.meta.env.PROD
        ? 'https://smartmed-ai.onrender.com'
        : 'http://127.0.0.1:5000');

const api = axios.create({
    baseURL: API_URL,
});

export const getLanguages = async () => {
    try {
        const response = await api.get('/languages');
        return response.data;
    } catch (error) {
        console.error("API Error (Languages):", error);
        return {};
    }
};

// Helper to sleep
const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

export const analyzeReport = async (file, language, onProgress) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', language);

    const MAX_RETRIES = 3;
    const RETRY_DELAY = 8000; // 8 seconds

    for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
        try {
            // Increase timeout for OCR processing
            const response = await api.post('/analyze', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                timeout: 60000 // 60s
            });
            return response.data;

        } catch (error) {
            const isNetworkError = !error.response; // Network error or timeout
            const isServerBusy = error.response && (error.response.status === 502 || error.response.status === 503 || error.response.status === 504);

            // If we have retries left AND it's a retryable error
            if ((isNetworkError || isServerBusy) && attempt < MAX_RETRIES) {
                console.warn(`Attempt ${attempt + 1} failed. Retrying in ${RETRY_DELAY / 1000}s...`);

                if (onProgress) {
                    onProgress(attempt + 1);
                }

                await wait(RETRY_DELAY);
                continue; // Retry loop
            }

            console.error("API Error (Analyze):", error);

            // Final Error Handling
            if (error.response && error.response.data) {
                return error.response.data;
            } else if (isNetworkError) {
                return {
                    error: "Server is still starting or unavailable. Please try again in a minute.",
                    details: "Request timed out after multiple attempts."
                };
            } else {
                return { error: "An unexpected error occurred." };
            }
        }
    }
};


