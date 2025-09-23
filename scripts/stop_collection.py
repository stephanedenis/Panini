#!/usr/bin/env python3
"""
⏹️ Stop Collection - Arrêt propre du système
"""

import os
import subprocess
import signal

def stop_collector():
    """Arrêter le collecteur"""
    pid_file = 'colab_results/collector_pid.txt'
    
    if os.path.exists(pid_file):
        try:
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            os.kill(pid, signal.SIGTERM)
            print(f"✅ Collecteur arrêté (PID: {pid})")
            
            os.remove(pid_file)
            
        except (ProcessLookupError, ValueError):
            print("⚠️ Collecteur déjà arrêté")
    else:
        print("⚠️ Aucun collecteur en cours")

def kill_collector_processes():
    """Forcer l'arrêt de tous les processus collecteur"""
    try:
        subprocess.run(['pkill', '-f', 'fast_corpus_collector'], check=False)
        subprocess.run(['pkill', '-f', 'collector_loop'], check=False)
        print("🔄 Tous les processus collecteur arrêtés")
    except Exception as e:
        print(f"⚠️ Erreur arrêt forcé: {e}")

def main():
    print("⏹️ Arrêt du système de collecte...")
    stop_collector()
    kill_collector_processes()
    print("✅ Système arrêté!")

if __name__ == "__main__":
    main()