import React, { useState, useEffect } from 'react';
import { useLanguage } from '../context/LanguageContext';

const QuotesTicker = () => {
    const { t } = useLanguage();
    const quotes = t('quotes') || []; // Get localized quotes array

    const [index, setIndex] = useState(0);
    const [fade, setFade] = useState(true);

    // Reset index when quotes change (language switch)
    useEffect(() => {
        setIndex(0);
    }, [quotes]);

    useEffect(() => {
        if (quotes.length === 0) return;

        const interval = setInterval(() => {
            setFade(false); // Start fade out
            setTimeout(() => {
                setIndex((prevIndex) => (prevIndex + 1) % quotes.length);
                setFade(true); // Start fade in
            }, 500); // Wait for fade out to complete
        }, 5000); // Change every 5 seconds

        return () => clearInterval(interval);
    }, [quotes]);

    if (quotes.length === 0) return null;

    return (
        <div style={{
            textAlign: 'center',
            margin: '0 auto 2rem',
            maxWidth: '600px',
            minHeight: '60px', // Prevent layout jump
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
        }}>
            <p style={{
                fontSize: '1.1rem',
                fontFamily: "'Playfair Display', serif",
                color: '#546E7A', // Darker text for light theme
                fontStyle: 'italic',
                opacity: fade ? 1 : 0,
                transform: fade ? 'translateY(0)' : 'translateY(10px)',
                transition: 'opacity 0.5s ease, transform 0.5s ease',
                textShadow: 'none',
                padding: '0 1rem',
                borderLeft: '3px solid var(--accent-color)',
                borderRight: '3px solid var(--accent-color)',
                display: 'inline-block'
            }}>
                “{quotes[index]}”
            </p>
        </div>
    );
};

export default QuotesTicker;
