#!/usr/bin/env python3
"""
Script d'installation pour PDF Reader AI
"""

import subprocess
import sys
import os

def install_dependencies():
    """Installer les dépendances Python"""
    print("📦 Installation des dépendances...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dépendances installées avec succès !")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erreur lors de l'installation des dépendances")
        return False

def setup_env_file():
    """Créer le fichier .env s'il n'existe pas"""
    if not os.path.exists(".env"):
        print("📝 Création du fichier .env...")
        try:
            with open(".env.example", "r") as source:
                content = source.read()
            with open(".env", "w") as target:
                target.write(content)
            print("✅ Fichier .env créé ! N'oubliez pas d'ajouter votre clé API OpenAI.")
        except Exception as e:
            print(f"⚠️ Impossible de créer le fichier .env : {e}")
    else:
        print("ℹ️ Le fichier .env existe déjà.")

def main():
    print("🚀 Installation de PDF Reader AI")
    print("=" * 40)
    
    # Installer les dépendances
    if not install_dependencies():
        sys.exit(1)
    
    # Configurer le fichier .env
    setup_env_file()
    
    print("\n🎉 Installation terminée !")
    print("\n📋 Prochaines étapes :")
    print("1. Ajoutez votre clé API OpenAI dans le fichier .env")
    print("2. Lancez l'application avec : python run.py")
    print("   ou directement avec : streamlit run app.py")
    print("\n💡 Besoin d'aide ? Consultez le README.md")

if __name__ == "__main__":
    main()