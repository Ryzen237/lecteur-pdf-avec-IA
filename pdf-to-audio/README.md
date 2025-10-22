# 📄➡️🔊 PDF to Audio Converter

Une application moderne pour convertir des fichiers PDF en audio avec l'intelligence artificielle.

## ✨ Fonctionnalités

- **Interface moderne** : Interface React.js intuitive avec drag & drop
- **Conversion IA** : Utilise des moteurs TTS avancés (Edge TTS, Google TTS, pyttsx3)
- **Lecteur intégré** : Lecteur audio complet avec contrôles avancés
- **Traitement asynchrone** : Conversion en arrière-plan avec suivi en temps réel
- **Responsive** : Fonctionne parfaitement sur desktop et mobile
- **Sécurisé** : Fichiers supprimés automatiquement après traitement

## 🏗️ Architecture

```
pdf-to-audio/
├── backend/                 # API FastAPI
│   ├── main.py             # Serveur principal
│   ├── pdf_processor.py    # Extraction de texte PDF
│   ├── audio_generator.py  # Génération audio IA
│   └── requirements.txt    # Dépendances Python
├── frontend/               # Interface React.js
│   ├── src/
│   │   ├── components/     # Composants React
│   │   ├── services/       # Services API
│   │   └── types/          # Types TypeScript
│   └── package.json
├── uploads/                # Fichiers PDF temporaires
└── audio/                  # Fichiers audio générés
```

## 🚀 Installation et Lancement

### Prérequis

- **Python 3.8+**
- **Node.js 16+**
- **npm ou yarn**

### 1. Installation du Backend

```bash
cd pdf-to-audio/backend

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
python main.py
```

Le backend sera accessible sur `http://localhost:8000`

### 2. Installation du Frontend

```bash
cd pdf-to-audio/frontend

# Installer les dépendances
npm install

# Lancer l'application
npm start
```

L'application sera accessible sur `http://localhost:3000`

## 🎯 Utilisation

1. **Téléchargement** : Glissez-déposez un fichier PDF ou cliquez pour parcourir
2. **Conversion** : L'IA extrait le texte et génère l'audio automatiquement
3. **Écoute** : Utilisez le lecteur intégré avec contrôles de vitesse et volume
4. **Téléchargement** : Sauvegardez le fichier audio MP3 sur votre appareil

## 🔧 Configuration

### Variables d'environnement (optionnel)

Créez un fichier `.env` dans le dossier backend :

```env
# Configuration optionnelle
MAX_FILE_SIZE=52428800  # 50MB en bytes
MAX_PAGES=100          # Limite de pages PDF
AUDIO_QUALITY=high     # low, medium, high
```

### Moteurs TTS disponibles

L'application détecte automatiquement les moteurs disponibles :

1. **Edge TTS** (Recommandé) - Haute qualité, gratuit
2. **Google TTS** - Bonne qualité, nécessite internet
3. **pyttsx3** - Qualité basique, fonctionne hors ligne

## 📱 Interface Utilisateur

### Page d'accueil
- Zone de drag & drop intuitive
- Validation automatique des fichiers
- Informations sur les formats supportés

### Progression
- Barre de progression en temps réel
- Étapes de traitement visualisées
- Estimation du temps restant

### Lecteur Audio
- Contrôles de lecture/pause
- Barre de progression interactive
- Contrôle du volume
- Vitesses de lecture (0.5x à 2x)
- Téléchargement du fichier MP3

## 🛠️ Développement

### Structure des composants React

```typescript
PDFToAudioConverter          # Composant principal
├── FileUpload              # Upload avec drag & drop
├── ProgressIndicator       # Suivi de progression
└── AudioReady             # Lecteur audio intégré
```

### API Endpoints

```
POST /upload              # Upload fichier PDF
GET  /status/{task_id}    # Statut de la tâche
GET  /download/{task_id}  # Télécharger audio
GET  /audio/{filename}    # Servir fichier audio
DELETE /task/{task_id}    # Supprimer tâche
GET  /health             # État de santé API
```

### Scripts de développement

```bash
# Backend - Mode développement
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend - Mode développement
cd frontend
npm start

# Tests
npm test

# Build de production
npm run build
```

## 🔒 Sécurité

- **Validation stricte** des fichiers PDF
- **Limite de taille** : 50MB maximum
- **Nettoyage automatique** des fichiers temporaires
- **Pas de stockage permanent** des données utilisateur
- **CORS configuré** pour les domaines autorisés

## 🌐 Déploiement

### Docker (Recommandé)

```dockerfile
# Dockerfile exemple pour le backend
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production

1. **Backend** : Déployez avec Gunicorn + Nginx
2. **Frontend** : Build et servez les fichiers statiques
3. **Base de données** : Optionnel pour persistance des tâches
4. **Storage** : S3 ou équivalent pour les fichiers

## 📊 Performances

- **Temps de conversion** : 1-3 minutes selon la taille du PDF
- **Qualité audio** : 128kbps MP3, optimisé pour la parole
- **Langues supportées** : Français (configurable)
- **Formats supportés** : PDF uniquement

## 🐛 Dépannage

### Problèmes courants

**"API non disponible"**
- Vérifiez que le backend est démarré sur le port 8000
- Contrôlez les logs du serveur

**"Erreur de conversion"**
- Vérifiez que le PDF contient du texte (pas seulement des images)
- Essayez avec un PDF plus petit

**"Aucun moteur TTS disponible"**
```bash
pip install edge-tts gTTS pyttsx3
```

### Logs et debugging

```bash
# Logs backend
tail -f backend.log

# Debug mode
export DEBUG=1
python main.py
```

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/amazing-feature`)
3. Committez vos changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- **FastAPI** pour l'API backend rapide
- **React.js** pour l'interface moderne
- **Edge TTS** pour la synthèse vocale de qualité
- **PyMuPDF** pour l'extraction de texte PDF

---

**Développé avec ❤️ pour simplifier la lecture de documents**