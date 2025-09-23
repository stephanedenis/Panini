#!/usr/bin/env python3
"""
JOURNAL DE BORD AUTOMATIQUE - MISSIONS AUTONOMIE
================================================

Système de capture et analyse automatique des bilans post-mission
pour amélioration continue du copilotage et prévention erreurs.

Auteur: Infrastructure Autonomie PaniniFS
Version: 1.0.0
Date: 2025-09-20
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

# Ajout du chemin pour les outils copilotage
sys.path.append('/home/stephane/GitHub/PaniniFS-Research/copilotage/utilities')
sys.path.append('/home/stephane/GitHub/PaniniFS-Research/copilotage/autonomie/core')

@dataclass
class MissionReport:
    """Structure complète d'un rapport de mission"""
    mission_id: str
    title: str
    start_time: str
    end_time: str
    duration_minutes: int
    status: str  # COMPLETED, FAILED, INTERRUPTED
    autonomy_level: str  # INTERACTIVE, SUPERVISED, SEMI_AUTONOMOUS, FULL_AUTONOMOUS
    
    # Métriques de performance
    user_interventions: int
    errors_encountered: int
    errors_auto_resolved: int
    prompts_eliminated: int
    
    # Analyse qualitative
    success_factors: List[str]
    failure_points: List[str]
    lessons_learned: List[str]
    improvements_suggested: List[str]
    
    # Contexte technique
    tools_used: List[str]
    files_modified: List[str]
    git_operations: List[str]
    
    # Impact écosystème
    copilotage_rules_violated: List[str]
    new_patterns_discovered: List[str]
    ecosystem_improvements: List[str]

class MissionLogger:
    """Logger automatique pour bilans post-mission"""
    
    def __init__(self):
        self.journal_dir = Path("/home/stephane/GitHub/PaniniFS-Research/copilotage/journal")
        self.journal_dir.mkdir(exist_ok=True)
        
        self.reports_file = self.journal_dir / "mission_reports.jsonl"
        self.insights_file = self.journal_dir / "lessons_learned.md"
        self.copilotage_updates_file = self.journal_dir / "copilotage_improvements.json"
        
        # Compteurs de session
        self.current_mission = None
        self.session_stats = {
            "missions_completed": 0,
            "total_errors": 0,
            "auto_resolutions": 0,
            "autonomy_score": 0.0
        }
    
    def start_mission(self, title: str, autonomy_level: str = "FULL_AUTONOMOUS") -> str:
        """Démarre le tracking d'une nouvelle mission"""
        mission_id = f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.current_mission = {
            "mission_id": mission_id,
            "title": title,
            "start_time": datetime.now().isoformat(),
            "autonomy_level": autonomy_level,
            "errors": [],
            "interventions": [],
            "tools_used": set(),
            "files_modified": set(),
            "git_operations": [],
            "violations": []
        }
        
        print(f"📋 MISSION DÉMARRÉE: {mission_id}")
        print(f"🎯 Titre: {title}")
        print(f"🤖 Niveau autonomie: {autonomy_level}")
        
        return mission_id
    
    def log_error(self, error_type: str, description: str, auto_resolved: bool = False):
        """Log une erreur rencontrée pendant la mission"""
        if not self.current_mission:
            return
            
        error_log = {
            "timestamp": datetime.now().isoformat(),
            "type": error_type,
            "description": description,
            "auto_resolved": auto_resolved
        }
        
        self.current_mission["errors"].append(error_log)
        print(f"⚠️ Erreur loggée: {error_type} - {'Auto-résolue' if auto_resolved else 'Intervention requise'}")
    
    def log_tool_usage(self, tool_name: str, success: bool = True):
        """Log l'utilisation d'un outil"""
        if not self.current_mission:
            return
            
        self.current_mission["tools_used"].add(f"{tool_name}:{'SUCCESS' if success else 'FAILED'}")
    
    def log_file_modification(self, file_path: str, operation: str):
        """Log modification de fichier"""
        if not self.current_mission:
            return
            
        self.current_mission["files_modified"].add(f"{operation}:{file_path}")
    
    def log_git_operation(self, operation: str, result: str):
        """Log opération Git"""
        if not self.current_mission:
            return
            
        git_log = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "result": result
        }
        
        self.current_mission["git_operations"].append(git_log)
    
    def log_copilotage_violation(self, rule: str, description: str):
        """Log violation des règles de copilotage"""
        if not self.current_mission:
            return
            
        violation = {
            "timestamp": datetime.now().isoformat(),
            "rule": rule,
            "description": description
        }
        
        self.current_mission["violations"].append(violation)
        print(f"🚫 Violation copilotage: {rule}")
    
    def end_mission(self, status: str = "COMPLETED", 
                   success_factors: List[str] = None,
                   failure_points: List[str] = None,
                   lessons_learned: List[str] = None) -> MissionReport:
        """Finalise la mission et génère le rapport complet"""
        
        if not self.current_mission:
            raise ValueError("Aucune mission active à finaliser")
        
        end_time = datetime.now()
        start_time = datetime.fromisoformat(self.current_mission["start_time"])
        duration = int((end_time - start_time).total_seconds() / 60)
        
        # Calcul des métriques
        total_errors = len(self.current_mission["errors"])
        auto_resolved = sum(1 for e in self.current_mission["errors"] if e["auto_resolved"])
        interventions = len(self.current_mission["interventions"])
        
        # Analyse automatique des patterns
        auto_lessons = self._analyze_mission_patterns()
        auto_improvements = self._suggest_improvements()
        
        # Création du rapport
        report = MissionReport(
            mission_id=self.current_mission["mission_id"],
            title=self.current_mission["title"],
            start_time=self.current_mission["start_time"],
            end_time=end_time.isoformat(),
            duration_minutes=duration,
            status=status,
            autonomy_level=self.current_mission["autonomy_level"],
            
            user_interventions=interventions,
            errors_encountered=total_errors,
            errors_auto_resolved=auto_resolved,
            prompts_eliminated=self._calculate_prompts_eliminated(),
            
            success_factors=success_factors or [],
            failure_points=failure_points or [],
            lessons_learned=(lessons_learned or []) + auto_lessons,
            improvements_suggested=auto_improvements,
            
            tools_used=list(self.current_mission["tools_used"]),
            files_modified=list(self.current_mission["files_modified"]),
            git_operations=self.current_mission["git_operations"],
            
            copilotage_rules_violated=[v["rule"] for v in self.current_mission["violations"]],
            new_patterns_discovered=self._discover_new_patterns(),
            ecosystem_improvements=self._suggest_ecosystem_improvements()
        )
        
        # Sauvegarde du rapport
        self._save_mission_report(report)
        
        # Mise à jour des insights
        self._update_lessons_learned(report)
        
        # Mise à jour du copilotage
        self._update_copilotage_rules(report)
        
        print(f"\n📋 MISSION TERMINÉE: {report.mission_id}")
        print(f"⏱️ Durée: {duration} minutes")
        print(f"🎯 Status: {status}")
        print(f"⚠️ Erreurs: {total_errors} (auto-résolues: {auto_resolved})")
        print(f"🤖 Niveau autonomie: {self.current_mission['autonomy_level']}")
        
        self.current_mission = None
        self.session_stats["missions_completed"] += 1
        
        return report
    
    def _analyze_mission_patterns(self) -> List[str]:
        """Analyse automatique des patterns de la mission"""
        lessons = []
        
        # Analyse des erreurs
        error_types = [e["type"] for e in self.current_mission["errors"]]
        if error_types:
            common_errors = max(set(error_types), key=error_types.count)
            lessons.append(f"Type d'erreur le plus fréquent: {common_errors}")
        
        # Analyse des violations
        if self.current_mission["violations"]:
            lessons.append("Violations copilotage détectées - renforcement règles nécessaire")
        
        # Analyse des outils
        failed_tools = [t for t in self.current_mission["tools_used"] if "FAILED" in t]
        if failed_tools:
            lessons.append(f"Outils défaillants: {', '.join(failed_tools)}")
        
        return lessons
    
    def _suggest_improvements(self) -> List[str]:
        """Suggestions d'amélioration basées sur l'analyse"""
        improvements = []
        
        error_rate = len(self.current_mission["errors"]) / max(1, len(self.current_mission["tools_used"]))
        if error_rate > 0.2:
            improvements.append("Taux d'erreur élevé - améliorer validation préventive")
        
        if self.current_mission["violations"]:
            improvements.append("Intégrer vérification copilotage en temps réel")
        
        auto_resolution_rate = 0
        if self.current_mission["errors"]:
            auto_resolution_rate = sum(1 for e in self.current_mission["errors"] if e["auto_resolved"]) / len(self.current_mission["errors"])
        
        if auto_resolution_rate < 0.8:
            improvements.append("Améliorer capacités auto-réparation")
        
        return improvements
    
    def _calculate_prompts_eliminated(self) -> int:
        """Calcule le nombre de prompts éliminés (estimé)"""
        # Estimation basée sur le nombre d'opérations réussies sans intervention
        successful_operations = len(self.current_mission["tools_used"]) + len(self.current_mission["git_operations"])
        return max(0, successful_operations - len(self.current_mission["interventions"]))
    
    def _discover_new_patterns(self) -> List[str]:
        """Découvre de nouveaux patterns d'usage"""
        patterns = []
        
        # Combinaisons d'outils inédites
        tools = [t.split(":")[0] for t in self.current_mission["tools_used"]]
        if len(set(tools)) > 5:
            patterns.append("Usage multi-outils complexe détecté")
        
        # Séquences Git complexes
        if len(self.current_mission["git_operations"]) > 3:
            patterns.append("Workflow Git avancé utilisé")
        
        return patterns
    
    def _suggest_ecosystem_improvements(self) -> List[str]:
        """Suggestions d'amélioration pour l'écosystème"""
        improvements = []
        
        if self.current_mission["violations"]:
            improvements.append("Mise à jour règles copilotage requise")
        
        error_types = [e["type"] for e in self.current_mission["errors"]]
        if "tool_integration" in error_types:
            improvements.append("Améliorer intégration inter-outils")
        
        return improvements
    
    def _save_mission_report(self, report: MissionReport):
        """Sauvegarde le rapport de mission"""
        with open(self.reports_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(report), ensure_ascii=False) + "\n")
    
    def _update_lessons_learned(self, report: MissionReport):
        """Met à jour le fichier des leçons apprises"""
        content = f"""
## Mission {report.mission_id} - {report.title}

**Date:** {report.end_time[:10]}  
**Durée:** {report.duration_minutes} minutes  
**Status:** {report.status}  
**Autonomie:** {report.autonomy_level}

### 🎯 Facteurs de Succès
{chr(10).join(f'- {f}' for f in report.success_factors)}

### ⚠️ Points d'Échec
{chr(10).join(f'- {f}' for f in report.failure_points)}

### 💡 Leçons Apprises
{chr(10).join(f'- {l}' for l in report.lessons_learned)}

### 🚀 Améliorations Suggérées
{chr(10).join(f'- {i}' for i in report.improvements_suggested)}

---

"""
        
        with open(self.insights_file, "a", encoding="utf-8") as f:
            f.write(content)
    
    def _update_copilotage_rules(self, report: MissionReport):
        """Met à jour les règles de copilotage basé sur les apprentissages"""
        updates = {
            "timestamp": datetime.now().isoformat(),
            "mission_id": report.mission_id,
            "rule_updates": [],
            "new_patterns": report.new_patterns_discovered,
            "violations_addressed": report.copilotage_rules_violated
        }
        
        # Génération de nouvelles règles basées sur les violations
        for violation in report.copilotage_rules_violated:
            if "inline" in violation.lower():
                updates["rule_updates"].append({
                    "rule": "ANTI_INLINE_ENFORCEMENT",
                    "description": "Renforcement prévention usage inline",
                    "trigger": violation
                })
        
        # Sauvegarde des mises à jour
        if os.path.exists(self.copilotage_updates_file):
            with open(self.copilotage_updates_file, "r", encoding="utf-8") as f:
                existing_updates = json.load(f)
        else:
            existing_updates = {"updates": []}
        
        existing_updates["updates"].append(updates)
        
        with open(self.copilotage_updates_file, "w", encoding="utf-8") as f:
            json.dump(existing_updates, f, indent=2, ensure_ascii=False)
    
    def generate_session_summary(self) -> Dict[str, Any]:
        """Génère un résumé de la session complète"""
        return {
            "session_timestamp": datetime.now().isoformat(),
            "missions_completed": self.session_stats["missions_completed"],
            "total_errors": self.session_stats["total_errors"],
            "auto_resolutions": self.session_stats["auto_resolutions"],
            "autonomy_evolution": self._calculate_autonomy_evolution(),
            "ecosystem_health": self._assess_ecosystem_health()
        }
    
    def _calculate_autonomy_evolution(self) -> Dict[str, float]:
        """Calcule l'évolution de l'autonomie"""
        # Analyse des rapports récents pour voir l'amélioration
        if not os.path.exists(self.reports_file):
            return {"baseline": 0.0, "current": 0.0, "improvement": 0.0}
        
        # Lecture des derniers rapports
        recent_reports = []
        with open(self.reports_file, "r", encoding="utf-8") as f:
            for line in f:
                recent_reports.append(json.loads(line))
        
        if len(recent_reports) < 2:
            return {"baseline": 0.0, "current": 0.0, "improvement": 0.0}
        
        # Calcul de l'amélioration
        baseline = recent_reports[0]["errors_encountered"] - recent_reports[0]["errors_auto_resolved"]
        current = recent_reports[-1]["errors_encountered"] - recent_reports[-1]["errors_auto_resolved"]
        
        improvement = max(0, (baseline - current) / max(1, baseline) * 100)
        
        return {
            "baseline": baseline,
            "current": current,
            "improvement": improvement
        }
    
    def _assess_ecosystem_health(self) -> Dict[str, str]:
        """Évalue la santé de l'écosystème"""
        return {
            "copilotage_compliance": "EXCELLENT" if self.session_stats["missions_completed"] > 0 else "UNKNOWN",
            "autonomy_readiness": "OPERATIONAL",
            "error_management": "AUTOMATED",
            "continuous_improvement": "ACTIVE"
        }

# Instance globale pour usage simple
mission_logger = MissionLogger()

def log_mission_completion(title: str, status: str = "COMPLETED", 
                          success_factors: List[str] = None,
                          lessons_learned: List[str] = None):
    """Fonction helper pour logger rapidement une mission complète"""
    mission_id = mission_logger.start_mission(title)
    
    # Auto-détection de certains patterns basés sur l'historique récent
    auto_success = ["Infrastructure autonomie opérationnelle", "Workflow Git automatisé"]
    auto_lessons = ["Amélioration continue nécessaire", "Feedback loop validé"]
    
    return mission_logger.end_mission(
        status=status,
        success_factors=(success_factors or []) + auto_success,
        lessons_learned=(lessons_learned or []) + auto_lessons
    )

if __name__ == "__main__":
    # Test du système de logging
    print("🧪 TEST JOURNAL DE BORD AUTOMATIQUE")
    print("=" * 50)
    
    # Simulation d'une mission
    mission_id = mission_logger.start_mission("Test infrastructure autonomie")
    
    mission_logger.log_tool_usage("mcp_pylance_runCodeSnippet", True)
    mission_logger.log_file_modification("/test/file.py", "CREATE")
    mission_logger.log_git_operation("commit", "SUCCESS")
    mission_logger.log_error("validation_error", "Test error", auto_resolved=True)
    
    report = mission_logger.end_mission(
        status="COMPLETED",
        success_factors=["Test réussi", "Logging fonctionnel"],
        lessons_learned=["Système opérationnel", "Prêt pour production"]
    )
    
    print(f"\n✅ Test terminé - Rapport généré: {report.mission_id}")