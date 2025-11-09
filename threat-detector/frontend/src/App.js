import React from 'react';
import URLScanner from './components/URLScanner';
import './styles/App.css';

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <h1>🛡️ Cyber Threat Detector</h1>
          <p className="subtitle">AI-Powered Real-Time URL Security Analysis</p>
        </div>
      </header>
      
      <main className="app-main">
        <URLScanner />
      </main>
      
      <footer className="app-footer">
        <p>Powered by Transformer AI Model | Real-Time Threat Detection</p>
        <p style={{ fontSize: '0.8rem', marginTop: '0.5rem', opacity: 0.8 }}>
          © 2024 Cyber Threat Detector - For Educational Purposes
        </p>
      </footer>
    </div>
  );
}

export default App;