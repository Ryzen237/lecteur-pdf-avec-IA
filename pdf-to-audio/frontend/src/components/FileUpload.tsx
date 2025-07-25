import React, { useState, useRef } from 'react';
import { FileUploadProps } from '../types';
import apiService from '../services/api';
import './FileUpload.css';

const FileUpload: React.FC<FileUploadProps> = ({ onFileUpload, isUploading }) => {
  const [dragOver, setDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelection(files[0]);
    }
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileSelection(files[0]);
    }
  };

  const handleFileSelection = (file: File) => {
    // Validation du fichier
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      alert('Veuillez sélectionner un fichier PDF.');
      return;
    }

    if (file.size > 50 * 1024 * 1024) { // 50MB
      alert('Le fichier est trop volumineux. Taille maximale : 50MB.');
      return;
    }

    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    try {
      const response = await apiService.uploadPDF(selectedFile);
      onFileUpload(response.task_id);
      setSelectedFile(null);
      
      // Réinitialiser l'input file
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (error) {
      alert(error instanceof Error ? error.message : 'Erreur lors de l\'upload');
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="file-upload-container">
      <div
        className={`drop-zone ${dragOver ? 'drag-over' : ''} ${selectedFile ? 'has-file' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleBrowseClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleFileInputChange}
          style={{ display: 'none' }}
          disabled={isUploading}
        />

        {!selectedFile ? (
          <div className="drop-zone-content">
            <div className="upload-icon">📄</div>
            <h3>Glissez-déposez votre PDF ici</h3>
            <p>ou <span className="browse-link">cliquez pour parcourir</span></p>
            <div className="file-requirements">
              <small>
                • Format accepté : PDF uniquement<br />
                • Taille maximale : 50MB<br />
                • Le fichier sera traité automatiquement
              </small>
            </div>
          </div>
        ) : (
          <div className="selected-file">
            <div className="file-icon">📄</div>
            <div className="file-info">
              <div className="file-name">{selectedFile.name}</div>
              <div className="file-size">{formatFileSize(selectedFile.size)}</div>
            </div>
            <button
              className="remove-file"
              onClick={(e) => {
                e.stopPropagation();
                setSelectedFile(null);
                if (fileInputRef.current) {
                  fileInputRef.current.value = '';
                }
              }}
              disabled={isUploading}
            >
              ×
            </button>
          </div>
        )}
      </div>

      {selectedFile && (
        <div className="upload-actions">
          <button
            className="upload-button"
            onClick={handleUpload}
            disabled={isUploading}
          >
            {isUploading ? (
              <>
                <span className="spinner">⏳</span>
                Téléchargement...
              </>
            ) : (
              <>
                🚀 Convertir en audio
              </>
            )}
          </button>
        </div>
      )}

      <div className="upload-info">
        <div className="info-item">
          <span className="info-icon">🔒</span>
          <span>Vos fichiers sont traités de manière sécurisée</span>
        </div>
        <div className="info-item">
          <span className="info-icon">⚡</span>
          <span>Conversion automatique avec l'IA</span>
        </div>
        <div className="info-item">
          <span className="info-icon">🗑️</span>
          <span>Fichiers supprimés automatiquement après traitement</span>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;