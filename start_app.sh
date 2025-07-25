#!/bin/bash

echo "🚀 Démarrage de PDF Reader AI..."
echo "📖🔊 Interface React + Backend FastAPI"

# Fonction pour arrêter les processus en cas d'interruption
cleanup() {
    echo -e "\n🛑 Arrêt des services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Capturer Ctrl+C
trap cleanup SIGINT

# Démarrer le backend FastAPI
echo "🔧 Démarrage du backend FastAPI..."
cd backend
pip3 install --break-system-packages -r requirements.txt > /dev/null 2>&1
python3 main.py &
BACKEND_PID=$!
echo "✅ Backend démarré sur http://localhost:8000 (PID: $BACKEND_PID)"

# Attendre que le backend soit prêt
sleep 3

# Démarrer le frontend React
echo "🎨 Démarrage du frontend React..."
cd ../frontend
npm start &
FRONTEND_PID=$!
echo "✅ Frontend démarré sur http://localhost:3000 (PID: $FRONTEND_PID)"

echo ""
echo "🌐 Application disponible sur:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo ""
echo "⚠️  N'oubliez pas de configurer votre clé OpenAI dans backend/.env"
echo "💡 Appuyez sur Ctrl+C pour arrêter l'application"

# Attendre que les processus se terminent
wait