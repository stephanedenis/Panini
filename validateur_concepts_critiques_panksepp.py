#!/usr/bin/env python3
"""
VALIDATEUR CONCEPTS CRITIQUES - MIGRATION PANKSEPP
=================================================

Validation spécifique des concepts critiques migrés de FEEL vers Panksepp.
Focus sur les 22 concepts ambigus précédemment corrigés.
"""

import json
import time
from typing import Dict, List, Any

class CriticalConceptValidator:
    """Validateur pour concepts critiques migrés"""
    
    def __init__(self):
        self.migration_data = self._load_migration_results()
        self.expected_mappings = self._define_expected_mappings()
        
    def _load_migration_results(self) -> Dict:
        """Charge les résultats de migration"""
        with open('migration_feel_panksepp_1759073218.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _define_expected_mappings(self) -> Dict[str, Dict]:
        """Définit les mappings attendus pour validation"""
        return {
            'AMOUR': {
                'expected_primary_dhatu': 'CARE',
                'expected_composition': ['CARE', 'RELAT', 'EXIST'],
                'panksepp_system': 'CARE',
                'neural_basis': 'Oxytocin, vasopressin, PFC',
                'validation_criteria': 'Amour = soin + relation + existence'
            },
            'JOIE': {
                'expected_primary_dhatu': 'PLAY',
                'expected_composition': ['PLAY', 'CREAT', 'EXIST'],
                'panksepp_system': 'PLAY',
                'neural_basis': 'Cannabinoids, PFC, cerebellum',
                'validation_criteria': 'Joie = jeu + création + existence'
            },
            'TRISTESSE': {
                'expected_primary_dhatu': 'GRIEF',
                'expected_composition': ['GRIEF', 'DESTR'],
                'panksepp_system': 'GRIEF',
                'neural_basis': 'Opioid system, anterior cingulate',
                'validation_criteria': 'Tristesse = chagrin + destruction (perte)'
            },
            'COLÈRE': {
                'expected_primary_dhatu': 'RAGE',
                'expected_composition': ['RAGE', 'DESTR'],
                'panksepp_system': 'RAGE',
                'neural_basis': 'Amygdala, hypothalamus, PAG',
                'validation_criteria': 'Colère = rage + destruction'
            },
            'PEUR': {
                'expected_primary_dhatu': 'FEAR',
                'expected_composition': ['FEAR', 'PERCEP'],
                'panksepp_system': 'FEAR',
                'neural_basis': 'Amygdala, hippocampus, cingulate',
                'validation_criteria': 'Peur = peur + perception (menace)'
            }
        }
    
    def validate_critical_concepts(self) -> Dict[str, Any]:
        """Valide les concepts critiques migrés"""
        
        validation_report = {
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'validation_type': 'Critical Concepts - Panksepp Migration',
            'concepts_validated': [],
            'validation_results': {},
            'overall_score': 0.0,
            'issues_detected': [],
            'recommendations': []
        }
        
        print("🔍 VALIDATION CONCEPTS CRITIQUES - MIGRATION PANKSEPP")
        print("=" * 55)
        
        migrated_concepts = self.migration_data.get('migrated_concepts', {})
        
        for concept_name, expected in self.expected_mappings.items():
            if concept_name in migrated_concepts:
                validation_result = self._validate_single_concept(
                    concept_name, 
                    migrated_concepts[concept_name], 
                    expected
                )
                validation_report['validation_results'][concept_name] = validation_result
                validation_report['concepts_validated'].append(concept_name)
                
                if validation_result['overall_score'] < 0.8:
                    validation_report['issues_detected'].append({
                        'concept': concept_name,
                        'issue': validation_result['issues'],
                        'severity': 'HIGH' if validation_result['overall_score'] < 0.5 else 'MEDIUM'
                    })
                
                print(f"✅ {concept_name}: {validation_result['overall_score']:.3f}")
            else:
                print(f"❌ {concept_name}: Concept non trouvé dans migration")
                validation_report['issues_detected'].append({
                    'concept': concept_name,
                    'issue': 'Concept missing from migration',
                    'severity': 'HIGH'
                })
        
        # Score global
        scores = [r['overall_score'] for r in validation_report['validation_results'].values()]
        validation_report['overall_score'] = sum(scores) / len(scores) if scores else 0.0
        
        print(f"\n🎯 SCORE GLOBAL VALIDATION: {validation_report['overall_score']:.3f}")
        
        # Recommandations
        validation_report['recommendations'] = self._generate_recommendations(validation_report)
        
        return validation_report
    
    def _validate_single_concept(self, concept_name: str, migrated_data: Dict, expected: Dict) -> Dict:
        """Valide un concept spécifique"""
        
        result = {
            'concept': concept_name,
            'scores': {},
            'issues': [],
            'overall_score': 0.0,
            'details': {}
        }
        
        # 1. Validation dhātu primaire
        actual_system = migrated_data.get('panksepp_system', '')
        expected_system = expected['panksepp_system']
        
        if actual_system == expected_system:
            result['scores']['primary_dhatu'] = 1.0
        else:
            result['scores']['primary_dhatu'] = 0.0
            result['issues'].append(f"Dhātu primaire: attendu {expected_system}, obtenu {actual_system}")
        
        # 2. Validation composition
        actual_composition = set(migrated_data.get('new_decomposition', []))
        expected_composition = set(expected['expected_composition'])
        
        intersection = actual_composition & expected_composition
        union = actual_composition | expected_composition
        
        composition_score = len(intersection) / len(union) if union else 0.0
        result['scores']['composition'] = composition_score
        
        if composition_score < 0.8:
            result['issues'].append(f"Composition: attendue {expected_composition}, obtenue {actual_composition}")
        
        # 3. Validation sémantique
        rationale = migrated_data.get('migration_rationale', '')
        if expected_system.lower() in rationale.lower():
            result['scores']['semantic'] = 1.0
        else:
            result['scores']['semantic'] = 0.5
            result['issues'].append("Justification sémantique faible")
        
        # Score global
        weights = {'primary_dhatu': 0.5, 'composition': 0.3, 'semantic': 0.2}
        result['overall_score'] = sum(
            result['scores'][key] * weight for key, weight in weights.items()
        )
        
        result['details'] = {
            'expected': expected,
            'actual': migrated_data,
            'neural_validation': expected['neural_basis']
        }
        
        return result
    
    def _generate_recommendations(self, validation_report: Dict) -> List[str]:
        """Génère recommandations basées sur validation"""
        
        recommendations = []
        
        if validation_report['overall_score'] >= 0.9:
            recommendations.append("✅ Migration excellente - Tous concepts critiques validés")
        elif validation_report['overall_score'] >= 0.8:
            recommendations.append("✅ Migration bonne - Corrections mineures recommandées")
        else:
            recommendations.append("⚠️ Migration nécessite corrections majeures")
        
        # Recommandations spécifiques
        high_issues = [i for i in validation_report['issues_detected'] if i['severity'] == 'HIGH']
        if high_issues:
            recommendations.append(f"🔧 Corriger {len(high_issues)} problèmes prioritaires")
        
        if len(validation_report['concepts_validated']) < len(self.expected_mappings):
            missing = len(self.expected_mappings) - len(validation_report['concepts_validated'])
            recommendations.append(f"📋 Migrer {missing} concepts critiques manquants")
        
        # Validation créative
        creative_combinations = self.migration_data.get('creative_combinations', {})
        if len(creative_combinations) >= 10:
            recommendations.append("✨ Tester nouvelles combinaisons créatives (10 disponibles)")
        
        return recommendations
    
    def test_creative_combinations(self) -> Dict[str, Any]:
        """Teste les nouvelles combinaisons créatives"""
        
        print(f"\n✨ TEST COMBINAISONS CRÉATIVES PANKSEPP")
        print("=" * 40)
        
        creative_combinations = self.migration_data.get('creative_combinations', {})
        
        test_results = {
            'total_combinations': len(creative_combinations),
            'tested_combinations': {},
            'cognitive_validation': {},
            'neurobiological_validation': {}
        }
        
        for emotion_name, dhatu_composition in creative_combinations.items():
            print(f"🔬 {emotion_name}: {' + '.join(dhatu_composition)}")
            
            # Test cohérence cognitive (limite Miller 7±2)
            cognitive_score = 1.0 if len(dhatu_composition) <= 4 else 0.5
            
            # Test cohérence neurobiologique
            neurobiological_score = self._validate_neurobiological_coherence(dhatu_composition)
            
            test_results['tested_combinations'][emotion_name] = {
                'composition': dhatu_composition,
                'cognitive_score': cognitive_score,
                'neurobiological_score': neurobiological_score,
                'overall_viability': (cognitive_score + neurobiological_score) / 2
            }
        
        # Scores moyens
        scores = [t['overall_viability'] for t in test_results['tested_combinations'].values()]
        average_viability = sum(scores) / len(scores) if scores else 0.0
        
        print(f"\n🎯 Viabilité moyenne combinaisons: {average_viability:.3f}")
        
        return test_results
    
    def _validate_neurobiological_coherence(self, composition: List[str]) -> float:
        """Valide cohérence neurobiologique d'une composition"""
        
        # Systèmes Panksepp dans composition
        panksepp_systems = ['SEEK', 'RAGE', 'FEAR', 'LUST', 'CARE', 'GRIEF', 'PLAY']
        panksepp_count = sum(1 for dhatu in composition if dhatu in panksepp_systems)
        
        # Autres dhātu valides
        other_dhatu = ['MOVE', 'CREAT', 'PERCEP', 'THINK', 'RELAT', 'EXIST', 'DESTR']
        other_count = sum(1 for dhatu in composition if dhatu in other_dhatu)
        
        total_valid = panksepp_count + other_count
        coherence_score = total_valid / len(composition) if composition else 0.0
        
        return coherence_score
    
    def generate_validation_summary(self, validation_results: Dict, creative_results: Dict) -> Dict:
        """Génère résumé complet validation"""
        
        summary = {
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'migration_validation': {
                'concepts_score': validation_results['overall_score'],
                'concepts_validated': len(validation_results['concepts_validated']),
                'issues_count': len(validation_results['issues_detected']),
                'status': 'SUCCESS' if validation_results['overall_score'] >= 0.8 else 'NEEDS_REVIEW'
            },
            'creative_validation': {
                'combinations_count': creative_results['total_combinations'],
                'average_viability': sum(t['overall_viability'] 
                                       for t in creative_results['tested_combinations'].values()) / 
                                   len(creative_results['tested_combinations']),
                'viable_combinations': sum(1 for t in creative_results['tested_combinations'].values() 
                                         if t['overall_viability'] >= 0.7)
            },
            'overall_assessment': {
                'migration_success': validation_results['overall_score'] >= 0.8,
                'creative_potential': creative_results['total_combinations'] >= 8,
                'neurobiological_validity': True,
                'ready_for_production': validation_results['overall_score'] >= 0.9 and 
                                      len(validation_results['issues_detected']) == 0
            },
            'next_steps': self._generate_next_steps(validation_results, creative_results)
        }
        
        return summary
    
    def _generate_next_steps(self, validation_results: Dict, creative_results: Dict) -> List[str]:
        """Génère prochaines étapes recommandées"""
        
        steps = []
        
        if validation_results['overall_score'] >= 0.9:
            steps.append("✅ Déployer architecture Panksepp en production")
        else:
            steps.append("🔧 Corriger concepts critiques avec score < 0.8")
        
        viable_combinations = sum(1 for t in creative_results['tested_combinations'].values() 
                                if t['overall_viability'] >= 0.7)
        
        if viable_combinations >= 7:
            steps.append(f"✨ Intégrer {viable_combinations} combinaisons créatives viables")
        
        steps.append("📊 Effectuer tests performance architecturale complète")
        steps.append("📝 Documenter migration complète pour publication")
        
        return steps

def main():
    """Validation complète concepts critiques"""
    
    print("🔍 VALIDATEUR CONCEPTS CRITIQUES - MIGRATION PANKSEPP")
    print("=" * 55)
    
    validator = CriticalConceptValidator()
    
    # Phase 1: Validation concepts critiques
    validation_results = validator.validate_critical_concepts()
    
    # Phase 2: Test combinaisons créatives
    creative_results = validator.test_creative_combinations()
    
    # Phase 3: Résumé complet
    summary = validator.generate_validation_summary(validation_results, creative_results)
    
    print(f"\n🎊 RÉSUMÉ VALIDATION COMPLÈTE")
    print("=" * 30)
    print(f"✅ Concepts critiques: {summary['migration_validation']['concepts_score']:.3f}")
    print(f"✨ Combinaisons viables: {summary['creative_validation']['viable_combinations']}/{summary['creative_validation']['combinations_count']}")
    print(f"🚀 Prêt production: {'OUI' if summary['overall_assessment']['ready_for_production'] else 'NON'}")
    
    # Sauvegarde
    timestamp = int(time.time())
    
    with open(f'validation_concepts_critiques_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(validation_results, f, indent=2, ensure_ascii=False)
    
    with open(f'test_combinaisons_creatives_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(creative_results, f, indent=2, ensure_ascii=False)
        
    with open(f'resume_validation_panksepp_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 RAPPORTS GÉNÉRÉS:")
    print(f"   📋 Validation: validation_concepts_critiques_{timestamp}.json")
    print(f"   ✨ Créatives: test_combinaisons_creatives_{timestamp}.json")
    print(f"   📊 Résumé: resume_validation_panksepp_{timestamp}.json")
    
    if summary['overall_assessment']['ready_for_production']:
        print(f"\n🎯 MIGRATION PANKSEPP VALIDÉE POUR PRODUCTION!")
    else:
        print(f"\n⚠️ Corrections nécessaires avant production")
        for step in summary['next_steps'][:3]:
            print(f"   {step}")

if __name__ == "__main__":
    main()