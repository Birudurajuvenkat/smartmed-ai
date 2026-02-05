import React, { useState, useEffect } from 'react';
import ParticleBackground from './components/ParticleBackground';
import { analyzeReport } from './services/api';
import QuotesTicker from './components/QuotesTicker';
import { useLanguage } from './context/LanguageContext';

function App() {
  const { language, changeLanguage, t, availableLanguages, getLanguageCode } = useLanguage();

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loadingMessage, setLoadingMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
    setError('');
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError(t('errUpload'));
      return;
    }

    setLoading(true);
    setError('');
    setLoadingMessage('Analyzing report, please wait...');

    try {
      // Find lang code for backend
      const langCode = getLanguageCode();
      const data = await analyzeReport(file, langCode, (retryCount) => {
        setLoadingMessage(`Server is waking up... (Attempt ${retryCount}/3)\nPlease wait ⏳`);
      });

      if (data.error) {
        // Here we could try to map backend errors to frontend translations if key exists
        // simplified logic: use message from backend
        setError(data.message || data.error);
      } else {
        setResult(data);
      }
    } catch (err) {
      console.error(err);
      setError(t('errServer'));
    } finally {
      setLoading(false);
      setLoadingMessage('');
    }
  };


  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      // Validate file type
      const fileType = droppedFile.name.split('.').pop().toLowerCase();
      if (['pdf', 'jpg', 'jpeg', 'png'].includes(fileType)) {
        setFile(droppedFile);
        setResult(null);
        setError('');
      } else {
        setError(t('errUpload') + " (PDF, JPG, PNG only)");
      }
    }
  };

  return (
    <div className="app-container">
      <ParticleBackground />

      <div className="glass-container">

        {/* Header */}
        <header className="header">
          <div>
            <div className="app-title">🩺 {t('appTitle')}</div>
            <div className="app-subtitle">{t('appSubtitle')}</div>
          </div>
          <select
            className="lang-select"
            value={language}
            onChange={(e) => changeLanguage(e.target.value)}
          >
            {Object.keys(translations).map(lang => (
              <option key={lang} value={lang}>{lang}</option>
            ))}
          </select>
        </header>

        {/* Quotes Section */}
        <QuotesTicker />

        {/* Main Content */}
        {!result ? (
          <div className="landing-view">
            {!file ? (
              <div
                className={`upload-area ${dragActive ? 'drag-active' : ''}`}
                onClick={() => document.getElementById('fileInput').click()}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <span style={{ fontSize: '3rem' }}>{dragActive ? '📂' : '📄'}</span>
                <h3>{dragActive ? 'Drop file here' : t('uploadTitle')}</h3>
                <p>{t('uploadSubtitle')}</p>
                <input
                  id="fileInput"
                  type="file"
                  accept=".pdf,.jpg,.jpeg,.png"
                  onChange={handleFileChange}
                  style={{ display: 'none' }}
                />
              </div>
            ) : (
              <div className="glass-card" style={{ marginBottom: '2rem', borderColor: 'var(--success-color)' }}>
                <div style={{ fontSize: '3rem', color: 'var(--success-color)' }}>✔</div>
                <h3 style={{ margin: '0.5rem 0', fontSize: '1.5rem' }}>{t('fileSelected')}</h3>
                <p style={{ fontWeight: 'bold', color: 'var(--text-primary)' }}>{file.name}</p>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{(file.size / 1024).toFixed(2)} KB</p>

                <div style={{ marginTop: '1.5rem', display: 'flex', gap: '1rem', justifyContent: 'center' }}>
                  <button
                    className="btn-primary"
                    onClick={() => document.getElementById('fileInput').click()}
                    style={{ background: 'transparent', border: '1px solid var(--text-secondary)', color: 'var(--text-secondary)', padding: '0.5rem 1.5rem' }}
                  >
                    Change File
                  </button>
                  {/* Hidden input for change file */}
                  <input
                    id="fileInput"
                    type="file"
                    accept=".pdf,.jpg,.jpeg,.png"
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                  />
                </div>
              </div>
            )}

            {loading && (
              <div style={{ textAlign: 'center', margin: '2rem 0' }}>
                <div className="loader" style={{ margin: '0 auto' }}></div>
                <p style={{ marginTop: '1rem', color: 'var(--text-secondary)', whiteSpace: 'pre-line' }}>{loadingMessage}</p>
              </div>
            )}

            {file && !loading && (
              <button
                className="btn-primary"
                onClick={handleAnalyze}
              >
                {t('analyzeBtn')}
              </button>
            )}

            {error && <div style={{ color: 'var(--danger-color)', marginTop: '1rem', textAlign: 'center' }}>{error}</div>}

            <div className="features-grid">
              <div className="glass-card">
                <h3>🔍</h3>
                <h4>{t('featOCR')}</h4>
                <p>{t('featOCRDesc')}</p>
              </div>
              <div className="glass-card">
                <h3>📊</h3>
                <h4>{t('featAnalysis')}</h4>
                <p>{t('featAnalysisDesc')}</p>
              </div>
              <div className="glass-card">
                <h3>🥗</h3>
                <h4>{t('featAdvice')}</h4>
                <p>{t('featAdviceDesc')}</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="results-view">
            <button className="btn-primary" onClick={() => { setResult(null); setFile(null); }} style={{ width: 'auto', marginBottom: '1rem', padding: '0.5rem 1rem' }}>
              {t('newAnalysisBtn')}
            </button>

            <h2>{t('resultsTitle')}</h2>

            {/* Stats */}
            <div style={{ display: 'flex', gap: '2rem', margin: '1rem 0' }}>
              <div>{t('testsFound')}: <strong>{result.results.length}</strong></div>
              <div>{t('abnormal')}: <strong style={{ color: 'var(--danger-color)' }}>{result.results.filter(r => r.status !== 'Normal').length}</strong></div>
            </div>

            {/* Table */}
            <div style={{ overflowX: 'auto' }}>
              <table className="results-table">
                <thead>
                  <tr>
                    <th>{t('thTest')}</th>
                    <th>{t('thValue')}</th>
                    <th>{t('thUnit')}</th>
                    <th>{t('thStatus')}</th>
                    <th>{t('thInterpretation')}</th>
                  </tr>
                </thead>
                <tbody>
                  {result.results.map((row, idx) => (
                    <tr key={idx}>
                      <td>{row.test}</td>
                      <td>{row.value}</td>
                      <td>{row.unit}</td>
                      <td className={`status-${row.status.toLowerCase()}`}>{row.status}</td>
                      <td>{row.interpretation}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Recommendations */}
            {Object.keys(result.recommendations).length > 0 && (
              <div className="recommendations-section">
                <h3 style={{ margin: '2rem 0 1rem' }}>{t('recTitle')}</h3>
                {Object.entries(result.recommendations).map(([test, rec]) => (
                  <div key={test} className="rec-card" style={{ borderColor: rec.status === 'High' || rec.status === 'Low' ? 'var(--danger-color)' : 'var(--success-color)' }}>
                    <h4 style={{ color: rec.status === 'High' || rec.status === 'Low' ? 'var(--danger-color)' : 'var(--success-color)' }}>
                      {test} ({rec.status})
                    </h4>

                    <div className="rec-grid">
                      <div className="rec-column">
                        <h5>{t('recFoods')}</h5>
                        <ul>{rec.foods.map((i, k) => <li key={k}>{i}</li>)}</ul>
                      </div>
                      <div className="rec-column">
                        <h5>{t('recLifestyle')}</h5>
                        <ul>{rec.lifestyle.map((i, k) => <li key={k}>{i}</li>)}</ul>
                      </div>
                      <div className="rec-column">
                        <h5>{t('recAvoid')}</h5>
                        <ul>{rec.avoid.map((i, k) => <li key={k}>{i}</li>)}</ul>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Feedback Removed per request */}
          </div>
        )}

      </div>

      <div style={{ textAlign: 'center', marginTop: '2rem', color: 'var(--text-secondary)', fontSize: '0.8rem', whiteSpace: 'pre-line' }}>
        {t('footer')}
      </div>
    </div>
  );
}

// Need to import translations for the select dropdown mapping 
// or I can iterate availableLanguages. But availableLanguages keys might be "English", "Hindi".
// Let's import translations to be safe for rendering keys.
import { translations } from './translations';

export default App;
