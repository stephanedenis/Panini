#!/usr/bin/env python3
"""
Collecteur Grand Corpus - Script simple
Lance la collection du grand corpus réel en arrière-plan
"""

import subprocess
import os
from pathlib import Path

def main():
    print("🚀 Lancement collection grand corpus réel...")
    
    # Chemin vers l'environnement virtuel
    venv_python = "/home/stephane/GitHub/PaniniFS-Research/.venv/bin/python"
    script_path = "tech/corpus_collector.py"
    log_file = "grand_corpus_collection.log"
    
    # Commande complète
    cmd = [
        "nohup", 
        venv_python, 
        script_path
    ]
    
    try:
        # Lancement en arrière-plan avec redirection
        with open(log_file, 'w') as f:
            process = subprocess.Popen(
                cmd,
                stdout=f,
                stderr=subprocess.STDOUT,
                cwd="/home/stephane/GitHub/PaniniFS-Research"
            )
        
        print(f"✅ Collection lancée en arrière-plan (PID: {process.pid})")
        print(f"📋 Logs: {log_file}")
        print("🔍 Pour suivre: tail -f grand_corpus_collection.log")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()