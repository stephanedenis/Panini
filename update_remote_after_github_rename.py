#!/usr/bin/env python3
# Script généré automatiquement pour mise à jour remote local
# À exécuter APRÈS renommage GitHub manual

import subprocess
from pathlib import Path

def update_remote():
    repo_path = Path("/home/stephane/GitHub/Panini")
    new_remote = "ssh://git@github.com/stephanedenis/Panini.git"
    
    try:
        # Mettre à jour remote origin
        subprocess.run([
            "git", "remote", "set-url", "origin", new_remote
        ], cwd=repo_path, check=True)
        
        print(f"✅ Remote mis à jour: {new_remote}")
        
        # Vérifier nouvelle configuration
        result = subprocess.run([
            "git", "remote", "get-url", "origin"
        ], cwd=repo_path, capture_output=True, text=True, check=True)
        
        print(f"✅ Vérification remote: {result.stdout.strip()}")
        
        # Test connexion
        subprocess.run([
            "git", "fetch", "origin"
        ], cwd=repo_path, check=True)
        
        print("✅ Test connexion réussi")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur mise à jour remote: {e}")
        return False

if __name__ == "__main__":
    success = update_remote()
    exit(0 if success else 1)
