import React from 'react';
import './App.css';
import PDFToAudioConverter from './components/PDFToAudioConverter';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>📄➡️🔊 PDF to Audio</h1>
        <p>Convertissez vos PDFs en audio avec l'IA</p>
      </header>
      <main className="App-main">
        <PDFToAudioConverter />
      </main>
      <footer className="App-footer">
        <p>Propulsé par FastAPI et React.js</p>
      </footer>
    </div>
  );
}

export default App;
