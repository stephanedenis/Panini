#!/usr/bin/env python3
"""
Détecteur de logs actifs et processus cachés
Trouve les sources d'activité qui échappent à la détection normale
"""

import subprocess
import os
import time
import glob
from datetime import datetime

def surveiller_fichiers_logs_actifs():
    """Surveille les fichiers logs avec écriture active"""
    print("👀 Surveillance des fichiers logs actifs...")
    
    # Patterns de logs possibles
    patterns = [
        "*.log", "*_log.txt", "*.json", 
        "etat_*.json", "*_iter*.json",
        "optimisation_*.log", "analyse_*.log"
    ]
    
    fichiers_actifs = []
    
    for pattern in patterns:
        for fichier in glob.glob(pattern):
            try:
                # Prendre la taille initiale
                taille_initiale = os.path.getsize(fichier)
                time.sleep(2)  # Attendre 2 secondes
                taille_finale = os.path.getsize(fichier)
                
                if taille_finale > taille_initiale:
                    print(f"📝 FICHIER ACTIF: {fichier}")
                    print(f"   Croissance: +{taille_finale - taille_initiale} bytes en 2s")
                    
                    # Lire les dernières lignes
                    try:
                        with open(fichier, 'r', encoding='utf-8', errors='ignore') as f:
                            lignes = f.readlines()
                            if lignes:
                                print(f"   Dernière ligne: {lignes[-1].strip()}")
                    except:
                        pass
                    
                    fichiers_actifs.append(fichier)
                    
            except Exception as e:
                continue
    
    return fichiers_actifs

def recherche_processus_exhaustive():
    """Recherche exhaustive de tous les processus Python"""
    print("\n🕵️ Recherche exhaustive de processus...")
    
    try:
        # Commande plus détaillée
        cmd = ["ps", "-ef"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        processus_suspects = []
        
        for line in result.stdout.split('\n'):
            if 'python' in line.lower():
                # Chercher des mots-clés suspects
                suspects = [
                    'iter', 'optimis', 'hill', 'evaluat', 'generat',
                    'ultime', 'analys', 'raffin', 'amelior', 'concept',
                    'geometr', 'ambigui'
                ]
                
                if any(suspect in line.lower() for suspect in suspects):
                    parts = line.split()
                    if len(parts) >= 2:
                        pid = parts[1]
                        print(f"🎯 PROCESSUS SUSPECT: PID {pid}")
                        print(f"   Commande: {line}")
                        processus_suspects.append(pid)
        
        return processus_suspects
        
    except Exception as e:
        print(f"❌ Erreur recherche exhaustive: {e}")
        return []

def detecter_processus_zombie_ou_cache():
    """Détecte des processus qui pourraient être cachés ou zombies"""
    print("\n🧟 Détection processus cachés/zombies...")
    
    try:
        # Chercher les processus par nom de fichier Python spécifique
        commandes = [
            ["pgrep", "-f", "optimiseur"],
            ["pgrep", "-f", "hillclimbing"], 
            ["pgrep", "-f", "analyseur"],
            ["pgrep", "-f", "ultime"],
            ["pgrep", "-f", "iteration"]
        ]
        
        pids_trouves = []
        
        for cmd in commandes:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.stdout.strip():
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        if pid.isdigit():
                            print(f"🔍 Trouvé PID {pid} avec {' '.join(cmd[2:])}")
                            pids_trouves.append(pid)
            except:
                continue
        
        return pids_trouves
        
    except Exception as e:
        print(f"❌ Erreur détection cachés: {e}")
        return []

def arreter_processus_par_pid(pid):
    """Arrête un processus par PID"""
    try:
        print(f"🛑 Arrêt forcé PID {pid}...")
        subprocess.run(["kill", "-9", pid], capture_output=True)
        time.sleep(1)
        
        # Vérifier si arrêté
        result = subprocess.run(["kill", "-0", pid], capture_output=True)
        if result.returncode != 0:
            print(f"✅ PID {pid} arrêté avec succès")
            return True
        else:
            print(f"❌ PID {pid} résiste encore")
            return False
    except:
        print(f"❌ Erreur arrêt PID {pid}")
        return False

def main():
    print("🔎 DÉTECTEUR AVANCÉ D'ACTIVITÉ RÉSIDUELLE")
    print("=" * 50)
    
    # 1. Surveiller les fichiers logs actifs
    fichiers_actifs = surveiller_fichiers_logs_actifs()
    
    if fichiers_actifs:
        print(f"\n⚠️ {len(fichiers_actifs)} fichiers logs avec activité détectée!")
        for fichier in fichiers_actifs:
            print(f"  📄 {fichier}")
    else:
        print("\n✅ Aucun fichier log actif détecté")
    
    # 2. Recherche exhaustive
    processus_suspects = recherche_processus_exhaustive()
    
    # 3. Détection cachée
    pids_caches = detecter_processus_zombie_ou_cache()
    
    # 4. Compilation des PIDs à arrêter
    tous_pids = list(set(processus_suspects + pids_caches))
    
    if tous_pids:
        print(f"\n🎯 {len(tous_pids)} processus suspects à arrêter:")
        for pid in tous_pids:
            print(f"  • PID {pid}")
        
        print(f"\n🛑 Arrêt de {len(tous_pids)} processus...")
        arretes = 0
        for pid in tous_pids:
            if arreter_processus_par_pid(pid):
                arretes += 1
        
        print(f"\n✅ {arretes}/{len(tous_pids)} processus arrêtés")
    else:
        print("\n✅ Aucun processus suspect détecté")
    
    # 5. Vérification finale des fichiers actifs
    print(f"\n🔄 Vérification finale des logs actifs...")
    time.sleep(3)
    
    fichiers_encore_actifs = surveiller_fichiers_logs_actifs()
    
    print(f"\n" + "=" * 50)
    if not fichiers_encore_actifs and not tous_pids:
        print("🎉 SYSTÈME COMPLÈTEMENT SILENCIEUX")
        print("   Aucune activité résiduelle détectée")
    elif len(fichiers_encore_actifs) == 0:
        print("✅ ACTIVITÉ ARRÊTÉE")  
        print("   Les logs ne grandissent plus")
    else:
        print("⚠️ ACTIVITÉ RÉSIDUELLE PERSISTANTE")
        print(f"   {len(fichiers_encore_actifs)} fichiers encore actifs")
        for f in fichiers_encore_actifs:
            print(f"   📄 {f}")

if __name__ == "__main__":
    main()