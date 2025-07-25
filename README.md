# 📖🔊 PDF Reader AI

Un outil intelligent qui convertit vos fichiers PDF en audio avec une voix IA naturelle et humaine.

## ✨ Fonctionnalités

- **📄 Extraction de texte PDF** : Capture automatiquement le contenu de toutes les pages
- **🎤 Synthèse vocale IA** : Utilise l'API OpenAI pour générer une voix naturelle
- **🎵 Choix de voix** : 6 voix différentes disponibles (masculine, féminine, neutre, etc.)
- **🔊 Lecteur intégré** : Écoutez directement dans l'interface web
- **💾 Téléchargement MP3** : Sauvegardez l'audio pour une écoute hors ligne
- **📊 Statistiques** : Analyse du contenu (pages, mots, temps estimé)
- **🎨 Interface moderne** : Interface utilisateur intuitive et responsive

## 🚀 Installation

1. **Cloner le projet** :
```bash
git clone <votre-repo>
cd pdf-reader-ai
```

2. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

3. **Configuration de l'API** :
   - Copiez `.env.example` vers `.env`
   - Ajoutez votre clé API OpenAI dans le fichier `.env`
   - Ou configurez-la directement dans l'interface

## 🎯 Utilisation

1. **Lancer l'application** :
```bash
streamlit run app.py
```

2. **Utiliser l'outil** :
   - Uploadez votre fichier PDF
   - Configurez votre clé API OpenAI (si pas déjà fait)
   - Choisissez une voix
   - Cliquez sur "Convertir en Audio"
   - Écoutez le résultat !

## 🎭 Voix disponibles

- **Alloy** : Voix neutre et équilibrée
- **Echo** : Voix masculine claire
- **Fable** : Accent britannique distingué
- **Onyx** : Voix profonde et autoritaire
- **Nova** : Voix féminine douce
- **Shimmer** : Voix très douce et apaisante

## 📋 Prérequis

- Python 3.8+
- Clé API OpenAI (pour la synthèse vocale)
- Connexion Internet

## 🛠️ Technologies utilisées

- **Streamlit** : Interface web interactive
- **PyPDF2** : Extraction de texte PDF
- **OpenAI API** : Synthèse vocale de haute qualité
- **Python** : Logique métier

## 💡 Conseils d'utilisation

- **Qualité PDF** : Les PDFs avec du texte sélectionnable donnent de meilleurs résultats
- **Taille** : Les fichiers volumineux peuvent prendre plus de temps à traiter
- **Coût** : L'API OpenAI facture selon l'usage (environ $15 pour 1M de caractères)
- **Limites** : Le texte est limité à 4000 caractères par requête pour optimiser les performances

## 🔧 Dépannage

### Erreur d'extraction PDF
- Vérifiez que le PDF contient du texte sélectionnable
- Essayez avec un autre fichier PDF

### Erreur API OpenAI
- Vérifiez que votre clé API est valide
- Assurez-vous d'avoir des crédits disponibles
- Vérifiez votre connexion Internet

### Performance lente
- Les gros fichiers prennent plus de temps
- L'API peut être plus lente aux heures de pointe

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## 📞 Support

Pour toute question ou problème, ouvrez une issue sur GitHub.

---

**Fait avec ❤️ et IA**
