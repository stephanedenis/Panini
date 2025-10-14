#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDITEUR REPOSITORIES GITHUB AUTONOME
====================================
Système autonome pour analyser et synchroniser les repositories GitHub
après refactoring architecture Panini.

Fonctionnalités:
- Audit état repositories locaux vs GitHub
- Détection conflits nommage post-refactoring  
- Analyse GitHub Projects/Tasks impactés
- Recommandations migration/nettoyage
- Exécution autonome respectant contraintes
"""

import os
import sys
import json
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class RepositoryAuditor:
    """Auditeur autonome des repositories GitHub"""
    
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.github_dir = Path("/home/stephane/GitHub")
        self.audit_results = {
            "timestamp": datetime.now().isoformat(),
            "local_repos": [],
            "conflicts": [],
            "migrations_needed": [],
            "github_projects_impact": [],
            "recommendations": []
        }
    
    def setup_logging(self):
        """Configuration logging autonome"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('audit_repositories_github.log'),
                logging.StreamHandler()
            ]
        )
    
    def scan_local_repositories(self) -> List[Dict]:
        """Scanner tous les repositories locaux"""
        self.logger.info("🔍 SCAN REPOSITORIES LOCAUX")
        
        local_repos = []
        
        try:
            # Trouver tous les dossiers .git
            result = subprocess.run(
                ["find", str(self.github_dir), "-name", ".git", "-type", "d"],
                capture_output=True, text=True, check=True
            )
            
            git_dirs = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            for git_dir in git_dirs:
                if git_dir:
                    repo_path = Path(git_dir).parent
                    repo_name = repo_path.name
                    
                    # Analyser chaque repository
                    repo_info = self.analyze_repository(repo_path)
                    if repo_info:
                        local_repos.append(repo_info)
                        self.logger.info(f"   📁 {repo_name}: {repo_info['status']}")
            
            self.audit_results["local_repos"] = local_repos
            self.logger.info(f"✅ {len(local_repos)} repositories analysés")
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Erreur scan repositories: {e}")
        
        return local_repos
    
    def analyze_repository(self, repo_path: Path) -> Optional[Dict]:
        """Analyser un repository individuel"""
        try:
            repo_name = repo_path.name
            
            # Obtenir remote origin
            remote_result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=repo_path, capture_output=True, text=True
            )
            
            remote_url = remote_result.stdout.strip() if remote_result.returncode == 0 else "NO_REMOTE"
            
            # Obtenir statut git
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo_path, capture_output=True, text=True
            )
            
            has_changes = bool(status_result.stdout.strip()) if status_result.returncode == 0 else False
            
            # Obtenir branche actuelle
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=repo_path, capture_output=True, text=True
            )
            
            current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"
            
            return {
                "name": repo_name,
                "path": str(repo_path),
                "remote_url": remote_url,
                "has_changes": has_changes,
                "current_branch": current_branch,
                "status": "ACTIVE" if remote_url != "NO_REMOTE" else "LOCAL_ONLY",
                "is_github": "github.com" in remote_url.lower()
            }
            
        except Exception as e:
            self.logger.warning(f"⚠️  Erreur analyse {repo_path.name}: {e}")
            return None
    
    def detect_naming_conflicts(self, repos: List[Dict]) -> List[Dict]:
        """Détecter les conflits de nommage post-refactoring"""
        self.logger.info("🔍 DÉTECTION CONFLITS NOMMAGE")
        
        conflicts = []
        
        # Mappings attendus post-refactoring
        expected_mappings = {
            "PaniniFS-Research": "Panini",
            "OntoWave": "Panini-OntoWave"
        }
        
        for repo in repos:
            repo_name = repo["name"]
            
            # Vérifier si c'est un ancien nom qui devrait être renommé
            if repo_name in expected_mappings:
                new_name = expected_mappings[repo_name]
                
                # Vérifier si le nouveau nom existe déjà
                new_repo_exists = any(r["name"] == new_name for r in repos)
                
                conflict = {
                    "type": "RENAMING_NEEDED",
                    "old_name": repo_name,
                    "new_name": new_name,
                    "old_path": repo["path"],
                    "new_exists": new_repo_exists,
                    "remote_url": repo["remote_url"],
                    "priority": "HIGH" if repo["is_github"] else "MEDIUM"
                }
                
                conflicts.append(conflict)
                self.logger.warning(f"   ⚠️  {repo_name} → {new_name} (nouveau existe: {new_repo_exists})")
            
            # Vérifier les modules PaniniFS-* qui pourraient être obsolètes
            if repo_name.startswith("PaniniFS-") and repo_name not in ["PaniniFS"]:
                potential_conflict = {
                    "type": "OBSOLETE_MODULE",
                    "name": repo_name,
                    "path": repo["path"],
                    "remote_url": repo["remote_url"],
                    "recommendation": "Vérifier si module toujours nécessaire ou à intégrer",
                    "priority": "LOW"
                }
                conflicts.append(potential_conflict)
        
        self.audit_results["conflicts"] = conflicts
        self.logger.info(f"✅ {len(conflicts)} conflits détectés")
        
        return conflicts
    
    def analyze_github_projects_impact(self, repos: List[Dict]) -> List[Dict]:
        """Analyser l'impact sur les GitHub Projects/Tasks"""
        self.logger.info("🔍 ANALYSE IMPACT GITHUB PROJECTS")
        
        impacted_projects = []
        
        for repo in repos:
            if repo["is_github"] and repo["name"] in ["PaniniFS-Research", "OntoWave"]:
                
                # Simulation analyse GitHub API (sans clés API pour autonomie)
                project_impact = {
                    "repository": repo["name"],
                    "remote_url": repo["remote_url"],
                    "estimated_projects": self.estimate_github_projects(repo["name"]),
                    "migration_complexity": self.assess_migration_complexity(repo["name"]),
                    "recommended_action": self.recommend_github_action(repo["name"])
                }
                
                impacted_projects.append(project_impact)
                self.logger.info(f"   📋 {repo['name']}: {project_impact['estimated_projects']} projets estimés")
        
        self.audit_results["github_projects_impact"] = impacted_projects
        self.logger.info(f"✅ {len(impacted_projects)} repositories GitHub analysés")
        
        return impacted_projects
    
    def estimate_github_projects(self, repo_name: str) -> str:
        """Estimer le nombre de projets GitHub (heuristique)"""
        if repo_name == "PaniniFS-Research":
            return "ÉLEVÉ (recherche active, potentiellement issues/milestones)"
        elif repo_name == "OntoWave":
            return "MOYEN (interface utilisateur, possibles issues UI)"
        else:
            return "FAIBLE"
    
    def assess_migration_complexity(self, repo_name: str) -> str:
        """Évaluer complexité migration"""
        if repo_name == "PaniniFS-Research":
            return "ÉLEVÉE (233GB données, historique recherche)"
        elif repo_name == "OntoWave":
            return "MOYENNE (TypeScript/Vite, dépendances)"
        else:
            return "FAIBLE"
    
    def recommend_github_action(self, repo_name: str) -> str:
        """Recommander action GitHub"""
        if repo_name == "PaniniFS-Research":
            return "RENOMMER repo GitHub PaniniFS-Research → Panini + migration projects"
        elif repo_name == "OntoWave":
            return "RENOMMER repo GitHub OntoWave → Panini-OntoWave + redirection"
        else:
            return "ÉVALUER si conservation nécessaire"
    
    def generate_migration_plan(self) -> List[Dict]:
        """Générer plan de migration autonome"""
        self.logger.info("📋 GÉNÉRATION PLAN MIGRATION")
        
        migrations = []
        
        for conflict in self.audit_results["conflicts"]:
            if conflict["type"] == "RENAMING_NEEDED":
                migration = {
                    "action": "REPOSITORY_RENAME",
                    "old_name": conflict["old_name"],
                    "new_name": conflict["new_name"],
                    "steps": [
                        f"1. Sauvegarder état actuel {conflict['old_name']}",
                        f"2. Renommer repository GitHub: {conflict['old_name']} → {conflict['new_name']}",
                        "3. Mettre à jour remote local",
                        "4. Migrer GitHub Projects/Issues si existants",
                        "5. Configurer redirections",
                        "6. Notifier collaborateurs"
                    ],
                    "priority": conflict["priority"],
                    "estimated_duration": "30-60 minutes",
                    "risks": [
                        "Perte liens externes temporaire",
                        "Impact GitHub Projects",
                        "Confusion collaborateurs"
                    ]
                }
                migrations.append(migration)
        
        # Ajouter nettoyage modules obsolètes
        obsolete_modules = [c for c in self.audit_results["conflicts"] if c["type"] == "OBSOLETE_MODULE"]
        if obsolete_modules:
            cleanup_migration = {
                "action": "CLEANUP_OBSOLETE_MODULES",
                "modules": [m["name"] for m in obsolete_modules],
                "steps": [
                    "1. Analyser utilisation effective de chaque module",
                    "2. Identifier dépendances inter-modules",
                    "3. Sauvegarder modules potentiellement utiles",
                    "4. Archiver ou supprimer modules obsolètes",
                    "5. Mettre à jour documentation"
                ],
                "priority": "LOW",
                "estimated_duration": "2-4 heures",
                "risks": ["Perte code potentiellement utile"]
            }
            migrations.append(cleanup_migration)
        
        self.audit_results["migrations_needed"] = migrations
        self.logger.info(f"✅ {len(migrations)} migrations planifiées")
        
        return migrations
    
    def generate_recommendations(self) -> List[str]:
        """Générer recommandations autonomes"""
        recommendations = []
        
        # Recommandations basées sur l'analyse
        if any(c["type"] == "RENAMING_NEEDED" for c in self.audit_results["conflicts"]):
            recommendations.append(
                "🔄 URGENT: Renommer repositories GitHub pour cohérence architecture"
            )
        
        if any(p["migration_complexity"] == "ÉLEVÉE" for p in self.audit_results["github_projects_impact"]):
            recommendations.append(
                "⚠️  ATTENTION: Migration complexe détectée - prévoir sauvegarde complète"
            )
        
        if len(self.audit_results["conflicts"]) > 3:
            recommendations.append(
                "🧹 NETTOYAGE: Nombreux conflits détectés - envisager refactoring complet GitHub"
            )
        
        # Recommandations constructives
        recommendations.extend([
            "✅ AUTOMATISATION: Utiliser GitHub API pour migration automatique",
            "📋 COMMUNICATION: Préparer annonce changements pour collaborateurs", 
            "🔗 REDIRECTIONS: Configurer redirections anciennes URLs",
            "📚 DOCUMENTATION: Mettre à jour liens dans documentation"
        ])
        
        self.audit_results["recommendations"] = recommendations
        return recommendations
    
    def save_audit_report(self) -> str:
        """Sauvegarder rapport d'audit complet"""
        report_file = f"audit_repositories_github_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.audit_results, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"✅ Rapport sauvegardé: {report_file}")
            return report_file
            
        except Exception as e:
            self.logger.error(f"❌ Erreur sauvegarde rapport: {e}")
            return ""
    
    def create_summary_report(self) -> str:
        """Créer rapport résumé lisible"""
        summary = f"""
🔍 AUDIT REPOSITORIES GITHUB - RAPPORT AUTONOME
===============================================
Exécuté le: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

📊 STATISTIQUES:
• Repositories analysés: {len(self.audit_results['local_repos'])}
• Conflits détectés: {len(self.audit_results['conflicts'])}
• Migrations nécessaires: {len(self.audit_results['migrations_needed'])}
• Impact GitHub Projects: {len(self.audit_results['github_projects_impact'])}

🚨 CONFLITS MAJEURS:
"""
        
        for conflict in self.audit_results["conflicts"]:
            if conflict["priority"] in ["HIGH", "MEDIUM"]:
                summary += f"• {conflict['type']}: {conflict.get('old_name', conflict.get('name', 'N/A'))}\n"
        
        summary += f"""
📋 MIGRATIONS RECOMMANDÉES:
"""
        
        for migration in self.audit_results["migrations_needed"]:
            summary += f"• {migration['action']} ({migration['priority']})\n"
        
        summary += f"""
💡 RECOMMANDATIONS PRIORITAIRES:
"""
        
        for i, rec in enumerate(self.audit_results["recommendations"][:5], 1):
            summary += f"{i}. {rec}\n"
        
        summary += f"""
🎯 ACTIONS IMMÉDIATES:
1. Renommer PaniniFS-Research → Panini sur GitHub
2. Renommer OntoWave → Panini-OntoWave sur GitHub  
3. Migrer GitHub Projects/Issues
4. Configurer redirections
5. Mettre à jour documentation

📁 Rapport détaillé: {self.save_audit_report()}
"""
        
        summary_file = f"AUDIT_REPOSITORIES_SUMMARY_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        try:
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary)
            
            self.logger.info(f"✅ Résumé sauvegardé: {summary_file}")
            return summary_file
            
        except Exception as e:
            self.logger.error(f"❌ Erreur résumé: {e}")
            return ""
    
    def run_autonomous_audit(self) -> bool:
        """Exécution autonome complète de l'audit"""
        self.logger.info("🚀 DÉMARRAGE AUDIT AUTONOME REPOSITORIES GITHUB")
        
        try:
            # Phase 1: Scanner repositories locaux
            repos = self.scan_local_repositories()
            
            # Phase 2: Détecter conflits nommage  
            conflicts = self.detect_naming_conflicts(repos)
            
            # Phase 3: Analyser impact GitHub Projects
            projects_impact = self.analyze_github_projects_impact(repos)
            
            # Phase 4: Générer plan migration
            migrations = self.generate_migration_plan()
            
            # Phase 5: Générer recommandations
            recommendations = self.generate_recommendations()
            
            # Phase 6: Créer rapports
            summary_file = self.create_summary_report()
            
            # Résultats
            self.logger.info("=" * 60)
            self.logger.info("🎯 AUDIT REPOSITORIES GITHUB - RÉSULTATS")
            self.logger.info(f"📁 Repositories: {len(repos)}")
            self.logger.info(f"⚠️  Conflits: {len(conflicts)}")
            self.logger.info(f"🔄 Migrations: {len(migrations)}")
            self.logger.info(f"💡 Recommandations: {len(recommendations)}")
            self.logger.info(f"📋 Rapport: {summary_file}")
            self.logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur audit autonome: {e}")
            return False


def main():
    """Point d'entrée principal"""
    print("🔍 AUDITEUR REPOSITORIES GITHUB AUTONOME")
    print("========================================")
    print("Analyse post-refactoring architecture Panini")
    print()
    
    auditor = RepositoryAuditor()
    success = auditor.run_autonomous_audit()
    
    if success:
        print("\n✅ AUDIT AUTONOME RÉUSSI")
        print("📋 Consultez les rapports générés pour actions recommandées")
    else:
        print("\n❌ ÉCHEC AUDIT AUTONOME")
        print("📋 Vérifiez les logs pour diagnostiquer les problèmes")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)