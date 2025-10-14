#!/usr/bin/env python3
"""
Vérificateur d'état du dashboard PanLang
Vérifie si le dashboard est actif et le relance si nécessaire
"""

import subprocess
import time
import os
import sys

def check_dashboard_process():
    """Vérifie si le processus dashboard est actif"""
    try:
        result = subprocess.run(['pgrep', '-f', 'dashboard_simplifie_panlang.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            return [pid for pid in pids if pid]
        return []
    except Exception as e:
        print(f"Erreur vérification processus: {e}")
        return []

def check_dashboard_port():
    """Vérifie si le port 8080 répond"""
    try:
        import urllib.request
        response = urllib.request.urlopen('http://localhost:8080', timeout=3)
        return response.getcode() == 200
    except:
        return False

def restart_dashboard():
    """Relance le dashboard en arrière-plan"""
    try:
        # Vérifier que le fichier dashboard existe
        if not os.path.exists('dashboard_simplifie_panlang.py'):
            print("❌ Fichier dashboard_simplifie_panlang.py introuvable")
            return False
        
        # Lancer en arrière-plan
        process = subprocess.Popen(
            ['python3', 'dashboard_simplifie_panlang.py'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        print(f"✅ Dashboard relancé - PID: {process.pid}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur relancement dashboard: {e}")
        return False

def main():
    """Fonction principale de vérification"""
    print("🔍 VÉRIFICATION ÉTAT DASHBOARD")
    print("=" * 35)
    
    # Vérification processus
    pids = check_dashboard_process()
    if pids:
        print(f"✅ Dashboard actif - PID(s): {', '.join(pids)}")
        
        # Vérification port
        if check_dashboard_port():
            print("✅ Dashboard accessible sur http://localhost:8080")
            return True
        else:
            print("⚠️ Dashboard actif mais port 8080 non accessible")
    else:
        print("❌ Aucun processus dashboard trouvé")
    
    # Tentative de relancement
    print("\n🚀 Tentative de relancement...")
    if restart_dashboard():
        # Attendre un peu puis revérifier
        time.sleep(2)
        
        if check_dashboard_port():
            print("✅ Dashboard relancé avec succès !")
            print("🌐 Accessible sur http://localhost:8080")
            return True
        else:
            print("⚠️ Dashboard relancé mais port non accessible")
            return False
    else:
        print("❌ Échec relancement dashboard")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)