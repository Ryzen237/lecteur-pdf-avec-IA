import React, { useState, useRef, useEffect } from 'react';
import { AudioReadyProps } from '../types';
import apiService from '../services/api';
import './AudioReady.css';

const AudioReady: React.FC<AudioReadyProps> = ({ task, onNewUpload }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [playbackRate, setPlaybackRate] = useState(1);
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handleLoadedMetadata = () => {
      setDuration(audio.duration);
    };

    const handleTimeUpdate = () => {
      setCurrentTime(audio.currentTime);
    };

    const handleEnded = () => {
      setIsPlaying(false);
      setCurrentTime(0);
    };

    audio.addEventListener('loadedmetadata', handleLoadedMetadata);
    audio.addEventListener('timeupdate', handleTimeUpdate);
    audio.addEventListener('ended', handleEnded);

    return () => {
      audio.removeEventListener('loadedmetadata', handleLoadedMetadata);
      audio.removeEventListener('timeupdate', handleTimeUpdate);
      audio.removeEventListener('ended', handleEnded);
    };
  }, []);

  const togglePlayPause = () => {
    const audio = audioRef.current;
    if (!audio) return;

    if (isPlaying) {
      audio.pause();
    } else {
      audio.play();
    }
    setIsPlaying(!isPlaying);
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const audio = audioRef.current;
    if (!audio) return;

    const newTime = parseFloat(e.target.value);
    audio.currentTime = newTime;
    setCurrentTime(newTime);
  };

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const audio = audioRef.current;
    if (!audio) return;

    const newVolume = parseFloat(e.target.value);
    audio.volume = newVolume;
    setVolume(newVolume);
  };

  const handlePlaybackRateChange = (rate: number) => {
    const audio = audioRef.current;
    if (!audio) return;

    audio.playbackRate = rate;
    setPlaybackRate(rate);
  };

  const handleDownload = async () => {
    try {
      const blob = await apiService.downloadAudio(task.id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${task.filename}.mp3`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      alert('Erreur lors du téléchargement');
    }
  };

  const formatTime = (time: number): string => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleString('fr-FR');
  };

  const audioUrl = task.audio_url ? apiService.getAudioUrl(task.audio_url) : '';

  return (
    <div className="audio-ready-container">
      <div className="success-header">
        <div className="success-icon">✅</div>
        <h2>Fichier prêt à écouter !</h2>
        <p>Votre PDF a été converti en audio avec succès</p>
      </div>

      <div className="file-summary">
        <div className="file-info">
          <span className="file-icon">📄</span>
          <div className="file-details">
            <h3 className="file-name">{task.filename}</h3>
            <div className="file-meta">
              <span>Converti le {formatDate(task.completed_at!)}</span>
              <span>•</span>
              <span>Durée: {formatTime(duration)}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="audio-player">
        <audio
          ref={audioRef}
          src={audioUrl}
          preload="metadata"
        />

        <div className="player-controls">
          <button 
            className="play-pause-btn"
            onClick={togglePlayPause}
          >
            {isPlaying ? '⏸️' : '▶️'}
          </button>

          <div className="time-display">
            {formatTime(currentTime)}
          </div>

          <div className="progress-container">
            <input
              type="range"
              className="progress-slider"
              min="0"
              max={duration || 0}
              value={currentTime}
              onChange={handleSeek}
            />
          </div>

          <div className="time-display">
            {formatTime(duration)}
          </div>

          <div className="volume-control">
            <span className="volume-icon">🔊</span>
            <input
              type="range"
              className="volume-slider"
              min="0"
              max="1"
              step="0.1"
              value={volume}
              onChange={handleVolumeChange}
            />
          </div>
        </div>

        <div className="player-options">
          <div className="playback-speed">
            <span className="option-label">Vitesse:</span>
            <div className="speed-buttons">
              {[0.5, 0.75, 1, 1.25, 1.5, 2].map((rate) => (
                <button
                  key={rate}
                  className={`speed-btn ${playbackRate === rate ? 'active' : ''}`}
                  onClick={() => handlePlaybackRateChange(rate)}
                >
                  {rate}x
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="action-buttons">
        <button 
          className="download-btn"
          onClick={handleDownload}
        >
          💾 Télécharger l'audio
        </button>

        <button 
          className="new-upload-btn"
          onClick={onNewUpload}
        >
          📄 Convertir un nouveau PDF
        </button>
      </div>

      <div className="audio-info">
        <div className="info-grid">
          <div className="info-item">
            <span className="info-icon">🎵</span>
            <div className="info-content">
              <div className="info-title">Format Audio</div>
              <div className="info-value">MP3, Haute qualité</div>
            </div>
          </div>
          
          <div className="info-item">
            <span className="info-icon">🤖</span>
            <div className="info-content">
              <div className="info-title">Technologie</div>
              <div className="info-value">IA Text-to-Speech</div>
            </div>
          </div>
          
          <div className="info-item">
            <span className="info-icon">🔒</span>
            <div className="info-content">
              <div className="info-title">Confidentialité</div>
              <div className="info-value">Fichiers supprimés automatiquement</div>
            </div>
          </div>
        </div>
      </div>

      <div className="tips">
        <h4>💡 Conseils d'écoute</h4>
        <ul>
          <li>Utilisez les contrôles de vitesse pour adapter la lecture à votre rythme</li>
          <li>Téléchargez le fichier pour l'écouter hors ligne</li>
          <li>La qualité audio est optimisée pour une écoute prolongée</li>
        </ul>
      </div>
    </div>
  );
};

export default AudioReady;