#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 PaniniFS Research Launcher
Lance traitement intensif Colab + collecte corpus parallèle
"""

import subprocess
import time
import json
from pathlib import Path
from datetime import datetime
import webbrowser

def main():
    """Démarrage coordonné recherche intensive"""
    
    print("🧬 PANINIFS RESEARCH - DÉMARRAGE INTENSIF")
    print("=" * 60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. Préparation environnement
    print("📂 PRÉPARATION ENVIRONNEMENT")
    print("-" * 30)
    
    # Vérifier répertoires
    colab_results = Path("/home/stephane/GitHub/PaniniFS-Research/colab_results")
    incremental_corpus = Path("/home/stephane/GitHub/PaniniFS-Research/data/incremental_corpus")
    
    colab_results.mkdir(exist_ok=True)
    incremental_corpus.mkdir(exist_ok=True)
    
    print(f"✅ Répertoire résultats Colab: {colab_results}")
    print(f"✅ Répertoire corpus incrémental: {incremental_corpus}")
    
    # 2. Status GitHub
    print(f"\n🔄 STATUT GITHUB")
    print("-" * 30)
    
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              cwd="/home/stephane/GitHub/PaniniFS-Research",
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            print("⚠️ Changements non commitís détectés:")
            print(result.stdout.strip())
        else:
            print("✅ Repository propre")
            
        # Quick commit si nécessaire
        if result.stdout.strip():
            subprocess.run(['git', 'add', '.'], 
                         cwd="/home/stephane/GitHub/PaniniFS-Research")
            subprocess.run(['git', 'commit', '-m', '🚀 Pre-intensive research setup'], 
                         cwd="/home/stephane/GitHub/PaniniFS-Research")
            subprocess.run(['git', 'push', 'origin', 'main'], 
                         cwd="/home/stephane/GitHub/PaniniFS-Research")
            print("✅ Changes pushed to GitHub")
    
    except Exception as e:
        print(f"⚠️ Git status check failed: {e}")
    
    # 3. Lancement collecteur corpus (background)
    print(f"\n🌍 LANCEMENT COLLECTEUR CORPUS")
    print("-" * 30)
    
    try:
        corpus_process = subprocess.Popen(
            ['python3', '/home/stephane/GitHub/PaniniFS-Research/scripts/simple_corpus_collector.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"✅ Collecteur corpus démarré (PID: {corpus_process.pid})")
        print("📈 Collecte continue en arrière-plan...")
        print("🔄 Push automatique vers GitHub toutes les 15 documents")
        
    except Exception as e:
        print(f"❌ Erreur lancement collecteur: {e}")
        corpus_process = None
    
    # 4. Affichage URLs Colab
    print(f"\n🧬 NOTEBOOKS COLAB DISPONIBLES")
    print("-" * 30)
    
    notebooks = {
        'Intensive Multi-Hypotheses': 'https://colab.research.google.com/github/stephanedenis/PaniniFS-Research/blob/main/notebooks/dhatu_multi_hypotheses_intensive.ipynb',
        'Main GPU Notebook': 'https://colab.research.google.com/github/stephanedenis/PaniniFS-Research/blob/main/PaniniFS_Colab_GPU.ipynb',
        'Phonological Analysis': 'https://colab.research.google.com/github/stephanedenis/PaniniFS-Research/blob/main/notebooks/analyse_phonologique.ipynb'
    }
    
    for name, url in notebooks.items():
        print(f"📓 {name}")
        print(f"   {url}")
        print()
    
    # 5. Instructions utilisateur
    print("🎯 INSTRUCTIONS DE DÉMARRAGE")
    print("-" * 30)
    print("1. 🖱️  Cliquer sur le lien 'Intensive Multi-Hypotheses' ci-dessus")
    print("2. ⚙️  Dans Colab: Runtime → Change runtime type → GPU")
    print("3. ▶️  Exécuter toutes les cellules (Ctrl+F9)")
    print("4. ⏱️  Le traitement prendra 30-60 minutes")
    print("5. 📊 Les résultats seront automatiquement pushés sur GitHub")
    print()
    print("Pendant ce temps:")
    print("📈 Le collecteur corpus tourne en arrière-plan")
    print("🔄 Nouveaux documents ajoutés automatiquement")
    print("💾 Sauvegarde continue sur GitHub")
    
    # 6. Monitoring simple
    print(f"\n📊 MONITORING")
    print("-" * 30)
    
    if corpus_process:
        print("⏰ Collecteur corpus actif")
        print("📁 Vérification fichiers créés:")
        
        # Attendre un peu et vérifier
        time.sleep(5)
        
        # Check fichiers récents
        recent_files = list(incremental_corpus.glob("*.json"))
        if recent_files:
            latest = max(recent_files, key=lambda f: f.stat().st_mtime)
            print(f"📄 Dernier fichier: {latest.name}")
        else:
            print("⏳ Premiers fichiers en cours de création...")
    
    # 7. Options utilisateur
    print(f"\n🎛️ OPTIONS")
    print("-" * 30)
    print("🌐 [O]uvrir notebook Colab automatiquement")
    print("📊 [M]onitor collecteur corpus")
    print("🛑 [S]top collecteur corpus")  
    print("❌ [Q]uit")
    
    while True:
        try:
            choice = input("\n👉 Choix: ").strip().lower()
            
            if choice == 'o':
                print("🌐 Ouverture Colab...")
                webbrowser.open(notebooks['Intensive Multi-Hypotheses'])
                break
                
            elif choice == 'm':
                print("📊 Monitoring collecteur...")
                monitor_corpus_collector()
                break
                
            elif choice == 's':
                if corpus_process:
                    corpus_process.terminate()
                    print("🛑 Collecteur arrêté")
                else:
                    print("ℹ️ Aucun collecteur en cours")
                break
                
            elif choice == 'q':
                if corpus_process:
                    corpus_process.terminate()
                    print("🛑 Collecteur arrêté")
                print("👋 Arrêt")
                break
                
            else:
                print("❓ Option invalide")
                
        except KeyboardInterrupt:
            if corpus_process:
                corpus_process.terminate()
            print("\n👋 Arrêt par utilisateur")
            break

def monitor_corpus_collector():
    """Monitor simple du collecteur corpus"""
    
    print("📊 MONITORING COLLECTEUR CORPUS")
    print("=" * 40)
    print("Press Ctrl+C to stop monitoring")
    print()
    
    incremental_dir = Path("/home/stephane/GitHub/PaniniFS-Research/data/incremental_corpus")
    
    last_count = 0
    
    try:
        while True:
            # Compter fichiers
            files = list(incremental_dir.glob("*.json"))
            current_count = len(files)
            
            if current_count != last_count:
                print(f"📄 Fichiers corpus: {current_count} (+{current_count - last_count})")
                
                if files:
                    # Info dernier fichier
                    latest = max(files, key=lambda f: f.stat().st_mtime)
                    size_kb = latest.stat().st_size // 1024
                    age_min = (time.time() - latest.stat().st_mtime) / 60
                    print(f"   📅 Dernier: {latest.name} ({size_kb}KB, {age_min:.1f}min)")
                
                last_count = current_count
            
            time.sleep(30)  # Check every 30 seconds
            
    except KeyboardInterrupt:
        print("\n📊 Monitoring arrêté")

if __name__ == "__main__":
    main()