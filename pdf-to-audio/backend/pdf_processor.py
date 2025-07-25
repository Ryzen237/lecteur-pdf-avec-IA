import asyncio
import logging
from pathlib import Path
from typing import Optional
import fitz  # PyMuPDF
import io

logger = logging.getLogger(__name__)

class PDFProcessor:
    """Classe pour traiter et extraire le texte des fichiers PDF"""
    
    def __init__(self):
        self.max_pages = 100  # Limite pour éviter les PDFs trop longs
        
    async def extract_text(self, file_path: str) -> str:
        """
        Extrait le texte d'un fichier PDF de manière asynchrone
        
        Args:
            file_path: Chemin vers le fichier PDF
            
        Returns:
            Texte extrait du PDF
        """
        try:
            # Exécuter l'extraction dans un thread pour ne pas bloquer
            loop = asyncio.get_event_loop()
            text = await loop.run_in_executor(None, self._extract_text_sync, file_path)
            return text
            
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction du PDF {file_path}: {str(e)}")
            raise Exception(f"Impossible d'extraire le texte du PDF: {str(e)}")
    
    def _extract_text_sync(self, file_path: str) -> str:
        """
        Extraction synchrone du texte du PDF
        
        Args:
            file_path: Chemin vers le fichier PDF
            
        Returns:
            Texte extrait
        """
        text_content = []
        
        try:
            # Ouvrir le document PDF
            doc = fitz.open(file_path)
            
            logger.info(f"📄 PDF ouvert: {len(doc)} pages")
            
            # Limiter le nombre de pages pour éviter les traitements trop longs
            max_pages = min(len(doc), self.max_pages)
            
            if len(doc) > self.max_pages:
                logger.warning(f"⚠️ PDF tronqué à {self.max_pages} pages (total: {len(doc)})")
            
            # Extraire le texte de chaque page
            for page_num in range(max_pages):
                try:
                    page = doc[page_num]
                    page_text = page.get_text()
                    
                    if page_text.strip():
                        text_content.append(page_text)
                        logger.debug(f"Page {page_num + 1}: {len(page_text)} caractères extraits")
                    else:
                        logger.debug(f"Page {page_num + 1}: aucun texte trouvé")
                        
                except Exception as e:
                    logger.warning(f"Erreur page {page_num + 1}: {str(e)}")
                    continue
            
            # Fermer le document
            doc.close()
            
            # Joindre tout le texte
            full_text = "\n\n".join(text_content)
            
            # Nettoyage du texte
            cleaned_text = self._clean_text(full_text)
            
            logger.info(f"✅ Extraction terminée: {len(cleaned_text)} caractères")
            
            return cleaned_text
            
        except Exception as e:
            logger.error(f"Erreur lors de l'ouverture du PDF: {str(e)}")
            raise Exception(f"Impossible de lire le fichier PDF: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """
        Nettoie et formate le texte extrait
        
        Args:
            text: Texte brut extrait
            
        Returns:
            Texte nettoyé
        """
        if not text:
            return ""
        
        # Supprimer les caractères de contrôle problématiques
        cleaned = text.replace('\x00', '')
        
        # Normaliser les espaces et retours à la ligne
        lines = []
        for line in cleaned.split('\n'):
            line = line.strip()
            if line:
                lines.append(line)
        
        # Rejoindre avec des espaces simples
        cleaned = ' '.join(lines)
        
        # Supprimer les espaces multiples
        while '  ' in cleaned:
            cleaned = cleaned.replace('  ', ' ')
        
        # Limiter la longueur pour éviter les textes trop longs
        max_chars = 50000  # ~10-15 minutes d'audio
        if len(cleaned) > max_chars:
            logger.warning(f"⚠️ Texte tronqué à {max_chars} caractères")
            cleaned = cleaned[:max_chars] + "..."
        
        return cleaned.strip()
    
    async def get_pdf_info(self, file_path: str) -> dict:
        """
        Récupère les informations du PDF
        
        Args:
            file_path: Chemin vers le fichier PDF
            
        Returns:
            Dictionnaire avec les informations du PDF
        """
        try:
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, self._get_pdf_info_sync, file_path)
            return info
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des infos PDF: {str(e)}")
            return {}
    
    def _get_pdf_info_sync(self, file_path: str) -> dict:
        """
        Récupération synchrone des informations du PDF
        
        Args:
            file_path: Chemin vers le fichier PDF
            
        Returns:
            Dictionnaire avec les informations
        """
        try:
            doc = fitz.open(file_path)
            
            info = {
                "pages": len(doc),
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
                "subject": doc.metadata.get("subject", ""),
                "creator": doc.metadata.get("creator", ""),
                "producer": doc.metadata.get("producer", ""),
                "creation_date": doc.metadata.get("creationDate", ""),
                "modification_date": doc.metadata.get("modDate", ""),
                "encrypted": doc.is_encrypted,
                "file_size": Path(file_path).stat().st_size
            }
            
            doc.close()
            return info
            
        except Exception as e:
            logger.error(f"Erreur lors de la lecture des métadonnées: {str(e)}")
            return {}

    def validate_pdf(self, file_path: str) -> bool:
        """
        Valide qu'un fichier est bien un PDF lisible
        
        Args:
            file_path: Chemin vers le fichier
            
        Returns:
            True si le PDF est valide
        """
        try:
            doc = fitz.open(file_path)
            is_valid = len(doc) > 0
            doc.close()
            return is_valid
            
        except Exception as e:
            logger.error(f"PDF invalide {file_path}: {str(e)}")
            return False