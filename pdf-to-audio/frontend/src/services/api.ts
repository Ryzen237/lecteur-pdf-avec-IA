// Service API pour communiquer avec le backend FastAPI

import { TaskStatus, UploadResponse, ApiError } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Upload d'un fichier PDF
   */
  async uploadPDF(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.detail || 'Erreur lors de l\'upload');
    }

    return response.json();
  }

  /**
   * Récupération du statut d'une tâche
   */
  async getTaskStatus(taskId: string): Promise<TaskStatus> {
    const response = await fetch(`${this.baseUrl}/status/${taskId}`);

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.detail || 'Erreur lors de la récupération du statut');
    }

    return response.json();
  }

  /**
   * Téléchargement du fichier audio
   */
  async downloadAudio(taskId: string): Promise<Blob> {
    const response = await fetch(`${this.baseUrl}/download/${taskId}`);

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.detail || 'Erreur lors du téléchargement');
    }

    return response.blob();
  }

  /**
   * Suppression d'une tâche
   */
  async deleteTask(taskId: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}/task/${taskId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.detail || 'Erreur lors de la suppression');
    }
  }

  /**
   * Vérification de l'état de santé de l'API
   */
  async healthCheck(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/health`);
    
    if (!response.ok) {
      throw new Error('API non disponible');
    }

    return response.json();
  }

  /**
   * Construction de l'URL complète pour l'audio
   */
  getAudioUrl(audioPath: string): string {
    return `${this.baseUrl}${audioPath}`;
  }
}

// Instance singleton du service API
export const apiService = new ApiService();
export default apiService;