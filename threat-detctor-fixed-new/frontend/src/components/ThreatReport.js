import React from 'react';

const ThreatReport = ({ result }) => {
  const getThreatColor = (level) => {
    switch (level) {
      case 'LOW':
        return '#10b981';
      case 'MEDIUM':
        return '#f59e0b';
      case 'HIGH':
        return '#ef4444';
      default:
        return '#6b7280';
    }
  };

  const getStatusIcon = (isSafe) => {
    return isSafe ? '✅' : '🚨';
  };

  const getScoreDescription = (score) => {
    if (score < 30) return 'This URL appears to be safe to visit';
    if (score < 60) return 'Exercise caution when visiting this URL';
    return 'This URL is potentially dangerous - avoid visiting';
  };

  return (
    <div className="threat-report">
      <div className={`status-banner ${result.is_safe ? 'safe' : 'unsafe'}`}>
        <span className="status-icon">{getStatusIcon(result.is_safe)}</span>
        <div>
          <h3>{result.is_safe ? 'Website Appears Safe' : 'Threat Detected!'}</h3>
          <p style={{ fontSize: '0.9rem', marginTop: '0.25rem', opacity: 0.95 }}>
            {getScoreDescription(result.threat_score)}
          </p>
        </div>
      </div>

      <div className="report-section">
        <h4>📊 Threat Analysis</h4>
        <div className="threat-score">
          <div className="score-label">Threat Score</div>
          <div 
            className="score-value" 
            style={{ color: getThreatColor(result.threat_level) }}
          >
            {result.threat_score}%
          </div>
          <div 
            className="threat-level" 
            style={{ backgroundColor: getThreatColor(result.threat_level) }}
          >
            {result.threat_level} RISK
          </div>
        </div>
        <div style={{ 
          marginTop: '1rem', 
          padding: '1rem', 
          background: '#fff', 
          borderRadius: '8px',
          textAlign: 'center',
          color: '#6b7280',
          fontSize: '0.85rem'
        }}>
          Analysis completed in real-time using AI-powered threat detection
        </div>
      </div>

      {result.anomalies && result.anomalies.length > 0 && (
        <div className="report-section">
          <h4>🔍 Detected Anomalies</h4>
          <ul className="anomalies-list">
            {result.anomalies.map((anomaly, index) => (
              <li key={index} className="anomaly-item">
                <span className="anomaly-bullet">⚠️</span>
                <span>{anomaly}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {result.recommendations && result.recommendations.length > 0 && (
        <div className="report-section">
          <h4>💡 Security Recommendations</h4>
          <ul className="recommendations-list">
            {result.recommendations.map((recommendation, index) => (
              <li key={index} className="recommendation-item">
                {recommendation}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="report-section">
        <h4>📋 Technical Details</h4>
        <div className="details-grid">
          <div className="detail-item">
            <span className="detail-label">URL Length</span>
            <span className="detail-value">
              {result.details.url_length} characters
            </span>
          </div>
          <div className="detail-item">
            <span className="detail-label">HTTPS Encryption</span>
            <span className="detail-value">
              {result.details.has_https ? '✓ Enabled' : '✗ Not Enabled'}
            </span>
          </div>
          <div className="detail-item">
            <span className="detail-label">IP Address Used</span>
            <span className="detail-value">
              {result.details.has_ip ? '✓ Yes' : '✗ No'}
            </span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Subdomain Count</span>
            <span className="detail-value">
              {result.details.subdomain_count}
            </span>
          </div>
          <div className="detail-item">
            <span className="detail-label">URL Redirects</span>
            <span className="detail-value">
              {result.details.has_redirect ? '✓ Detected' : '✗ None'}
            </span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Suspicious Keywords</span>
            <span className="detail-value">
              {result.details.has_suspicious_keywords ? '✓ Found' : '✗ None'}
            </span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Special Characters</span>
            <span className="detail-value">
              {result.details.special_char_count}
            </span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Domain Age</span>
            <span className="detail-value">
              {result.details.domain_age > 0.5 ? 'Established' : 'New'}
            </span>
          </div>
        </div>
      </div>

      <div className="scanned-url">
        <strong>🌐 Scanned URL:</strong> 
        <br />
        <span style={{ wordBreak: 'break-all' }}>{result.url}</span>
      </div>
      
      <div style={{ 
        marginTop: '1rem', 
        padding: '1rem', 
        background: '#fffbeb', 
        borderRadius: '8px',
        fontSize: '0.85rem',
        color: '#92400e',
        borderLeft: '4px solid #f59e0b'
      }}>
        <strong>⚡ Note:</strong> This analysis is performed by an AI model and should be used 
        as one of many factors in assessing website security. Always exercise caution when 
        visiting unfamiliar websites.
      </div>
    </div>
  );
};

export default ThreatReport;