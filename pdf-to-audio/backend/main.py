from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import uuid
import asyncio
from pathlib import Path
import logging
from typing import Dict, Any
import json
from datetime import datetime

from pdf_processor import PDFProcessor
from audio_generator import AudioGenerator

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation de l'application FastAPI
app = FastAPI(
    title="PDF to Audio Converter",
    description="Convertit des fichiers PDF en audio avec l'IA",
    version="1.0.0"
)

# Configuration CORS pour permettre les requêtes depuis React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dossiers de stockage
UPLOAD_DIR = Path("../uploads")
AUDIO_DIR = Path("../audio")
UPLOAD_DIR.mkdir(exist_ok=True)
AUDIO_DIR.mkdir(exist_ok=True)

# Servir les fichiers audio statiques
app.mount("/audio", StaticFiles(directory=str(AUDIO_DIR)), name="audio")

# Stockage en mémoire des tâches (en production, utiliser Redis ou une base de données)
tasks: Dict[str, Dict[str, Any]] = {}

# Initialisation des services
pdf_processor = PDFProcessor()
audio_generator = AudioGenerator()

@app.on_event("startup")
async def startup_event():
    """Initialisation au démarrage de l'application"""
    logger.info("🚀 Démarrage du serveur PDF-to-Audio")
    logger.info(f"📁 Dossier uploads: {UPLOAD_DIR.absolute()}")
    logger.info(f"🔊 Dossier audio: {AUDIO_DIR.absolute()}")

@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "message": "PDF to Audio Converter API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Vérification de l'état de santé de l'API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "pdf_processor": "ready",
            "audio_generator": "ready"
        }
    }

async def process_pdf_to_audio(task_id: str, file_path: str, filename: str):
    """Traitement asynchrone du PDF vers audio"""
    try:
        logger.info(f"🔄 Début du traitement pour la tâche {task_id}")
        
        # Mise à jour du statut
        tasks[task_id]["status"] = "processing"
        tasks[task_id]["stage"] = "Extraction du texte du PDF..."
        
        # 1. Extraction du texte du PDF
        text_content = await pdf_processor.extract_text(file_path)
        if not text_content.strip():
            raise Exception("Aucun texte trouvé dans le PDF")
        
        logger.info(f"📄 Texte extrait: {len(text_content)} caractères")
        
        # Mise à jour du statut
        tasks[task_id]["stage"] = "Génération de l'audio avec l'IA..."
        tasks[task_id]["progress"] = 50
        
        # 2. Génération de l'audio avec l'IA
        audio_filename = f"{task_id}.mp3"
        audio_path = AUDIO_DIR / audio_filename
        
        await audio_generator.text_to_speech(text_content, str(audio_path))
        
        # Mise à jour du statut final
        tasks[task_id].update({
            "status": "completed",
            "stage": "Terminé",
            "progress": 100,
            "audio_url": f"/audio/{audio_filename}",
            "audio_filename": audio_filename,
            "completed_at": datetime.now().isoformat()
        })
        
        logger.info(f"✅ Traitement terminé pour la tâche {task_id}")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du traitement {task_id}: {str(e)}")
        tasks[task_id].update({
            "status": "error",
            "stage": f"Erreur: {str(e)}",
            "error": str(e)
        })

@app.post("/upload")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """Upload et traitement d'un fichier PDF"""
    
    # Validation du fichier
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Seuls les fichiers PDF sont acceptés"
        )
    
    if file.size and file.size > 50 * 1024 * 1024:  # 50MB max
        raise HTTPException(
            status_code=400,
            detail="Le fichier est trop volumineux (max 50MB)"
        )
    
    try:
        # Génération d'un ID unique pour la tâche
        task_id = str(uuid.uuid4())
        
        # Sauvegarde du fichier
        file_path = UPLOAD_DIR / f"{task_id}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Initialisation de la tâche
        tasks[task_id] = {
            "id": task_id,
            "filename": file.filename,
            "status": "uploaded",
            "stage": "Fichier téléchargé",
            "progress": 0,
            "created_at": datetime.now().isoformat()
        }
        
        # Lancement du traitement en arrière-plan
        background_tasks.add_task(
            process_pdf_to_audio,
            task_id,
            str(file_path),
            file.filename
        )
        
        logger.info(f"📤 Fichier uploadé: {file.filename} (tâche: {task_id})")
        
        return {
            "task_id": task_id,
            "message": "Fichier téléchargé avec succès",
            "filename": file.filename,
            "status": "uploaded"
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'upload: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du traitement du fichier: {str(e)}"
        )

@app.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """Récupération du statut d'une tâche"""
    
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Tâche non trouvée"
        )
    
    return tasks[task_id]

@app.get("/download/{task_id}")
async def download_audio(task_id: str):
    """Téléchargement du fichier audio généré"""
    
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Tâche non trouvée"
        )
    
    task = tasks[task_id]
    
    if task["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail="Le fichier audio n'est pas encore prêt"
        )
    
    audio_path = AUDIO_DIR / task["audio_filename"]
    
    if not audio_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Fichier audio non trouvé"
        )
    
    return FileResponse(
        path=str(audio_path),
        filename=f"{task['filename']}.mp3",
        media_type="audio/mpeg"
    )

@app.delete("/task/{task_id}")
async def delete_task(task_id: str):
    """Suppression d'une tâche et de ses fichiers associés"""
    
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Tâche non trouvée"
        )
    
    task = tasks[task_id]
    
    # Suppression des fichiers
    try:
        # Fichier PDF uploadé
        pdf_files = list(UPLOAD_DIR.glob(f"{task_id}_*"))
        for pdf_file in pdf_files:
            pdf_file.unlink(missing_ok=True)
        
        # Fichier audio généré
        if "audio_filename" in task:
            audio_path = AUDIO_DIR / task["audio_filename"]
            audio_path.unlink(missing_ok=True)
        
        # Suppression de la tâche
        del tasks[task_id]
        
        logger.info(f"🗑️ Tâche {task_id} supprimée")
        
        return {"message": "Tâche supprimée avec succès"}
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la suppression: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la suppression: {str(e)}"
        )

@app.get("/tasks")
async def list_tasks():
    """Liste de toutes les tâches"""
    return {
        "tasks": list(tasks.values()),
        "total": len(tasks)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )