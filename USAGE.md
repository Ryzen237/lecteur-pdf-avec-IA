# Guide d'utilisation rapide - Lecteur PE

## 🚀 Démarrage rapide

### 1. Lancement de l'interface graphique
```bash
# Méthode 1 : Script de lancement automatique
./run_pe_gui.sh

# Méthode 2 : Lancement direct
python3 pe_reader_gui.py
```

### 2. Analyse en ligne de commande
```bash
# Analyser un fichier PE
python3 pe_reader.py /chemin/vers/fichier.exe

# Exemple avec un fichier Windows
python3 pe_reader.py notepad.exe
```

### 3. Tests et démonstration
```bash
# Lancer les tests
python3 test_pe.py
```

## 📝 Formats supportés

- **.exe** : Exécutables Windows
- **.dll** : Bibliothèques dynamiques
- **.sys** : Pilotes système
- **.ocx** : Contrôles ActiveX
- **Autres** : Tout fichier au format PE

## 🔍 Que fait l'analyseur ?

### Informations extraites :
- **En-têtes** : DOS, PE/COFF, optionnel
- **Architecture** : x86, x64, ARM, etc.
- **Sections** : Code, données, ressources
- **Caractéristiques** : Permissions, type de fichier
- **Métadonnées** : Date de compilation, version

### Interface graphique :
- **Vue d'ensemble** : Résumé des informations principales
- **En-têtes** : Détails techniques complets
- **Sections** : Tableau interactif des sections
- **Log complet** : Sortie détaillée de l'analyse

## ⚠️ Dépannage

### Problème : "tkinter n'est pas disponible"
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter

# Fedora
sudo dnf install python3-tkinter
```

### Problème : "Signature DOS invalide"
- Normal pour les fichiers non-PE (binaires Linux, etc.)
- Vérifiez que le fichier est bien un exécutable Windows

### Problème : "Fichier non trouvé"
- Vérifiez le chemin du fichier
- Assurez-vous d'avoir les permissions de lecture

## 💡 Conseils d'utilisation

1. **Fichiers de test** : Copiez des fichiers .exe ou .dll Windows pour tester
2. **Analyse sécurisée** : Le lecteur ne modifie jamais les fichiers
3. **Performance** : L'interface graphique analyse en arrière-plan
4. **Compatibilité** : Fonctionne sur Linux, Windows et macOS

## 🔗 Liens utiles

- [Format PE Microsoft](https://docs.microsoft.com/en-us/windows/win32/debug/pe-format)
- [Spécification COFF](https://wiki.osdev.org/COFF)
- [Outils PE alternatifs](https://github.com/topics/pe-parser)