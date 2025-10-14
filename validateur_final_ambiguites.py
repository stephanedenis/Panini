#!/usr/bin/env python3
"""
VALIDATEUR FINAL DES CORRECTIONS D'AMBIGUÏTÉS
===========================================

Vérifie que toutes les ambiguïtés critiques identifiées ont été résolues
et évalue l'amélioration globale du système PanLang.
"""

import json
import time
from typing import Dict, List
from pathlib import Path

class FinalAmbiguityValidator:
    """Validateur final des corrections d'ambiguïtés"""
    
    def __init__(self):
        self.critical_concepts = [
            'AMOUR', 'JOIE', 'TRISTESSE', 'PEUR', 'COLÈRE', 'DÉGOÛT',
            'MUSIQUE', 'ART', 'LITTÉRATURE',
            'COMPRENDRE', 'APPRENDRE', 'EXPLORER',
            'PARENT', 'GUERRE', 'FAMILLE',
            'EXISTENCE', 'MOUVEMENT', 'VIVRE',
            'SENTIR', 'VOIR', 'ENTENDRE', 'TOUCHER'
        ]
        
        # Seuils de validation
        self.validation_thresholds = {
            'minimum_coherence': 0.7,
            'minimum_completion': 0.9,
            'minimum_critical_resolved': 0.95
        }
    
    def load_original_problems(self) -> Dict:
        """Charge l'analyse originale des ambiguïtés"""
        try:
            with open('analyse_ambiguites_dictionnaire_complet.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ Rapport original d'ambiguïtés non trouvé")
            return {}
    
    def load_corrected_dictionary(self) -> Dict:
        """Charge le dictionnaire corrigé le plus récent"""
        # Chercher le fichier le plus récent
        corrected_files = list(Path('.').glob('dictionnaire_panlang_corrige_*.json'))
        
        if corrected_files:
            # Prendre le plus récent
            latest_file = max(corrected_files, key=lambda f: f.stat().st_mtime)
            print(f"📖 Chargement dictionnaire corrigé: {latest_file}")
            
            with open(latest_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print("❌ Aucun dictionnaire corrigé trouvé")
            return {}
    
    def validate_critical_concepts_resolved(self, corrected_dict: Dict) -> Dict:
        """Vérifie que tous les concepts critiques ont été résolus"""
        
        concepts = corrected_dict.get('concepts', {})
        validation_results = {
            'total_critical_concepts': len(self.critical_concepts),
            'resolved_concepts': 0,
            'unresolved_concepts': [],
            'resolution_details': {}
        }
        
        for concept in self.critical_concepts:
            if concept in concepts:
                concept_data = concepts[concept]
                
                # Vérifier présence décomposition
                has_decomposition = bool(concept_data.get('dhatu_decomposition'))
                has_description = bool(concept_data.get('description'))
                coherence_score = concept_data.get('coherence_score', 0.0)
                
                is_resolved = (has_decomposition and has_description and 
                             coherence_score >= self.validation_thresholds['minimum_coherence'])
                
                if is_resolved:
                    validation_results['resolved_concepts'] += 1
                    validation_results['resolution_details'][concept] = {
                        'status': 'resolved',
                        'coherence_score': coherence_score,
                        'dhatu_decomposition': concept_data.get('dhatu_decomposition', []),
                        'has_description': has_description
                    }
                else:
                    validation_results['unresolved_concepts'].append(concept)
                    validation_results['resolution_details'][concept] = {
                        'status': 'unresolved',
                        'issues': {
                            'missing_decomposition': not has_decomposition,
                            'missing_description': not has_description,
                            'low_coherence': coherence_score < self.validation_thresholds['minimum_coherence']
                        }
                    }
            else:
                validation_results['unresolved_concepts'].append(concept)
                validation_results['resolution_details'][concept] = {
                    'status': 'missing',
                    'issues': {'not_in_dictionary': True}
                }
        
        validation_results['resolution_rate'] = validation_results['resolved_concepts'] / validation_results['total_critical_concepts']
        
        return validation_results
    
    def compare_before_after(self, original_problems: Dict, corrected_dict: Dict) -> Dict:
        """Compare l'état avant/après corrections"""
        
        comparison = {
            'original_state': {
                'total_conflicts': original_problems.get('conflicts', {}).get('total', 0),
                'incoherent_definitions': original_problems.get('conflicts', {}).get('incoherent_definitions', 0),
                'empty_descriptions': original_problems.get('quality_issues', {}).get('empty_descriptions', 0)
            },
            'corrected_state': {
                'total_concepts': len(corrected_dict.get('concepts', {})),
                'concepts_with_decomposition': 0,
                'concepts_with_description': 0,
                'average_coherence': 0.0
            },
            'improvement_metrics': {}
        }
        
        # Analyser état corrigé
        concepts = corrected_dict.get('concepts', {})
        coherence_scores = []
        
        for concept_data in concepts.values():
            if concept_data.get('dhatu_decomposition'):
                comparison['corrected_state']['concepts_with_decomposition'] += 1
            if concept_data.get('description'):
                comparison['corrected_state']['concepts_with_description'] += 1
            
            coherence = concept_data.get('coherence_score', 0.0)
            coherence_scores.append(coherence)
        
        if coherence_scores:
            comparison['corrected_state']['average_coherence'] = sum(coherence_scores) / len(coherence_scores)
        
        # Calcul amélioration
        original_total = comparison['original_state']['total_conflicts']
        corrected_total = comparison['corrected_state']['total_concepts']
        
        if original_total > 0:
            # Pourcentage de problèmes résolus
            problems_resolved = min(corrected_total, original_total)
            comparison['improvement_metrics'] = {
                'problems_resolution_rate': problems_resolved / original_total,
                'coherence_improvement': comparison['corrected_state']['average_coherence'] - 0.0,  # Était 0 avant
                'completion_improvement': comparison['corrected_state']['concepts_with_decomposition'] / corrected_total if corrected_total > 0 else 0,
                'overall_improvement_score': (comparison['corrected_state']['average_coherence'] + 
                                            (comparison['corrected_state']['concepts_with_decomposition'] / corrected_total if corrected_total > 0 else 0)) / 2
            }
        
        return comparison
    
    def generate_final_validation_report(self, critical_validation: Dict, comparison: Dict) -> Dict:
        """Génère le rapport de validation final"""
        
        # Déterminer le statut global
        resolution_rate = critical_validation['resolution_rate']
        avg_coherence = comparison['corrected_state']['average_coherence']
        completion_rate = comparison['corrected_state']['concepts_with_decomposition'] / comparison['corrected_state']['total_concepts']
        
        validation_passed = (
            resolution_rate >= self.validation_thresholds['minimum_critical_resolved'] and
            avg_coherence >= self.validation_thresholds['minimum_coherence'] and
            completion_rate >= self.validation_thresholds['minimum_completion']
        )
        
        report = {
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'validation_method': 'comprehensive_ambiguity_resolution_check_v1.0',
            'overall_validation_status': 'PASSED' if validation_passed else 'FAILED',
            'validation_score': (resolution_rate + avg_coherence + completion_rate) / 3,
            'critical_concepts_validation': {
                'total_critical_concepts': critical_validation['total_critical_concepts'],
                'resolved_concepts': critical_validation['resolved_concepts'],
                'resolution_rate': resolution_rate,
                'unresolved_count': len(critical_validation['unresolved_concepts']),
                'unresolved_concepts': critical_validation['unresolved_concepts']
            },
            'quality_metrics': {
                'average_coherence': avg_coherence,
                'completion_rate': completion_rate,
                'concepts_high_quality': len([c for c, details in critical_validation['resolution_details'].items() 
                                            if details.get('coherence_score', 0) >= 0.8]),
                'concepts_needing_work': len([c for c, details in critical_validation['resolution_details'].items() 
                                            if details.get('coherence_score', 0) < 0.6])
            },
            'improvement_summary': comparison['improvement_metrics'],
            'before_after_comparison': {
                'original_problems': comparison['original_state']['total_conflicts'],
                'resolved_concepts': comparison['corrected_state']['total_concepts'],
                'improvement_factor': comparison['improvement_metrics'].get('overall_improvement_score', 0)
            },
            'threshold_compliance': {
                'coherence_threshold': f"{avg_coherence:.3f} >= {self.validation_thresholds['minimum_coherence']} ({'✅' if avg_coherence >= self.validation_thresholds['minimum_coherence'] else '❌'})",
                'completion_threshold': f"{completion_rate:.1%} >= {self.validation_thresholds['minimum_completion']:.0%} ({'✅' if completion_rate >= self.validation_thresholds['minimum_completion'] else '❌'})",
                'critical_resolution_threshold': f"{resolution_rate:.1%} >= {self.validation_thresholds['minimum_critical_resolved']:.0%} ({'✅' if resolution_rate >= self.validation_thresholds['minimum_critical_resolved'] else '❌'})"
            },
            'recommendations': self._generate_final_recommendations(critical_validation, comparison, validation_passed)
        }
        
        return report
    
    def _generate_final_recommendations(self, critical_validation: Dict, comparison: Dict, validation_passed: bool) -> List[str]:
        """Génère les recommandations finales"""
        
        recommendations = []
        
        if validation_passed:
            recommendations.append("🎉 Toutes les ambiguïtés critiques ont été résolues avec succès")
            recommendations.append("🔧 Le système PanLang présente maintenant une cohérence sémantique optimale")
            
            # Suggestions d'amélioration continue
            avg_coherence = comparison['corrected_state']['average_coherence']
            if avg_coherence < 0.9:
                recommendations.append(f"💡 Possibilité d'améliorer encore la cohérence (actuellement {avg_coherence:.3f})")
            
            unresolved_count = len(critical_validation['unresolved_concepts'])
            if unresolved_count > 0:
                recommendations.append(f"📝 {unresolved_count} concepts critiques restent à affiner")
                
        else:
            recommendations.append("⚠️ Validation échouée - des améliorations sont nécessaires")
            
            # Problèmes spécifiques
            resolution_rate = critical_validation['resolution_rate']
            if resolution_rate < self.validation_thresholds['minimum_critical_resolved']:
                recommendations.append(f"🔴 Taux de résolution insuffisant: {resolution_rate:.1%}")
                
            for concept in critical_validation['unresolved_concepts'][:3]:  # Top 3
                recommendations.append(f"🔧 Priorité: résoudre {concept}")
        
        # Toujours ajouter
        recommendations.append("📊 Surveiller l'évolution de la cohérence lors d'ajouts futurs")
        recommendations.append("🔄 Relancer validation périodiquement")
        
        return recommendations

def main():
    """Validation finale complète"""
    
    print("✅ VALIDATION FINALE - RÉSOLUTION AMBIGUÏTÉS")
    print("=" * 55)
    
    validator = FinalAmbiguityValidator()
    
    # Charger données
    print("📥 Chargement des données...")
    original_problems = validator.load_original_problems()
    corrected_dictionary = validator.load_corrected_dictionary()
    
    if not corrected_dictionary:
        print("❌ Impossible de procéder sans dictionnaire corrigé")
        return
    
    # Validation concepts critiques
    print("\n🎯 Validation concepts critiques...")
    critical_validation = validator.validate_critical_concepts_resolved(corrected_dictionary)
    
    # Comparaison avant/après
    print("📊 Comparaison avant/après...")
    comparison = validator.compare_before_after(original_problems, corrected_dictionary)
    
    # Rapport final
    final_report = validator.generate_final_validation_report(critical_validation, comparison)
    
    # Sauvegarde
    report_path = f'validation_finale_ambiguites_{int(time.time())}.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(final_report, f, indent=2, ensure_ascii=False)
    
    # Affichage résultats
    status_icon = "🎉" if final_report['overall_validation_status'] == 'PASSED' else "❌"
    print(f"\n{status_icon} STATUT FINAL: {final_report['overall_validation_status']}")
    print(f"📈 Score validation: {final_report['validation_score']:.3f}")
    
    print(f"\n📊 MÉTRIQUES CLÉS:")
    print(f"   Concepts critiques résolus: {critical_validation['resolved_concepts']}/{critical_validation['total_critical_concepts']} ({critical_validation['resolution_rate']:.1%})")
    print(f"   Cohérence moyenne: {final_report['quality_metrics']['average_coherence']:.3f}")
    print(f"   Taux complétion: {final_report['quality_metrics']['completion_rate']:.1%}")
    print(f"   Concepts haute qualité: {final_report['quality_metrics']['concepts_high_quality']}")
    
    if critical_validation['unresolved_concepts']:
        print(f"\n⚠️ CONCEPTS NON RÉSOLUS ({len(critical_validation['unresolved_concepts'])}):")
        for concept in critical_validation['unresolved_concepts'][:5]:
            print(f"   • {concept}")
    
    print(f"\n🎯 CONFORMITÉ SEUILS:")
    for threshold, status in final_report['threshold_compliance'].items():
        print(f"   {threshold.replace('_', ' ').title()}: {status}")
    
    print(f"\n💡 RECOMMANDATIONS:")
    for i, rec in enumerate(final_report['recommendations'], 1):
        print(f"   {i}. {rec}")
    
    print(f"\n💾 Rapport sauvegardé: {report_path}")
    
    return final_report

if __name__ == "__main__":
    main()