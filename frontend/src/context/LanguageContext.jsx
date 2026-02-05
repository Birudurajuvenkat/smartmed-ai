import React, { createContext, useState, useContext, useEffect } from 'react';
import { translations } from '../translations';
import { getLanguages } from '../services/api';

const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
    const [language, setLanguage] = useState(localStorage.getItem('appLang') || 'English');
    const [availableLanguages, setAvailableLanguages] = useState({});

    // Fetch supported backend languages on mount
    useEffect(() => {
        getLanguages().then(langs => {
            setAvailableLanguages(langs);
        });
    }, []);

    const changeLanguage = (langName) => {
        setLanguage(langName);
        localStorage.setItem('appLang', langName);
    };

    // Translation helper
    const t = (key) => {
        const langData = translations[language] || translations['English'];
        return langData[key] || key;
    };

    // Get current language code for backend (e.g., 'Hindi' -> 'hi')
    const getLanguageCode = () => {
        return availableLanguages[language] || 'en';
    };

    return (
        <LanguageContext.Provider value={{ language, changeLanguage, t, availableLanguages, getLanguageCode }}>
            {children}
        </LanguageContext.Provider>
    );
};

export const useLanguage = () => useContext(LanguageContext);
