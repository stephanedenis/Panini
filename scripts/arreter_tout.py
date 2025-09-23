#!/usr/bin/env python3

import psutil
import time

def arreter_tous_les_processus():
    """Arrête proprement tous les processus autonomes"""
    
    print("🛑 ARRÊT DE TOUS LES PROCESSUS AUTONOMES")
    print("=" * 45)
    
    # Processus à arrêter
    keywords = [
        'systeme_evenementiel_cpu.py',
        'dashboard_evenementiel.py',
        'dashboard_realtime_avance.py',
        'moniteur_systeme_avance.py',
        'coordinateur_global_autonome.py',
        'systeme_autonome_recherche_dhatu.py',
        'collecteur_corpus_autonome.py',
        'optimiseur_ml_autonome.py'
    ]
    
    processes_found = []
    
    # Trouve tous les processus autonomes
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or [])
            
            for keyword in keywords:
                if keyword in cmdline:
                    processes_found.append({
                        'pid': proc.info['pid'],
                        'name': keyword,
                        'process': proc
                    })
                    break
                    
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if not processes_found:
        print("✅ Aucun processus autonome détecté")
        return True
    
    print(f"📊 {len(processes_found)} processus trouvés:")
    for p in processes_found:
        print(f"   🔸 {p['name']} (PID {p['pid']})")
    
    # Arrêt propre avec SIGTERM
    print("\n🔄 Arrêt propre avec SIGTERM...")
    terminated = []
    
    for p in processes_found:
        try:
            p['process'].terminate()
            print(f"📤 SIGTERM envoyé à {p['name']} (PID {p['pid']})")
            terminated.append(p)
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"⚠️ Impossible d'arrêter {p['name']}: {e}")
    
    # Attente de l'arrêt propre
    print("⏳ Attente arrêt propre (5 secondes)...")
    time.sleep(5)
    
    # Vérifie quels processus sont encore actifs
    still_running = []
    for p in terminated:
        try:
            if p['process'].is_running():
                still_running.append(p)
            else:
                print(f"✅ {p['name']} arrêté proprement")
        except psutil.NoSuchProcess:
            print(f"✅ {p['name']} arrêté")
    
    # Force l'arrêt des processus récalcitrants
    if still_running:
        print(f"\n🔥 Arrêt forcé de {len(still_running)} processus récalcitrants...")
        
        for p in still_running:
            try:
                p['process'].kill()
                print(f"💀 SIGKILL envoyé à {p['name']} (PID {p['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print(f"⚠️ {p['name']} déjà arrêté")
        
        time.sleep(2)
    
    # Vérification finale
    print("\n🔍 Vérification finale...")
    remaining = 0
    
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or [])
            for keyword in keywords:
                if keyword in cmdline:
                    print(f"⚠️ Processus encore actif: {keyword} (PID {proc.info['pid']})")
                    remaining += 1
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if remaining == 0:
        print("✅ Tous les processus autonomes sont arrêtés")
        return True
    else:
        print(f"❌ {remaining} processus encore actifs")
        return False

def verifier_ports():
    """Vérifie que les ports sont libérés"""
    
    print("\n🌐 VÉRIFICATION DES PORTS")
    print("=" * 30)
    
    ports_to_check = [8890, 8891, 8892]
    ports_used = []
    
    for conn in psutil.net_connections():
        if conn.laddr and conn.laddr.port in ports_to_check:
            ports_used.append(conn.laddr.port)
    
    if not ports_used:
        print("✅ Tous les ports dashboard sont libres")
    else:
        print(f"⚠️ Ports encore utilisés: {ports_used}")
    
    return len(ports_used) == 0

if __name__ == "__main__":
    
    print("🛑 ARRÊT COMPLET AVANT RÉORGANISATION")
    print("=" * 50)
    print("Ceci va arrêter tous les processus autonomes")
    print("pour permettre une réorganisation propre des fichiers")
    
    # Arrêt des processus
    if arreter_tous_les_processus():
        
        # Vérification des ports
        ports_free = verifier_ports()
        
        print(f"\n🎯 RÉSUMÉ")
        print("✅ Processus autonomes: ARRÊTÉS")
        print(f"{'✅' if ports_free else '⚠️'} Ports dashboard: {'LIBRES' if ports_free else 'OCCUPÉS'}")
        
        print(f"\n💡 WORKSPACE PRÊT POUR RÉORGANISATION")
        print("Vous pouvez maintenant déplacer les fichiers en sécurité")
        print("Pour redémarrer après réorganisation:")
        print("   python3 systeme_evenementiel/systeme_evenementiel_cpu.py &")
        
    else:
        print(f"\n❌ ARRÊT INCOMPLET")
        print("Certains processus résistent. Vérifiez manuellement.")