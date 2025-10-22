#!/bin/bash
# Script de lancement pour l'interface graphique du lecteur PE

echo "🚀 Lancement du Lecteur PE - Interface Graphique"
echo "=================================================="

# Vérifier si Python est disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé ou non accessible"
    echo "Veuillez installer Python 3 pour continuer"
    exit 1
fi

# Vérifier si tkinter est disponible
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ tkinter n'est pas disponible"
    echo "Installation recommandée:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  CentOS/RHEL: sudo yum install tkinter"
    echo "  Fedora: sudo dnf install python3-tkinter"
    exit 1
fi

echo "✅ Environnement vérifié"
echo "📂 Répertoire de travail: $(pwd)"
echo "🐍 Version Python: $(python3 --version)"
echo ""
echo "Lancement de l'interface graphique..."

# Lancer l'interface graphique
python3 pe_reader_gui.py

echo ""
echo "Interface fermée. Au revoir !"