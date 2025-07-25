#!/bin/bash

echo "🎨 Démarrage du frontend PDF-to-Audio"
echo "====================================="

# Vérifier si Node.js est installé
if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé"
    echo "Veuillez installer Node.js depuis https://nodejs.org/"
    exit 1
fi

# Vérifier si npm est installé
if ! command -v npm &> /dev/null; then
    echo "❌ npm n'est pas installé"
    exit 1
fi

# Aller dans le dossier frontend
cd frontend

# Vérifier si les dépendances sont installées
if [ ! -d "node_modules" ]; then
    echo "📦 Installation des dépendances..."
    npm install
    if [ $? -eq 0 ]; then
        echo "✅ Dépendances installées avec succès"
    else
        echo "❌ Erreur lors de l'installation des dépendances"
        exit 1
    fi
else
    echo "✅ Dépendances déjà installées"
fi

echo "🔧 Configuration:"
echo "  - Port: 3000"
echo "  - Mode: Development"
echo "  - Backend API: http://localhost:8000"
echo ""

echo "🎯 L'application sera accessible sur: http://localhost:3000"
echo ""
echo "⚠️  Assurez-vous que le backend est démarré (port 8000)"
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

# Lancer l'application React
npm start