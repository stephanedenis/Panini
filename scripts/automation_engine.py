#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatisation Complète PaniniFS Research
Élimine TOUTES les opérations manuelles
"""

import os
import sys
import json
import time
import shutil
import requests
import subprocess
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from datetime import datetime
import schedule


class AutomationEngine:
    """Moteur d'automatisation complète"""
    
    def __init__(self, repo_path: str = "/home/stephane/GitHub/PaniniFS-Research"):
        self.repo_path = Path(repo_path)
        self.results_dir = self.repo_path / "colab_results"
        self.processed_file = self.repo_path / "automation_processed.json"
        
        # Créer dossier résultats si nécessaire
        self.results_dir.mkdir(exist_ok=True)
        
        # Plus de dépendance Downloads - tout via GitHub
        self.log("🚀 Automation Engine - Mode GitHub-Only")
        self.log(f"📂 Surveillance: {self.results_dir}")
        
    def log(self, message: str, level: str = "INFO"):
        """Log avec timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def detect_new_colab_results(self) -> List[Dict]:
        """Détecte nouveaux résultats via surveillance GitHub"""
        new_results = []
        
        # Patterns de fichiers Colab dans le repo
        patterns = [
            "colab_results/**/*.json",
            "results/**/*session*.json",
            "**/*analysis_results_*.json"
        ]
        
        # Scanner les fichiers récents (dernières 24h)
        cutoff_time = time.time() - (24 * 3600)
        
        for pattern in patterns:
            matches = list(self.repo_path.glob(pattern))
            for match in matches:
                if match.is_file() and match.stat().st_mtime > cutoff_time:
                    try:
                        # Détecter type de fichier et session ID
                        filename = match.name
                        if "analysis_results_" in filename:
                            session_id = filename.replace("analysis_results_", "").replace(".json", "")
                        elif "session_" in filename:
                            session_id = filename.replace("session_", "").replace(".json", "")
                        else:
                            session_id = "unknown"
                        
                        new_results.append({
                            "file": match,
                            "session_id": session_id,
                            "type": "colab_result",
                            "detected_at": datetime.now().isoformat()
                        })
                    except Exception as e:
                        self.log(f"Erreur parsing {match.name}: {e}", "ERROR")
        
        return new_results
    
    def auto_import_results(self, files: list) -> int:
        """Importe automatiquement les résultats"""
        if not files:
            return 0
        
        imported = 0
        
        for file_path in files:
            try:
                self.log(f"📥 Import: {file_path.name}")
                
                # Extraire session ID du nom de fichier
                filename = file_path.name
                if "dhatu_analysis_session_" in filename:
                    session_id = filename.replace("dhatu_analysis_session_", "").replace(".json", "")
                elif "session_summary_" in filename:
                    session_id = filename.replace("session_summary_", "").replace(".md", "")
                else:
                    session_id = f"auto_{int(time.time())}"
                
                # Créer dossier session
                session_dir = self.results_dir / session_id
                session_dir.mkdir(parents=True, exist_ok=True)
                
                # Copier fichier
                target_path = session_dir / file_path.name
                shutil.copy2(file_path, target_path)
                
                # Créer métadonnées
                if not (session_dir / "session_metadata.json").exists():
                    metadata = {
                        "session_id": session_id,
                        "imported_at": datetime.now().isoformat(),
                        "source_file": str(file_path),
                        "auto_imported": True
                    }
                    
                    with open(session_dir / "session_metadata.json", 'w') as f:
                        json.dump(metadata, f, indent=2)
                
                self.log(f"✅ Importé: {session_id}")
                imported += 1
                
                # Optionnel: supprimer fichier source pour éviter doublons
                try:
                    file_path.unlink()
                    self.log(f"🗑️  Nettoyé: {file_path.name}")
                except:
                    pass
                
            except Exception as e:
                self.log(f"❌ Erreur import {file_path}: {e}", "ERROR")
        
        return imported
    
    def auto_sync_with_api(self) -> bool:
        """Synchronise automatiquement avec l'API"""
        try:
            # Vérifier API active
            response = requests.get(f"{self.api_endpoint}/health", timeout=3)
            if response.status_code != 200:
                self.log("❌ API non disponible", "ERROR")
                return False
            
            # Lancer sync via script existant
            result = subprocess.run([
                sys.executable, "scripts/panini_manager.py", "sync"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.log("✅ Sync API réussie")
                return True
            else:
                self.log(f"❌ Erreur sync: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Erreur sync API: {e}", "ERROR")
            return False
    
    def auto_git_commit(self) -> bool:
        """Commit automatique des nouveaux résultats"""
        try:
            # Vérifier s'il y a des changements
            result = subprocess.run(
                ["git", "status", "--porcelain", "colab_integration/"], 
                capture_output=True, text=True
            )
            
            if not result.stdout.strip():
                self.log("ℹ️  Aucun changement Git")
                return True
            
            # Add changements
            subprocess.run(["git", "add", "colab_integration/"], check=True)
            
            # Commit avec message automatique
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            commit_msg = f"🤖 Auto-import résultats Colab {timestamp}"
            
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            self.log(f"✅ Commit auto: {commit_msg}")
            
            # Push si configuré
            try:
                subprocess.run(["git", "push"], check=True, timeout=10)
                self.log("✅ Push auto réussi")
            except:
                self.log("ℹ️  Push auto échoué (normal si pas configuré)")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Erreur Git: {e}", "ERROR")
            return False
    
    def full_automation_cycle(self):
        """Cycle complet d'automatisation"""
        self.log("🤖 DÉMARRAGE CYCLE AUTOMATISATION")
        self.log("=" * 40)
        
        try:
            # 1. Détecter nouveaux résultats
            new_files = self.detect_new_colab_results()
            
            if not new_files:
                self.log("ℹ️  Aucun nouveau résultat")
                return
            
            # 2. Importer automatiquement
            imported = self.auto_import_results(new_files)
            
            if imported > 0:
                self.log(f"📊 {imported} fichiers importés")
                
                # 3. Synchroniser avec API
                self.auto_sync_with_api()
                
                # 4. Commit Git automatique
                self.auto_git_commit()
                
                self.log("✅ CYCLE AUTOMATISATION TERMINÉ")
            
        except Exception as e:
            self.log(f"❌ Erreur cycle: {e}", "ERROR")
    
    def start_continuous_monitoring(self):
        """Surveillance continue automatique"""
        self.log("🎯 DÉMARRAGE SURVEILLANCE CONTINUE")
        self.log("   Vérification toutes les 5 minutes")
        self.log("   Ctrl+C pour arrêter")
        
        # Programmer vérifications
        schedule.every(5).minutes.do(self.full_automation_cycle)
        
        # Cycle initial
        self.full_automation_cycle()
        
        # Boucle surveillance
        try:
            while True:
                schedule.run_pending()
                time.sleep(30)  # Vérifier toutes les 30s
        except KeyboardInterrupt:
            self.log("🛑 Surveillance arrêtée")


def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automatisation complète PaniniFS")
    parser.add_argument("--once", action="store_true", help="Exécuter une seule fois")
    parser.add_argument("--monitor", action="store_true", help="Surveillance continue")
    parser.add_argument("--detect-only", action="store_true", help="Détecter seulement")
    
    args = parser.parse_args()
    
    engine = AutomationEngine()
    
    if args.detect_only:
        files = engine.detect_new_colab_results()
        print(f"📊 {len(files)} fichiers détectés")
        for f in files:
            print(f"   📄 {f}")
    
    elif args.once:
        engine.full_automation_cycle()
    
    elif args.monitor:
        engine.start_continuous_monitoring()
    
    else:
        print("Usage:")
        print("  python3 scripts/automation_engine.py --once      # Une fois")
        print("  python3 scripts/automation_engine.py --monitor   # Surveillance")
        print("  python3 scripts/automation_engine.py --detect-only # Détecter")


if __name__ == "__main__":
    main()