#!/usr/bin/env python3
"""
Lanceur Collection Corpus Multilingue et Développemental
"""

import subprocess
import sys
from datetime import datetime

def launch_multilingual_collection():
    """Lance la collection corpus multilingue et développemental"""
    
    print("🌍 LANCEMENT COLLECTION MULTILINGUE & DÉVELOPPEMENTALE")
    print("=" * 60)
    print("🎯 Cibles: Littérature, corpus enfant, préscolaire")
    print("🌐 Langues: 10+ langues développementales")
    print("👶 Âges: Infantile → Adolescence")
    print("📚 Sources: ArXiv, CHILDES, HAL, Littérature")
    print()
    
    # Commande collection
    cmd = [
        sys.executable,
        "collecteur_multilingue_dev.py"
    ]
    
    print(f"🚀 Exécution: {' '.join(cmd)}")
    print(f"⏰ Démarrage: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    try:
        # Lance en arrière-plan avec logs
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        print(f"🔄 Collection en cours (PID: {process.pid})")
        print("📊 Suivi en temps réel:")
        print("-" * 40)
        
        # Affiche output en temps réel
        for line in iter(process.stdout.readline, ''):
            if line.strip():
                print(line.strip())
        
        process.stdout.close()
        return_code = process.wait()
        
        print("-" * 40)
        if return_code == 0:
            print("✅ Collection terminée avec succès")
        else:
            print(f"❌ Erreur collection (code: {return_code})")
            
        print(f"⏰ Fin: {datetime.now().strftime('%H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Erreur lancement: {e}")
        return False
        
    return True

if __name__ == "__main__":
    success = launch_multilingual_collection()
    sys.exit(0 if success else 1)