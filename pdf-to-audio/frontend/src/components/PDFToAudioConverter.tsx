import React, { useState, useEffect } from 'react';
import { TaskStatus } from '../types';
import apiService from '../services/api';
import FileUpload from './FileUpload';
import ProgressIndicator from './ProgressIndicator';
import AudioReady from './AudioReady';
import './PDFToAudioConverter.css';

const PDFToAudioConverter: React.FC = () => {
  const [currentTask, setCurrentTask] = useState<TaskStatus | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isApiHealthy, setIsApiHealthy] = useState(true);

  // Vérification de l'état de l'API au démarrage
  useEffect(() => {
    checkApiHealth();
  }, []);

  // Polling pour mettre à jour le statut de la tâche
  useEffect(() => {
    let interval: NodeJS.Timeout;

    if (currentTask && (currentTask.status === 'uploaded' || currentTask.status === 'processing')) {
      interval = setInterval(async () => {
        try {
          const updatedTask = await apiService.getTaskStatus(currentTask.id);
          setCurrentTask(updatedTask);

          // Arrêter le polling si la tâche est terminée
          if (updatedTask.status === 'completed' || updatedTask.status === 'error') {
            clearInterval(interval);
          }
        } catch (err) {
          console.error('Erreur lors de la mise à jour du statut:', err);
          setError('Erreur lors de la mise à jour du statut');
        }
      }, 2000); // Vérifier toutes les 2 secondes
    }

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [currentTask]);

  const checkApiHealth = async () => {
    try {
      await apiService.healthCheck();
      setIsApiHealthy(true);
    } catch (err) {
      setIsApiHealthy(false);
      setError('Le serveur backend n\'est pas disponible. Veuillez le démarrer.');
    }
  };

  const handleFileUpload = async (taskId: string) => {
    setIsUploading(true);
    setError(null);

    try {
      // Récupérer le statut initial de la tâche
      const task = await apiService.getTaskStatus(taskId);
      setCurrentTask(task);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors de l\'upload');
    } finally {
      setIsUploading(false);
    }
  };

  const handleNewUpload = () => {
    setCurrentTask(null);
    setError(null);
  };

  const handleRetry = () => {
    setError(null);
    checkApiHealth();
  };

  // Affichage d'erreur de connexion API
  if (!isApiHealthy) {
    return (
      <div className="converter-container">
        <div className="error-container">
          <div className="error-icon">⚠️</div>
          <h2>Connexion impossible</h2>
          <p>{error}</p>
          <div className="error-actions">
            <button onClick={handleRetry} className="retry-button">
              🔄 Réessayer
            </button>
          </div>
          <div className="help-text">
            <p><strong>Pour démarrer le backend :</strong></p>
            <code>cd pdf-to-audio/backend && python main.py</code>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="converter-container">
      {error && (
        <div className="error-message">
          <span className="error-icon">❌</span>
          {error}
          <button onClick={() => setError(null)} className="close-error">×</button>
        </div>
      )}

      {!currentTask && (
        <div className="upload-section">
          <div className="welcome-message">
            <h2>📄 Convertissez votre PDF en audio</h2>
            <p>Téléchargez un fichier PDF et notre IA le convertira en audio pour vous.</p>
            <ul className="features-list">
              <li>✨ Conversion automatique avec l'IA</li>
              <li>🎵 Audio de haute qualité</li>
              <li>⚡ Traitement rapide</li>
              <li>🔒 Sécurisé et privé</li>
            </ul>
          </div>
          <FileUpload onFileUpload={handleFileUpload} isUploading={isUploading} />
        </div>
      )}

      {currentTask && currentTask.status !== 'completed' && (
        <ProgressIndicator task={currentTask} />
      )}

      {currentTask && currentTask.status === 'completed' && (
        <AudioReady task={currentTask} onNewUpload={handleNewUpload} />
      )}
    </div>
  );
};

export default PDFToAudioConverter;