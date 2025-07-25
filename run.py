#!/usr/bin/env python3
"""
Script de lancement pour PDF Reader AI
"""

import subprocess
import sys
import os

def check_dependencies():
    """Vérifier si les dépendances sont installées"""
    try:
        import streamlit
        import PyPDF2
        import openai
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("💡 Installez les dépendances avec: pip install -r requirements.txt")
        return False

def main():
    print("🚀 Lancement de PDF Reader AI...")
    
    # Vérifier les dépendances
    if not check_dependencies():
        sys.exit(1)
    
    # Lancer Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Erreur lors du lancement de l'application")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Application fermée par l'utilisateur")

if __name__ == "__main__":
    main()