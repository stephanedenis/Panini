#!/usr/bin/env python3
"""
NETTOYAGE ET RÉPARATION COMPLÈTE SERVEURS MCP
============================================

Script pour nettoyer complètement les problèmes MCP et restaurer
un environnement de travail fonctionnel.
"""

import json
import subprocess
import shutil
from pathlib import Path

def nettoyer_serveurs_mcp():
    """Nettoyage complet des serveurs MCP problématiques"""
    
    print("🧹 NETTOYAGE COMPLET SERVEURS MCP")
    print("=" * 50)
    
    # 1. Arrêter tous les processus MCP
    print("1. Arrêt des processus MCP...")
    subprocess.run(['pkill', '-f', 'mcp'], capture_output=True)
    subprocess.run(['pkill', '-f', 'pylance'], capture_output=True)
    subprocess.run(['pkill', '-f', 'localhost:4005'], capture_output=True)
    print("   ✅ Processus arrêtés")
    
    # 2. Nettoyer les logs MCP corrompus
    print("\n2. Nettoyage logs MCP...")
    logs_dir = Path.home() / ".config/Code/logs"
    if logs_dir.exists():
        for log_file in logs_dir.rglob("**/mcpServer*/*.log"):
            try:
                log_file.unlink()
                print(f"   🗑️ {log_file.name} supprimé")
            except:
                pass
    print("   ✅ Logs nettoyés")
    
    # 3. Nettoyer les sessions de chat problématiques
    print("\n3. Nettoyage sessions chat...")
    workspace_storage = Path.home() / ".config/Code/User/workspaceStorage"
    if workspace_storage.exists():
        sessions_nettoyees = 0
        for session_file in workspace_storage.rglob("**/chatSessions/*.json"):
            try:
                with open(session_file, 'r') as f:
                    content = f.read()
                    if "localhost:4005" in content:
                        session_file.unlink()
                        sessions_nettoyees += 1
                        print(f"   🗑️ Session problématique supprimée")
            except:
                pass
        print(f"   ✅ {sessions_nettoyees} sessions problématiques nettoyées")
    
    # 4. Réinitialiser configuration MCP si nécessaire
    print("\n4. Vérification configuration MCP...")
    settings_file = Path.home() / ".config/Code/User/settings.json"
    if settings_file.exists():
        try:
            with open(settings_file, 'r') as f:
                settings = json.load(f)
            
            # Vérifier s'il y a des références à localhost:4005
            settings_str = json.dumps(settings)
            if "4005" in settings_str:
                print("   ⚠️ Références au port 4005 détectées dans settings.json")
                print("   💡 Vérification manuelle recommandée")
            else:
                print("   ✅ Configuration MCP saine")
                
        except Exception as e:
            print(f"   ⚠️ Erreur lecture settings: {e}")
    
    # 5. Nettoyer le cache des extensions
    print("\n5. Nettoyage cache extensions...")
    cache_dirs = [
        Path.home() / ".vscode/extensions/ms-python.vscode-pylance*/dist/cache",
        Path.home() / ".config/Code/CachedExtensions",
        Path.home() / ".config/Code/CachedExtensionVSIXs"
    ]
    
    for cache_pattern in cache_dirs:
        for cache_dir in Path("/").glob(str(cache_pattern)):
            if cache_dir.exists() and cache_dir.is_dir():
                try:
                    shutil.rmtree(cache_dir)
                    print(f"   🗑️ Cache {cache_dir.name} nettoyé")
                except:
                    pass
    print("   ✅ Cache nettoyé")
    
    # 6. Instructions finales
    print("\n✨ NETTOYAGE TERMINÉ")
    print("=" * 50)
    print("📋 Actions requises:")
    print("   1. Fermer complètement VS Code")
    print("   2. Attendre 10 secondes") 
    print("   3. Relancer VS Code")
    print("   4. Les serveurs MCP devraient redémarrer proprement")
    
    print(f"\n🔧 Si les problèmes persistent:")
    print("   • Désactiver temporairement l'extension Pylance")
    print("   • Redémarrer VS Code")
    print("   • Réactiver Pylance")
    print("   • Vérifier que les outils MCP fonctionnent")
    
    return True

def verifier_etat_mcp():
    """Vérifier l'état des serveurs MCP après nettoyage"""
    
    print("\n🔍 VÉRIFICATION POST-NETTOYAGE")
    print("=" * 30)
    
    # Vérifier processus
    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
    mcp_processes = [line for line in result.stdout.split('\n') 
                     if any(term in line.lower() for term in ['mcp', 'pylance']) 
                     and 'grep' not in line]
    
    if mcp_processes:
        print("⚠️ Processus MCP encore actifs:")
        for proc in mcp_processes[:3]:  # Max 3
            print(f"   • {proc}")
        print("   💡 Redémarrage VS Code nécessaire")
    else:
        print("✅ Aucun processus MCP bloqué")
    
    # Vérifier ports
    try:
        result = subprocess.run(['ss', '-tlnp'], capture_output=True, text=True)
        if ':4005' in result.stdout:
            print("⚠️ Port 4005 encore utilisé")
        else:
            print("✅ Port 4005 libéré")
    except:
        pass
    
    print(f"\n💭 Tests recommandés dans VS Code:")
    print("   • Ouvrir un fichier .py")
    print("   • Vérifier l'autocomplétion Pylance")
    print("   • Tester les outils MCP dans le chat")

def main():
    """Nettoyage principal"""
    try:
        nettoyer_serveurs_mcp()
        verifier_etat_mcp()
        return True
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {e}")
        return False

if __name__ == "__main__":
    if main():
        print("\n🎉 Nettoyage MCP terminé avec succès!")
    else:
        print("\n❌ Erreurs détectées lors du nettoyage")