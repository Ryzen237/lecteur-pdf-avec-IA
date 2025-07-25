import React, { useState, useRef } from 'react';
import axios from 'axios';
import './App.css';

interface UploadResponse {
  success: boolean;
  message: string;
  audio_filename: string;
  text_length: number;
  pages_count: number;
}

interface Voice {
  id: string;
  name: string;
  description: string;
}

const App: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedVoice, setSelectedVoice] = useState<string>('alloy');
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null);
  const [error, setError] = useState<string>('');
  const [isDragOver, setIsDragOver] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const voices: Voice[] = [
    { id: 'alloy', name: 'Alloy', description: 'Voix neutre et équilibrée' },
    { id: 'echo', name: 'Echo', description: 'Voix masculine profonde' },
    { id: 'fable', name: 'Fable', description: 'Voix expressive britannique' },
    { id: 'onyx', name: 'Onyx', description: 'Voix masculine grave' },
    { id: 'nova', name: 'Nova', description: 'Voix féminine jeune' },
    { id: 'shimmer', name: 'Shimmer', description: 'Voix féminine douce' }
  ];

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setError('');
      setUploadResult(null);
    } else {
      setError('Veuillez sélectionner un fichier PDF valide');
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragOver(false);
    
    const file = event.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setError('');
      setUploadResult(null);
    } else {
      setError('Veuillez déposer un fichier PDF valide');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Veuillez sélectionner un fichier PDF');
      return;
    }

    setIsUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('voice', selectedVoice);

    try {
      const response = await axios.post<UploadResponse>(
        'http://localhost:8000/upload-pdf/',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      setUploadResult(response.data);
    } catch (err: any) {
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Erreur lors du traitement du fichier. Vérifiez que le backend est démarré.');
      }
    } finally {
      setIsUploading(false);
    }
  };

  const resetForm = () => {
    setSelectedFile(null);
    setUploadResult(null);
    setError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>📖🔊 PDF Reader AI</h1>
        <p>Transformez vos documents PDF en audio avec une voix IA naturelle</p>
      </header>

      <main className="app-main">
        {!uploadResult ? (
          <div className="upload-section">
            <div className="voice-selector">
              <h3>🎤 Choisissez votre voix</h3>
              <div className="voices-grid">
                {voices.map((voice) => (
                  <label key={voice.id} className="voice-option">
                    <input
                      type="radio"
                      name="voice"
                      value={voice.id}
                      checked={selectedVoice === voice.id}
                      onChange={(e) => setSelectedVoice(e.target.value)}
                    />
                    <div className="voice-info">
                      <strong>{voice.name}</strong>
                      <small>{voice.description}</small>
                    </div>
                  </label>
                ))}
              </div>
            </div>

            <div
              className={`file-upload-area ${isDragOver ? 'drag-over' : ''}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <div className="upload-icon">📄</div>
              <h3>Glissez-déposez votre PDF ici</h3>
              <p>ou cliquez pour parcourir vos fichiers</p>
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                onChange={handleFileSelect}
                style={{ display: 'none' }}
              />
            </div>

            {selectedFile && (
              <div className="selected-file">
                <div className="file-info">
                  <span className="file-icon">📄</span>
                  <div className="file-details">
                    <strong>{selectedFile.name}</strong>
                    <small>{(selectedFile.size / (1024 * 1024)).toFixed(2)} MB</small>
                  </div>
                </div>
                <button
                  className="process-button"
                  onClick={handleUpload}
                  disabled={isUploading}
                >
                  {isUploading ? '🔄 Traitement en cours...' : '🎯 Convertir en audio'}
                </button>
              </div>
            )}

            {error && (
              <div className="error-message">
                <span className="error-icon">❌</span>
                {error}
              </div>
            )}
          </div>
        ) : (
          <div className="result-section">
            <div className="success-message">
              <div className="success-icon">✅</div>
              <h2>Fichier prêt à être écouté !</h2>
              <p>{uploadResult.message}</p>
              
              <div className="file-stats">
                <div className="stat">
                  <strong>{uploadResult.pages_count}</strong>
                  <span>pages</span>
                </div>
                <div className="stat">
                  <strong>{uploadResult.text_length}</strong>
                  <span>caractères</span>
                </div>
              </div>
            </div>

            <div className="audio-player-section">
              <h3>🎧 Lecteur Audio</h3>
              <audio
                controls
                className="audio-player"
                src={`http://localhost:8000/audio/${uploadResult.audio_filename}`}
                preload="metadata"
              >
                Votre navigateur ne supporte pas le lecteur audio.
              </audio>
            </div>

            <div className="action-buttons">
              <a
                href={`http://localhost:8000/audio/${uploadResult.audio_filename}`}
                download
                className="download-button"
              >
                💾 Télécharger l'audio
              </a>
              <button
                className="reset-button"
                onClick={resetForm}
              >
                📄 Nouveau fichier
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;