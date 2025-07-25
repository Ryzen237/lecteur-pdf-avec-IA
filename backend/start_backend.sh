#!/bin/bash

echo "🚀 Démarrage du backend PDF Reader AI..."

# Installer les dépendances si nécessaire
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# Lancer FastAPI
echo "🌐 Lancement de l'API sur http://localhost:8000"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload