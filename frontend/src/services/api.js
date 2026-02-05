import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000';

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

export const analyzeReport = async (file, language) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', language);

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
        console.error("API Error (Analyze):", error);
        if (error.response && error.response.data) {
            // Backend returned an error response (e.g., 400 validation error)
            // Return it so App.jsx can display the message
            return error.response.data;
        } else if (error.request) {
            // Network error (server down)
            return { error: "Server is unavailable. Please check if the backend is running." };
        } else {
            return { error: "An unexpected error occurred." };
        }
    }
};


