#!/bin/bash

echo "📄➡️🔊 PDF to Audio Converter"
echo "=============================="
echo ""

# Fonction pour vérifier si un port est libre
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1
    else
        return 0
    fi
}

# Fonction pour arrêter les processus
cleanup() {
    echo ""
    echo "🛑 Arrêt de l'application..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "✅ Backend arrêté"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "✅ Frontend arrêté"
    fi
    
    echo "👋 Au revoir !"
    exit 0
}

# Capturer Ctrl+C
trap cleanup SIGINT

# Vérifier les prérequis
echo "🔍 Vérification des prérequis..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    echo "Veuillez installer Python 3.8+ depuis https://python.org/"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé"
    echo "Veuillez installer Node.js 16+ depuis https://nodejs.org/"
    exit 1
fi

echo "✅ Python $(python3 --version | cut -d' ' -f2) détecté"
echo "✅ Node.js $(node --version | cut -c2-) détecté"

# Vérifier les ports
echo ""
echo "🔍 Vérification des ports..."

if ! check_port 8000; then
    echo "❌ Le port 8000 est déjà utilisé (backend)"
    echo "Veuillez libérer le port ou arrêter l'autre processus"
    exit 1
fi

if ! check_port 3000; then
    echo "❌ Le port 3000 est déjà utilisé (frontend)"
    echo "Veuillez libérer le port ou arrêter l'autre processus"
    exit 1
fi

echo "✅ Ports 8000 et 3000 disponibles"

# Créer les dossiers nécessaires
mkdir -p uploads audio

# Démarrer le backend
echo ""
echo "🚀 Démarrage du backend..."
cd backend

# Installer les dépendances backend si nécessaire
if [ ! -f ".dependencies_installed" ]; then
    echo "📦 Installation des dépendances backend..."
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        touch .dependencies_installed
        echo "✅ Dépendances backend installées"
    else
        echo "❌ Erreur lors de l'installation des dépendances backend"
        exit 1
    fi
fi

# Lancer le backend en arrière-plan
python main.py &
BACKEND_PID=$!

# Attendre que le backend soit prêt
echo "⏳ Attente du démarrage du backend..."
sleep 3

# Vérifier si le backend fonctionne
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "❌ Le backend ne répond pas"
    cleanup
    exit 1
fi

echo "✅ Backend démarré sur http://localhost:8000"

# Démarrer le frontend
echo ""
echo "🎨 Démarrage du frontend..."
cd ../frontend

# Installer les dépendances frontend si nécessaire
if [ ! -d "node_modules" ]; then
    echo "📦 Installation des dépendances frontend..."
    npm install
    if [ $? -eq 0 ]; then
        echo "✅ Dépendances frontend installées"
    else
        echo "❌ Erreur lors de l'installation des dépendances frontend"
        cleanup
        exit 1
    fi
fi

# Lancer le frontend en arrière-plan
npm start &
FRONTEND_PID=$!

echo "✅ Frontend en cours de démarrage..."

# Attendre un peu pour que le frontend démarre
sleep 5

echo ""
echo "🎉 Application démarrée avec succès !"
echo ""
echo "📱 Interface utilisateur: http://localhost:3000"
echo "🔧 API Backend:          http://localhost:8000"
echo "📚 Documentation API:    http://localhost:8000/docs"
echo ""
echo "💡 Conseils:"
echo "  • Glissez-déposez un fichier PDF dans l'interface"
echo "  • La conversion peut prendre 1-3 minutes"
echo "  • Les fichiers sont supprimés automatiquement"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter l'application"

# Attendre indéfiniment
while true; do
    sleep 1
done