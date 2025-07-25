import React from 'react';
import { ProgressIndicatorProps } from '../types';
import './ProgressIndicator.css';

const ProgressIndicator: React.FC<ProgressIndicatorProps> = ({ task }) => {
  const getProgressPercentage = (): number => {
    if (task.status === 'uploaded') return 10;
    if (task.status === 'processing') return task.progress || 50;
    if (task.status === 'completed') return 100;
    return 0;
  };

  const getStatusIcon = (): string => {
    switch (task.status) {
      case 'uploaded':
        return '📤';
      case 'processing':
        return '⚙️';
      case 'error':
        return '❌';
      default:
        return '⏳';
    }
  };

  const getStatusColor = (): string => {
    switch (task.status) {
      case 'uploaded':
        return '#3498db';
      case 'processing':
        return '#f39c12';
      case 'error':
        return '#e74c3c';
      default:
        return '#95a5a6';
    }
  };

  const formatTime = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('fr-FR');
  };

  const getEstimatedTime = (): string => {
    if (task.status === 'uploaded') {
      return 'Démarrage du traitement...';
    }
    if (task.status === 'processing') {
      const progress = task.progress || 0;
      if (progress < 30) return 'Environ 2-3 minutes restantes';
      if (progress < 70) return 'Environ 1-2 minutes restantes';
      return 'Presque terminé...';
    }
    return '';
  };

  return (
    <div className="progress-container">
      <div className="progress-header">
        <div className="file-info">
          <span className="file-icon">📄</span>
          <div className="file-details">
            <h3 className="file-name">{task.filename}</h3>
            <p className="upload-time">
              Téléchargé à {formatTime(task.created_at)}
            </p>
          </div>
        </div>
        <div className="status-badge" style={{ backgroundColor: getStatusColor() }}>
          <span className="status-icon">{getStatusIcon()}</span>
          <span className="status-text">{task.stage}</span>
        </div>
      </div>

      <div className="progress-content">
        <div className="progress-bar-container">
          <div className="progress-bar">
            <div 
              className="progress-fill"
              style={{ 
                width: `${getProgressPercentage()}%`,
                backgroundColor: getStatusColor()
              }}
            />
          </div>
          <div className="progress-percentage">
            {getProgressPercentage()}%
          </div>
        </div>

        <div className="progress-details">
          <div className="current-stage">
            <span className="stage-icon">🔄</span>
            <span className="stage-text">{task.stage}</span>
          </div>
          
          {task.status !== 'error' && (
            <div className="estimated-time">
              <span className="time-icon">⏱️</span>
              <span className="time-text">{getEstimatedTime()}</span>
            </div>
          )}
        </div>

        {task.status === 'processing' && (
          <div className="processing-animation">
            <div className="processing-steps">
              <div className={`step ${task.progress >= 20 ? 'completed' : 'active'}`}>
                <span className="step-icon">📄</span>
                <span className="step-label">Lecture du PDF</span>
              </div>
              <div className={`step ${task.progress >= 60 ? 'completed' : task.progress >= 20 ? 'active' : ''}`}>
                <span className="step-icon">🤖</span>
                <span className="step-label">Traitement IA</span>
              </div>
              <div className={`step ${task.progress >= 90 ? 'completed' : task.progress >= 60 ? 'active' : ''}`}>
                <span className="step-icon">🎵</span>
                <span className="step-label">Génération audio</span>
              </div>
            </div>
          </div>
        )}

        {task.status === 'error' && (
          <div className="error-details">
            <div className="error-icon">⚠️</div>
            <div className="error-message">
              <h4>Erreur lors du traitement</h4>
              <p>{task.error || 'Une erreur inattendue s\'est produite'}</p>
            </div>
          </div>
        )}
      </div>

      <div className="progress-footer">
        <div className="progress-info">
          <span className="info-text">
            {task.status === 'processing' 
              ? 'Votre fichier est en cours de traitement. Vous pouvez fermer cette page et revenir plus tard.'
              : 'Le traitement va commencer sous peu...'
            }
          </span>
        </div>
      </div>
    </div>
  );
};

export default ProgressIndicator;