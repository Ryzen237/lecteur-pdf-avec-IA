import asyncio
import logging
from pathlib import Path
from typing import Optional
import os
import tempfile
import subprocess

# Essayer d'importer les modules TTS
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

logger = logging.getLogger(__name__)

class AudioGenerator:
    """Classe pour générer de l'audio à partir de texte avec différentes méthodes TTS"""
    
    def __init__(self):
        self.preferred_method = self._detect_best_method()
        logger.info(f"🎤 Méthode TTS sélectionnée: {self.preferred_method}")
        
    def _detect_best_method(self) -> str:
        """Détecte la meilleure méthode TTS disponible"""
        if EDGE_TTS_AVAILABLE:
            return "edge_tts"  # Meilleure qualité
        elif GTTS_AVAILABLE:
            return "gtts"      # Bonne qualité, nécessite internet
        elif PYTTSX3_AVAILABLE:
            return "pyttsx3"   # Qualité basique, fonctionne hors ligne
        else:
            return "fallback"  # Méthode de secours
    
    async def text_to_speech(self, text: str, output_path: str) -> None:
        """
        Convertit le texte en audio
        
        Args:
            text: Texte à convertir
            output_path: Chemin de sortie du fichier audio
        """
        if not text.strip():
            raise Exception("Le texte est vide")
        
        logger.info(f"🔊 Génération audio avec {self.preferred_method}")
        logger.info(f"📝 Texte: {len(text)} caractères")
        
        try:
            if self.preferred_method == "edge_tts":
                await self._generate_with_edge_tts(text, output_path)
            elif self.preferred_method == "gtts":
                await self._generate_with_gtts(text, output_path)
            elif self.preferred_method == "pyttsx3":
                await self._generate_with_pyttsx3(text, output_path)
            else:
                await self._generate_fallback(text, output_path)
                
            logger.info(f"✅ Audio généré: {output_path}")
            
        except Exception as e:
            logger.error(f"❌ Erreur génération audio: {str(e)}")
            # Essayer une méthode de fallback
            await self._generate_fallback(text, output_path)
    
    async def _generate_with_edge_tts(self, text: str, output_path: str) -> None:
        """Génération avec Edge TTS (Microsoft) - Haute qualité"""
        try:
            # Voix française de qualité
            voice = "fr-FR-DeniseNeural"  # Voix féminine française
            
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_path)
            
        except Exception as e:
            logger.error(f"Erreur Edge TTS: {str(e)}")
            raise
    
    async def _generate_with_gtts(self, text: str, output_path: str) -> None:
        """Génération avec Google TTS - Bonne qualité"""
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._gtts_sync, text, output_path)
            
        except Exception as e:
            logger.error(f"Erreur Google TTS: {str(e)}")
            raise
    
    def _gtts_sync(self, text: str, output_path: str) -> None:
        """Génération synchrone avec gTTS"""
        # Diviser le texte en chunks si trop long (gTTS a une limite)
        max_length = 5000
        chunks = []
        
        if len(text) <= max_length:
            chunks = [text]
        else:
            # Diviser par phrases
            sentences = text.split('. ')
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk + sentence) <= max_length:
                    current_chunk += sentence + ". "
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence + ". "
            
            if current_chunk:
                chunks.append(current_chunk.strip())
        
        # Générer l'audio pour chaque chunk
        temp_files = []
        
        try:
            for i, chunk in enumerate(chunks):
                tts = gTTS(text=chunk, lang='fr', slow=False)
                temp_path = f"{output_path}.temp_{i}.mp3"
                tts.save(temp_path)
                temp_files.append(temp_path)
            
            # Combiner les fichiers si plusieurs chunks
            if len(temp_files) == 1:
                os.rename(temp_files[0], output_path)
            else:
                self._combine_audio_files(temp_files, output_path)
                
        finally:
            # Nettoyer les fichiers temporaires
            for temp_file in temp_files:
                if os.path.exists(temp_file) and temp_file != output_path:
                    os.remove(temp_file)
    
    async def _generate_with_pyttsx3(self, text: str, output_path: str) -> None:
        """Génération avec pyttsx3 - Qualité basique mais hors ligne"""
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._pyttsx3_sync, text, output_path)
            
        except Exception as e:
            logger.error(f"Erreur pyttsx3: {str(e)}")
            raise
    
    def _pyttsx3_sync(self, text: str, output_path: str) -> None:
        """Génération synchrone avec pyttsx3"""
        engine = pyttsx3.init()
        
        # Configuration de la voix
        voices = engine.getProperty('voices')
        
        # Chercher une voix française
        french_voice = None
        for voice in voices:
            if 'french' in voice.name.lower() or 'fr' in voice.id.lower():
                french_voice = voice.id
                break
        
        if french_voice:
            engine.setProperty('voice', french_voice)
        
        # Configuration de la vitesse et du volume
        engine.setProperty('rate', 180)  # Vitesse de parole
        engine.setProperty('volume', 0.9)  # Volume
        
        # Sauvegarder en fichier
        engine.save_to_file(text, output_path)
        engine.runAndWait()
    
    async def _generate_fallback(self, text: str, output_path: str) -> None:
        """Méthode de fallback si aucune TTS n'est disponible"""
        logger.warning("⚠️ Aucune TTS disponible, génération d'un fichier audio de test")
        
        # Créer un fichier audio silencieux comme fallback
        try:
            # Utiliser ffmpeg si disponible pour créer un fichier audio silencieux
            duration = min(len(text) * 0.1, 300)  # ~0.1s par caractère, max 5 minutes
            
            cmd = [
                'ffmpeg', '-f', 'lavfi', '-i', f'anullsrc=duration={duration}',
                '-c:a', 'mp3', '-b:a', '128k', '-y', output_path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await process.communicate()
            
            if process.returncode == 0:
                logger.info("📢 Fichier audio silencieux créé (fallback)")
            else:
                raise Exception("Échec de la génération fallback")
                
        except Exception as e:
            logger.error(f"Erreur fallback: {str(e)}")
            # Dernière tentative: créer un fichier vide
            Path(output_path).touch()
            raise Exception("Impossible de générer l'audio. Veuillez installer un moteur TTS.")
    
    def _combine_audio_files(self, file_list: list, output_path: str) -> None:
        """Combine plusieurs fichiers audio en un seul"""
        try:
            # Utiliser ffmpeg pour combiner les fichiers
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                for file_path in file_list:
                    f.write(f"file '{file_path}'\n")
                concat_file = f.name
            
            cmd = [
                'ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_file,
                '-c', 'copy', '-y', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            os.unlink(concat_file)
            
            if result.returncode != 0:
                logger.warning("Échec de la combinaison, utilisation du premier fichier")
                os.rename(file_list[0], output_path)
                
        except Exception as e:
            logger.warning(f"Erreur combinaison: {str(e)}, utilisation du premier fichier")
            if file_list:
                os.rename(file_list[0], output_path)
    
    def get_available_voices(self) -> list:
        """Retourne la liste des voix disponibles"""
        voices = []
        
        try:
            if self.preferred_method == "edge_tts":
                # Quelques voix Edge TTS françaises populaires
                voices = [
                    {"id": "fr-FR-DeniseNeural", "name": "Denise (Française)", "gender": "female"},
                    {"id": "fr-FR-HenriNeural", "name": "Henri (Français)", "gender": "male"},
                    {"id": "fr-CA-SylvieNeural", "name": "Sylvie (Canadienne)", "gender": "female"},
                ]
            elif self.preferred_method == "pyttsx3":
                engine = pyttsx3.init()
                system_voices = engine.getProperty('voices')
                for voice in system_voices:
                    voices.append({
                        "id": voice.id,
                        "name": voice.name,
                        "gender": "unknown"
                    })
                engine.stop()
            else:
                voices = [{"id": "fr", "name": "Français (Google)", "gender": "female"}]
                
        except Exception as e:
            logger.error(f"Erreur récupération voix: {str(e)}")
        
        return voices
    
    def get_status(self) -> dict:
        """Retourne le statut du générateur audio"""
        return {
            "method": self.preferred_method,
            "available_engines": {
                "edge_tts": EDGE_TTS_AVAILABLE,
                "gtts": GTTS_AVAILABLE,
                "pyttsx3": PYTTSX3_AVAILABLE
            },
            "status": "ready"
        }