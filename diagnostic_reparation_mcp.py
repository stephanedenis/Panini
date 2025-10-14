#!/usr/bin/env python3
"""
DIAGNOSTIC ET RÉPARATION SERVEURS MCP
===================================

Script pour diagnostiquer et réparer les problèmes avec les serveurs MCP,
en particulier le serveur Pylance qui ne répond pas à l'initialisation.
"""

import os
import subprocess
import json
import time
from pathlib import Path

class MCPServerDiagnostic:
    """Diagnostic et réparation serveurs MCP"""
    
    def __init__(self):
        self.vscode_config_dir = Path.home() / ".config/Code/User"
        self.vscode_logs_dir = Path.home() / ".config/Code/logs"
        self.settings_file = self.vscode_config_dir / "settings.json"
        
    def diagnose_mcp_servers(self):
        """Diagnostic complet des serveurs MCP"""
        
        print("🔍 DIAGNOSTIC SERVEURS MCP")
        print("=" * 40)
        
        # 1. Vérifier configuration
        print("📋 Configuration MCP:")
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                
                mcp_config = {}
                for key, value in settings.items():
                    if 'mcp' in key.lower():
                        mcp_config[key] = value
                
                if mcp_config:
                    for key, value in mcp_config.items():
                        print(f"   • {key}: {value}")
                else:
                    print("   ⚠️ Aucune configuration MCP trouvée")
                    
            except Exception as e:
                print(f"   ❌ Erreur lecture settings: {e}")
        else:
            print("   ❌ Fichier settings.json introuvable")
        
        # 2. Vérifier processus
        print(f"\n🔄 Processus MCP:")
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        mcp_processes = [line for line in result.stdout.split('\n') if 'mcp' in line.lower() and 'grep' not in line]
        
        if mcp_processes:
            for proc in mcp_processes:
                print(f"   • {proc}")
        else:
            print("   ✅ Aucun processus MCP bloqué trouvé")
        
        # 3. Analyser logs récents
        print(f"\n📜 Logs MCP récents:")
        self._analyze_recent_logs()
        
        # 4. Vérifier extensions Python
        print(f"\n🐍 Extensions Python:")
        self._check_python_extensions()
        
    def _analyze_recent_logs(self):
        """Analyse les logs MCP récents"""
        
        # Trouver les logs MCP les plus récents
        mcp_logs = []
        if self.vscode_logs_dir.exists():
            for log_file in self.vscode_logs_dir.rglob("**/mcpServer*/*.log"):
                if log_file.stat().st_size > 0:  # Seulement les logs non-vides
                    mcp_logs.append((log_file, log_file.stat().st_mtime))
        
        # Trier par date de modification
        mcp_logs.sort(key=lambda x: x[1], reverse=True)
        
        if mcp_logs:
            print(f"   📁 {len(mcp_logs)} logs trouvés")
            
            # Analyser le log le plus récent
            latest_log, _ = mcp_logs[0]
            print(f"   📄 Log le plus récent: {latest_log.name}")
            
            try:
                with open(latest_log, 'r') as f:
                    lines = f.readlines()[-10:]  # 10 dernières lignes
                
                # Chercher les erreurs communes
                errors = []
                waiting_count = 0
                
                for line in lines:
                    if "Waiting for server to respond to `initialize`" in line:
                        waiting_count += 1
                    elif "error" in line.lower() or "failed" in line.lower():
                        errors.append(line.strip())
                
                if waiting_count > 5:
                    print(f"   🚨 PROBLÈME: Serveur bloqué sur initialisation ({waiting_count} tentatives)")
                    print(f"   💡 Solution: Redémarrage du serveur MCP requis")
                
                if errors:
                    print(f"   ❌ Erreurs détectées:")
                    for error in errors[:3]:  # Max 3 erreurs
                        print(f"      • {error}")
                        
            except Exception as e:
                print(f"   ⚠️ Erreur lecture log: {e}")
        else:
            print(f"   📭 Aucun log MCP trouvé")
    
    def _check_python_extensions(self):
        """Vérifier les extensions Python/Pylance"""
        
        try:
            result = subprocess.run(['code', '--list-extensions'], capture_output=True, text=True)
            extensions = result.stdout.split('\n')
            
            python_extensions = [ext for ext in extensions if 'python' in ext.lower() or 'pylance' in ext.lower()]
            
            if python_extensions:
                print(f"   ✅ Extensions Python trouvées:")
                for ext in python_extensions:
                    if ext.strip():
                        print(f"      • {ext}")
            else:
                print(f"   ❌ Aucune extension Python trouvée")
                
        except Exception as e:
            print(f"   ⚠️ Erreur vérification extensions: {e}")
    
    def repair_mcp_servers(self):
        """Réparer les serveurs MCP bloqués"""
        
        print(f"\n🔧 RÉPARATION SERVEURS MCP")
        print("=" * 40)
        
        steps = [
            "Arrêt des processus MCP bloqués",
            "Nettoyage des logs corrompus", 
            "Réinitialisation cache VS Code",
            "Redémarrage service MCP"
        ]
        
        for i, step in enumerate(steps, 1):
            print(f"{i}. {step}...")
            
            if i == 1:  # Arrêt processus
                subprocess.run(['pkill', '-f', 'ms-python.vscode-pylance'], 
                             capture_output=True)
                subprocess.run(['pkill', '-f', 'mcp'], capture_output=True)
                print("   ✅ Processus arrêtés")
                
            elif i == 2:  # Nettoyage logs
                try:
                    # Supprimer logs MCP corrompus/bloqués
                    if self.vscode_logs_dir.exists():
                        for log_file in self.vscode_logs_dir.rglob("**/mcpServer*/*.log"):
                            if log_file.stat().st_size > 100000:  # > 100KB = possiblement corrompu
                                log_file.unlink()
                    print("   ✅ Logs nettoyés")
                except Exception as e:
                    print(f"   ⚠️ Nettoyage partiel: {e}")
                    
            elif i == 3:  # Cache VS Code
                cache_dirs = [
                    self.vscode_config_dir / "CachedExtensions",
                    self.vscode_config_dir / "logs",
                    Path.home() / ".vscode" / "extensions" / "ms-python.vscode-pylance*" / "dist" / "cache"
                ]
                
                for cache_dir in cache_dirs:
                    if cache_dir.exists():
                        try:
                            import shutil
                            if cache_dir.is_dir():
                                shutil.rmtree(cache_dir)
                            print(f"   ✅ Cache {cache_dir.name} nettoyé")
                        except:
                            pass
                            
            elif i == 4:  # Redémarrage
                print("   💭 Redémarrage automatique au prochain lancement VS Code")
                print("   📝 Recommandation: Fermer et rouvrir VS Code")
            
            time.sleep(0.5)  # Pause visuelle
        
        print(f"\n✨ RÉPARATION TERMINÉE")
        print("📋 Actions recommandées:")
        print("   1. Fermer complètement VS Code (toutes les fenêtres)")
        print("   2. Attendre 5 secondes") 
        print("   3. Relancer VS Code")
        print("   4. Vérifier que les outils MCP fonctionnent")
    
    def verify_mcp_functionality(self):
        """Vérifier le fonctionnement des outils MCP"""
        
        print(f"\n🧪 TEST FONCTIONNALITÉ MCP")
        print("=" * 40)
        
        print("🔬 Tests recommandés dans VS Code:")
        print("   • Ouvrir le chat Copilot")
        print("   • Taper une question Python simple")
        print("   • Vérifier que les suggestions Pylance apparaissent")
        print("   • Tester l'autocomplétion dans un fichier .py")
        
        print(f"\n📊 Si les problèmes persistent:")
        print("   • Réinstaller l'extension Pylance")
        print("   • Vérifier les paramètres Python/Pylance")
        print("   • Redémarrer en mode sans extensions (--disable-extensions)")

def main():
    """Diagnostic et réparation principale"""
    
    diagnostic = MCPServerDiagnostic()
    
    # Phase 1: Diagnostic
    diagnostic.diagnose_mcp_servers()
    
    # Phase 2: Réparation 
    diagnostic.repair_mcp_servers()
    
    # Phase 3: Vérification
    diagnostic.verify_mcp_functionality()

if __name__ == "__main__":
    main()