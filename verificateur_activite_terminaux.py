#!/usr/bin/env python3
"""
Vérificateur d'activité des terminaux
Analyse l'activité résiduelle après le nettoyage
"""

import subprocess
import json
import time
from datetime import datetime

def obtenir_processus_actifs():
    """Obtient tous les processus Python actifs liés au projet"""
    try:
        cmd = ["ps", "aux"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        processus_projet = []
        lines = result.stdout.split('\n')
        
        for line in lines[1:]:  # Skip header
            if line.strip() and 'python' in line.lower():
                parts = line.split(None, 10)
                if len(parts) >= 11:
                    processus_projet.append({
                        'pid': parts[1],
                        'cpu': parts[2],
                        'mem': parts[3],
                        'temps': parts[9],
                        'commande': parts[10]
                    })
        
        return processus_projet
    except Exception as e:
        print(f"❌ Erreur obtention processus: {e}")
        return []

def analyser_terminaux_actifs():
    """Analyse les terminaux avec activité récente"""
    try:
        # Vérifier les processus bash/python
        cmd = ["ps", "-ef"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        terminaux_actifs = []
        for line in result.stdout.split('\n'):
            if ('bash' in line or 'python' in line) and 'PaniniFS' in line:
                terminaux_actifs.append(line.strip())
        
        return terminaux_actifs
    except Exception as e:
        print(f"❌ Erreur analyse terminaux: {e}")
        return []

def verifier_fichiers_logs_recents():
    """Vérifie les fichiers de log avec activité récente"""
    import os
    import glob
    
    fichiers_logs = []
    patterns = ['*.log', '*_log.txt', 'nettoyage_rapport_*.json']
    
    for pattern in patterns:
        for fichier in glob.glob(pattern):
            try:
                stat = os.stat(fichier)
                age_minutes = (time.time() - stat.st_mtime) / 60
                if age_minutes < 10:  # Modifié dans les 10 dernières minutes
                    fichiers_logs.append({
                        'fichier': fichier,
                        'age_minutes': round(age_minutes, 2),
                        'taille': stat.st_size
                    })
            except:
                continue
    
    return sorted(fichiers_logs, key=lambda x: x['age_minutes'])

def verifier_ports_ecoute():
    """Vérifie les ports en écoute (dashboard, etc.)"""
    try:
        cmd = ["netstat", "-tlnp"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        ports_actifs = []
        for line in result.stdout.split('\n'):
            if ':8080' in line or ':5000' in line or 'python' in line:
                ports_actifs.append(line.strip())
        
        return ports_actifs
    except Exception as e:
        print(f"❌ Erreur vérification ports: {e}")
        return []

def main():
    print("🔍 VÉRIFICATION ACTIVITÉ TERMINAUX APRÈS NETTOYAGE")
    print("=" * 60)
    
    # 1. Processus Python actifs
    print("\n📊 PROCESSUS PYTHON ACTIFS:")
    processus = obtenir_processus_actifs()
    if processus:
        for p in processus:
            if any(keyword in p['commande'].lower() for keyword in 
                   ['dashboard', 'panini', 'analyseur', 'collecteur']):
                print(f"  🟡 PID {p['pid']}: {p['commande'][:80]}...")
                print(f"     CPU: {p['cpu']}% | MEM: {p['mem']}% | Temps: {p['temps']}")
    else:
        print("  ✅ Aucun processus Python projet détecté")
    
    # 2. Terminaux avec activité
    print("\n🖥️ TERMINAUX ACTIFS:")
    terminaux = analyser_terminaux_actifs()
    if terminaux:
        for terminal in terminaux[:5]:  # Limiter à 5
            print(f"  🔄 {terminal}")
    else:
        print("  ✅ Aucun terminal projet actif détecté")
    
    # 3. Fichiers logs récents
    print("\n📋 LOGS RÉCENTS (< 10 min):")
    logs_recents = verifier_fichiers_logs_recents()
    if logs_recents:
        for log in logs_recents[:10]:
            print(f"  📄 {log['fichier']}: {log['age_minutes']} min | {log['taille']} bytes")
    else:
        print("  ✅ Aucun log récent détecté")
    
    # 4. Ports en écoute
    print("\n🌐 PORTS EN ÉCOUTE:")
    ports = verifier_ports_ecoute()
    if ports:
        for port in ports[:5]:
            print(f"  🔌 {port}")
    else:
        print("  ✅ Aucun port projet en écoute")
    
    # 5. Analyse de l'activité résiduelle
    print("\n🎯 ANALYSE ACTIVITÉ RÉSIDUELLE:")
    
    # Compter les éléments actifs
    nb_processus = len([p for p in processus if any(k in p['commande'].lower() 
                                                   for k in ['dashboard', 'panini', 'analyseur'])])
    nb_logs_recents = len(logs_recents)
    nb_ports = len(ports)
    
    if nb_processus > 0:
        print(f"  ⚠️ {nb_processus} processus projet encore actifs")
        print("     → Activité normale si dashboard ou processus intentionnels")
    
    if nb_logs_recents > 0:
        print(f"  📝 {nb_logs_recents} fichiers logs récents")
        print("     → Activité de logging normale après opérations récentes")
    
    if nb_ports > 0:
        print(f"  🌐 {nb_ports} ports en écoute")
        print("     → Dashboard ou services toujours actifs")
    
    # Verdict final
    print("\n" + "="*60)
    if nb_processus <= 2 and nb_logs_recents <= 3:
        print("✅ ACTIVITÉ RÉSIDUELLE NORMALE")
        print("   Les processus essentiels (dashboard) sont préservés")
        print("   L'activité visible est probablement liée au système ou au dashboard")
    else:
        print("⚠️ ACTIVITÉ RÉSIDUELLE ÉLEVÉE")
        print("   Vérifiez si des processus supplémentaires doivent être arrêtés")
    
    # Sauvegarde rapport
    rapport = {
        'timestamp': datetime.now().isoformat(),
        'processus_actifs': len(processus),
        'logs_recents': len(logs_recents),
        'ports_actifs': len(ports),
        'activite_normale': nb_processus <= 2 and nb_logs_recents <= 3
    }
    
    with open(f'verification_terminaux_{int(time.time())}.json', 'w', encoding='utf-8') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Rapport sauvegardé: verification_terminaux_{int(time.time())}.json")

if __name__ == "__main__":
    main()