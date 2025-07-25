from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import PyPDF2
import openai
import os
import tempfile
import uuid
from pathlib import Path
from dotenv import load_dotenv
import io

# Charger les variables d'environnement
load_dotenv()

app = FastAPI(title="PDF Reader AI API", version="1.0.0")

# Configuration CORS pour permettre les requêtes depuis React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL du frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Dossier pour stocker les fichiers audio générés
AUDIO_DIR = Path("audio_files")
AUDIO_DIR.mkdir(exist_ok=True)

def extract_text_from_pdf(pdf_file):
    """Extraire le texte d'un fichier PDF"""
    try:
        pdf_content = pdf_file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de l'extraction du PDF: {str(e)}")

async def generate_speech(text: str, voice: str = "alloy") -> str:
    """Générer l'audio à partir du texte avec OpenAI TTS"""
    try:
        # Limiter la longueur du texte si nécessaire
        if len(text) > 4000:
            text = text[:4000] + "..."
        
        response = openai.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        # Générer un nom de fichier unique
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = AUDIO_DIR / audio_filename
        
        # Sauvegarder l'audio
        response.stream_to_file(audio_path)
        
        return audio_filename
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération audio: {str(e)}")

@app.get("/")
async def root():
    return {"message": "PDF Reader AI API"}

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...), voice: str = "alloy"):
    """Endpoint pour uploader un PDF et générer l'audio"""
    
    # Vérifier le type de fichier
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Le fichier doit être un PDF")
    
    try:
        # Extraire le texte du PDF
        text = extract_text_from_pdf(file.file)
        
        if not text:
            raise HTTPException(status_code=400, detail="Aucun texte trouvé dans le PDF")
        
        # Générer l'audio
        audio_filename = await generate_speech(text, voice)
        
        return {
            "success": True,
            "message": "PDF traité avec succès",
            "audio_filename": audio_filename,
            "text_length": len(text),
            "pages_count": text.count('\n') + 1
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """Endpoint pour récupérer un fichier audio"""
    audio_path = AUDIO_DIR / filename
    
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Fichier audio non trouvé")
    
    return FileResponse(
        audio_path,
        media_type="audio/mpeg",
        filename=filename
    )

@app.get("/voices/")
async def get_available_voices():
    """Retourner la liste des voix disponibles"""
    return {
        "voices": [
            {"id": "alloy", "name": "Alloy", "description": "Voix neutre et équilibrée"},
            {"id": "echo", "name": "Echo", "description": "Voix masculine profonde"},
            {"id": "fable", "name": "Fable", "description": "Voix expressive britannique"},
            {"id": "onyx", "name": "Onyx", "description": "Voix masculine grave"},
            {"id": "nova", "name": "Nova", "description": "Voix féminine jeune"},
            {"id": "shimmer", "name": "Shimmer", "description": "Voix féminine douce"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)