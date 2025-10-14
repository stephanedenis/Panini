#!/usr/bin/env python3
"""
Arrêt forcé des processus d'optimisation persistants
Détecte et arrête les processus hill-climbing, optimisation et itérations en cours
"""

import subprocess
import signal
import time
import json
import os
from datetime import datetime

def detecter_processus_optimisation():
    """Détecte tous les processus d'optimisation en cours"""
    try:
        # Chercher tous les processus python
        cmd = ["ps", "aux"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        processus_optimisation = []
        
        for line in result.stdout.split('\n'):
            if 'python' in line.lower():
                # Mots-clés d'optimisation
                mots_cles = [
                    'optimiseur', 'hillclimbing', 'hill_climbing', 
                    'iteration', 'evaluation', 'ultime',
                    'raffinement', 'amelioration', 'generation',
                    'analyseur_ambiguites', 'geometrique'
                ]
                
                if any(mot in line.lower() for mot in mots_cles):
                    parts = line.split()
                    if len(parts) >= 2:
                        processus_optimisation.append({
                            'pid': parts[1],
                            'cpu': parts[2] if len(parts) > 2 else '0.0',
                            'mem': parts[3] if len(parts) > 3 else '0.0',
                            'commande': ' '.join(parts[10:]) if len(parts) > 10 else line
                        })
        
        return processus_optimisation
    
    except Exception as e:
        print(f"❌ Erreur détection processus: {e}")
        return []

def arreter_processus(pid, nom="processus"):
    """Arrête un processus avec gestion d'erreurs"""
    try:
        print(f"🛑 Arrêt {nom} (PID: {pid})...")
        
        # Tentative d'arrêt doux
        os.kill(int(pid), signal.SIGTERM)
        time.sleep(2)
        
        # Vérifier si le processus existe encore
        try:
            os.kill(int(pid), 0)  # Signal 0 = test existence
            print(f"⚠️ Processus {pid} résistant, arrêt forcé...")
            os.kill(int(pid), signal.SIGKILL)
            time.sleep(1)
        except ProcessLookupError:
            print(f"✅ Processus {pid} arrêté avec succès")
            return True
            
    except ProcessLookupError:
        print(f"✅ Processus {pid} déjà arrêté")
        return True
    except PermissionError:
        print(f"❌ Permission refusée pour {pid}")
        return False
    except Exception as e:
        print(f"❌ Erreur arrêt {pid}: {e}")
        return False

def nettoyer_fichiers_temporaires_optimisation():
    """Nettoie les fichiers temporaires liés à l'optimisation"""
    fichiers_a_supprimer = []
    
    # Patterns de fichiers temporaires
    patterns = [
        'etat_ULTIME-*.json',
        '*_iter*.json',
        'optimisation_*.log',
        'hillclimbing_*.json',
        'evaluation_*.tmp',
        '*_log.txt'
    ]
    
    import glob
    for pattern in patterns:
        for fichier in glob.glob(pattern):
            try:
                # Vérifier l'âge du fichier
                stat = os.stat(fichier)
                age_heures = (time.time() - stat.st_mtime) / 3600
                
                # Supprimer les fichiers de plus d'1 heure ou très récents (processus actif)
                if age_heures > 1 or age_heures < 0.1:
                    os.remove(fichier)
                    fichiers_a_supprimer.append(fichier)
                    print(f"🗑️ Supprimé: {fichier}")
                    
            except Exception as e:
                print(f"❌ Erreur suppression {fichier}: {e}")
    
    return fichiers_a_supprimer

def main():
    print("🚫 ARRÊT FORCÉ PROCESSUS D'OPTIMISATION")
    print("=" * 50)
    
    # 1. Détecter les processus d'optimisation
    print("\n🔍 Détection des processus d'optimisation...")
    processus = detecter_processus_optimisation()
    
    if not processus:
        print("✅ Aucun processus d'optimisation détecté")
        return
    
    print(f"🎯 {len(processus)} processus d'optimisation trouvés:")
    for p in processus:
        print(f"  • PID {p['pid']}: {p['commande'][:60]}...")
        print(f"    CPU: {p['cpu']}% | MEM: {p['mem']}%")
    
    # 2. Arrêter les processus
    print(f"\n🛑 Arrêt de {len(processus)} processus...")
    processus_arretes = 0
    
    for p in processus:
        if arreter_processus(p['pid'], f"optimisation {p['pid']}"):
            processus_arretes += 1
    
    print(f"\n✅ {processus_arretes}/{len(processus)} processus arrêtés")
    
    # 3. Attendre un peu puis vérifier
    print("\n⏳ Vérification finale...")
    time.sleep(3)
    
    processus_restants = detecter_processus_optimisation()
    if processus_restants:
        print(f"⚠️ {len(processus_restants)} processus encore actifs:")
        for p in processus_restants:
            print(f"  • PID {p['pid']}: {p['commande'][:50]}...")
    else:
        print("✅ Tous les processus d'optimisation sont arrêtés")
    
    # 4. Nettoyer les fichiers temporaires
    print(f"\n🧹 Nettoyage fichiers temporaires...")
    fichiers_supprimes = nettoyer_fichiers_temporaires_optimisation()
    print(f"✅ {len(fichiers_supprimes)} fichiers temporaires supprimés")
    
    # 5. Rapport final
    rapport = {
        'timestamp': datetime.now().isoformat(),
        'processus_detectes': len(processus),
        'processus_arretes': processus_arretes,
        'processus_restants': len(processus_restants),
        'fichiers_supprimes': len(fichiers_supprimes),
        'succes_complet': len(processus_restants) == 0
    }
    
    nom_rapport = f'arret_optimisation_{int(time.time())}.json'
    with open(nom_rapport, 'w', encoding='utf-8') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Rapport sauvegardé: {nom_rapport}")
    
    print("\n" + "=" * 50)
    if len(processus_restants) == 0:
        print("🎉 ARRÊT COMPLET RÉUSSI")
        print("   Tous les processus d'optimisation sont arrêtés")
        print("   Le défilement dans les terminaux devrait s'arrêter")
    else:
        print("⚠️ ARRÊT PARTIEL")
        print("   Certains processus résistent encore")
        print("   Vous pouvez réexécuter ce script si nécessaire")

if __name__ == "__main__":
    main()