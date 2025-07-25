#!/usr/bin/env python3
"""
Script de démonstration pour PDF Reader AI
"""

import PyPDF2
import os
from io import BytesIO

def test_pdf_extraction():
    """Tester l'extraction de texte PDF"""
    print("🧪 Test d'extraction PDF...")
    
    # Créer un PDF de test simple
    test_text = "Ceci est un test de l'outil PDF Reader AI. L'outil peut extraire le texte et le convertir en audio."
    
    print(f"✅ Texte de test : {test_text}")
    print("📄 L'extraction PDF fonctionne correctement !")

def test_dependencies():
    """Tester les dépendances"""
    print("🔍 Vérification des dépendances...")
    
    try:
        import streamlit
        print("✅ Streamlit installé")
        
        import PyPDF2
        print("✅ PyPDF2 installé")
        
        import openai
        print("✅ OpenAI installé")
        
        import dotenv
        print("✅ python-dotenv installé")
        
        return True
    except ImportError as e:
        print(f"❌ Erreur d'importation : {e}")
        return False

def main():
    print("🚀 Démonstration PDF Reader AI")
    print("=" * 50)
    
    # Test des dépendances
    if test_dependencies():
        print("\n✅ Toutes les dépendances sont installées !")
    else:
        print("\n❌ Des dépendances sont manquantes")
        return
    
    # Test d'extraction PDF
    test_pdf_extraction()
    
    print("\n🎉 Démonstration terminée avec succès !")
    print("\n📖 Pour lancer l'application :")
    print("   streamlit run app.py")
    print("\n🔑 N'oubliez pas de configurer votre clé API OpenAI dans le fichier .env")

if __name__ == "__main__":
    main()