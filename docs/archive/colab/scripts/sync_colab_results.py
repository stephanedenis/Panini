#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Synchroniseur résultats Colab - PaniniFS Research
Remplace scripts/sync_colab_results.sh par version Python
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class ColabResultsSyncer:
    """Synchroniseur résultats Colab vers local"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.results_dir = self.repo_path / "colab_integration" / "results"
        self.integration_script = self.repo_path / "scripts" / "integrate_colab_results.py"
        
    def log(self, message: str, level: str = "INFO"):
        """Log avec timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def run_command(self, command: List[str], capture_output: bool = True) -> tuple:
        """Exécute une commande et retourne (success, output, error)"""
        try:
            result = subprocess.run(
                command, 
                capture_output=capture_output, 
                text=True, 
                cwd=self.repo_path
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def check_git_status(self) -> Dict[str, any]:
        """Vérifie l'état Git du repository"""
        self.log("Vérification état Git...")
        
        # Status général
        success, output, error = self.run_command(["git", "status", "--porcelain"])
        if not success:
            self.log(f"Erreur git status: {error}", "ERROR")
            return {"clean": False, "error": error}
        
        # Fetch dernières modifications
        success, _, error = self.run_command(["git", "fetch", "origin"])
        if not success:
            self.log(f"Warning git fetch: {error}", "WARNING")
        
        # Vérifier si on est à jour avec origin/main
        success, output, _ = self.run_command([
            "git", "rev-list", "--count", "HEAD..origin/main"
        ])
        
        commits_behind = 0
        if success and output.strip().isdigit():
            commits_behind = int(output.strip())
        
        return {
            "clean": True,
            "commits_behind": commits_behind,
            "needs_pull": commits_behind > 0
        }
    
    def pull_latest_changes(self) -> bool:
        """Pull les derniers changements depuis GitHub"""
        self.log("Pull des derniers changements...")
        
        success, output, error = self.run_command(["git", "pull", "origin", "main"])
        if not success:
            self.log(f"Erreur git pull: {error}", "ERROR")
            return False
        
        self.log("✅ Repository mis à jour")
        return True
    
    def scan_colab_results(self) -> List[Dict]:
        """Scan les résultats Colab récents"""
        self.log("Scan résultats Colab...")
        
        if not self.results_dir.exists():
            self.log(f"❌ Dossier résultats non trouvé: {self.results_dir}")
            return []
        
        sessions = []
        
        # Chercher les dossiers de session
        for session_dir in self.results_dir.iterdir():
            if not session_dir.is_dir():
                continue
                
            # Chercher metadata de session
            metadata_file = session_dir / "session_metadata.json"
            if not metadata_file.exists():
                continue
            
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                # Vérifier si c'est une session récente (dernières 24h)
                session_time = datetime.fromisoformat(metadata.get('timestamp', ''))
                now = datetime.now()
                hours_diff = (now - session_time).total_seconds() / 3600
                
                if hours_diff <= 24:  # Sessions des dernières 24h
                    sessions.append({
                        'session_id': metadata.get('session_id', session_dir.name),
                        'path': session_dir,
                        'metadata': metadata,
                        'hours_ago': hours_diff
                    })
                    
            except Exception as e:
                self.log(f"❌ Erreur lecture {session_dir}: {e}", "WARNING")
        
        # Trier par timestamp (plus récent en premier)
        sessions.sort(key=lambda x: x['metadata'].get('timestamp', ''), reverse=True)
        
        self.log(f"📊 {len(sessions)} sessions récentes trouvées")
        return sessions
    
    def display_sessions(self, sessions: List[Dict]):
        """Affiche les sessions trouvées"""
        if not sessions:
            self.log("ℹ️  Aucune session Colab récente trouvée")
            return
        
        self.log("📋 Sessions Colab récentes:")
        for i, session in enumerate(sessions[:5], 1):
            metadata = session['metadata']
            session_id = session['session_id']
            hours_ago = session['hours_ago']
            
            # Infos performance
            corpus_stats = metadata.get('corpus_stats', {})
            docs = corpus_stats.get('total_documents', 0)
            throughput = corpus_stats.get('throughput', 0)
            gpu_name = metadata.get('gpu_info', {}).get('device_name', 'Unknown')
            
            self.log(f"  {i}. {session_id}")
            self.log(f"     🕒 Il y a {hours_ago:.1f}h")
            self.log(f"     🔥 GPU: {gpu_name}")
            self.log(f"     📊 {docs} docs, {throughput:.1f} docs/sec")
    
    def integrate_with_api(self) -> bool:
        """Intègre les résultats avec l'API locale"""
        if not self.integration_script.exists():
            self.log(f"❌ Script intégration non trouvé: {self.integration_script}", "ERROR")
            return False
        
        self.log("🔗 Intégration avec API locale...")
        
        success, output, error = self.run_command([
            sys.executable, str(self.integration_script), "--sync"
        ], capture_output=True)
        
        if not success:
            self.log(f"❌ Erreur intégration API: {error}", "ERROR")
            return False
        
        # Afficher output de l'intégration
        if output.strip():
            for line in output.strip().split('\n'):
                self.log(f"   {line}")
        
        return True
    
    def check_api_health(self) -> bool:
        """Vérifie si l'API locale est active"""
        try:
            import requests
            response = requests.get("http://localhost:5000/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                self.log(f"✅ API locale active: {health_data.get('status', 'unknown')}")
                return True
            else:
                self.log(f"⚠️  API répond mais status {response.status_code}", "WARNING")
                return False
        except ImportError:
            self.log("⚠️  Module requests non disponible, skip vérification API", "WARNING")
            return False
        except Exception as e:
            self.log(f"❌ API locale non accessible: {e}", "WARNING")
            return False
    
    def sync_all(self) -> bool:
        """Synchronisation complète Colab → Local"""
        self.log("🔄 SYNCHRONISATION RÉSULTATS COLAB")
        self.log("=" * 40)
        
        start_time = time.time()
        
        # 1. Vérification Git
        git_status = self.check_git_status()
        if not git_status["clean"]:
            self.log("❌ Repository Git en état instable", "ERROR")
            return False
        
        # 2. Pull si nécessaire
        if git_status["needs_pull"]:
            if not self.pull_latest_changes():
                return False
        else:
            self.log("✅ Repository déjà à jour")
        
        # 3. Scan résultats Colab
        sessions = self.scan_colab_results()
        self.display_sessions(sessions)
        
        if not sessions:
            self.log("ℹ️  Aucun nouveau résultat à synchroniser")
            return True
        
        # 4. Vérification API locale
        api_available = self.check_api_health()
        
        # 5. Intégration API si disponible
        if api_available:
            if not self.integrate_with_api():
                self.log("⚠️  Intégration API échouée, mais résultats disponibles", "WARNING")
        else:
            self.log("ℹ️  API locale non disponible, skip intégration")
        
        # 6. Résumé final
        sync_time = time.time() - start_time
        self.log("\n✅ SYNCHRONISATION TERMINÉE")
        self.log(f"   📊 {len(sessions)} sessions trouvées")
        self.log(f"   ⏱️  Temps: {sync_time:.1f}s")
        self.log(f"   🔗 API: {'✅ Intégrée' if api_available else '❌ Non disponible'}")
        
        return True


def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Synchronisation résultats Colab")
    parser.add_argument("--repo", default=".", help="Chemin vers repository")
    parser.add_argument("--list-only", action="store_true", help="Lister sessions seulement")
    parser.add_argument("--no-api", action="store_true", help="Skip intégration API")
    
    args = parser.parse_args()
    
    syncer = ColabResultsSyncer(args.repo)
    
    if args.list_only:
        sessions = syncer.scan_colab_results()
        syncer.display_sessions(sessions)
        return
    
    success = syncer.sync_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()