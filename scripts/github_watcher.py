#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Détecteur Intelligent GitHub-Colab
Surveillance automatique des commits de résultats
"""

import json
import time
import requests
import subprocess
from pathlib import Path
from datetime import datetime, timedelta


class GitHubColabWatcher:
    """Surveillance intelligente GitHub pour résultats Colab"""
    
    def __init__(self):
        self.repo_owner = "stephanedenis"
        self.repo_name = "PaniniFS-Research"
        self.watch_paths = [
            "colab_integration/results/",
            "dhatu_analysis_session_",
            "session_summary_"
        ]
        self.last_check_file = Path(".github_last_check")
        self.api_base = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"
        
    def log(self, message: str, level: str = "INFO"):
        """Log avec timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def get_last_check_time(self) -> str:
        """Récupère timestamp dernière vérification"""
        if self.last_check_file.exists():
            return self.last_check_file.read_text().strip()
        else:
            # Par défaut : 1 heure avant
            default_time = datetime.now() - timedelta(hours=1)
            return default_time.isoformat()
    
    def save_check_time(self):
        """Sauvegarde timestamp vérification"""
        current_time = datetime.now().isoformat()
        self.last_check_file.write_text(current_time)
    
    def check_github_commits(self) -> list:
        """Vérifie nouveaux commits sur GitHub"""
        self.log("🔍 Vérification commits GitHub...")
        
        try:
            last_check = self.get_last_check_time()
            
            # API GitHub : commits récents
            url = f"{self.api_base}/commits"
            params = {
                "since": last_check,
                "per_page": 20
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            commits = response.json()
            self.log(f"📊 {len(commits)} commits depuis {last_check[:19]}")
            
            # Filtrer commits avec résultats Colab
            colab_commits = []
            for commit in commits:
                message = commit['commit']['message'].lower()
                
                if any(keyword in message for keyword in [
                    'colab', 'dhatu', 'gpu', 'résultats', 'analysis'
                ]):
                    colab_commits.append(commit)
                    self.log(f"✓ Commit Colab: {commit['sha'][:8]} - "
                            f"{commit['commit']['message'][:50]}...")
            
            return colab_commits
            
        except Exception as e:
            self.log(f"❌ Erreur GitHub API: {e}", "ERROR")
            return []
    
    def check_commit_files(self, commit_sha: str) -> list:
        """Vérifie fichiers modifiés dans un commit"""
        try:
            url = f"{self.api_base}/commits/{commit_sha}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            commit_data = response.json()
            files = commit_data.get('files', [])
            
            # Filtrer fichiers résultats Colab
            colab_files = []
            for file_info in files:
                filename = file_info['filename']
                
                if any(path in filename for path in self.watch_paths):
                    colab_files.append({
                        'filename': filename,
                        'status': file_info['status'],  # added, modified, removed
                        'additions': file_info.get('additions', 0),
                        'deletions': file_info.get('deletions', 0)
                    })
            
            return colab_files
            
        except Exception as e:
            self.log(f"❌ Erreur vérification commit {commit_sha}: {e}", "ERROR")
            return []
    
    def auto_pull_latest(self) -> bool:
        """Pull automatique des derniers changements"""
        try:
            self.log("🔄 Pull automatique...")
            
            # Git fetch
            subprocess.run(["git", "fetch"], check=True, timeout=15)
            
            # Vérifier s'il y a des changements
            result = subprocess.run([
                "git", "log", "HEAD..origin/main", "--oneline"
            ], capture_output=True, text=True)
            
            if not result.stdout.strip():
                self.log("ℹ️  Aucune mise à jour disponible")
                return True
            
            # Pull
            subprocess.run(["git", "pull", "origin", "main"], check=True, timeout=15)
            self.log("✅ Pull réussi")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Erreur pull: {e}", "ERROR")
            return False
    
    def detect_new_local_results(self) -> list:
        """Détecte nouveaux résultats locaux après pull"""
        results_dir = Path("colab_integration/results")
        
        if not results_dir.exists():
            return []
        
        # Chercher sessions récentes (dernières 6h)
        cutoff_time = time.time() - (6 * 3600)
        recent_sessions = []
        
        for session_dir in results_dir.iterdir():
            if not session_dir.is_dir():
                continue
            
            # Vérifier timestamp dossier
            dir_time = session_dir.stat().st_mtime
            if dir_time > cutoff_time:
                recent_sessions.append(session_dir)
        
        return recent_sessions
    
    def smart_github_monitoring(self):
        """Surveillance intelligente GitHub"""
        self.log("🎯 SURVEILLANCE INTELLIGENTE GITHUB")
        self.log("=" * 40)
        
        try:
            # 1. Vérifier commits récents
            new_commits = self.check_github_commits()
            
            has_colab_updates = False
            
            if new_commits:
                self.log(f"📊 {len(new_commits)} commits Colab détectés")
                
                # Vérifier contenu commits
                for commit in new_commits:
                    files = self.check_commit_files(commit['sha'])
                    if files:
                        self.log(f"   📄 {len(files)} fichiers résultats "
                                f"dans {commit['sha'][:8]}")
                        has_colab_updates = True
            
            # 2. Pull si nécessaire
            if has_colab_updates or new_commits:
                if self.auto_pull_latest():
                    # 3. Détecter nouveaux résultats
                    new_results = self.detect_new_local_results()
                    
                    if new_results:
                        self.log(f"✅ {len(new_results)} nouvelles sessions trouvées")
                        
                        # 4. Synchroniser avec système local
                        self.trigger_local_sync()
                    else:
                        self.log("ℹ️  Aucun nouveau résultat détecté")
            else:
                self.log("ℹ️  Aucune mise à jour Colab")
            
            # 5. Sauvegarder timestamp
            self.save_check_time()
            
        except Exception as e:
            self.log(f"❌ Erreur surveillance: {e}", "ERROR")
    
    def trigger_local_sync(self):
        """Déclenche synchronisation système local"""
        try:
            import subprocess
            import sys
            
            result = subprocess.run([
                sys.executable, "scripts/panini_manager.py", "sync"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.log("✅ Sync locale déclenchée")
            else:
                self.log(f"❌ Erreur sync: {result.stderr}", "ERROR")
                
        except Exception as e:
            self.log(f"❌ Erreur déclenchement sync: {e}", "ERROR")


def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Surveillance GitHub-Colab")
    parser.add_argument("--check", action="store_true", help="Vérification unique")
    parser.add_argument("--monitor", action="store_true", help="Surveillance continue")
    parser.add_argument("--reset", action="store_true", help="Reset timestamp")
    
    args = parser.parse_args()
    
    watcher = GitHubColabWatcher()
    
    if args.reset:
        if watcher.last_check_file.exists():
            watcher.last_check_file.unlink()
        print("✅ Timestamp reset")
        return
    
    if args.monitor:
        # Surveillance continue
        import schedule
        
        print("🎯 SURVEILLANCE CONTINUE GITHUB-COLAB")
        print("   Vérification toutes les 10 minutes")
        print("   Ctrl+C pour arrêter")
        
        # Programmer vérifications
        schedule.every(10).minutes.do(watcher.smart_github_monitoring)
        
        # Vérification initiale
        watcher.smart_github_monitoring()
        
        # Boucle
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Vérifier chaque minute
        except KeyboardInterrupt:
            print("\n🛑 Surveillance arrêtée")
    
    elif args.check:
        watcher.smart_github_monitoring()
    
    else:
        print("Usage:")
        print("  python3 scripts/github_watcher.py --check    # Une vérification")
        print("  python3 scripts/github_watcher.py --monitor  # Surveillance")
        print("  python3 scripts/github_watcher.py --reset    # Reset timestamp")


if __name__ == "__main__":
    main()