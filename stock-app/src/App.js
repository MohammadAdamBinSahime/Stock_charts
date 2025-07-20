import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [htmlContent, setHtmlContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadHtmlFile = async () => {
      try {
        const response = await fetch('/stock_charts_collage.html');
        if (!response.ok) {
          throw new Error(`Failed to load file: ${response.status}`);
        }
        const content = await response.text();
        setHtmlContent(content);
      } catch (err) {
        setError(err.message);
        console.error('Error loading HTML file:', err);
      } finally {
        setLoading(false);
      }
    };

    loadHtmlFile();
  }, []);

  if (loading) {
    return (
      <div className="App">
        <div style={{ padding: '20px', textAlign: 'center' }}>
          <h2>Loading Stock Charts...</h2>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="App">
        <div style={{ padding: '20px', textAlign: 'center', color: 'red' }}>
          <h2>Error Loading Charts</h2>
          <p>{error}</p>
          <p>Note: Loading local files directly may require running a local server or adjusting browser security settings.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <iframe
        srcDoc={htmlContent}
        style={{
          width: '100%',
          height: '100vh',
          border: 'none'
        }}
        title="Stock Charts Collage"
      />
    </div>
  );
}

export default App;
