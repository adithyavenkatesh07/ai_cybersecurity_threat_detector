import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ThreatReport from './ThreatReport';
import MetricsReport from './MetricsReport';

const URLScanner = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [visualizationsData, setVisualizationsData] = useState(null);

  // Backend API URL - Change if your backend runs on different port
  const API_URL = 'http://localhost:5000/api';

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await axios.get(`${API_URL}/metrics`);
        setMetrics(response.data);
      } catch (err) {
        console.error('Error fetching metrics:', err);
      }
    };

    fetchMetrics();
  }, []);

  const isValidUrl = (string) => {
    try {
      new URL(string);
      return true;
    } catch (_) {
      return false;
    }
  };

  const handleScan = async (e) => {
    e.preventDefault();
    
    if (!url.trim()) {
      setError('Please enter a URL to scan');
      setResult(null);
      return;
    }

    if (!isValidUrl(url.trim())) {
      setError('Please enter a valid URL format.');
      setResult(null);
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/scan`, { 
        url: url.trim() 
      }, {
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 30000 // 30 second timeout
      });
      
      setResult(response.data);
      setVisualizationsData(response.data.visualizations);
      setError(null);
    } catch (err) {
      console.error('Scan error:', err);
      
      if (err.code === 'ECONNABORTED') {
        setError('Request timeout. Please try again.');
      } else if (err.response) {
        setError(err.response.data?.error || 'Server error occurred');
      } else if (err.request) {
        setError('Cannot connect to server. Make sure backend is running on port 5000.');
      } else {
        setError('An unexpected error occurred while scanning the URL');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (exampleUrl) => {
    setUrl(exampleUrl);
    setError(null);
    setResult(null);
  };

  const exampleUrls = [
    { url: 'https://www.google.com', label: 'Safe Site Example' },
    { url: 'http://192.168.1.1/admin/login', label: 'IP Address Example' },
    { url: 'https://secure-banking-verify-account.com', label: 'Suspicious Keywords Example' }
  ];

  return (
    <div className="url-scanner">
      <div className="scanner-card">
        <h2>🔍 Enter URL to Scan</h2>
        <p style={{ color: '#6b7280', marginBottom: '1.5rem' }}>
          Analyze any website URL for potential security threats and anomalies
        </p>
        
        <form onSubmit={handleScan} className="scan-form">
          <div className="input-group">
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com"
              className="url-input"
              disabled={loading}
              autoFocus
            />
            <button 
              type="submit" 
              className="scan-button"
              disabled={loading || !url.trim()}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Scanning...
                </>
              ) : (
                <>
                  <span>🔍</span>
                  Scan URL
                </>
              )}
            </button>
          </div>
        </form>

        <div className="example-urls">
          <p>💡 Try these example URLs:</p>
          <div className="example-buttons">
            {exampleUrls.map((example, index) => (
              <button
                key={index}
                onClick={() => handleExampleClick(example.url)}
                className="example-button"
                disabled={loading}
                title={example.label}
              >
                <strong>{example.label}:</strong> {example.url}
              </button>
            ))}
          </div>
        </div>

        {error && (
          <div className="error-message">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {result && <ThreatReport result={result} />}
        
        {result && metrics && <MetricsReport metricsData={metrics} visualizationsData={visualizationsData} />}

        {!result && !error && !loading && (
          <div style={{
            marginTop: '2rem',
            padding: '1.5rem',
            background: '#f0f9ff',
            borderRadius: '12px',
            color: '#0369a1'
          }}>
            <h4 style={{ marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span>ℹ️</span> How it works
            </h4>
            <p style={{ fontSize: '0.9rem', lineHeight: '1.6' }}>
              Our AI-powered system analyzes URLs using a Transformer-based machine learning model.
              It checks for suspicious patterns, phishing indicators, SSL security, and various
              threat signals to provide you with a comprehensive security assessment.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default URLScanner;