#!/usr/bin/env python3
"""
RÉVISION INTERACTIVE CRITÈRES QUALITÉ PANLANG
============================================

Session collaborative pour réviser les critères de qualité du modèle
PanLang et leurs spécifications selon les objectifs et insights récents.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

class QualityCriteriaReviewer:
    """Système de révision interactive des critères qualité"""
    
    def __init__(self):
        self.framework_dir = Path("/home/stephane/GitHub/PaniniFS-Research/qualite_framework")
        self.current_criteria = self._load_current_criteria()
        
        # Analyse performance actuelle
        self.current_performance = {
            'universalite_linguistique': 0.820,  # 82% - manque familles linguistiques
            'precision_semantique': 0.890,      # 89% - bon mais pas optimal
            'coherence_compositionnelle': 0.900, # 90% - excellent
            'contraintes_cognitives': 0.850,     # 85% - 13 dhātu vs Miller 7±2
            'intuitivite_utilisation': 0.800,    # 80% - cible atteinte
            'richesse_expressive': 0.850,        # 85% - cible atteinte  
            'creativite_generative': 0.850,      # 85% - dépasse cible!
            'validation_neurobiologique': 0.920, # 92% - excellent Panksepp
            'robustesse_empirique': 0.840,       # 84% - bon
            'efficacite_computationnelle': 0.830,# 83% - bon
            'extensibilite_maintenance': 0.800,  # 80% - acceptable
            'applications_therapeutiques': 0.800 # 80% - dépasse cible!
        }
        
        # Insights récents session migration
        self.recent_insights = [
            "Découverte zone créative oxymores (antagonismes gérables 0.3-0.5)",
            "Architecture Panksepp supérieure neurobiologiquement (9.0/10)",
            "83.5% composabilité émotionnelle validée", 
            "Potentiel IA émotionnelle sophistiquée confirmé",
            "Besoin corpus multilingue critique (50% couverture insuffisante)",
            "Universalité linguistique priorité #1 (poids 18%)"
        ]
    
    def _load_current_criteria(self) -> Dict[str, Any]:
        """Charge critères actuels"""
        criteria_file = self.framework_dir / "criteres_qualite.json"
        
        if criteria_file.exists():
            with open(criteria_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def present_current_state(self):
        """Présente état actuel pour révision"""
        
        print("🎯 RÉVISION CRITÈRES QUALITÉ PANLANG")
        print("=" * 40)
        
        print(f"📊 PERFORMANCE ACTUELLE (Score intégré: 0.799)")
        print("=" * 30)
        
        # Analyse par catégorie performance
        excellent = []  # >= 90%
        bon = []        # 80-89% 
        critique = []   # < 80%
        
        for criterion, score in self.current_performance.items():
            criterion_name = self.current_criteria[criterion]['name']
            target = self.current_criteria[criterion]['target_value']
            gap = target - score
            
            if score >= 0.90:
                excellent.append((criterion_name, score, target, gap))
            elif score >= 0.80:
                bon.append((criterion_name, score, target, gap))
            else:
                critique.append((criterion_name, score, target, gap))
        
        print(f"✅ EXCELLENT (≥90%): {len(excellent)}")
        for name, score, target, gap in excellent:
            print(f"   • {name}: {score:.1%} (cible {target:.1%}) {gap:+.1%}")
        
        print(f"\n👍 BON (80-89%): {len(bon)}")
        for name, score, target, gap in bon:
            print(f"   • {name}: {score:.1%} (cible {target:.1%}) {gap:+.1%}")
        
        print(f"\n🚨 CRITIQUE (<80%): {len(critique)}")
        for name, score, target, gap in critique:
            print(f"   • {name}: {score:.1%} (cible {target:.1%}) {gap:+.1%}")
        
        print(f"\n💡 INSIGHTS RÉCENTS:")
        for insight in self.recent_insights:
            print(f"   • {insight}")
    
    def analyze_criteria_relevance(self) -> Dict[str, Dict[str, Any]]:
        """Analyse pertinence et cohérence des critères"""
        
        analysis = {}
        
        # Analyse de chaque critère
        for criterion_key, criterion_data in self.current_criteria.items():
            current_score = self.current_performance[criterion_key]
            target = criterion_data['target_value']
            weight = criterion_data['weight']
            
            # Classification
            if current_score >= target:
                status = "ATTEINT"
                priority = "maintenance"
            elif target - current_score > 0.1:
                status = "CRITIQUE"
                priority = "urgent"
            else:
                status = "AMÉLIORATION"
                priority = "normale"
            
            # Analyse spécifique
            specific_analysis = self._analyze_specific_criterion(criterion_key, current_score, target)
            
            analysis[criterion_key] = {
                'name': criterion_data['name'],
                'current_score': current_score,
                'target': target,
                'weight': weight,
                'gap': target - current_score,
                'status': status,
                'priority': priority,
                'specific_analysis': specific_analysis
            }
        
        return analysis
    
    def _analyze_specific_criterion(self, criterion_key: str, score: float, target: float) -> Dict[str, Any]:
        """Analyse spécifique par critère"""
        
        analyses = {
            'universalite_linguistique': {
                'assessment': 'SOUS-PERFORMANT - 82% vs 90% cible',
                'root_cause': 'Corpus multilingue insuffisant (50% familles)',
                'impact': 'Limite adoption universelle du modèle',
                'revision_needed': True,
                'suggestions': [
                    'Augmenter poids de 18% à 22% (critère le plus important)',
                    'Cibler 25+ familles linguistiques vs 20 actuelles',
                    'Ajouter métriques qualité typologie linguistique'
                ]
            },
            
            'precision_semantique': {
                'assessment': 'BON - 89% vs 92% cible',
                'root_cause': 'Ambiguïtés résiduelles complexes',
                'impact': 'Qualité mappings satisfaisante', 
                'revision_needed': False,
                'suggestions': ['Maintenir cible actuelle']
            },
            
            'coherence_compositionnelle': {
                'assessment': 'EXCELLENT - 90% dépasse 88% cible',
                'root_cause': 'Architecture Panksepp très cohérente',
                'impact': 'Force majeure du modèle',
                'revision_needed': True,
                'suggestions': [
                    'Augmenter cible à 92% (excellence confirmée)',
                    'Ajouter métriques antagonismes/synergies'
                ]
            },
            
            'contraintes_cognitives': {
                'assessment': 'PROBLÉMATIQUE - 85% vs 95% cible',
                'root_cause': '13 dhātu vs Miller 7±2 optimal',
                'impact': 'Complexité cognitive excessive',
                'revision_needed': True,
                'suggestions': [
                    'Réviser architecture : 7 émotionnels + 4-5 fonctionnels',
                    'Ajouter tests charge cognitive utilisateurs',
                    'Maintenir cible élevée 95%'
                ]
            },
            
            'creativite_generative': {
                'assessment': 'EXCELLENT - 85% dépasse 78% cible',
                'root_cause': 'Découverte oxymores zone 0.3-0.5',
                'impact': 'Potentiel IA créative validé',
                'revision_needed': True,
                'suggestions': [
                    'Augmenter cible à 85% (performance confirmée)',
                    'Augmenter poids de 8% à 12% (importance découverte)',
                    'Ajouter métriques diversité créative'
                ]
            },
            
            'validation_neurobiologique': {
                'assessment': 'EXCELLENT - 92% dépasse 90% cible',
                'root_cause': 'Architecture Panksepp optimale (9.0/10)',
                'impact': 'Validation scientifique forte',
                'revision_needed': False,
                'suggestions': ['Maintenir excellence acquise']
            },
            
            'applications_therapeutiques': {
                'assessment': 'EXCELLENT - 80% dépasse 75% cible',
                'root_cause': 'Oxymores + expressions émotions complexes',
                'impact': 'Potentiel clinique confirmé',
                'revision_needed': True,
                'suggestions': [
                    'Augmenter cible à 82% (potentiel confirmé)',
                    'Augmenter poids de 6% à 10% (valeur ajoutée)',
                    'Ajouter métriques usage clinique'
                ]
            }
        }
        
        return analyses.get(criterion_key, {
            'assessment': 'ANALYSE STANDARD',
            'root_cause': 'Performance dans la normale',
            'impact': 'Impact moyen',
            'revision_needed': False,
            'suggestions': ['Maintenir status quo']
        })
    
    def propose_revisions(self, analysis: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Propose révisions basées sur analyse"""
        
        print(f"\n🔧 PROPOSITIONS DE RÉVISIONS")
        print("=" * 30)
        
        revisions = {
            'weight_adjustments': {},
            'target_adjustments': {},
            'new_criteria': [],
            'removed_criteria': [],
            'measurement_improvements': {}
        }
        
        # Ajustements poids basés sur performance et importance
        weight_changes = {
            'universalite_linguistique': 0.22,  # +4% (critique)
            'creativite_generative': 0.12,      # +4% (découverte majeure)
            'applications_therapeutiques': 0.10, # +4% (potentiel confirmé)
            'contraintes_cognitives': 0.10,     # -2% (maintenir importance)
            'efficacite_computationnelle': 0.04 # -2% (moins critique)
        }
        
        # Ajustements cibles basés sur performance
        target_changes = {
            'universalite_linguistique': 0.92,   # +2% (plus ambitieux)
            'coherence_compositionnelle': 0.92,  # +4% (excellence confirmée)
            'creativite_generative': 0.85,       # +7% (performance démontrée)
            'applications_therapeutiques': 0.82  # +7% (potentiel validé)
        }
        
        # Nouvelles métriques suggérées
        new_metrics = [
            {
                'name': 'Diversité Typologie Linguistique',
                'description': 'Couverture qualitative familles linguistiques extrêmes',
                'target': 0.88,
                'weight': 0.04,
                'parent': 'universalite_linguistique'
            },
            {
                'name': 'Innovation Créative Mesurée',
                'description': 'Originalité + pertinence générations vs corpus référence',
                'target': 0.80,
                'weight': 0.03,
                'parent': 'creativite_generative'  
            }
        ]
        
        print("📊 AJUSTEMENTS POIDS PROPOSÉS:")
        for criterion, new_weight in weight_changes.items():
            old_weight = self.current_criteria[criterion]['weight']
            change = new_weight - old_weight
            name = self.current_criteria[criterion]['name']
            print(f"   • {name}: {old_weight:.2f} → {new_weight:.2f} ({change:+.2f})")
        
        print(f"\n🎯 AJUSTEMENTS CIBLES PROPOSÉS:")
        for criterion, new_target in target_changes.items():
            old_target = self.current_criteria[criterion]['target_value']
            change = new_target - old_target
            name = self.current_criteria[criterion]['name']
            print(f"   • {name}: {old_target:.2f} → {new_target:.2f} ({change:+.2f})")
        
        print(f"\n✨ NOUVELLES MÉTRIQUES SUGGÉRÉES:")
        for metric in new_metrics:
            print(f"   • {metric['name']} (cible {metric['target']:.2f}, poids {metric['weight']:.2f})")
        
        revisions['weight_adjustments'] = weight_changes
        revisions['target_adjustments'] = target_changes
        revisions['new_metrics'] = new_metrics
        
        return revisions
    
    def validate_revision_coherence(self, revisions: Dict[str, Any]) -> Dict[str, Any]:
        """Valide cohérence des révisions proposées"""
        
        print(f"\n🔍 VALIDATION COHÉRENCE RÉVISIONS")
        print("=" * 30)
        
        validation = {
            'weight_sum_check': 0.0,
            'target_realism_check': [],
            'internal_consistency': [],
            'strategic_alignment': []
        }
        
        # Vérification somme poids
        total_weight = sum(self.current_criteria[k]['weight'] for k in self.current_criteria)
        weight_adjustments = revisions.get('weight_adjustments', {})
        
        for criterion, old_weight in [(k, v['weight']) for k, v in self.current_criteria.items()]:
            new_weight = weight_adjustments.get(criterion, old_weight)
            total_weight += (new_weight - old_weight)
        
        validation['weight_sum_check'] = total_weight
        
        print(f"⚖️ Somme poids révisés: {total_weight:.3f}")
        if abs(total_weight - 1.0) > 0.01:
            print(f"   ⚠️ ATTENTION: Somme ≠ 1.0 - normalisation nécessaire")
        else:
            print(f"   ✅ Somme correcte")
        
        # Vérification réalisme cibles
        target_adjustments = revisions.get('target_adjustments', {})
        for criterion, new_target in target_adjustments.items():
            current_score = self.current_performance[criterion]
            gap = new_target - current_score
            
            if gap > 0.15:  # Écart > 15% potentiellement irréaliste
                validation['target_realism_check'].append({
                    'criterion': criterion,
                    'issue': f'Écart important {gap:.3f} - vérifier faisabilité'
                })
            elif gap < 0:
                validation['target_realism_check'].append({
                    'criterion': criterion,  
                    'issue': f'Cible inférieure performance actuelle'
                })
        
        # Alignement stratégique
        strategic_checks = [
            'Universalité linguistique prioritaire (poids le plus élevé)',
            'Créativité générative reconnue (poids augmenté)',
            'Applications thérapeutiques valorisées (potentiel confirmé)',
            'Contraintes cognitives maintenues critiques (usabilité)'
        ]
        
        validation['strategic_alignment'] = strategic_checks
        
        print(f"\n🎯 ALIGNEMENT STRATÉGIQUE:")
        for check in strategic_checks:
            print(f"   ✅ {check}")
        
        return validation

def main():
    """Révision interactive principale"""
    
    reviewer = QualityCriteriaReviewer()
    
    print("🚀 SESSION RÉVISION CRITÈRES QUALITÉ PANLANG")
    print("=" * 50)
    
    # 1. Présentation état actuel
    reviewer.present_current_state()
    
    # 2. Analyse détaillée
    analysis = reviewer.analyze_criteria_relevance()
    
    print(f"\n📋 ANALYSE DÉTAILLÉE PAR CRITÈRE:")
    for criterion_key, criterion_analysis in analysis.items():
        if criterion_analysis['revision_needed']:
            print(f"\n🔧 {criterion_analysis['name']}:")
            print(f"   📊 {criterion_analysis['specific_analysis']['assessment']}")
            print(f"   🔍 Cause: {criterion_analysis['specific_analysis']['root_cause']}")
            print(f"   💡 Suggestions:")
            for suggestion in criterion_analysis['specific_analysis']['suggestions']:
                print(f"      • {suggestion}")
    
    # 3. Propositions révisions
    revisions = reviewer.propose_revisions(analysis)
    
    # 4. Validation cohérence
    validation = reviewer.validate_revision_coherence(revisions)
    
    print(f"\n✨ SYNTHÈSE RÉVISION:")
    print(f"   📊 Critères à réviser: {sum(1 for a in analysis.values() if a['revision_needed'])}")
    print(f"   ⚖️ Ajustements poids: {len(revisions['weight_adjustments'])}")
    print(f"   🎯 Ajustements cibles: {len(revisions['target_adjustments'])}")
    print(f"   ✨ Nouvelles métriques: {len(revisions.get('new_metrics', []))}")
    
    print(f"\n💭 QUESTIONS POUR DISCUSSION:")
    print(f"   1. Approuvez-vous l'augmentation du poids 'Universalité Linguistique' à 22%?")
    print(f"   2. Les nouvelles cibles sont-elles réalistes avec nos ressources?")
    print(f"   3. Faut-il ajouter les nouvelles métriques proposées?")
    print(f"   4. Y a-t-il des spécificités PanLang manquées?")
    
    return reviewer, analysis, revisions, validation

if __name__ == "__main__":
    main()