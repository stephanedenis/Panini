#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RENOMMEUR GITHUB REPOSITORY AUTONOME
===================================
Système Python autonome pour renommer repository GitHub
PaniniFS-Research → Panini

Respecte contraintes autonomie :
- Python pur (pas de shell, pipes, python3 -c)
- Gestion complète via git commands subprocess
- Sauvegarde automatique avant modifications
- Migration GitHub Projects/Issues
"""

import subprocess
import logging
import json
from pathlib import Path
from datetime import datetime


class GitHubRepositoryRenamer:
    """Renommeur autonome repository GitHub"""
    
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.old_name = "PaniniFS-Research"
        self.new_name = "Panini"
        self.repo_path = Path("/home/stephane/GitHub/Panini")
        self.backup_info = {}
        
    def setup_logging(self):
        """Configuration logging autonome"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('renommage_github_repository.log'),
                logging.StreamHandler()
            ]
        )
    
    def validate_preconditions(self) -> bool:
        """Valider préconditions renommage"""
        self.logger.info("🔍 VALIDATION PRÉCONDITIONS")
        
        # Vérifier existence repository local
        if not self.repo_path.exists():
            self.logger.error(f"❌ Repository local introuvable: {self.repo_path}")
            return False
        
        # Vérifier que c'est un repository git
        git_dir = self.repo_path / ".git"
        if not git_dir.exists():
            self.logger.error(f"❌ Pas un repository git: {self.repo_path}")
            return False
        
        # Vérifier remote origin
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            remote_url = result.stdout.strip()
            self.logger.info(f"✅ Remote actuel: {remote_url}")
            
            # Vérifier que c'est bien le bon repository
            if self.old_name not in remote_url:
                self.logger.warning(f"⚠️  Remote ne contient pas {self.old_name}")
                return False
            
            self.backup_info["original_remote"] = remote_url
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Erreur vérification remote: {e}")
            return False
    
    def create_safety_backup(self) -> bool:
        """Créer sauvegarde sécurisée avant renommage"""
        self.logger.info("💾 CRÉATION SAUVEGARDE SÉCURISÉE")
        
        try:
            # Tag de sauvegarde avec timestamp
            backup_tag = f"v-pre-rename-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            # Créer tag local
            subprocess.run(
                ["git", "tag", "-a", backup_tag, "-m", 
                 f"Sauvegarde avant renommage {self.old_name} → {self.new_name}"],
                cwd=self.repo_path,
                check=True
            )
            
            # Push tag vers GitHub
            subprocess.run(
                ["git", "push", "origin", backup_tag],
                cwd=self.repo_path,
                check=True
            )
            
            self.backup_info["backup_tag"] = backup_tag
            self.logger.info(f"✅ Tag sauvegarde créé: {backup_tag}")
            
            # Sauvegarder état actuel
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            self.backup_info["pre_rename_status"] = status_result.stdout
            self.backup_info["timestamp"] = datetime.now().isoformat()
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Erreur création sauvegarde: {e}")
            return False
    
    def analyze_github_impact(self) -> dict:
        """Analyser impact potential sur GitHub Projects/Issues"""
        self.logger.info("📋 ANALYSE IMPACT GITHUB PROJECTS")
        
        impact_analysis = {
            "repository": self.old_name,
            "estimated_impact": "HIGH",
            "potential_issues": [
                "GitHub Projects associés au repository",
                "Issues et Pull Requests avec liens",
                "Webhooks configurés",
                "Pages GitHub (github.io)",
                "Liens externes vers repository"
            ],
            "mitigation_steps": [
                "GitHub devrait créer redirections automatiques",
                "Notifier collaborateurs du changement",
                "Mettre à jour documentation externe",
                "Vérifier webhooks post-renommage"
            ]
        }
        
        self.backup_info["github_impact"] = impact_analysis
        self.logger.info("✅ Analyse impact complétée")
        
        return impact_analysis
    
    def prepare_rename_instructions(self) -> dict:
        """Préparer instructions renommage GitHub"""
        self.logger.info("📋 PRÉPARATION INSTRUCTIONS RENOMMAGE")
        
        # Note: GitHub repository rename doit être fait manuellement
        # via interface web ou GitHub API (nécessite authentification)
        
        instructions = {
            "method": "MANUAL_VIA_GITHUB_WEB",
            "steps": [
                f"1. Aller sur https://github.com/stephanedenis/{self.old_name}",
                "2. Cliquer 'Settings' dans le menu repository",
                "3. Descendre à section 'Repository name'",
                f"4. Changer '{self.old_name}' → '{self.new_name}'",
                "5. Confirmer avec 'Rename repository'",
                "6. GitHub créera automatiquement redirections"
            ],
            "post_rename_local_update": [
                f"7. Mettre à jour remote local après renommage GitHub",
                f"8. Nouveau remote: ssh://git@github.com/stephanedenis/{self.new_name}.git",
                "9. Vérifier fonctionnement push/pull"
            ],
            "verification": [
                f"10. Tester accès https://github.com/stephanedenis/{self.new_name}",
                f"11. Vérifier redirection https://github.com/stephanedenis/{self.old_name}",
                "12. Contrôler GitHub Projects/Issues migration automatique"
            ]
        }
        
        self.backup_info["rename_instructions"] = instructions
        return instructions
    
    def prepare_local_remote_update(self) -> str:
        """Préparer script mise à jour remote local"""
        self.logger.info("🔧 PRÉPARATION SCRIPT MISE À JOUR LOCAL")
        
        update_script = f"""#!/usr/bin/env python3
# Script généré automatiquement pour mise à jour remote local
# À exécuter APRÈS renommage GitHub manual

import subprocess
from pathlib import Path

def update_remote():
    repo_path = Path("{self.repo_path}")
    new_remote = "ssh://git@github.com/stephanedenis/{self.new_name}.git"
    
    try:
        # Mettre à jour remote origin
        subprocess.run([
            "git", "remote", "set-url", "origin", new_remote
        ], cwd=repo_path, check=True)
        
        print(f"✅ Remote mis à jour: {{new_remote}}")
        
        # Vérifier nouvelle configuration
        result = subprocess.run([
            "git", "remote", "get-url", "origin"
        ], cwd=repo_path, capture_output=True, text=True, check=True)
        
        print(f"✅ Vérification remote: {{result.stdout.strip()}}")
        
        # Test connexion
        subprocess.run([
            "git", "fetch", "origin"
        ], cwd=repo_path, check=True)
        
        print("✅ Test connexion réussi")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur mise à jour remote: {{e}}")
        return False

if __name__ == "__main__":
    success = update_remote()
    exit(0 if success else 1)
"""
        
        script_file = "update_remote_after_github_rename.py"
        
        try:
            with open(script_file, 'w', encoding='utf-8') as f:
                f.write(update_script)
            
            # Rendre exécutable
            import os
            os.chmod(script_file, 0o755)
            
            self.logger.info(f"✅ Script créé: {script_file}")
            return script_file
            
        except Exception as e:
            self.logger.error(f"❌ Erreur création script: {e}")
            return ""
    
    def generate_complete_report(self) -> str:
        """Générer rapport complet renommage"""
        self.logger.info("📋 GÉNÉRATION RAPPORT COMPLET")
        
        report = f"""
🔄 RENOMMAGE GITHUB REPOSITORY - RAPPORT COMPLET
===============================================
Généré le: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

📊 INFORMATIONS GÉNÉRALES:
• Repository: {self.old_name} → {self.new_name}
• Path local: {self.repo_path}
• Remote original: {self.backup_info.get('original_remote', 'N/A')}
• Tag sauvegarde: {self.backup_info.get('backup_tag', 'N/A')}

🔒 SAUVEGARDE SÉCURISÉE:
✅ Tag de sauvegarde créé et pushé sur GitHub
✅ État repository sauvegardé
✅ Rollback possible si nécessaire

📋 IMPACT GITHUB PROJECTS:
• Niveau impact: HIGH
• Projects/Issues: Migration automatique GitHub
• Redirections: Créées automatiquement par GitHub
• Liens externes: Nécessitent mise à jour manuelle

🎯 ACTIONS REQUISES:

ÉTAPE 1 - RENOMMAGE GITHUB (MANUEL):
1. Aller sur: https://github.com/stephanedenis/{self.old_name}
2. Settings → Repository name
3. Changer: {self.old_name} → {self.new_name}
4. Confirmer renommage

ÉTAPE 2 - MISE À JOUR LOCAL (AUTO):
Exécuter: python3 update_remote_after_github_rename.py

ÉTAPE 3 - VÉRIFICATIONS:
• Tester accès nouveau repository
• Vérifier redirections
• Contrôler Projects/Issues
• Mettre à jour documentation externe

⚠️  IMPORTANT:
- Renommage GitHub doit être fait manuellement (interface web)
- Script local ready pour mise à jour automatique remote
- Sauvegarde créée pour rollback si nécessaire
- GitHub créera redirections automatiques

🔧 ROLLBACK SI NÉCESSAIRE:
1. Renommer repository GitHub: {self.new_name} → {self.old_name}
2. git remote set-url origin {self.backup_info.get('original_remote', '')}
3. git checkout {self.backup_info.get('backup_tag', '')}

✅ PRÉPARATION COMPLÈTE - PRÊT POUR RENOMMAGE MANUEL
"""
        
        report_file = f"RENOMMAGE_GITHUB_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            self.logger.info(f"✅ Rapport sauvegardé: {report_file}")
            return report_file
            
        except Exception as e:
            self.logger.error(f"❌ Erreur rapport: {e}")
            return ""
    
    def save_backup_metadata(self) -> str:
        """Sauvegarder métadonnées complètes"""
        metadata_file = f"backup_metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.backup_info, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"✅ Métadonnées sauvées: {metadata_file}")
            return metadata_file
            
        except Exception as e:
            self.logger.error(f"❌ Erreur métadonnées: {e}")
            return ""
    
    def run_preparation_complete(self) -> bool:
        """Exécution complète préparation renommage"""
        self.logger.info("🚀 DÉMARRAGE PRÉPARATION RENOMMAGE GITHUB")
        
        try:
            # Validation préconditions
            if not self.validate_preconditions():
                self.logger.error("❌ Préconditions non validées")
                return False
            
            # Sauvegarde sécurisée
            if not self.create_safety_backup():
                self.logger.error("❌ Échec sauvegarde sécurisée")
                return False
            
            # Analyse impact
            impact = self.analyze_github_impact()
            
            # Instructions renommage
            instructions = self.prepare_rename_instructions()
            
            # Script mise à jour local
            update_script = self.prepare_local_remote_update()
            
            # Rapport complet
            report_file = self.generate_complete_report()
            
            # Métadonnées
            metadata_file = self.save_backup_metadata()
            
            # Résultats finaux
            print("\n" + "="*60)
            print("🎯 PRÉPARATION RENOMMAGE GITHUB COMPLÉTÉE")
            print("="*60)
            print(f"🔄 {self.old_name} → {self.new_name}")
            print(f"💾 Sauvegarde: {self.backup_info.get('backup_tag', 'N/A')}")
            print(f"📋 Rapport: {report_file}")
            print(f"🔧 Script auto: {update_script}")
            print("\n🎯 PROCHAINE ÉTAPE:")
            print("1. Renommage MANUEL sur GitHub (interface web)")
            print(f"2. Exécuter: python3 {update_script}")
            print("="*60)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur préparation: {e}")
            return False


def main():
    """Point d'entrée principal"""
    print("🔄 RENOMMEUR GITHUB REPOSITORY AUTONOME")
    print("======================================")
    print("PaniniFS-Research → Panini")
    print("Python pur - Respect contraintes autonomie")
    print()
    
    renamer = GitHubRepositoryRenamer()
    success = renamer.run_preparation_complete()
    
    if success:
        print("\n✅ PRÉPARATION COMPLÈTE - PRÊT POUR RENOMMAGE")
        print("🎯 Action manuelle requise: renommage GitHub interface web")
    else:
        print("\n❌ ÉCHEC PRÉPARATION")
        print("📋 Vérifiez logs pour diagnostic")
    
    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)