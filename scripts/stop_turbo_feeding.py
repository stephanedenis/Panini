#!/usr/bin/env python3
"""
⏹️ Stop Turbo Feeding - Arrêt coordonné du système turbo
"""

import os
import signal
import subprocess

def stop_turbo_feeding():
    """Arrêter tous les composants turbo"""
    print("⏹️ Arrêt du système TURBO FEEDING...")
    
    stopped_components = []
    
    # Arrêter Smart Feeder
    feeder_pid_file = 'colab_results/smart_feeder_pid.txt'
    if os.path.exists(feeder_pid_file):
        try:
            with open(feeder_pid_file, 'r') as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGTERM)
            os.remove(feeder_pid_file)
            stopped_components.append(f"Smart Feeder (PID: {pid})")
        except (ProcessLookupError, ValueError):
            pass
    
    # Arrêter Collecteur Turbo
    turbo_pid_file = 'colab_results/turbo_collector_pid.txt'
    if os.path.exists(turbo_pid_file):
        try:
            with open(turbo_pid_file, 'r') as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGTERM)
            os.remove(turbo_pid_file)
            stopped_components.append(f"Collecteur Turbo (PID: {pid})")
        except (ProcessLookupError, ValueError):
            pass
    
    # Force kill de tous les processus liés
    try:
        subprocess.run(['pkill', '-f', 'turbo_corpus_collector'], check=False)
        subprocess.run(['pkill', '-f', 'smart_feeder'], check=False)
        subprocess.run(['pkill', '-f', 'fast_corpus_collector'], check=False)
    except Exception:
        pass
    
    if stopped_components:
        print("✅ Composants arrêtés:")
        for component in stopped_components:
            print(f"  - {component}")
    else:
        print("⚠️ Aucun composant turbo actif trouvé")
    
    print("🔄 Tous les processus de collecte arrêtés")
    print("✅ Système turbo arrêté!")

if __name__ == "__main__":
    stop_turbo_feeding()