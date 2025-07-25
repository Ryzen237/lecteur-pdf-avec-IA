# 📖🔊 Guide d'Utilisation - PDF Reader AI

## 🚀 Démarrage Rapide

### 1. Configuration de la Clé API
Avant d'utiliser l'outil, vous devez configurer votre clé API OpenAI :

1. Ouvrez le fichier `.env`
2. Remplacez `sk-your-openai-api-key-here` par votre vraie clé API OpenAI
3. Sauvegardez le fichier

### 2. Lancement de l'Application
```bash
# Option 1 : Script de lancement automatique
./start.sh

# Option 2 : Lancement direct
streamlit run app.py
```

### 3. Utilisation de l'Interface

#### 📄 Étape 1 : Charger votre PDF
- Cliquez sur "Parcourir les fichiers" ou glissez-déposez votre PDF
- Formats supportés : PDF uniquement
- Taille maximale : 200 MB

#### 🎤 Étape 2 : Choisir la Voix
Sélectionnez parmi 6 voix disponibles :
- **alloy** : Voix neutre et équilibrée
- **echo** : Voix masculine profonde
- **fable** : Voix expressive britannique
- **onyx** : Voix masculine grave
- **nova** : Voix féminine jeune
- **shimmer** : Voix féminine douce

#### ⚙️ Étape 3 : Configurer les Options
- **Vitesse de lecture** : 0.25x à 4.0x (défaut : 1.0x)
- **Prévisualisation** : Voir le texte extrait avant conversion

#### 🎵 Étape 4 : Générer l'Audio
1. Cliquez sur "🎤 Générer l'Audio"
2. Attendez la génération (peut prendre quelques minutes)
3. Écoutez directement dans l'interface
4. Téléchargez le fichier MP3 si souhaité

## 🔧 Fonctionnalités Avancées

### 📊 Statistiques du Document
L'outil affiche automatiquement :
- Nombre de pages
- Nombre de mots
- Temps de lecture estimé
- Taille du fichier

### 🎨 Interface Responsive
- Compatible desktop et mobile
- Mode sombre/clair automatique
- Interface intuitive et moderne

### 💾 Sauvegarde Audio
- Format MP3 haute qualité
- Nom de fichier automatique basé sur le PDF
- Téléchargement direct depuis l'interface

## ⚠️ Limitations et Conseils

### Limitations
- Nécessite une connexion internet (API OpenAI)
- Coût par caractère converti (selon votre plan OpenAI)
- PDFs avec images/graphiques : seul le texte est extrait
- PDFs protégés par mot de passe non supportés

### Conseils d'Utilisation
- **PDFs scannés** : Utilisez un outil OCR avant conversion
- **Gros fichiers** : La génération peut prendre du temps
- **Qualité audio** : Choisissez la voix qui convient à votre contenu
- **Vitesse** : Ajustez selon vos préférences d'écoute

## 🆘 Dépannage

### Erreur "Clé API invalide"
- Vérifiez votre clé API dans le fichier `.env`
- Assurez-vous d'avoir du crédit sur votre compte OpenAI

### Erreur d'extraction PDF
- Vérifiez que le PDF n'est pas corrompu
- Essayez avec un autre fichier PDF
- Vérifiez que le PDF contient du texte (pas seulement des images)

### Application ne se lance pas
```bash
# Réinstaller les dépendances
pip3 install --break-system-packages -r requirements.txt

# Tester les dépendances
python3 demo.py
```

## 📞 Support

Pour toute question ou problème :
1. Vérifiez ce guide d'utilisation
2. Consultez les logs d'erreur dans le terminal
3. Testez avec le script `demo.py`

---

**🎉 Profitez de votre expérience d'écoute avec PDF Reader AI !**