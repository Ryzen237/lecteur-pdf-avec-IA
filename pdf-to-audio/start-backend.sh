#!/bin/bash

echo "🚀 Démarrage du backend PDF-to-Audio"
echo "===================================="

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Aller dans le dossier backend
cd backend

# Vérifier si les dépendances sont installées
if [ ! -f ".dependencies_installed" ]; then
    echo "📦 Installation des dépendances..."
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        touch .dependencies_installed
        echo "✅ Dépendances installées avec succès"
    else
        echo "❌ Erreur lors de l'installation des dépendances"
        exit 1
    fi
else
    echo "✅ Dépendances déjà installées"
fi

# Créer les dossiers nécessaires
mkdir -p ../uploads ../audio

echo "🔧 Configuration:"
echo "  - Port: 8000"
echo "  - Host: 0.0.0.0"
echo "  - Mode: Development"
echo ""

echo "🎯 Le backend sera accessible sur: http://localhost:8000"
echo "📚 Documentation API: http://localhost:8000/docs"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

# Lancer le serveur
python main.py