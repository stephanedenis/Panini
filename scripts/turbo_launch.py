#!/usr/bin/env python3
"""
🚀 Turbo Launch - Lancement coordonné haute vitesse
Démarre collecteur turbo + smart feeder pour nourrir Colab rapidement
"""

import os
import subprocess
import time
import json
from datetime import datetime

def print_turbo_banner():
    """Bannière turbo"""
    print("⚡" + "="*60 + "⚡")
    print("   TURBO LAUNCH - ALIMENTATION HAUTE VITESSE")
    print("   Colab affamé? On le nourrit massivement!")
    print("⚡" + "="*60 + "⚡")

def check_colab_hunger():
    """Vérifier si Colab a faim (buffer bas)"""
    data_dir = "data/incremental_corpus"
    files_count = len([f for f in os.listdir(data_dir) if f.endswith('.json')])
    
    print(f"📊 Buffer actuel: {files_count} fichiers")
    
    if files_count < 20:
        return "critique"
    elif files_count < 50:
        return "bas"
    else:
        return "ok"

def launch_turbo_collection():
    """Lancer collecte turbo immédiate"""
    print("🚀 Lancement COLLECTE TURBO...")
    
    try:
        process = subprocess.Popen(
            ['python3', 'scripts/turbo_corpus_collector.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print(f"✅ Collecteur turbo lancé (PID: {process.pid})")
        
        # Sauvegarder PID
        with open('colab_results/turbo_collector_pid.txt', 'w') as f:
            f.write(str(process.pid))
        
        return process.pid
        
    except Exception as e:
        print(f"❌ Erreur lancement turbo: {e}")
        return None

def launch_smart_feeder():
    """Lancer le smart feeder en arrière-plan"""
    print("🎯 Lancement SMART FEEDER...")
    
    try:
        process = subprocess.Popen(
            ['python3', 'scripts/smart_feeder.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print(f"✅ Smart Feeder lancé (PID: {process.pid})")
        
        # Sauvegarder PID
        with open('colab_results/smart_feeder_pid.txt', 'w') as f:
            f.write(str(process.pid))
        
        return process.pid
        
    except Exception as e:
        print(f"❌ Erreur lancement feeder: {e}")
        return None

def create_turbo_status():
    """Créer fichier de statut turbo"""
    status = {
        'timestamp': datetime.now().isoformat(),
        'mode': 'turbo_feeding',
        'components': {
            'turbo_collector': 'active',
            'smart_feeder': 'active',
            'colab_notebook': 'ready'
        },
        'feeding_rate': 'maximum',
        'target': 'maintain_buffer_50_files',
        'instructions': [
            '1. Colab notebook prêt à analyser',
            '2. Collecte turbo active',
            '3. Feeder intelligent surveille le buffer',
            '4. Alimentation continue garantie'
        ]
    }
    
    os.makedirs('colab_results', exist_ok=True)
    with open('colab_results/turbo_status.json', 'w', encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=2)
    
    print("📝 Statut turbo créé")

def show_turbo_info():
    """Afficher infos turbo"""
    print("\n📊 CONFIGURATION TURBO:")
    print("├── 🚀 Collecteur Turbo: 15 docs/cycle, sources multiples")
    print("├── 🎯 Smart Feeder: Buffer auto-maintenu à 50 fichiers")
    print("├── ⚡ Débit cible: 30-50 docs/minute")
    print("└── 🔄 Synchronisation GitHub continue")
    
    print("\n🎯 MONITORING:")
    print("├── 📋 Logs: turbo_collector.log")
    print("├── 📊 Stats: colab_results/turbo_collector_stats.json")
    print("├── 🎯 Feeder: colab_results/smart_feeder_stats.json")
    print("└── 📁 Buffer: data/incremental_corpus/")
    
    print("\n⏹️ ARRÊT:")
    print("   python3 scripts/stop_turbo_feeding.py")

def wait_for_initial_boost():
    """Attendre le boost initial"""
    print("\n⏳ Phase de boost initial...")
    
    initial_files = len([f for f in os.listdir('data/incremental_corpus') if f.endswith('.json')])
    target_boost = initial_files + 20  # +20 fichiers
    
    start_time = time.time()
    timeout = 300  # 5 minutes max
    
    while time.time() - start_time < timeout:
        current_files = len([f for f in os.listdir('data/incremental_corpus') if f.endswith('.json')])
        
        if current_files >= target_boost:
            boost_time = time.time() - start_time
            rate = (current_files - initial_files) / (boost_time / 60)
            print(f"🚀 Boost terminé! +{current_files - initial_files} fichiers en {boost_time:.1f}s ({rate:.1f} fichiers/min)")
            break
        
        print(f"📈 Buffer: {current_files} fichiers (+{current_files - initial_files})")
        time.sleep(10)
    
    return current_files >= target_boost

def main():
    """Point d'entrée turbo"""
    print_turbo_banner()
    
    # Vérifier l'état du buffer
    hunger_level = check_colab_hunger()
    print(f"🍽️ Niveau de faim Colab: {hunger_level}")
    
    # Stratégie selon la faim
    if hunger_level == "critique":
        print("🚨 SITUATION CRITIQUE - Boost immédiat!")
        strategy = "emergency_boost"
    elif hunger_level == "bas":
        print("⚠️ Buffer bas - Alimentation renforcée")
        strategy = "reinforced_feeding"
    else:
        print("✅ Buffer OK - Maintien préventif")
        strategy = "preventive_maintenance"
    
    print(f"\n🎯 Stratégie: {strategy}")
    
    # Lancer les composants
    print("\n🚀 DÉMARRAGE COORDONNÉ...")
    
    # 1. Smart Feeder (surveillance continue)
    feeder_pid = launch_smart_feeder()
    
    # 2. Collecte turbo immédiate si nécessaire
    if hunger_level in ["critique", "bas"]:
        turbo_pid = launch_turbo_collection()
        time.sleep(2)  # Laisser démarrer
    
    # 3. Créer statut
    create_turbo_status()
    
    # 4. Attendre boost initial si critique
    if hunger_level == "critique":
        boost_success = wait_for_initial_boost()
        if boost_success:
            print("✅ Boost réussi - Colab peut manger!")
        else:
            print("⚠️ Boost partiel - Continuons...")
    
    # Affichage final
    print("\n" + "="*70)
    show_turbo_info()
    print("="*70)
    
    print(f"\n🎯 TURBO FEEDING ACTIF!")
    print("📊 Buffer maintenu automatiquement")
    print("🔥 Colab peut analyser à pleine vitesse!")
    
    if feeder_pid:
        print(f"✅ Smart Feeder actif (PID: {feeder_pid})")

if __name__ == "__main__":
    main()