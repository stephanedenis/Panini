#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLAN DE REDRESSEMENT ARCHITECTURAL - ÉCOSYSTÈME PANINI
====================================================
Réorganisation complète : Panini comme parent principal
Tous les modules PaniniFS-* → Panini-*

Objectifs :
1. Panini = Parent principal avec tous les autres en submodules
2. PaniniFS → Panini-FS (pour la partie filesystem)
3. Tous PaniniFS-* → Panini-* 
4. Structure cohérente et hiérarchique claire
"""

import os
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


class PaniniArchitecturalRedressing:
    """Planificateur redressement architectural Panini"""
    
    def __init__(self):
        self.base_path = Path("/home/stephane/GitHub")
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.plan_file = f"redressement_architectural_plan_{self.timestamp}.json"
        
        # Mapping des renommages nécessaires
        self.renaming_plan = {
            # Repository principal (garde son nom)
            "Panini": "Panini",
            
            # Filesystem core
            "PaniniFS": "Panini-FS",
            
            # Modules spécialisés
            "PaniniFS-AttributionRegistry": "Panini-AttributionRegistry",
            "PaniniFS-AutonomousMissions": "Panini-AutonomousMissions", 
            "PaniniFS-CloudOrchestrator": "Panini-CloudOrchestrator",
            "PaniniFS-CoLabController": "Panini-CoLabController",
            "PaniniFS-CopilotageShared": "Panini-CopilotageShared",
            "PaniniFS-DatasetsIngestion": "Panini-DatasetsIngestion",
            "PaniniFS-ExecutionOrchestrator": "Panini-ExecutionOrchestrator",
            "PaniniFS-PublicationEngine": "Panini-PublicationEngine",
            "PaniniFS-SemanticCore": "Panini-SemanticCore",
            "PaniniFS-SpecKit-Shared": "Panini-SpecKit-Shared",
            "PaniniFS-UltraReactive": "Panini-UltraReactive",
            
            # Projets dérivés (gardent leur structure)
            "Panini-Gest": "Panini-Gest",
            "Panini-OntoWave": "Panini-OntoWave",
            
            # Recherche (consolidation)
            "Panini-Research": "Panini-Research",  # Sera supprimé après consolidation
            "PaniniFS-Research": None  # Sera intégré dans Panini
        }
    
    def scan_current_repositories(self) -> Dict:
        """Scanner les repositories actuels"""
        repos = {}
        
        for item in self.base_path.iterdir():
            if item.is_dir() and "Panini" in item.name and item.name != ".git":
                repo_info = {
                    "current_name": item.name,
                    "target_name": self.renaming_plan.get(item.name, item.name),
                    "path": str(item),
                    "exists": True,
                    "has_git": (item / ".git").exists(),
                    "has_readme": (item / "README.md").exists(),
                    "action": self.determine_action(item.name)
                }
                
                if repo_info["has_git"]:
                    try:
                        # Récupérer l'URL remote
                        result = subprocess.run(
                            ["git", "-C", str(item), "remote", "get-url", "origin"],
                            capture_output=True, text=True, check=True
                        )
                        repo_info["remote_url"] = result.stdout.strip()
                    except:
                        repo_info["remote_url"] = "unknown"
                
                repos[item.name] = repo_info
        
        return repos
    
    def determine_action(self, current_name: str) -> str:
        """Déterminer l'action nécessaire pour chaque repository"""
        if current_name == "Panini":
            return "KEEP_AS_PARENT"
        elif current_name == "Panini-Research":
            return "CONSOLIDATE_INTO_PARENT"
        elif current_name == "PaniniFS-Research":
            return "INTEGRATE_AS_SUBMODULE"
        elif current_name.startswith("PaniniFS"):
            return "RENAME_AND_SUBMODULE"
        elif current_name.startswith("Panini-"):
            return "CONVERT_TO_SUBMODULE"
        else:
            return "ANALYZE"
    
    def generate_new_architecture(self) -> Dict:
        """Générer la nouvelle architecture cible"""
        return {
            "parent": {
                "name": "Panini",
                "description": "Parent principal - Écosystème complet de compression sémantique universelle",
                "role": "Orchestrateur principal et workspace de développement"
            },
            "submodules": {
                "core": {
                    "Panini-FS": {
                        "path": "modules/core/filesystem",
                        "description": "Système de fichiers sémantique core",
                        "current": "PaniniFS"
                    },
                    "Panini-SemanticCore": {
                        "path": "modules/core/semantic",
                        "description": "Moteur sémantique principal",
                        "current": "PaniniFS-SemanticCore"
                    }
                },
                "orchestration": {
                    "Panini-CloudOrchestrator": {
                        "path": "modules/orchestration/cloud",
                        "description": "Orchestrateur cloud",
                        "current": "PaniniFS-CloudOrchestrator"
                    },
                    "Panini-ExecutionOrchestrator": {
                        "path": "modules/orchestration/execution",
                        "description": "Orchestrateur d'exécution",
                        "current": "PaniniFS-ExecutionOrchestrator"
                    }
                },
                "services": {
                    "Panini-CoLabController": {
                        "path": "modules/services/colab",
                        "description": "Contrôleur Google Colab",
                        "current": "PaniniFS-CoLabController"
                    },
                    "Panini-PublicationEngine": {
                        "path": "modules/services/publication",
                        "description": "Moteur de publication",
                        "current": "PaniniFS-PublicationEngine"
                    },
                    "Panini-DatasetsIngestion": {
                        "path": "modules/services/datasets",
                        "description": "Ingestion de datasets",
                        "current": "PaniniFS-DatasetsIngestion"
                    }
                },
                "infrastructure": {
                    "Panini-UltraReactive": {
                        "path": "modules/infrastructure/reactive",
                        "description": "Système ultra-réactif",
                        "current": "PaniniFS-UltraReactive"
                    },
                    "Panini-AutonomousMissions": {
                        "path": "modules/infrastructure/autonomous",
                        "description": "Missions autonomes",
                        "current": "PaniniFS-AutonomousMissions"
                    }
                },
                "shared": {
                    "Panini-CopilotageShared": {
                        "path": "shared/copilotage",
                        "description": "Configuration copilotage partagée",
                        "current": "PaniniFS-CopilotageShared"
                    },
                    "Panini-SpecKit-Shared": {
                        "path": "shared/speckit",
                        "description": "Kit de spécifications partagé",
                        "current": "PaniniFS-SpecKit-Shared"
                    },
                    "Panini-AttributionRegistry": {
                        "path": "shared/attribution",
                        "description": "Registre d'attribution",
                        "current": "PaniniFS-AttributionRegistry"
                    }
                },
                "projects": {
                    "Panini-Gest": {
                        "path": "projects/gest",
                        "description": "Gestionnaire Panini",
                        "current": "Panini-Gest"
                    },
                    "Panini-OntoWave": {
                        "path": "projects/ontowave",
                        "description": "Navigateur d'ontologies",
                        "current": "Panini-OntoWave"
                    }
                }
            }
        }
    
    def create_migration_phases(self) -> List[Dict]:
        """Créer les phases de migration"""
        return [
            {
                "phase": 1,
                "name": "Préparation et sauvegarde",
                "actions": [
                    "Sauvegarde complète de tous les repositories",
                    "Création des scripts de renommage GitHub",
                    "Validation de l'état Git de tous les repos",
                    "Export des GitHub Projects/Issues"
                ],
                "duration": "1-2 heures",
                "risk": "Faible"
            },
            {
                "phase": 2,
                "name": "Renommage des repositories GitHub",
                "actions": [
                    "Renommage PaniniFS → Panini-FS",
                    "Renommage tous PaniniFS-* → Panini-*",
                    "Mise à jour des URLs remotes locales",
                    "Vérification accessibilité repositories"
                ],
                "duration": "2-3 heures",
                "risk": "Moyen"
            },
            {
                "phase": 3,
                "name": "Restructuration Panini parent",
                "actions": [
                    "Consolidation Panini-Research dans Panini",
                    "Création structure modules/ avec catégories",
                    "Configuration .gitmodules pour tous les submodules",
                    "Mise à jour documentation principale"
                ],
                "duration": "3-4 heures", 
                "risk": "Moyen"
            },
            {
                "phase": 4,
                "name": "Configuration submodules",
                "actions": [
                    "Ajout de tous les modules comme submodules",
                    "Configuration des chemins selon nouvelle architecture",
                    "Synchronisation et tests",
                    "Mise à jour des références croisées"
                ],
                "duration": "2-3 heures",
                "risk": "Élevé"
            },
            {
                "phase": 5,
                "name": "Finalisation et documentation",
                "actions": [
                    "Mise à jour de toute la documentation",
                    "Création guides migration pour utilisateurs",
                    "Tests complets de l'écosystème",
                    "Communication changements"
                ],
                "duration": "1-2 heures",
                "risk": "Faible"
            }
        ]
    
    def generate_github_rename_script(self, repos: Dict) -> str:
        """Générer le script de renommage GitHub"""
        script_lines = [
            "#!/bin/bash",
            "# Script automatique de renommage repositories GitHub",
            "# ATTENTION : Vérifiez les permissions GitHub avant exécution",
            "",
            "set -e",
            "",
            "echo '🔄 DÉBUT RENOMMAGE REPOSITORIES GITHUB'",
            "echo '======================================'",
            ""
        ]
        
        for current_name, info in repos.items():
            if info["action"] == "RENAME_AND_SUBMODULE":
                target = info["target_name"]
                script_lines.extend([
                    f"echo '📝 Renommage {current_name} → {target}'",
                    f"gh repo rename {current_name} {target} --repo stephanedenis/{current_name}",
                    f"cd /home/stephane/GitHub/{current_name}",
                    f"git remote set-url origin git@github.com:stephanedenis/{target}.git",
                    f"cd ..",
                    f"mv {current_name} {target}",
                    ""
                ])
        
        script_lines.extend([
            "echo '✅ RENOMMAGE TERMINÉ'",
            "echo 'Vérifiez manuellement que tous les repositories sont accessibles'"
        ])
        
        return "\n".join(script_lines)
    
    def generate_full_plan(self) -> Dict:
        """Générer le plan complet de redressement"""
        print("🔍 Scanning repositories actuels...")
        current_repos = self.scan_current_repositories()
        
        print("🏗️ Génération nouvelle architecture...")
        new_architecture = self.generate_new_architecture()
        
        print("📋 Création phases de migration...")
        migration_phases = self.create_migration_phases()
        
        print("📝 Génération script renommage...")
        rename_script = self.generate_github_rename_script(current_repos)
        
        full_plan = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "version": "1.0",
                "scope": "Complete Panini ecosystem architectural redressing"
            },
            "current_state": {
                "repositories": current_repos,
                "total_repos": len(current_repos),
                "parent_repo": "Panini"
            },
            "target_architecture": new_architecture,
            "migration_phases": migration_phases,
            "rename_script": rename_script,
            "risks_and_mitigations": {
                "GitHub API limits": "Utiliser authentification et espacer les requêtes",
                "Broken links": "Maintenir redirections temporaires",
                "Submodule conflicts": "Tests incrémentaux et rollback préparé",
                "Documentation obsolète": "Mise à jour systématique"
            },
            "success_criteria": [
                "Tous repositories renommés selon convention Panini-*",
                "Panini comme parent avec submodules organisés",
                "Toute la documentation mise à jour",
                "Tests de fonctionnement réussis",
                "Écosystème cohérent et navigable"
            ]
        }
        
        return full_plan
    
    def save_plan(self, plan: Dict):
        """Sauvegarder le plan complet"""
        plan_path = Path(self.plan_file)
        
        with open(plan_path, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Plan sauvegardé : {plan_path}")
        
        # Créer aussi un résumé markdown
        self.create_plan_summary(plan)
    
    def create_plan_summary(self, plan: Dict):
        """Créer un résumé Markdown du plan"""
        summary_file = f"PLAN_REDRESSEMENT_ARCHITECTURAL_{self.timestamp}.md"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("# 🏗️ PLAN DE REDRESSEMENT ARCHITECTURAL PANINI\n\n")
            f.write(f"**Créé le :** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 📊 État Actuel\n\n")
            f.write(f"- **Total repositories :** {plan['current_state']['total_repos']}\n")
            f.write(f"- **Repository parent :** {plan['current_state']['parent_repo']}\n\n")
            
            f.write("### Repositories à renommer :\n")
            for repo_name, info in plan['current_state']['repositories'].items():
                if info['target_name'] and info['target_name'] != repo_name:
                    f.write(f"- `{repo_name}` → `{info['target_name']}`\n")
            
            f.write("\n## 🎯 Architecture Cible\n\n")
            f.write("```\nPanini (Parent principal)\n")
            for category, modules in plan['target_architecture']['submodules'].items():
                f.write(f"├── {category}/\n")
                for module_name, module_info in modules.items():
                    f.write(f"│   ├── {module_name} → {module_info['path']}\n")
            f.write("```\n\n")
            
            f.write("## 📋 Phases de Migration\n\n")
            for phase in plan['migration_phases']:
                f.write(f"### Phase {phase['phase']}: {phase['name']}\n")
                f.write(f"**Durée estimée :** {phase['duration']}\n")
                f.write(f"**Risque :** {phase['risk']}\n\n")
                f.write("**Actions :**\n")
                for action in phase['actions']:
                    f.write(f"- {action}\n")
                f.write("\n")
        
        print(f"📄 Résumé créé : {summary_file}")


def main():
    """Point d'entrée principal"""
    print("🏗️ PLANIFICATEUR REDRESSEMENT ARCHITECTURAL PANINI")
    print("==================================================")
    print("Objectif : Réorganiser l'écosystème avec Panini comme parent principal")
    print()
    
    planner = PaniniArchitecturalRedressing()
    plan = planner.generate_full_plan()
    planner.save_plan(plan)
    
    print("\n🎯 ÉTAPES SUIVANTES RECOMMANDÉES :")
    print("1. Réviser le plan généré")
    print("2. Tester le script de renommage sur un repository de test")
    print("3. Exécuter phase par phase avec validation")
    print("4. Maintenir communication pendant transition")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)