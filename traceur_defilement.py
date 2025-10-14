#!/usr/bin/env python3
"""
Traceur de défilement terminal - Identifie la source exacte du défilement
"""

import subprocess
import time
import os
from datetime import datetime

def identifier_terminal_actif():
    """Identifie quel terminal génère du défilement"""
    print("🖥️ IDENTIFICATION TERMINAL AVEC DÉFILEMENT")
    print("=" * 50)
    
    print("\n📋 INSTRUCTIONS:")
    print("1. Gardez ouvert le terminal où vous voyez le défilement")
    print("2. Ce script va analyser tous les terminaux actifs")
    print("3. Nous allons identifier la source exacte")
    
    input("\n👆 Appuyez sur Entrée quand vous êtes prêt...")
    
    # 1. Lister tous les terminaux/TTY actifs
    print("\n🔍 Analyse des terminaux actifs...")
    
    try:
        # Obtenir tous les processus de terminaux
        cmd = ["ps", "aux"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        terminaux = []
        processus_bash = []
        
        for line in result.stdout.split('\n'):
            if 'bash' in line or 'zsh' in line or 'sh' in line:
                if 'pts' in line or 'tty' in line:
                    terminaux.append(line.strip())
            
            if 'python' in line.lower() and any(word in line.lower() for word in 
                    ['dashboard', 'optimis', 'analys', 'iter']):
                processus_bash.append(line.strip())
        
        print(f"\n🖥️ {len(terminaux)} terminaux détectés:")
        for i, terminal in enumerate(terminaux[:10], 1):
            parts = terminal.split()
            if len(parts) >= 2:
                print(f"  {i}. TTY/PTS: {parts[6] if len(parts) > 6 else 'N/A'} - PID: {parts[1]}")
        
        if processus_bash:
            print(f"\n🐍 {len(processus_bash)} processus Python suspects:")
            for proc in processus_bash[:5]:
                parts = proc.split()
                print(f"  • PID {parts[1]}: {' '.join(parts[10:])[:60]}...")
    
    except Exception as e:
        print(f"❌ Erreur analyse terminaux: {e}")
    
    # 2. Vérifier les logs système récents  
    print(f"\n📋 Vérification logs système récents...")
    
    try:
        # Chercher dans les logs système
        logs_systeme = [
            "/var/log/syslog",
            "/var/log/messages", 
            "/var/log/daemon.log"
        ]
        
        for log_file in logs_systeme:
            if os.path.exists(log_file):
                try:
                    # Regarder les 10 dernières lignes
                    cmd = ["tail", "-10", log_file]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                    
                    if result.stdout.strip():
                        print(f"  📄 {log_file}:")
                        lignes = result.stdout.strip().split('\n')[-3:]  # 3 dernières lignes
                        for ligne in lignes:
                            if ligne.strip():
                                print(f"    {ligne[:80]}...")
                except:
                    continue
    except:
        print("  ⚠️ Impossible d'accéder aux logs système")
    
    # 3. Processus en cours d'écriture
    print(f"\n📝 Recherche processus écrivant activement...")
    
    try:
        # Utiliser lsof pour trouver les fichiers ouverts en écriture
        cmd = ["lsof", "+D", ".", "-a", "-d", "1,2"]  # stdout/stderr dans le répertoire courant
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.stdout.strip():
            print("  🔍 Processus écrivant dans le répertoire:")
            lignes = result.stdout.strip().split('\n')[1:]  # Skip header
            for ligne in lignes[:5]:  # Limiter à 5
                if 'python' in ligne.lower():
                    print(f"    📌 {ligne}")
    
    except subprocess.TimeoutExpired:
        print("  ⏰ Timeout lsof")
    except FileNotFoundError:
        print("  ⚠️ lsof non disponible")
    except Exception as e:
        print(f"  ❌ Erreur lsof: {e}")
    
    # 4. Recommandations
    print(f"\n" + "=" * 50)
    print("🎯 RECOMMANDATIONS POUR IDENTIFIER LA SOURCE:")
    print("\n1. 📱 Vérifiez dans quel terminal vous voyez le défilement")
    print("2. 🔍 Dans ce terminal, tapez: ps -p $$")  
    print("3. 📋 Ou tapez: echo $0 (pour voir le shell)")
    print("4. 🖥️ Ou tapez: tty (pour voir le terminal)")
    
    print("\n5. 🛑 Si le défilement persiste, essayez:")
    print("   • Ctrl+C dans le terminal qui défile")
    print("   • Fermer et rouvrir ce terminal")
    print("   • pkill -f [nom_du_processus_qui_défile]")
    
    print("\n6. 🔍 Pour trouver le processus exact:")
    print("   • ps aux | grep [partie_du_log_qui_défile]")
    print("   • pgrep -f iteration")
    print("   • pgrep -f ULTIME")

def main():
    identifier_terminal_actif()
    
    print(f"\n⚡ ACTION IMMÉDIATE SUGGÉRÉE:")
    print("Si vous voyez encore le défilement avec les logs 'ITÉRATION', essayez:")
    print("1. pkill -f ULTIME")  
    print("2. pkill -f iteration")
    print("3. pkill -f optimiseur")
    print("4. Dans le terminal qui défile: Ctrl+C")

if __name__ == "__main__":
    main()