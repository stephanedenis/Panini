#!/usr/bin/env python3
"""
🔍 TEST SURVEILLANCE SYSTÈMES AUTONOMES
=====================================
Test rapide de la surveillance sans serveur web
"""

import json
import time
import psutil
import subprocess
from pathlib import Path
from datetime import datetime


def test_autonomous_systems_monitoring():
    """Test surveillance systèmes autonomes"""
    workspace = Path('/home/stephane/GitHub/PaniniFS-Research')
    
    print("🎯 TEST SURVEILLANCE SYSTÈMES AUTONOMES")
    print("=" * 50)
    
    # Systèmes à surveiller
    monitored_systems = {
        'coordinateur_global_autonome.py': 'Coordinateur Global 🎯',
        'systeme_autonome_recherche_dhatu.py': 'Moteur Recherche 🔬',
        'collecteur_corpus_autonome.py': 'Collecteur Corpus 📚',
        'optimiseur_ml_autonome.py': 'Optimiseur ML 🧠',
        'systeme_validation_metriques.py': 'Validation Métriques 📊'
    }
    
    print("\n1. 🔍 ÉTAT DES PROCESSUS:")
    running_count = 0
    
    for script, name in monitored_systems.items():
        try:
            result = subprocess.run([
                'pgrep', '-f', script
            ], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0 and result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                pid = int(pids[0]) if pids[0] else None
                
                if pid:
                    try:
                        proc = psutil.Process(pid)
                        status = "🟢 ACTIF"
                        cpu = proc.cpu_percent()
                        memory = proc.memory_percent()
                        uptime = time.time() - proc.create_time()
                        running_count += 1
                        
                        print(f"   {name}: {status}")
                        print(f"      PID: {pid}, CPU: {cpu:.1f}%, RAM: {memory:.1f}%, Uptime: {int(uptime)}s")
                    except psutil.NoSuchProcess:
                        print(f"   {name}: 🟡 ZOMBIE")
                else:
                    print(f"   {name}: 🔴 ARRÊTÉ")
            else:
                print(f"   {name}: 🔴 ARRÊTÉ")
                
        except Exception as e:
            print(f"   {name}: ❌ ERREUR - {e}")
    
    print(f"\n   📊 RÉSUMÉ: {running_count}/{len(monitored_systems)} systèmes actifs")
    
    # Répertoires autonomes
    print("\n2. 📁 RÉPERTOIRES AUTONOMES:")
    
    patterns = [
        'autonomous_research_*',
        'coordination_*', 
        'corpus_collection_*',
        'optimization_*',
        'validation_metrics_*'
    ]
    
    total_dirs = 0
    total_files = 0
    total_size = 0
    
    for pattern in patterns:
        dirs = list(workspace.glob(pattern))
        if dirs:
            print(f"   📂 {pattern}:")
            for dir_path in dirs:
                if dir_path.is_dir():
                    files = list(dir_path.glob('*'))
                    files_count = len([f for f in files if f.is_file()])
                    dir_size = sum(f.stat().st_size for f in files if f.is_file())
                    
                    last_mod = max(
                        (f.stat().st_mtime for f in files if f.is_file()),
                        default=0
                    )
                    last_mod_str = datetime.fromtimestamp(last_mod).strftime('%H:%M:%S')
                    
                    print(f"      {dir_path.name}: {files_count} fichiers, {dir_size/(1024*1024):.1f}MB, modifié: {last_mod_str}")
                    
                    total_dirs += 1
                    total_files += files_count
                    total_size += dir_size
    
    print(f"\n   📊 TOTAL: {total_dirs} répertoires, {total_files} fichiers, {total_size/(1024*1024):.1f}MB")
    
    # Métriques de recherche
    print("\n3. 📈 MÉTRIQUES DE RECHERCHE:")
    
    cycles = 0
    hypotheses = 0
    errors = 0
    corpus_size = 0
    
    # Scan logs
    log_files = list(workspace.glob('**/*.log'))
    print(f"   📋 Analyse de {len(log_files)} fichiers log...")
    
    for log_file in log_files:
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            cycles += len([m for m in content.split('\n') if 'Début cycle' in m])
            hypotheses += len([m for m in content.split('\n') if 'nouvelles hypothèses' in m])
            errors += len([m for m in content.split('\n') if 'ERROR' in m or 'Erreur' in m])
            
        except Exception:
            continue
    
    # Scan JSON
    json_files = list(workspace.glob('**/*.json'))
    print(f"   📋 Analyse de {len(json_files)} fichiers JSON...")
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list) and any('dhatu' in str(item) for item in data[:5]):
                corpus_size += len(data)
                
        except Exception:
            continue
    
    print(f"   🔄 Cycles de recherche: {cycles}")
    print(f"   🧠 Hypothèses générées: {hypotheses}")
    print(f"   📚 Taille corpus: {corpus_size}")
    print(f"   ❌ Erreurs détectées: {errors}")
    
    # Santé système
    print("\n4. 🏥 SANTÉ SYSTÈME:")
    
    try:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        print(f"   💻 CPU: {cpu:.1f}%")
        print(f"   🧠 RAM: {memory.percent:.1f}% ({memory.available/(1024**3):.1f}GB libre)")
        print(f"   💾 Disque: {disk.percent:.1f}%")
        
        # Évaluation
        if cpu > 90 or memory.percent > 95:
            status = "🔴 CRITIQUE"
        elif cpu > 75 or memory.percent > 85:
            status = "🟡 ATTENTION"
        else:
            status = "🟢 SAIN"
        
        print(f"   📊 Statut global: {status}")
        
    except Exception as e:
        print(f"   ❌ Erreur santé système: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Test surveillance terminé")
    
    return {
        'running_systems': running_count,
        'total_systems': len(monitored_systems),
        'directories': total_dirs,
        'files': total_files,
        'research_cycles': cycles,
        'hypotheses': hypotheses,
        'corpus_size': corpus_size,
        'errors': errors
    }


if __name__ == "__main__":
    results = test_autonomous_systems_monitoring()
    
    print(f"\n🎯 RÉSUMÉ SURVEILLANCE:")
    print(f"   Systèmes actifs: {results['running_systems']}/{results['total_systems']}")
    print(f"   Répertoires créés: {results['directories']}")
    print(f"   Cycles recherche: {results['research_cycles']}")
    print(f"   Corpus collecté: {results['corpus_size']} éléments")