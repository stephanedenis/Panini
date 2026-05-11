#!/usr/bin/env python3
"""
Script de test des imports pour Colab
Simule exactement l'environnement Colab
"""

import sys
import os
import subprocess

def test_colab_imports():
    """Test des imports dans un environnement similaire à Colab"""
    
    print("🔍 DIAGNOSTIC COLAB - Test des imports")
    print("=" * 50)
    
    # 1. Vérification environnement
    print(f"📍 Python version: {sys.version}")
    print(f"📍 Répertoire courant: {os.getcwd()}")
    print(f"📍 Python path initial: {len(sys.path)} entrées")
    
    # 2. Simulation clone GitHub (comme Colab)
    repo_url = "https://github.com/stephanedenis/PaniniFS-Research.git"
    repo_dir = "PaniniFS-Research"
    
    # Nettoyer et cloner (simulation Colab)
    if os.path.exists(repo_dir):
        subprocess.run(["rm", "-rf", repo_dir])
    
    print(f"\n📥 Clonage repo: {repo_url}")
    result = subprocess.run(["git", "clone", repo_url], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Erreur clone: {result.stderr}")
        return
        
    print("✅ Clone réussi")
    
    # 3. Navigation dans le repo (comme Colab)
    os.chdir(repo_dir)
    print(f"📂 Changement répertoire: {os.getcwd()}")
    
    # 4. Vérification structure
    print(f"\n📁 Structure repo:")
    if os.path.exists("src"):
        print(f"  - src/: {os.listdir('src')}")
        if os.path.exists("src/github_sync"):
            print(f"  - src/github_sync/: {os.listdir('src/github_sync')}")
    else:
        print("  ❌ Dossier src/ manquant!")
        return
    
    # 5. Ajout chemin Python (simulation notebook)
    src_path = os.path.join(os.getcwd(), "src")
    sys.path.insert(0, src_path)
    print(f"\n🔧 Chemin ajouté: {src_path}")
    print(f"🔧 Python path mis à jour: {sys.path[:3]}...")
    
    # 6. Test imports individuels
    print(f"\n🧪 TEST IMPORTS:")
    modules_to_test = [
        "github_sync.config_manager",
        "github_sync.github_loader", 
        "github_sync.hot_reload",
        "github_sync.module_updater"
    ]
    
    success_count = 0
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"  ✅ {module_name}")
            success_count += 1
        except Exception as e:
            print(f"  ❌ {module_name}: {e}")
            print(f"     Type: {type(e).__name__}")
    
    # 7. Résultat final
    print(f"\n📊 RÉSULTAT: {success_count}/{len(modules_to_test)} modules importés")
    
    if success_count == len(modules_to_test):
        print("🎉 TOUS LES IMPORTS FONCTIONNENT!")
        
        # Test classes principales
        print(f"\n🏗️ Test classes principales:")
        try:
            from github_sync.config_manager import GitHubSyncConfig
            from github_sync.github_loader import GitHubModuleLoader
            print("  ✅ Classes principales OK")
        except Exception as e:
            print(f"  ❌ Erreur classes: {e}")
    else:
        print("🚨 ERREURS D'IMPORT DÉTECTÉES")
    
    # Retour au répertoire parent
    os.chdir("..")

if __name__ == "__main__":
    test_colab_imports()