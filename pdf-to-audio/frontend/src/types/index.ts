// Types pour l'application PDF-to-Audio

export interface TaskStatus {
  id: string;
  filename: string;
  status: 'uploaded' | 'processing' | 'completed' | 'error';
  stage: string;
  progress: number;
  created_at: string;
  completed_at?: string;
  audio_url?: string;
  audio_filename?: string;
  error?: string;
}

export interface UploadResponse {
  task_id: string;
  message: string;
  filename: string;
  status: string;
}

export interface ApiError {
  detail: string;
}

export interface AudioPlayerProps {
  audioUrl: string;
  filename: string;
}

export interface FileUploadProps {
  onFileUpload: (taskId: string) => void;
  isUploading: boolean;
}

export interface ProgressIndicatorProps {
  task: TaskStatus;
}

export interface AudioReadyProps {
  task: TaskStatus;
  onNewUpload: () => void;
}