import streamlit as st
import PyPDF2
import openai
import os
import tempfile
import base64
from io import BytesIO
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="📖🔊 PDF Reader AI",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .upload-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #dee2e6;
        text-align: center;
        margin: 2rem 0;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #e7f3ff;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class PDFReaderAI:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def extract_text_from_pdf(self, pdf_file):
        """Extraire le texte de toutes les pages du PDF"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text_content = []
            
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text.strip():  # Ignorer les pages vides
                    text_content.append({
                        'page': page_num + 1,
                        'text': page_text.strip()
                    })
            
            return text_content
        except Exception as e:
            st.error(f"Erreur lors de l'extraction du texte : {str(e)}")
            return None
    
    def text_to_speech(self, text, voice="alloy"):
        """Convertir le texte en audio avec OpenAI TTS"""
        try:
            if not self.openai_api_key:
                st.error("Clé API OpenAI manquante. Veuillez la configurer dans les variables d'environnement.")
                return None
            
            client = openai.OpenAI(api_key=self.openai_api_key)
            
            # Limiter la taille du texte pour éviter les erreurs
            max_chars = 4000
            if len(text) > max_chars:
                text = text[:max_chars] + "..."
            
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text,
                response_format="mp3"
            )
            
            return response.content
        except Exception as e:
            st.error(f"Erreur lors de la synthèse vocale : {str(e)}")
            return None
    
    def create_audio_player(self, audio_content):
        """Créer un lecteur audio pour Streamlit"""
        if audio_content:
            audio_base64 = base64.b64encode(audio_content).decode()
            audio_html = f"""
            <audio controls style="width: 100%;">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                Votre navigateur ne supporte pas l'élément audio.
            </audio>
            """
            return audio_html
        return None

def main():
    # En-tête principal
    st.markdown("""
    <div class="main-header">
        <h1>📖🔊 PDF Reader AI</h1>
        <p>Convertissez vos fichiers PDF en audio avec une voix IA naturelle</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialiser l'outil
    pdf_reader = PDFReaderAI()
    
    # Sidebar pour la configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Configuration de l'API OpenAI
        api_key_input = st.text_input(
            "Clé API OpenAI",
            type="password",
            help="Entrez votre clé API OpenAI pour utiliser la synthèse vocale"
        )
        
        if api_key_input:
            os.environ["OPENAI_API_KEY"] = api_key_input
            pdf_reader.openai_api_key = api_key_input
            openai.api_key = api_key_input
        
        # Choix de la voix
        voice_options = {
            "Alloy (Neutre)": "alloy",
            "Echo (Masculine)": "echo", 
            "Fable (Britannique)": "fable",
            "Onyx (Profonde)": "onyx",
            "Nova (Féminine)": "nova",
            "Shimmer (Douce)": "shimmer"
        }
        
        selected_voice = st.selectbox(
            "Choisir la voix",
            list(voice_options.keys()),
            help="Sélectionnez le type de voix pour la lecture"
        )
        
        st.markdown("---")
        st.markdown("""
        ### 📋 Instructions
        1. **Uploadez** votre fichier PDF
        2. **Configurez** votre clé API OpenAI
        3. **Choisissez** une voix
        4. **Cliquez** sur "Convertir en Audio"
        5. **Écoutez** le résultat !
        """)
    
    # Zone principale
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Section d'upload
        st.markdown("""
        <div class="upload-section">
            <h3>📁 Télécharger votre PDF</h3>
            <p>Glissez-déposez ou cliquez pour sélectionner votre fichier PDF</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choisir un fichier PDF",
            type=['pdf'],
            help="Formats supportés: PDF uniquement"
        )
        
        if uploaded_file is not None:
            st.markdown(f"""
            <div class="success-message">
                ✅ <strong>Fichier chargé:</strong> {uploaded_file.name}<br>
                📊 <strong>Taille:</strong> {uploaded_file.size / 1024:.1f} KB
            </div>
            """, unsafe_allow_html=True)
            
            # Extraire le texte
            with st.spinner("🔍 Extraction du texte du PDF..."):
                text_content = pdf_reader.extract_text_from_pdf(uploaded_file)
            
            if text_content:
                st.success(f"✅ Texte extrait avec succès ! {len(text_content)} page(s) trouvée(s).")
                
                # Afficher un aperçu du contenu
                with st.expander("👀 Aperçu du contenu extrait"):
                    for page_info in text_content[:3]:  # Afficher les 3 premières pages
                        st.write(f"**Page {page_info['page']}:**")
                        preview_text = page_info['text'][:500] + "..." if len(page_info['text']) > 500 else page_info['text']
                        st.write(preview_text)
                        st.write("---")
                
                # Bouton de conversion
                if st.button("🎵 Convertir en Audio", type="primary", use_container_width=True):
                    if not pdf_reader.openai_api_key:
                        st.error("⚠️ Veuillez configurer votre clé API OpenAI dans la sidebar.")
                    else:
                        # Combiner tout le texte
                        combined_text = "\n\n".join([page['text'] for page in text_content])
                        
                        with st.spinner("🎤 Génération de l'audio en cours..."):
                            audio_content = pdf_reader.text_to_speech(
                                combined_text, 
                                voice_options[selected_voice]
                            )
                        
                        if audio_content:
                            st.success("🎉 Audio généré avec succès !")
                            
                            # Lecteur audio
                            audio_html = pdf_reader.create_audio_player(audio_content)
                            if audio_html:
                                st.markdown("### 🔊 Écoutez votre PDF")
                                st.markdown(audio_html, unsafe_allow_html=True)
                                
                                # Bouton de téléchargement
                                st.download_button(
                                    label="💾 Télécharger l'audio (MP3)",
                                    data=audio_content,
                                    file_name=f"{uploaded_file.name.replace('.pdf', '')}_audio.mp3",
                                    mime="audio/mp3"
                                )
    
    with col2:
        # Informations et conseils
        st.markdown("""
        <div class="info-box">
            <h4>💡 Conseils d'utilisation</h4>
            <ul>
                <li><strong>Qualité PDF:</strong> Les PDFs avec du texte sélectionnable donnent de meilleurs résultats</li>
                <li><strong>Taille:</strong> Les fichiers volumineux peuvent prendre plus de temps à traiter</li>
                <li><strong>Voix:</strong> Testez différentes voix pour trouver celle qui vous convient</li>
                <li><strong>API:</strong> Vous avez besoin d'une clé API OpenAI valide</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Statistiques (si fichier uploadé)
        if uploaded_file is not None and 'text_content' in locals():
            st.markdown("### 📊 Statistiques")
            total_chars = sum(len(page['text']) for page in text_content)
            total_words = sum(len(page['text'].split()) for page in text_content)
            
            st.metric("Pages", len(text_content))
            st.metric("Mots", f"{total_words:,}")
            st.metric("Caractères", f"{total_chars:,}")
            
            # Estimation du temps de lecture
            reading_speed = 150  # mots par minute
            estimated_time = total_words / reading_speed
            st.metric("Temps estimé", f"{estimated_time:.1f} min")

if __name__ == "__main__":
    main()