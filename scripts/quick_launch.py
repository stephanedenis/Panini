#!/usr/bin/env python3
"""
🚀 Quick Launch - Démarrage rapide Colab + Collecteur
Lancement simplifié pour interaction optimale
"""

import os
import time
import subprocess
import webbrowser
import json
from datetime import datetime

def print_banner():
    """Bannière d'accueil"""
    print("🚀" + "="*60 + "🚀")
    print("   PANINI RESEARCH - LANCEMENT RAPIDE")
    print("   Colab + Collecteur = Interaction optimisée")
    print("🚀" + "="*60 + "🚀")

def check_git_status():
    """Vérifier que Git est prêt"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        
        if result.stdout.strip():
            print("📝 Changements Git détectés, commit automatique...")
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', '🔄 Pre-launch sync'], check=True)
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
            print("✅ Git synchronisé!")
        else:
            print("✅ Git déjà à jour!")
            
    except subprocess.CalledProcessError:
        print("⚠️ Problème Git, continuons quand même...")

def create_colab_launch_info():
    """Créer info de lancement pour Colab"""
    launch_info = {
        'timestamp': datetime.now().isoformat(),
        'colab_notebook': 'notebooks/colab_dhatu_simple.ipynb',
        'colab_url': 'https://colab.research.google.com/github/stephanedenis/PaniniFS-Research/blob/main/notebooks/colab_dhatu_simple.ipynb',
        'collector_status': 'ready_to_start',
        'data_location': 'data/incremental_corpus/',
        'feedback_location': 'colab_results/colab_feedback.json',
        'instructions': [
            '1. Ouvrir le lien Colab ci-dessus',
            '2. Exécuter les cellules dans l\'ordre',
            '3. Le collecteur démarrera automatiquement',
            '4. Interaction via GitHub synchronisée'
        ]
    }
    
    os.makedirs('colab_results', exist_ok=True)
    with open('colab_results/launch_info.json', 'w', encoding='utf-8') as f:
        json.dump(launch_info, f, ensure_ascii=False, indent=2)
    
    return launch_info

def start_collector_background():
    """Démarrer le collecteur en arrière-plan"""
    print("🤖 Démarrage du collecteur rapide...")
    
    # Créer un script wrapper pour lancement continu
    wrapper_content = '''#!/bin/bash
cd /home/stephane/GitHub/PaniniFS-Research
while true; do
    echo "🔄 $(date): Démarrage cycle collecteur"
    python3 scripts/fast_corpus_collector.py
    echo "⏸️ $(date): Pause 60 secondes"
    sleep 60
done
'''
    
    with open('scripts/collector_loop.sh', 'w') as f:
        f.write(wrapper_content)
    
    os.chmod('scripts/collector_loop.sh', 0o755)
    
    # Lancer en arrière-plan
    process = subprocess.Popen(['bash', 'scripts/collector_loop.sh'], 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE)
    
    print(f"✅ Collecteur démarré en arrière-plan (PID: {process.pid})")
    
    # Sauvegarder le PID
    with open('colab_results/collector_pid.txt', 'w') as f:
        f.write(str(process.pid))
    
    return process.pid

def open_colab():
    """Ouvrir Colab dans le navigateur"""
    colab_url = "https://colab.research.google.com/github/stephanedenis/PaniniFS-Research/blob/main/notebooks/colab_dhatu_simple.ipynb"
    
    print(f"🌐 Ouverture de Colab: {colab_url}")
    
    try:
        webbrowser.open(colab_url)
        print("✅ Colab ouvert dans le navigateur!")
    except Exception as e:
        print(f"⚠️ Impossible d'ouvrir automatiquement: {e}")
        print(f"📋 Copiez ce lien dans votre navigateur:")
        print(f"   {colab_url}")

def show_status_info():
    """Afficher les informations de statut"""
    print("\n📊 INFORMATIONS DE LANCEMENT:")
    print("├── 📓 Notebook Colab: colab_dhatu_simple.ipynb")
    print("├── 🤖 Collecteur: fast_corpus_collector.py (mode continu)")
    print("├── 📁 Données: data/incremental_corpus/")
    print("├── 🔄 Feedback: colab_results/colab_feedback.json")
    print("└── 📋 Logs: fast_collector.log")
    
    print("\n🎯 UTILISATION:")
    print("1. Colab s'ouvre automatiquement")
    print("2. Exécutez les cellules dans l'ordre")
    print("3. Le collecteur tourne en continu")
    print("4. Synchronisation automatique via GitHub")
    
    print("\n⏹️ POUR ARRÊTER:")
    print("   python3 scripts/stop_collection.py")

def main():
    """Point d'entrée principal"""
    print_banner()
    
    # Étape 1: Vérifier Git
    print("\n🔧 PRÉPARATION...")
    check_git_status()
    
    # Étape 2: Créer infos de lancement
    launch_info = create_colab_launch_info()
    print("📝 Informations de lancement créées")
    
    # Étape 3: Démarrer collecteur
    print("\n🚀 DÉMARRAGE...")
    collector_pid = start_collector_background()
    
    # Étape 4: Ouvrir Colab
    time.sleep(2)  # Petite pause
    open_colab()
    
    # Étape 5: Afficher infos
    print("\n" + "="*70)
    show_status_info()
    print("="*70)
    
    print(f"\n✅ SYSTÈME PRÊT! Collecteur PID: {collector_pid}")
    print("🌐 Colab ouvert, commencez l'analyse!")

if __name__ == "__main__":
    main()