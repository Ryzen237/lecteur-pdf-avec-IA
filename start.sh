#!/bin/bash

# Script de lancement pour PDF Reader AI
echo "🚀 Lancement de PDF Reader AI..."

# Vérifier si le fichier .env existe
if [ ! -f ".env" ]; then
    echo "⚠️  Fichier .env manquant. Création d'un fichier d'exemple..."
    cp .env.example .env
    echo "📝 Veuillez configurer votre clé API OpenAI dans le fichier .env"
fi

# Lancer Streamlit
echo "🌐 Ouverture de l'application sur http://localhost:8501"
streamlit run app.py --server.port 8501 --server.address 0.0.0.0