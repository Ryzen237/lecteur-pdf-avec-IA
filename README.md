# Lecteur PE - Analyseur de fichiers exécutables Windows

Un outil complet pour analyser les fichiers PE (Portable Executable) comme les fichiers .exe, .dll, .sys et autres exécutables Windows.

## 🚀 Fonctionnalités

- **Analyse complète des en-têtes** : DOS, PE/COFF, et en-tête optionnel
- **Détection d'architecture** : Support PE32 et PE32+ (x86, x64, ARM, etc.)
- **Analyse des sections** : Informations détaillées sur toutes les sections
- **Interface en ligne de commande** : Utilisation simple via terminal
- **Interface graphique moderne** : GUI conviviale avec tkinter
- **Détection des caractéristiques** : Type de fichier, permissions, etc.
- **Support multi-format** : .exe, .dll, .sys, .ocx et autres PE

## 📋 Prérequis

- Python 3.6 ou plus récent
- Modules Python standard (aucune dépendance externe)

## 🛠️ Installation

1. Clonez ou téléchargez ce repository
2. Aucune installation supplémentaire requise - utilise uniquement les modules Python standard

## 💻 Utilisation

### Interface en ligne de commande

```bash
# Analyser un fichier PE
python pe_reader.py fichier.exe

# Exemples
python pe_reader.py C:\Windows\System32\notepad.exe
python pe_reader.py sample.dll
```

### Interface graphique

```bash
# Lancer l'interface graphique
python pe_reader_gui.py
```

L'interface graphique offre :
- Sélection de fichier par dialogue
- Analyse en arrière-plan avec barre de progression
- Résultats organisés en onglets
- Vue d'ensemble, en-têtes détaillés, sections et log complet

### Script de test et démonstration

```bash
# Lancer les tests et démonstrations
python test_pe.py
```

## 📊 Informations analysées

### En-têtes
- **En-tête DOS** : Signature MZ, offset PE
- **En-tête PE/COFF** : Architecture, nombre de sections, date de compilation
- **En-tête optionnel** : Point d'entrée, base de l'image, alignements

### Sections
- Nom et taille de chaque section
- Adresses virtuelles et offsets fichier
- Caractéristiques (lecture, écriture, exécution)
- Type de contenu (code, données, ressources)

### Caractéristiques du fichier
- Type (EXE, DLL, pilote système)
- Architecture cible (x86, x64, ARM64, etc.)
- Flags de compilation et linking

## 🔍 Exemple de sortie

```
Analyse du fichier: notepad.exe
==================================================

🔍 EN-TÊTE DOS
------------------------------
Signature: MZ
Offset en-tête PE: 0x000000f8

🔍 EN-TÊTE PE
------------------------------
Signature: PE
Machine: AMD x64
Nombre de sections: 6
Date de compilation: 2021-12-07 10:30:45

📋 CARACTÉRISTIQUES
------------------------------
  • Executable image
  • Large address aware
  • Debug info stripped

📂 SECTIONS
------------------------------

Section 1: .text
  Adresse virtuelle: 0x00001000
  Taille virtuelle: 196608 bytes
  Offset fichier: 0x00000400
  Taille fichier: 196608 bytes
  Caractéristiques:
    • Contains code
    • Executable
    • Readable
```

## 🏗️ Architecture du code

### `pe_reader.py`
Module principal contenant la classe `PEReader` avec :
- Parsing des en-têtes DOS, PE et optionnel
- Analyse des sections
- Décodage des caractéristiques et flags
- Support des architectures multiples

### `pe_reader_gui.py`
Interface graphique avec :
- Sélection de fichier intuitive
- Analyse en thread séparé
- Affichage organisé en onglets
- Gestion d'erreurs et feedback utilisateur

### `test_pe.py`
Script de test et démonstration avec :
- Tests automatiques sur fichiers système
- Démonstration des structures PE
- Exemples d'utilisation

## 🔧 Types de machines supportés

- Intel 386/486/Pentium
- AMD x64
- ARM (32-bit et 64-bit)
- MIPS (diverses variantes)
- PowerPC
- Alpha AXP
- Et bien d'autres...

## ⚠️ Limitations

- Analyse en lecture seule (pas de modification)
- Pas d'analyse des imports/exports (peut être ajouté)
- Pas de décompilation ou désassemblage
- Optimisé pour l'analyse structurelle

## 🤝 Contribution

Les contributions sont les bienvenues ! Vous pouvez :
- Ajouter le support d'autres formats
- Améliorer l'interface graphique
- Ajouter l'analyse des imports/exports
- Optimiser les performances

## 📄 Licence

Ce projet est libre d'utilisation pour des fins éducatives et de recherche.

## 🔗 Ressources utiles

- [Spécification PE Microsoft](https://docs.microsoft.com/en-us/windows/win32/debug/pe-format)
- [PE Format détaillé](https://wiki.osdev.org/PE)
- [Structure des fichiers PE](https://0xrick.github.io/win-internals/pe1/)
