# 📖🔊 PDF Reader AI

Une application moderne qui convertit vos fichiers PDF en audio avec une voix IA naturelle et humaine.

## 🏗️ Architecture

- **Frontend**: React.js avec TypeScript
- **Backend**: FastAPI (Python)
- **IA**: OpenAI TTS (Text-to-Speech)
- **Extraction PDF**: PyPDF2

## ✨ Fonctionnalités

- **📄 Upload de PDF** : Glissez-déposez ou sélectionnez vos fichiers PDF
- **🎤 6 Voix IA** : Choisissez parmi 6 voix naturelles différentes
- **🔄 Traitement temps réel** : Conversion instantanée PDF vers audio
- **🎧 Lecteur intégré** : Écoutez directement dans l'interface
- **💾 Téléchargement** : Sauvegardez l'audio en MP3
- **📊 Statistiques** : Informations sur le document traité
- **🎨 Interface moderne** : Design responsive et intuitif

## 🚀 Installation Rapide

### Prérequis
- Python 3.8+
- Node.js 16+
- npm ou yarn
- Clé API OpenAI

### 1. Cloner le projet
```bash
git clone <votre-repo>
cd pdf-reader-ai
```

### 2. Configuration de la clé API
```bash
# Éditez le fichier backend/.env
nano backend/.env

# Ajoutez votre clé OpenAI
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

### 3. Lancement automatique
```bash
./start_app.sh
```

L'application sera disponible sur :
- **Frontend** : http://localhost:3000
- **API Backend** : http://localhost:8000

## 🛠️ Installation Manuelle

### Backend (FastAPI)
```bash
cd backend
pip3 install --break-system-packages -r requirements.txt
python3 main.py
```

### Frontend (React)
```bash
cd frontend
npm install
npm start
```

## 📋 API Endpoints

### `POST /upload-pdf/`
Upload et conversion d'un PDF en audio
- **Paramètres** : 
  - `file` : Fichier PDF
  - `voice` : ID de la voix (alloy, echo, fable, onyx, nova, shimmer)
- **Réponse** : Informations sur le fichier audio généré

### `GET /audio/{filename}`
Récupération d'un fichier audio
- **Paramètres** : `filename` - Nom du fichier audio
- **Réponse** : Fichier MP3

### `GET /voices/`
Liste des voix disponibles
- **Réponse** : Liste des voix avec descriptions

## 🎤 Voix Disponibles

| Voix | Description |
|------|-------------|
| **Alloy** | Voix neutre et équilibrée |
| **Echo** | Voix masculine profonde |
| **Fable** | Voix expressive britannique |
| **Onyx** | Voix masculine grave |
| **Nova** | Voix féminine jeune |
| **Shimmer** | Voix féminine douce |

## 🔧 Configuration

### Variables d'environnement (backend/.env)
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Limites
- Taille maximale PDF : 200 MB
- Longueur de texte : 4000 caractères (limitation OpenAI TTS)
- Formats supportés : PDF uniquement

## 📁 Structure du Projet

```
pdf-reader-ai/
├── backend/
│   ├── main.py              # API FastAPI
│   ├── requirements.txt     # Dépendances Python
│   ├── .env                 # Configuration
│   ├── audio_files/         # Fichiers audio générés
│   └── start_backend.sh     # Script de lancement backend
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Interface principale
│   │   ├── App.css          # Styles
│   │   └── ...
│   ├── package.json         # Dépendances Node.js
│   └── ...
├── start_app.sh             # Lancement global
└── README.md                # Documentation
```

## 🔍 Utilisation

1. **Démarrer l'application** avec `./start_app.sh`
2. **Ouvrir** http://localhost:3000 dans votre navigateur
3. **Choisir une voix** parmi les 6 disponibles
4. **Glisser-déposer** ou sélectionner votre fichier PDF
5. **Cliquer** sur "Convertir en audio"
6. **Écouter** le résultat avec le lecteur intégré
7. **Télécharger** l'audio si souhaité

## 🐛 Dépannage

### Erreur "Fichier audio non trouvé"
- Vérifiez que le backend est démarré
- Vérifiez la clé API OpenAI

### Erreur CORS
- Assurez-vous que le frontend est sur localhost:3000
- Vérifiez la configuration CORS dans main.py

### Erreur d'installation
```bash
# Si pip échoue
pip3 install --break-system-packages -r requirements.txt

# Si npm échoue
cd frontend && npm install --legacy-peer-deps
```

## 📄 Licence

Ce projet est sous licence MIT.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou proposer une pull request.

## 📞 Support

Pour toute question ou problème, ouvrez une issue sur GitHub.
