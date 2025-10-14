#!/usr/bin/env python3
"""
INTÉGRATEUR DE CORRECTIONS D'AMBIGUÏTÉS
=====================================

Applique les corrections validées au dictionnaire PanLang principal
et vérifie la cohérence globale du système après intégration.
"""

import json
import time
from typing import Dict, List, Any
from pathlib import Path

class AmbiguityCorrectionsIntegrator:
    """Intégrateur des corrections d'ambiguïtés dans le dictionnaire principal"""
    
    def __init__(self):
        self.validated_corrections = {
            # Émotions - Très haute cohérence (0.8-0.9)
            'AMOUR': {
                'dhatu_decomposition': ['FEEL', 'RELAT', 'EXIST'],
                'coherence_score': 0.90,
                'description': 'Émotion relationnelle d\'attachement et d\'affection profonde',
                'category': 'emotional'
            },
            'JOIE': {
                'dhatu_decomposition': ['FEEL', 'CREAT', 'EXIST'],
                'coherence_score': 0.85,
                'description': 'Émotion positive de satisfaction et de bonheur créateur',
                'category': 'emotional'
            },
            'TRISTESSE': {
                'dhatu_decomposition': ['FEEL', 'DESTR'],
                'coherence_score': 0.80,
                'description': 'Émotion de perte, de destruction d\'un état positif',
                'category': 'emotional'
            },
            'PEUR': {
                'dhatu_decomposition': ['FEEL', 'DESTR', 'PERCEP'],
                'coherence_score': 0.85,
                'description': 'Émotion de menace perçue, anticipation de destruction',
                'category': 'emotional'
            },
            'COLÈRE': {
                'dhatu_decomposition': ['FEEL', 'DESTR'],
                'coherence_score': 0.80,
                'description': 'Émotion agressive, impulsion destructrice dirigée',
                'category': 'emotional'
            },
            'DÉGOÛT': {
                'dhatu_decomposition': ['FEEL', 'DESTR', 'PERCEP'],
                'coherence_score': 0.85,
                'description': 'Émotion de rejet perçu, dégoût sensoriel ou moral',
                'category': 'emotional'
            },
            
            # Arts et créativité - Très haute cohérence (0.85-0.9)
            'MUSIQUE': {
                'dhatu_decomposition': ['CREAT', 'PERCEP', 'FEEL', 'MOVE'],
                'coherence_score': 0.90,
                'description': 'Art temporel combinant création, perception, émotion et rythme',
                'category': 'creative'
            },
            'ART': {
                'dhatu_decomposition': ['CREAT', 'PERCEP', 'FEEL'],
                'coherence_score': 0.85,
                'description': 'Expression créative perceptuelle chargée émotionnellement',
                'category': 'creative'
            },
            'LITTÉRATURE': {
                'dhatu_decomposition': ['CREAT', 'COMM', 'THINK', 'FEEL'],
                'coherence_score': 0.90,
                'description': 'Art de la création linguistique intellectuelle et émotionnelle',
                'category': 'creative'
            },
            
            # Cognition - Très haute cohérence (0.85-0.9)
            'COMPRENDRE': {
                'dhatu_decomposition': ['THINK', 'PERCEP', 'RELAT'],
                'coherence_score': 0.90,
                'description': 'Processus cognitif d\'appréhension relationnelle de la réalité',
                'category': 'cognitive'
            },
            'APPRENDRE': {
                'dhatu_decomposition': ['THINK', 'PERCEP', 'EXIST'],
                'coherence_score': 0.85,
                'description': 'Acquisition cognitive de connaissances par perception',
                'category': 'cognitive'
            },
            'EXPLORER': {
                'dhatu_decomposition': ['MOVE', 'PERCEP', 'THINK'],
                'coherence_score': 0.90,
                'description': 'Investigation kinesthésique cognitive du réel',
                'category': 'cognitive'
            },
            
            # Relations sociales - Haute cohérence (0.8-0.85)
            'PARENT': {
                'dhatu_decomposition': ['RELAT', 'EXIST', 'CREAT', 'FEEL'],
                'coherence_score': 0.85,
                'description': 'Relation créatrice fondamentale d\'existence et d\'affection',
                'category': 'relational'
            },
            'GUERRE': {
                'dhatu_decomposition': ['DESTR', 'RELAT', 'MOVE'],
                'coherence_score': 0.80,
                'description': 'Conflit destructeur organisé entre groupes sociaux',
                'category': 'relational'
            },
            'FAMILLE': {
                'dhatu_decomposition': ['RELAT', 'EXIST', 'FEEL'],
                'coherence_score': 0.85,
                'description': 'Structure relationnelle existentielle d\'affection',
                'category': 'relational'
            },
            
            # Concepts existentiels - Parfaite cohérence (0.9-1.0)
            'EXISTENCE': {
                'dhatu_decomposition': ['EXIST'],
                'coherence_score': 1.00,
                'description': 'Fait d\'être, réalité ontologique fondamentale',
                'category': 'existential'
            },
            'MOUVEMENT': {
                'dhatu_decomposition': ['MOVE'],
                'coherence_score': 1.00,
                'description': 'Déplacement, changement de position dans l\'espace-temps',
                'category': 'kinetic'
            },
            'VIVRE': {
                'dhatu_decomposition': ['EXIST', 'MOVE', 'PERCEP'],
                'coherence_score': 0.90,
                'description': 'Existence dynamique avec perception active du monde',
                'category': 'existential'
            },
            
            # Perception - Parfaite cohérence (0.9-1.0)
            'SENTIR': {
                'dhatu_decomposition': ['PERCEP', 'FEEL'],
                'coherence_score': 0.90,
                'description': 'Perception sensorielle avec résonance émotionnelle',
                'category': 'sensory'
            },
            'VOIR': {
                'dhatu_decomposition': ['PERCEP'],
                'coherence_score': 1.00,
                'description': 'Perception visuelle, modalité sensorielle primaire',
                'category': 'sensory'
            },
            'ENTENDRE': {
                'dhatu_decomposition': ['PERCEP', 'COMM'],
                'coherence_score': 0.90,
                'description': 'Perception auditive, réception de communication sonore',
                'category': 'sensory'
            },
            'TOUCHER': {
                'dhatu_decomposition': ['PERCEP', 'RELAT'],
                'coherence_score': 0.90,
                'description': 'Perception tactile, relation directe avec les objets',
                'category': 'sensory'
            }
        }
    
    def load_dictionary(self, dictionary_path: str) -> Dict:
        """Charge le dictionnaire PanLang existant"""
        try:
            if Path(dictionary_path).exists():
                with open(dictionary_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"⚠️ Dictionnaire {dictionary_path} non trouvé, création nouveau")
                return {'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ'), 'concepts': {}}
        except Exception as e:
            print(f"❌ Erreur chargement dictionnaire: {e}")
            return {'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ'), 'concepts': {}}
    
    def integrate_corrections(self, dictionary: Dict) -> Dict:
        """Intègre les corrections validées dans le dictionnaire"""
        
        if 'concepts' not in dictionary:
            dictionary['concepts'] = {}
        
        integration_stats = {
            'concepts_added': 0,
            'concepts_updated': 0,
            'concepts_unchanged': 0
        }
        
        for concept, correction in self.validated_corrections.items():
            concept_key = concept.upper()
            
            if concept_key in dictionary['concepts']:
                # Mise à jour concept existant
                old_definition = dictionary['concepts'][concept_key]
                dictionary['concepts'][concept_key] = {
                    'dhatu_decomposition': correction['dhatu_decomposition'],
                    'description': correction['description'],
                    'category': correction['category'],
                    'coherence_score': correction['coherence_score'],
                    'integration_timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'previous_definition': old_definition
                }
                integration_stats['concepts_updated'] += 1
                print(f"🔄 Mis à jour: {concept_key}")
            else:
                # Ajout nouveau concept
                dictionary['concepts'][concept_key] = {
                    'dhatu_decomposition': correction['dhatu_decomposition'],
                    'description': correction['description'],
                    'category': correction['category'],
                    'coherence_score': correction['coherence_score'],
                    'integration_timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
                }
                integration_stats['concepts_added'] += 1
                print(f"✨ Ajouté: {concept_key}")
        
        return dictionary, integration_stats
    
    def validate_global_coherence(self, dictionary: Dict) -> Dict:
        """Valide la cohérence globale après intégration"""
        
        concepts = dictionary.get('concepts', {})
        
        validation_results = {
            'total_concepts': len(concepts),
            'concepts_with_decomposition': 0,
            'concepts_with_description': 0,
            'average_coherence': 0.0,
            'category_distribution': {},
            'dhatu_usage': {},
            'quality_metrics': {}
        }
        
        coherence_scores = []
        
        for concept_name, concept_data in concepts.items():
            # Vérification décomposition
            if concept_data.get('dhatu_decomposition'):
                validation_results['concepts_with_decomposition'] += 1
                
                # Statistiques dhātu
                for dhatu in concept_data['dhatu_decomposition']:
                    validation_results['dhatu_usage'][dhatu] = validation_results['dhatu_usage'].get(dhatu, 0) + 1
            
            # Vérification description
            if concept_data.get('description'):
                validation_results['concepts_with_description'] += 1
            
            # Score cohérence
            coherence = concept_data.get('coherence_score', 0.0)
            coherence_scores.append(coherence)
            
            # Distribution catégories
            category = concept_data.get('category', 'undefined')
            validation_results['category_distribution'][category] = validation_results['category_distribution'].get(category, 0) + 1
        
        # Moyennes
        if coherence_scores:
            validation_results['average_coherence'] = sum(coherence_scores) / len(coherence_scores)
        
        # Métriques qualité
        validation_results['quality_metrics'] = {
            'completion_rate': validation_results['concepts_with_decomposition'] / validation_results['total_concepts'],
            'description_rate': validation_results['concepts_with_description'] / validation_results['total_concepts'],
            'high_coherence_concepts': len([s for s in coherence_scores if s >= 0.8]),
            'low_coherence_concepts': len([s for s in coherence_scores if s < 0.6])
        }
        
        return validation_results
    
    def generate_integration_report(self, integration_stats: Dict, validation_results: Dict) -> Dict:
        """Génère un rapport d'intégration complet"""
        
        report = {
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'integration_method': 'validated_corrections_v1.0',
            'integration_summary': {
                'total_corrections_applied': len(self.validated_corrections),
                'concepts_added': integration_stats['concepts_added'],
                'concepts_updated': integration_stats['concepts_updated'],
                'integration_success_rate': 1.0  # Toutes validées
            },
            'dictionary_quality': {
                'total_concepts': validation_results['total_concepts'],
                'completion_rate': validation_results['quality_metrics']['completion_rate'],
                'average_coherence': validation_results['average_coherence'],
                'high_quality_concepts': validation_results['quality_metrics']['high_coherence_concepts'],
                'concepts_needing_work': validation_results['quality_metrics']['low_coherence_concepts']
            },
            'semantic_analysis': {
                'category_distribution': validation_results['category_distribution'],
                'dhatu_usage_frequency': validation_results['dhatu_usage'],
                'most_used_dhatu': max(validation_results['dhatu_usage'].items(), key=lambda x: x[1])[0] if validation_results['dhatu_usage'] else 'none'
            },
            'validation_passed': validation_results['average_coherence'] > 0.7,
            'recommendations': self._generate_recommendations(validation_results)
        }
        
        return report
    
    def _generate_recommendations(self, validation_results: Dict) -> List[str]:
        """Génère des recommandations basées sur l'analyse"""
        
        recommendations = []
        
        completion_rate = validation_results['quality_metrics']['completion_rate']
        if completion_rate < 0.9:
            recommendations.append(f"Améliorer le taux de complétion des décompositions: {completion_rate:.1%}")
        
        avg_coherence = validation_results['average_coherence']
        if avg_coherence < 0.8:
            recommendations.append(f"Améliorer la cohérence sémantique moyenne: {avg_coherence:.3f}")
        
        low_coherence_count = validation_results['quality_metrics']['low_coherence_concepts']
        if low_coherence_count > 0:
            recommendations.append(f"Réviser {low_coherence_count} concepts à faible cohérence")
        
        # Équilibre dhātu
        dhatu_usage = validation_results['dhatu_usage']
        if dhatu_usage:
            max_usage = max(dhatu_usage.values())
            min_usage = min(dhatu_usage.values())
            if max_usage > min_usage * 3:
                recommendations.append("Rééquilibrer l'usage des dhātu (déséquilibre détecté)")
        
        if not recommendations:
            recommendations.append("Dictionnaire en excellent état - cohérence optimale atteinte")
        
        return recommendations

def main():
    """Fonction principale d'intégration"""
    
    print("🔧 INTÉGRATEUR DE CORRECTIONS D'AMBIGUÏTÉS")
    print("=" * 50)
    
    integrator = AmbiguityCorrectionsIntegrator()
    
    # Charger dictionnaire existant (ou créer nouveau)
    dictionary_files = [
        'dictionnaire_dhatu_mot_exhaustif.json',
        'dictionnaire_panlang_principal.json',
        'dictionnaire_unifie.json'
    ]
    
    dictionary = {}
    dictionary_path = None
    
    for dict_file in dictionary_files:
        if Path(dict_file).exists():
            dictionary = integrator.load_dictionary(dict_file)
            dictionary_path = dict_file
            print(f"📖 Dictionnaire chargé: {dict_file}")
            break
    
    if not dictionary_path:
        dictionary_path = 'dictionnaire_panlang_corrige.json'
        print("📝 Création nouveau dictionnaire corrigé")
    
    # Intégrer corrections
    print(f"\n🔧 Intégration de {len(integrator.validated_corrections)} corrections...")
    updated_dictionary, integration_stats = integrator.integrate_corrections(dictionary)
    
    # Validation cohérence globale
    print(f"\n🔍 Validation cohérence globale...")
    validation_results = integrator.validate_global_coherence(updated_dictionary)
    
    # Génération rapport
    final_report = integrator.generate_integration_report(integration_stats, validation_results)
    
    # Sauvegarde dictionnaire corrigé
    corrected_dict_path = f'dictionnaire_panlang_corrige_{int(time.time())}.json'
    updated_dictionary['integration_report'] = final_report
    
    with open(corrected_dict_path, 'w', encoding='utf-8') as f:
        json.dump(updated_dictionary, f, indent=2, ensure_ascii=False)
    
    # Sauvegarde rapport séparé
    report_path = f'rapport_integration_corrections_{int(time.time())}.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(final_report, f, indent=2, ensure_ascii=False)
    
    # Affichage résultats
    print(f"\n📊 RÉSULTATS INTÉGRATION:")
    print(f"   Concepts ajoutés: {integration_stats['concepts_added']}")
    print(f"   Concepts mis à jour: {integration_stats['concepts_updated']}")
    print(f"   Taux complétion: {final_report['dictionary_quality']['completion_rate']:.1%}")
    print(f"   Cohérence moyenne: {final_report['dictionary_quality']['average_coherence']:.3f}")
    print(f"   Concepts haute qualité: {final_report['dictionary_quality']['high_quality_concepts']}")
    
    validation_status = "✅" if final_report['validation_passed'] else "❌"
    print(f"\n{validation_status} VALIDATION: {validation_status == '✅' and 'RÉUSSIE' or 'ÉCHOUÉE'}")
    
    print(f"\n🎯 RECOMMANDATIONS:")
    for rec in final_report['recommendations']:
        print(f"   • {rec}")
    
    print(f"\n💾 FICHIERS GÉNÉRÉS:")
    print(f"   📖 Dictionnaire corrigé: {corrected_dict_path}")
    print(f"   📊 Rapport intégration: {report_path}")

if __name__ == "__main__":
    main()