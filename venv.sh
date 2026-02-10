#!/bin/bash

echo "🐍 Création du virtual environment..."
python3 -m venv venv

echo "✨ Activation du virtual environment..."
source venv/bin/activate

echo "📦 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup terminé ! L'environnement virtuel est prêt."
echo "💡 Pour l'activer plus tard, utilisez: source venv/bin/activate"
