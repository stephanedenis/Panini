#!/usr/bin/env python3
"""
Test simple de génération Colab
"""

import os
import json
from pathlib import Path

def create_simple_colab_notebook():
    """Crée un notebook Colab simple pour test"""
    
    # Créer le dossier
    notebook_dir = Path("colab_notebooks")
    notebook_dir.mkdir(exist_ok=True)
    
    # Contenu du notebook
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# PaniniFS Research - Test Colab Integration\\n",
                    "\\n",
                    "Notebook de test pour intégration Google Colab Pro"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Test configuration GPU\\n",
                    "import torch\\n",
                    "\\n",
                    "print('PyTorch version:', torch.__version__)\\n",
                    "print('CUDA available:', torch.cuda.is_available())\\n",
                    "\\n",
                    "if torch.cuda.is_available():\\n",
                    "    print('GPU:', torch.cuda.get_device_name())"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Connexion au repository PaniniFS\\n",
                    "!git clone https://github.com/stephanedenis/PaniniFS-Research.git\\n",
                    "%cd PaniniFS-Research\\n",
                    "\\n",
                    "print('✅ Repository cloné avec succès')"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Test d'analyse simple\\n",
                    "texts = [\\n",
                    "    'This is a test sentence.',\\n",
                    "    'Machine learning is fascinating.',\\n",
                    "    'Natural language processing rocks!'\\n",
                    "]\\n",
                    "\\n",
                    "print('Analyse de', len(texts), 'textes')\\n",
                    "for i, text in enumerate(texts):\\n",
                    "    print(f'{i+1}. {text}')"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    # Sauvegarder
    notebook_path = notebook_dir / "panini_test_colab.ipynb"
    
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    return notebook_path

def main():
    """Test principal"""
    print("🧪 CRÉATION NOTEBOOK TEST COLAB")
    print("=" * 35)
    
    try:
        notebook_path = create_simple_colab_notebook()
        print(f"✅ Notebook créé: {notebook_path}")
        print(f"📁 Taille: {notebook_path.stat().st_size} bytes")
        print()
        print("🔗 UTILISATION:")
        print("1. Aller sur Google Colab (colab.research.google.com)")
        print("2. File → Upload notebook")
        print("3. Sélectionner le fichier .ipynb créé")
        print("4. Runtime → Change runtime type → GPU")
        print("5. Exécuter les cellules")
        print()
        print("🎯 Ce notebook teste l'intégration de base avec PaniniFS")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()