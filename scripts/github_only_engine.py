#!/usr/bin/env python3
"""
🚀 GitHub-Only Workflow Engine
=============================

Ce système élimine complètement les dépendances de téléchargement
et fait tout passer par GitHub pour une architecture plus robuste.

Architecture:
- Colab commit directement sur GitHub
- Surveillance GitHub continue  
- Synchronisation bidirectionnelle pure
- Zéro dépendance Downloads/fichiers locaux
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Ajouter le chemin du projet
sys.path.append(str(Path(__file__).parent.parent))

class GitHubOnlyEngine:
    """Moteur de workflow 100% GitHub - zéro téléchargement"""
    
    def __init__(self, repo_path: str = "/home/stephane/GitHub/PaniniFS-Research"):
        self.repo_path = Path(repo_path)
        self.results_dir = self.repo_path / "colab_results"
        self.tracking_file = self.repo_path / "github_sync_tracking.json"
        
        # Créer dossier résultats si nécessaire
        self.results_dir.mkdir(exist_ok=True)
        
        self.log("🚀 GitHub-Only Engine initialisé")
        self.log(f"📂 Résultats: {self.results_dir}")
        
    def log(self, message: str, level: str = "INFO"):
        """Log avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def get_tracking_data(self) -> Dict:
        """Récupère les données de tracking GitHub"""
        if self.tracking_file.exists():
            try:
                with open(self.tracking_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.log(f"Erreur lecture tracking: {e}", "ERROR")
        
        return {
            "last_commit_hash": "",
            "processed_commits": [],
            "last_sync": "",
            "active_sessions": []
        }
    
    def save_tracking_data(self, data: Dict):
        """Sauvegarde les données de tracking"""
        try:
            with open(self.tracking_file, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log(f"Erreur sauvegarde tracking: {e}", "ERROR")
    
    def check_github_updates(self) -> List[Dict]:
        """Vérifie les nouveaux commits sur GitHub"""
        try:
            # Git fetch pour récupérer les dernières références
            result = subprocess.run(
                ["git", "fetch"], 
                cwd=self.repo_path,
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode != 0:
                self.log(f"Erreur git fetch: {result.stderr}", "ERROR")
                return []
            
            # Vérifier les nouveaux commits
            result = subprocess.run(
                ["git", "log", "--oneline", "--since=1 hour ago", "origin/main"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode != 0:
                return []
            
            commits = []
            tracking = self.get_tracking_data()
            processed = set(tracking.get("processed_commits", []))
            
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    commit_hash = line.split()[0]
                    commit_msg = ' '.join(line.split()[1:])
                    
                    if commit_hash not in processed:
                        commits.append({
                            "hash": commit_hash,
                            "message": commit_msg,
                            "timestamp": datetime.now().isoformat()
                        })
            
            return commits
            
        except Exception as e:
            self.log(f"Erreur vérification GitHub: {e}", "ERROR")
            return []
    
    def pull_latest_changes(self) -> bool:
        """Pull les derniers changements depuis GitHub"""
        try:
            result = subprocess.run(
                ["git", "pull", "origin", "main"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.log("✅ Pull GitHub réussi")
                return True
            else:
                self.log(f"❌ Erreur pull: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Exception pull: {e}", "ERROR")
            return False
    
    def scan_new_colab_results(self) -> List[Path]:
        """Scan les nouveaux résultats Colab dans le repo"""
        new_results = []
        
        # Patterns de fichiers Colab
        patterns = [
            "colab_results/**/*.json",
            "results/**/*colab*.json", 
            "**/*session_*.json",
            "**/*analysis_results_*.json",
            "**/*checkpoint_*.json"
        ]
        
        for pattern in patterns:
            matches = list(self.repo_path.glob(pattern))
            for match in matches:
                if match.is_file():
                    # Vérifier si fichier récent (moins de 2h)
                    age = time.time() - match.stat().st_mtime
                    if age < 7200:  # 2 heures
                        new_results.append(match)
        
        return new_results
    
    def process_colab_commit(self, commit: Dict) -> bool:
        """Traite un commit venant de Colab"""
        commit_hash = commit["hash"]
        commit_msg = commit["message"]
        
        self.log(f"🔄 Traitement commit: {commit_hash[:7]} - {commit_msg}")
        
        # Pull pour récupérer le commit
        if not self.pull_latest_changes():
            return False
        
        # Scanner les nouveaux résultats
        new_results = self.scan_new_colab_results()
        
        if new_results:
            self.log(f"📊 {len(new_results)} nouveaux résultats détectés")
            
            for result_file in new_results:
                self.process_result_file(result_file, commit_hash)
            
            # Marquer commit comme traité
            tracking = self.get_tracking_data()
            tracking["processed_commits"].append(commit_hash)
            tracking["last_sync"] = datetime.now().isoformat()
            self.save_tracking_data(tracking)
            
            return True
        else:
            self.log("📭 Pas de nouveaux résultats dans ce commit")
            return False
    
    def process_result_file(self, file_path: Path, commit_hash: str):
        """Traite un fichier de résultats"""
        try:
            self.log(f"📄 Traitement: {file_path.name}")
            
            # Lire et valider le fichier
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Créer résumé du traitement
            summary = {
                "source_file": str(file_path.relative_to(self.repo_path)),
                "commit_hash": commit_hash,
                "processed_at": datetime.now().isoformat(),
                "data_size": len(str(data)),
                "keys": list(data.keys()) if isinstance(data, dict) else [],
                "status": "processed"
            }
            
            # Sauvegarder résumé
            summary_file = self.results_dir / f"processing_{file_path.stem}_{commit_hash[:7]}.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            self.log(f"✅ Traité: {file_path.name} → {summary_file.name}")
            
        except Exception as e:
            self.log(f"❌ Erreur traitement {file_path.name}: {e}", "ERROR")
    
    def create_github_only_templates(self) -> Dict[str, str]:
        """Crée des templates Colab 100% GitHub"""
        templates = {}
        
        # Template export direct GitHub
        templates["github_export"] = '''
# 💾 Export Direct GitHub (sans téléchargement)
import json
import subprocess
from datetime import datetime

def export_to_github(data, session_id):
    """Export direct vers GitHub - zéro téléchargement"""
    
    # 1. Sauvegarder dans le repo local
    filename = f"colab_results/session_{session_id}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Sauvegardé: {filename}")
    
    # 2. Commit et push direct
    try:
        subprocess.run(["git", "add", filename], check=True)
        subprocess.run(["git", "commit", "-m", f"📊 Résultats Colab - {session_id}"], check=True)
        subprocess.run(["git", "push"], check=True)
        
        print("🚀 Pushé vers GitHub avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur push: {e}")
        return False

# Usage:
# export_to_github(my_results, SESSION_ID)
'''
        
        # Template surveillance GitHub
        templates["github_monitor"] = '''
# 🔍 Surveillance GitHub Automatique  
import time
import subprocess

def monitor_github_changes():
    """Surveille les changements GitHub en temps réel"""
    
    while True:
        try:
            # Fetch derniers changements
            subprocess.run(["git", "fetch"], check=True, timeout=10)
            
            # Vérifier nouveaux commits
            result = subprocess.run(
                ["git", "log", "--oneline", "-5", "origin/main"],
                capture_output=True, text=True
            )
            
            commits = result.stdout.strip().split('\\n')
            print(f"📊 Derniers commits: {len(commits)}")
            
            for commit in commits[:3]:
                print(f"   • {commit}")
            
            time.sleep(300)  # Check toutes les 5 minutes
            
        except Exception as e:
            print(f"❌ Erreur monitoring: {e}")
            time.sleep(60)

# Démarrer surveillance
# monitor_github_changes()
'''
        
        return templates
    
    def generate_colab_github_cell(self, session_id: str) -> str:
        """Génère une cellule Colab pour export GitHub direct"""
        return f'''
# 🚀 Export GitHub Direct - Session {session_id}
import json
import subprocess
from datetime import datetime

# Configuration session
SESSION_ID = "{session_id}"
RESULTS_DIR = "colab_results"

def direct_github_export(results_data):
    """Export direct vers GitHub sans téléchargement"""
    
    # Créer nom fichier unique
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{{RESULTS_DIR}}/analysis_{{SESSION_ID}}_{{timestamp}}.json"
    
    # Sauvegarder résultats
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Résultats sauvegardés: {{filename}}")
    
    # Commit direct vers GitHub
    try:
        !git add {{filename}}
        !git commit -m "📊 Résultats Colab {{SESSION_ID}} - {{timestamp}}"
        !git push origin main
        
        print("🚀 Résultats pushés vers GitHub avec succès!")
        print("📡 Synchronisation automatique locale activée")
        
        return filename
        
    except Exception as e:
        print(f"❌ Erreur push GitHub: {{e}}")
        return None

# REMPLACER 'your_results' par vos vraies données:
# filename = direct_github_export(your_results)

print("✅ Cellule export GitHub prête")
print("💡 Utilisez: direct_github_export(vos_donnees)")
'''
    
    def start_monitoring(self, interval: int = 300):
        """Démarre la surveillance GitHub continue"""
        self.log(f"🔍 Démarrage surveillance GitHub (intervalle: {interval}s)")
        
        while True:
            try:
                # Vérifier nouveaux commits
                new_commits = self.check_github_updates()
                
                if new_commits:
                    self.log(f"🆕 {len(new_commits)} nouveaux commits détectés")
                    
                    for commit in new_commits:
                        self.process_colab_commit(commit)
                else:
                    self.log("📭 Pas de nouveaux commits")
                
                # Attendre avant prochaine vérification
                time.sleep(interval)
                
            except KeyboardInterrupt:
                self.log("🛑 Surveillance arrêtée par utilisateur")
                break
            except Exception as e:
                self.log(f"❌ Erreur surveillance: {e}", "ERROR")
                time.sleep(60)  # Attendre 1 min avant retry


def main():
    """Point d'entrée principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="GitHub-Only Workflow Engine")
    parser.add_argument("--monitor", action="store_true", help="Démarrer surveillance")
    parser.add_argument("--check", action="store_true", help="Vérifier une fois")
    parser.add_argument("--templates", action="store_true", help="Afficher templates")
    parser.add_argument("--interval", type=int, default=300, help="Intervalle surveillance (s)")
    
    args = parser.parse_args()
    
    engine = GitHubOnlyEngine()
    
    if args.templates:
        templates = engine.create_github_only_templates()
        print("🎯 TEMPLATES GITHUB-ONLY:")
        print("=" * 50)
        for name, code in templates.items():
            print(f"\n📝 {name.upper()}:")
            print("-" * 30)
            print(code)
    
    elif args.check:
        print("🔍 VÉRIFICATION UNIQUE:")
        print("=" * 30)
        new_commits = engine.check_github_updates()
        
        if new_commits:
            print(f"🆕 {len(new_commits)} nouveaux commits:")
            for commit in new_commits:
                print(f"   • {commit['hash'][:7]} - {commit['message']}")
                engine.process_colab_commit(commit)
        else:
            print("📭 Pas de nouveaux commits")
    
    elif args.monitor:
        print("🚀 SURVEILLANCE CONTINUE:")
        print("=" * 30)
        engine.start_monitoring(args.interval)
    
    else:
        print("🎯 GitHub-Only Workflow Engine")
        print("Usage:")
        print("  --monitor    : Surveillance continue")
        print("  --check      : Vérification unique")
        print("  --templates  : Afficher templates")
        print("  --interval N : Intervalle surveillance (s)")


if __name__ == "__main__":
    main()