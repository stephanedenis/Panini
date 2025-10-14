#!/usr/bin/env python3
"""
INTÉGRATEUR SYSTÈMES VALIDATION & QUALITÉ
========================================

Intégration des systèmes de validation continue et framework qualité
pour un processus unifié de développement et amélioration PanLang.

Objectif: Pipeline automatique validation → analyse → amélioration → validation
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

# Imports des systèmes
from systeme_validation_continue import ContinuousValidationSystem
from framework_criteres_qualite import PanLangQualityFramework

@dataclass
class IntegratedReport:
    """Rapport intégré validation + qualité"""
    timestamp: str
    validation_results: Dict[str, Any]
    quality_assessment: Dict[str, Any]
    integrated_score: float
    priority_actions: List[str]
    improvement_roadmap: Dict[str, Any]
    next_validation_trigger: str

class IntegratedValidationQualitySystem:
    """Système intégré validation continue + framework qualité"""
    
    def __init__(self):
        self.workspace_path = Path("/home/stephane/GitHub/PaniniFS-Research")
        self.integration_dir = self.workspace_path / "validation_integree"
        self.integration_dir.mkdir(exist_ok=True)
        
        # Initialisation sous-systèmes
        self.validator = ContinuousValidationSystem()
        self.quality_framework = PanLangQualityFramework()
        
        # Correction poids framework qualité
        self._fix_quality_framework_weights()
        
        # Historique intégré
        self.integrated_history = self.integration_dir / "historique_integre.jsonl"
        self.reports_dir = self.integration_dir / "rapports"
        self.reports_dir.mkdir(exist_ok=True)
    
    def _fix_quality_framework_weights(self):
        """Corrige les poids du framework qualité pour sommer à 1.0"""
        
        total_weight = sum(c.weight for c in self.quality_framework.quality_criteria.values())
        correction_factor = 1.0 / total_weight
        
        print(f"🔧 CORRECTION POIDS: facteur {correction_factor:.3f}")
        
        for criterion in self.quality_framework.quality_criteria.values():
            criterion.weight *= correction_factor
        
        # Vérification
        new_total = sum(c.weight for c in self.quality_framework.quality_criteria.values())
        print(f"✅ Nouveau total poids: {new_total:.6f}")
    
    def run_integrated_validation(self, trigger: str = "manual") -> IntegratedReport:
        """Exécute validation intégrée complète"""
        
        print("🔄 VALIDATION INTÉGRÉE PANLANG")
        print("=" * 35)
        
        timestamp = datetime.now().isoformat()
        
        # 1. Validation continue technique
        print("📊 Phase 1: Validation continue...")
        validation_metrics = self.validator.validate_current_architecture(trigger)
        
        # 2. Évaluation qualité framework
        print("\n🎯 Phase 2: Évaluation framework qualité...")
        
        # Récupération modèle actuel
        current_model = self.quality_framework.benchmark_models["panlang_panksepp_actuel"]
        quality_assessment = self.quality_framework.evaluate_model_candidate(current_model)
        
        # 3. Intégration scores
        print("\n🔗 Phase 3: Intégration résultats...")
        integrated_score = self._calculate_integrated_score(validation_metrics, quality_assessment)
        
        # 4. Analyse priorités
        priority_actions = self._analyze_integrated_priorities(validation_metrics, quality_assessment)
        
        # 5. Roadmap amélioration
        improvement_roadmap = self._generate_integrated_roadmap(validation_metrics, quality_assessment)
        
        # 6. Déclencheur suivant
        next_trigger = self._determine_next_trigger(integrated_score, improvement_roadmap)
        
        # Création rapport intégré
        integrated_report = IntegratedReport(
            timestamp=timestamp,
            validation_results=asdict(validation_metrics),
            quality_assessment=asdict(quality_assessment),
            integrated_score=integrated_score,
            priority_actions=priority_actions,
            improvement_roadmap=improvement_roadmap,
            next_validation_trigger=next_trigger
        )
        
        # Sauvegarde et affichage
        self._save_integrated_report(integrated_report)
        self._display_integrated_results(integrated_report)
        
        return integrated_report
    
    def _calculate_integrated_score(self, validation_metrics, quality_assessment) -> float:
        """Calcule score intégré validation + qualité"""
        
        # Score validation continue (0.764 actuel)
        validation_score = validation_metrics.overall_quality_score
        
        # Score qualité framework (normalisé à 1.0)
        quality_score = min(1.0, quality_assessment.overall_score)
        
        # Moyenne pondérée (60% technique, 40% qualité)
        integrated_score = validation_score * 0.6 + quality_score * 0.4
        
        return integrated_score
    
    def _analyze_integrated_priorities(self, validation_metrics, quality_assessment) -> List[str]:
        """Analyse priorités intégrées"""
        
        priorities = []
        
        # Priorités validation continue
        if validation_metrics.multilingual_coverage < 0.6:
            priorities.append("CRITIQUE: Étendre corpus multilingue (couverture 50%)")
        
        if validation_metrics.cross_linguistic_consistency < 0.75:
            priorities.append("HAUTE: Améliorer consistance inter-lingue (70%)")
        
        if validation_metrics.semantic_precision < 0.85:
            priorities.append("HAUTE: Affiner précision sémantique (88.1%)")
        
        # Priorités framework qualité  
        quality_gaps = []
        for criterion_name, score in quality_assessment.criterion_scores.items():
            criterion = self.quality_framework.quality_criteria[criterion_name]
            if score < criterion.target_value - 0.05:
                gap = criterion.target_value - score
                weight = criterion.weight
                quality_gaps.append((gap * weight, criterion_name, criterion.name, gap))
        
        quality_gaps.sort(reverse=True)
        
        for weighted_gap, criterion_key, criterion_name, gap in quality_gaps[:3]:
            priorities.append(f"QUALITÉ: {criterion_name} (écart {gap:.3f})")
        
        return priorities[:8]  # Top 8 priorités
    
    def _generate_integrated_roadmap(self, validation_metrics, quality_assessment) -> Dict[str, Any]:
        """Génère roadmap intégrée"""
        
        current_integrated = self._calculate_integrated_score(validation_metrics, quality_assessment)
        
        # Objectifs par domaine
        validation_targets = {
            'multilingual_coverage': 0.85,
            'semantic_precision': 0.90,
            'cross_linguistic_consistency': 0.85,
            'creative_generation_score': 0.80
        }
        
        quality_targets = {
            'universalite_linguistique': 0.90,
            'precision_semantique': 0.92,
            'contraintes_cognitives': 0.95
        }
        
        # Timeline basée sur écarts
        total_validation_gap = sum(
            max(0, target - getattr(validation_metrics, field))
            for field, target in validation_targets.items()
        )
        
        total_quality_gap = sum(
            max(0, target - quality_assessment.criterion_scores.get(field, 0.5))
            for field, target in quality_targets.items()
        )
        
        if total_validation_gap + total_quality_gap < 0.3:
            timeline = "2-3 semaines"
            effort = "Optimisation fine"
        elif total_validation_gap + total_quality_gap < 0.6:
            timeline = "1-2 mois"  
            effort = "Améliorations ciblées"
        else:
            timeline = "2-3 mois"
            effort = "Développements majeurs"
        
        roadmap = {
            'current_integrated_score': current_integrated,
            'target_integrated_score': 0.90,
            'estimated_timeline': timeline,
            'effort_level': effort,
            'validation_priorities': validation_targets,
            'quality_priorities': quality_targets,
            'success_criteria': [
                'Score intégré > 0.90',
                'Couverture multilingue > 85%',
                'Précision sémantique > 90%',
                'Tous critères qualité au-dessus seuils'
            ]
        }
        
        return roadmap
    
    def _determine_next_trigger(self, integrated_score: float, roadmap: Dict[str, Any]) -> str:
        """Détermine déclencheur validation suivante"""
        
        if integrated_score < 0.7:
            return "architecture_critical_improvement"
        elif integrated_score < 0.8:
            return "targeted_improvements"
        else:
            return "optimization_cycle"
    
    def _save_integrated_report(self, report: IntegratedReport):
        """Sauvegarde rapport intégré"""
        
        # Historique JSONL
        with open(self.integrated_history, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(report), ensure_ascii=False) + '\n')
        
        # Rapport détaillé
        timestamp_str = report.timestamp.replace(':', '-').replace('T', '_')[:19]
        detailed_report_path = self.reports_dir / f"rapport_integre_{timestamp_str}.json"
        
        with open(detailed_report_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(report), f, indent=2, ensure_ascii=False)
        
        # Rapport Markdown lisible
        md_report_path = self.reports_dir / f"rapport_integre_{timestamp_str}.md"
        self._generate_markdown_report(report, md_report_path)
    
    def _generate_markdown_report(self, report: IntegratedReport, output_path: Path):
        """Génère rapport Markdown lisible"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# RAPPORT VALIDATION INTÉGRÉE PANLANG\n\n")
            f.write(f"**Timestamp:** {report.timestamp}  \n")
            f.write(f"**Score Intégré:** {report.integrated_score:.3f}  \n")
            f.write(f"**Prochain Déclencheur:** {report.next_validation_trigger}  \n\n")
            
            f.write(f"## 📊 VALIDATION TECHNIQUE\n\n")
            validation = report.validation_results
            f.write(f"- **Score Global:** {validation['overall_quality_score']:.3f}\n")
            f.write(f"- **Couverture Multilingue:** {validation['multilingual_coverage']:.3f}\n")
            f.write(f"- **Précision Sémantique:** {validation['semantic_precision']:.3f}\n")
            f.write(f"- **Cohérence Compositionnelle:** {validation['compositional_coherence']:.3f}\n\n")
            
            f.write(f"## 🎯 ÉVALUATION QUALITÉ\n\n")
            quality = report.quality_assessment
            f.write(f"- **Score Global:** {quality['overall_score']:.3f}\n")
            f.write(f"- **Forces:** {len(quality.get('strengths', []))}\n")
            f.write(f"- **Faiblesses:** {len(quality.get('weaknesses', []))}\n\n")
            
            f.write(f"## 🚀 PRIORITÉS D'ACTION\n\n")
            for i, action in enumerate(report.priority_actions, 1):
                f.write(f"{i}. {action}\n")
            f.write(f"\n")
            
            f.write(f"## 🗺️ ROADMAP AMÉLIORATION\n\n")
            roadmap = report.improvement_roadmap
            f.write(f"- **Timeline:** {roadmap['estimated_timeline']}\n")
            f.write(f"- **Effort:** {roadmap['effort_level']}\n")
            f.write(f"- **Score Cible:** {roadmap['target_integrated_score']:.3f}\n\n")
    
    def _display_integrated_results(self, report: IntegratedReport):
        """Affiche résultats intégrés"""
        
        print(f"\n🎊 RÉSULTATS VALIDATION INTÉGRÉE")
        print("=" * 40)
        
        print(f"🏆 Score Intégré: {report.integrated_score:.3f}")
        
        if report.integrated_score >= 0.9:
            level = "EXCELLENCE ⭐⭐⭐⭐"
        elif report.integrated_score >= 0.8:
            level = "TRÈS BON ⭐⭐⭐"
        elif report.integrated_score >= 0.7:
            level = "BON ⭐⭐"
        else:
            level = "À AMÉLIORER ⭐"
        
        print(f"🎖️ Niveau: {level}")
        
        print(f"\n🚨 TOP PRIORITÉS:")
        for i, priority in enumerate(report.priority_actions[:5], 1):
            print(f"   {i}. {priority}")
        
        print(f"\n🗺️ ROADMAP:")
        roadmap = report.improvement_roadmap
        print(f"   ⏱️ Timeline: {roadmap['estimated_timeline']}")
        print(f"   🎯 Score cible: {roadmap['target_integrated_score']:.3f}")
        print(f"   📈 Écart: {roadmap['target_integrated_score'] - report.integrated_score:.3f}")
        
        print(f"\n🔄 Prochain déclencheur: {report.next_validation_trigger}")
    
    def monitor_continuous_improvement(self, iterations: int = 5) -> List[IntegratedReport]:
        """Monitoring amélioration continue"""
        
        print("🔄 MONITORING AMÉLIORATION CONTINUE")
        print("=" * 40)
        
        reports = []
        
        for i in range(iterations):
            print(f"\n📋 ITÉRATION {i+1}/{iterations}")
            
            trigger = "continuous_monitoring" if i > 0 else "baseline"
            report = self.run_integrated_validation(trigger)
            
            reports.append(report)
            
            # Simulation amélioration (en réalité, changements seraient appliqués)
            if i < iterations - 1:
                print(f"⏳ Simulation application améliorations...")
                time.sleep(2)  # Simulation travail
        
        # Analyse évolution
        self._analyze_improvement_trajectory(reports)
        
        return reports
    
    def _analyze_improvement_trajectory(self, reports: List[IntegratedReport]):
        """Analyse trajectoire d'amélioration"""
        
        print(f"\n📈 ANALYSE TRAJECTOIRE AMÉLIORATION")
        print("=" * 40)
        
        scores = [r.integrated_score for r in reports]
        
        if len(scores) >= 2:
            initial_score = scores[0]
            final_score = scores[-1]
            improvement = final_score - initial_score
            
            print(f"📊 Score initial: {initial_score:.3f}")
            print(f"📊 Score final: {final_score:.3f}")
            print(f"📈 Amélioration: {improvement:+.3f}")
            
            if improvement > 0.05:
                trend = "EXCELLENT - Amélioration forte ⭐⭐⭐"
            elif improvement > 0.02:
                trend = "BON - Amélioration modérée ⭐⭐"
            elif improvement > 0.00:
                trend = "FAIBLE - Amélioration marginale ⭐"
            else:
                trend = "STAGNANT - Révision stratégie nécessaire ⚠️"
            
            print(f"🎯 Tendance: {trend}")

def main():
    """Système principal intégré"""
    
    print("🚀 INITIALISATION SYSTÈME INTÉGRÉ VALIDATION & QUALITÉ")
    print("=" * 60)
    
    # Création système intégré
    integrated_system = IntegratedValidationQualitySystem()
    
    # Validation intégrée baseline
    baseline_report = integrated_system.run_integrated_validation("system_baseline")
    
    print(f"\n💾 SYSTÈME INTÉGRÉ OPÉRATIONNEL")
    print(f"📁 Répertoire: {integrated_system.integration_dir}")
    print(f"📊 Historique: {integrated_system.integrated_history}")
    print(f"📋 Rapports: {integrated_system.reports_dir}")
    
    print(f"\n✨ PROCESSUS DE TRAVAIL ÉTABLI:")
    print(f"   1. Modifications modèle → Validation automatique")
    print(f"   2. Évaluation qualité → Identification lacunes")
    print(f"   3. Roadmap intégrée → Priorisation améliorations")
    print(f"   4. Application améliorations → Nouvelle validation")
    
    return integrated_system, baseline_report

if __name__ == "__main__":
    main()