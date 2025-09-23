#!/usr/bin/env python3
"""
Vérificateur Performance Système
Script simple pour vérifier l'état après optimisation des goulots d'étranglement
"""

import requests
import json
import psutil
import time
from datetime import datetime

def verifier_performance_systeme():
    """Vérifie les performances du système après optimisation"""
    print("🔍 VÉRIFICATION PERFORMANCE SYSTÈME")
    print("=" * 50)
    
    # 1. État général du système
    print("\n📊 RESSOURCES SYSTÈME:")
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    print(f"   CPU: {cpu_percent:.1f}%")
    print(f"   RAM: {memory.percent:.1f}% ({memory.used // (1024**3):.1f}GB / {memory.total // (1024**3):.1f}GB)")
    print(f"   Processus: {len(psutil.pids())}")
    
    # 2. Processus PaniniFS
    print("\n🔄 PROCESSUS PANINIFS:")
    panini_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_percent']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or [])
            if any(term in cmdline.lower() for term in ['panini', 'orchestrateur', 'gestionnaire', 'collecteur', 'dashboard']):
                cpu = proc.cpu_percent()
                memory = proc.memory_percent()
                name = proc.info['name']
                pid = proc.info['pid']
                
                # Identifier le type de processus
                if 'orchestrateur' in cmdline:
                    type_proc = "🎭 Orchestrateur"
                elif 'gestionnaire' in cmdline:
                    type_proc = "⚙️  Gestionnaire"
                elif 'collecteur' in cmdline:
                    type_proc = "📚 Collecteur"
                elif 'dashboard' in cmdline:
                    type_proc = "🖥️  Dashboard"
                else:
                    type_proc = "🔧 Autre"
                
                print(f"   {type_proc}: PID {pid} | CPU {cpu:.1f}% | RAM {memory:.1f}%")
                panini_processes.append((type_proc, pid, cpu, memory))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    print(f"\n   Total processus PaniniFS: {len(panini_processes)}")
    
    # 3. Dashboard API
    print("\n🌐 DASHBOARD API:")
    try:
        response = requests.get('http://localhost:8097/api/modules', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Dashboard accessible")
            print(f"   📊 Modules actifs: {data.get('active_modules', 0)}")
            print(f"   ⚡ CPU système: {data.get('system', {}).get('cpu_percent', 0):.1f}%")
            print(f"   📈 Performance: {data.get('performance', {}).get('efficiency', 0)}% efficacité")
            
            # Détails modules
            print("\n   📋 DÉTAILS MODULES:")
            modules = ['orchestrateur', 'collecteur', 'gestionnaire']
            for module in modules:
                module_data = data.get(module, {})
                if module_data:
                    active = "✅" if module_data.get('active', False) else "❌"
                    cpu = module_data.get('cpu_percent', 0)
                    print(f"      {module.capitalize()}: {active} | CPU {cpu:.1f}%")
        else:
            print(f"   ❌ Dashboard inaccessible (code: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erreur connexion dashboard: {e}")
    
    # 4. Analyse des améliorations
    print("\n🎯 ANALYSE AMÉLIORATIONS:")
    
    # Charge CPU
    if cpu_percent < 30:
        print("   ✅ Charge CPU optimale (< 30%)")
    elif cpu_percent < 60:
        print("   ⚠️  Charge CPU modérée (30-60%)")
    else:
        print("   🚨 Charge CPU élevée (> 60%)")
    
    # RAM
    if memory.percent < 50:
        print("   ✅ Utilisation RAM optimale (< 50%)")
    elif memory.percent < 80:
        print("   ⚠️  Utilisation RAM modérée (50-80%)")
    else:
        print("   🚨 Utilisation RAM élevée (> 80%)")
    
    # Processus
    if len(panini_processes) <= 5:
        print("   ✅ Nombre de processus raisonnable (≤ 5)")
    elif len(panini_processes) <= 10:
        print("   ⚠️  Nombre de processus modéré (6-10)")
    else:
        print("   🚨 Trop de processus (> 10)")
    
    # 5. Recommandations
    print("\n💡 RECOMMANDATIONS:")
    
    if cpu_percent > 60:
        print("   🔧 Réduire charge CPU - vérifier processus gourmands")
    
    if memory.percent > 70:
        print("   🔧 Libérer mémoire - arrêter processus non-essentiels")
    
    if len(panini_processes) > 8:
        print("   🔧 Optimiser nombre de processus - consolider services")
    
    try:
        response = requests.get('http://localhost:8097/api/modules', timeout=2)
        if response.status_code != 200:
            print("   🔧 Vérifier dashboard - relancer si nécessaire")
    except:
        print("   🔧 Dashboard inaccessible - vérifier processus")
    
    # 6. Résumé
    print("\n📋 RÉSUMÉ:")
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   CPU: {cpu_percent:.1f}% | RAM: {memory.percent:.1f}% | Processus: {len(panini_processes)}")
    
    # Score global
    score = 100
    if cpu_percent > 30: score -= (cpu_percent - 30) * 2
    if memory.percent > 50: score -= (memory.percent - 50) * 1.5
    if len(panini_processes) > 5: score -= (len(panini_processes) - 5) * 5
    
    score = max(0, min(100, score))
    
    if score >= 90:
        print(f"   🎉 Score système: {score:.0f}/100 - EXCELLENT")
    elif score >= 70:
        print(f"   ✅ Score système: {score:.0f}/100 - BON")
    elif score >= 50:
        print(f"   ⚠️  Score système: {score:.0f}/100 - MOYEN")
    else:
        print(f"   🚨 Score système: {score:.0f}/100 - PROBLÉMATIQUE")

def verifier_goulots_etranglement():
    """Vérifie spécifiquement les goulots d'étranglement"""
    print("\n\n🚨 VÉRIFICATION GOULOTS D'ÉTRANGLEMENT")
    print("=" * 50)
    
    # Processus amdgpu_top
    amdgpu_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or [])
            if 'amdgpu_top' in cmdline:
                amdgpu_processes.append(proc)
        except:
            continue
    
    if amdgpu_processes:
        print(f"   🚨 ALERTE: {len(amdgpu_processes)} processus amdgpu_top détectés")
        for proc in amdgpu_processes:
            print(f"      PID {proc.pid}: CPU {proc.cpu_percent()}%")
    else:
        print("   ✅ Aucun processus amdgpu_top parasite")
    
    # Redémarrages excessifs
    try:
        with open('gestionnaire_arriere_plan.log', 'r') as f:
            lines = f.readlines()
            restarts_recent = sum(1 for line in lines[-100:] if 'Redémarrage processus' in line)
            
        if restarts_recent > 10:
            print(f"   🚨 ALERTE: {restarts_recent} redémarrages récents détectés")
        elif restarts_recent > 3:
            print(f"   ⚠️  {restarts_recent} redémarrages récents")
        else:
            print(f"   ✅ Redémarrages sous contrôle ({restarts_recent})")
    except:
        print("   ⚠️  Impossible de vérifier logs redémarrages")
    
    # Processus haute consommation
    high_cpu_procs = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            cpu = proc.cpu_percent()
            if cpu > 50:
                high_cpu_procs.append((proc.pid, proc.name(), cpu))
        except:
            continue
    
    if high_cpu_procs:
        print(f"   ⚠️  {len(high_cpu_procs)} processus haute consommation CPU:")
        for pid, name, cpu in high_cpu_procs[:5]:
            print(f"      PID {pid} ({name}): {cpu:.1f}%")
    else:
        print("   ✅ Aucun processus haute consommation CPU")

if __name__ == "__main__":
    try:
        verifier_performance_systeme()
        verifier_goulots_etranglement()
    except KeyboardInterrupt:
        print("\n⏹️  Vérification interrompue")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")