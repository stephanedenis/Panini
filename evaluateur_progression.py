#!/usr/bin/env python3
"""
Évaluateur de progression et recommandations stratégiques
Analyse les résultats obtenus et détermine la meilleure stratégie
"""

import json
import os
import time
from pathlib import Path
import subprocess

class ProgressionEvaluator:
    """Évaluateur de progression des analyses PaniniFS"""
    
    def __init__(self):
        self.results = {}
        self.processes = {}
        self.recommendations = []
        self.quality_score = 0.0
        
    def load_analysis_results(self):
        """Charge tous les résultats d'analyses disponibles"""
        print("📊 CHARGEMENT RÉSULTATS ANALYSES")
        print("=" * 40)
        
        # Résultats ambiguïtés
        ambiguity_files = list(Path('.').glob('analyse_ambiguites_dictionnaire_*.json'))
        if ambiguity_files:
            latest_ambiguity = max(ambiguity_files, key=os.path.getctime)
            with open(latest_ambiguity, 'r', encoding='utf-8') as f:
                self.results['ambiguity'] = json.load(f)
            print(f"✅ Ambiguïtés: {latest_ambiguity}")
        
        # Résultats raffinement
        refinement_files = list(Path('.').glob('dictionnaire_raffine_*.json'))
        if refinement_files:
            latest_refinement = max(refinement_files, key=os.path.getctime)
            with open(latest_refinement, 'r', encoding='utf-8') as f:
                self.results['refinement'] = json.load(f)
            print(f"✅ Raffinement: {latest_refinement}")
        
        # Résultats géométriques
        geometric_files = list(Path('.').glob('parallel_analysis_result_*.json'))
        if geometric_files:
            latest_geometric = max(geometric_files, key=os.path.getctime)
            with open(latest_geometric, 'r', encoding='utf-8') as f:
                self.results['geometric'] = json.load(f)
            print(f"✅ Géométrique: {latest_geometric}")
        
        # Registre processus
        if os.path.exists('registre_processus_actifs.json'):
            with open('registre_processus_actifs.json', 'r', encoding='utf-8') as f:
                self.processes = json.load(f)
            print("✅ Registre processus chargé")
    
    def evaluate_ambiguity_analysis(self):
        """Évalue résultats analyse ambiguïtés"""
        if 'ambiguity' not in self.results:
            return {'score': 0, 'status': 'missing'}
        
        data = self.results['ambiguity']
        conflicts = data.get('total_conflicts', 0)
        coverage = len(data.get('quality_analyses', {}))
        
        if conflicts > 150 and coverage > 150:
            score = 0.9  # Excellent
            status = "🎯 EXCELLENT - Détection complète"
        elif conflicts > 100:
            score = 0.7  # Bon
            status = "✅ BON - Couverture satisfaisante"
        else:
            score = 0.4  # Moyen
            status = "⚠️ MOYEN - Couverture limitée"
        
        return {
            'score': score,
            'status': status,
            'conflicts': conflicts,
            'coverage': coverage,
            'value': 'Fondamental pour qualité'
        }
    
    def evaluate_refinement_process(self):
        """Évalue résultats raffinement"""
        if 'refinement' not in self.results:
            return {'score': 0, 'status': 'missing'}
        
        data = self.results['refinement']
        refined_count = data.get('refinement_count', 0)
        concepts = data.get('concepts_raffines', {})
        
        avg_confidence = 0.0
        if concepts:
            confidences = [c.get('confidence_score', 0.5) for c in concepts.values()]
            avg_confidence = sum(confidences) / len(confidences)
        
        if refined_count >= 20 and avg_confidence > 0.6:
            score = 0.85
            status = "🚀 TRÈS BON - Raffinement efficace"
        elif refined_count >= 10:
            score = 0.6
            status = "✅ ACCEPTABLE - Progrès visible"
        else:
            score = 0.3
            status = "⚠️ LIMITÉ - Peu d'impact"
        
        return {
            'score': score,
            'status': status,
            'refined_count': refined_count,
            'avg_confidence': avg_confidence,
            'value': 'Amélioration qualitative'
        }
    
    def evaluate_geometric_analysis(self):
        """Évalue résultats analyse géométrique"""
        if 'geometric' not in self.results:
            return {'score': 0, 'status': 'missing'}
        
        data = self.results['geometric']
        processing_time = data.get('processing_time', 999)
        quality_metrics = data.get('quality_metrics', {})
        dhatu_coverage = quality_metrics.get('dhatu_coverage', 0)
        
        if processing_time < 1.0 and dhatu_coverage >= 5:
            score = 0.95  # Révolutionnaire
            status = "🔺 RÉVOLUTIONNAIRE - Innovation majeure"
        elif processing_time < 5.0:
            score = 0.8   # Très prometteur
            status = "🚀 TRÈS PROMETTEUR - Performance excellent"
        else:
            score = 0.5   # Expérimental
            status = "🧪 EXPÉRIMENTAL - Potentiel à exploiter"
        
        return {
            'score': score,
            'status': status,
            'processing_time': processing_time,
            'dhatu_coverage': dhatu_coverage,
            'value': 'Innovation algorithimique'
        }
    
    def check_running_processes(self):
        """Vérifie processus en cours"""
        try:
            # Vérifier dashboard
            dashboard_check = subprocess.run(['pgrep', '-f', 'dashboard'], 
                                           capture_output=True, text=True)
            dashboard_active = dashboard_check.returncode == 0
            
            return {
                'dashboard': dashboard_active,
                'total_analyses_completed': len(self.results)
            }
        except:
            return {'dashboard': False, 'total_analyses_completed': 0}
    
    def calculate_overall_progress(self):
        """Calcule progression globale"""
        evaluations = {
            'ambiguity': self.evaluate_ambiguity_analysis(),
            'refinement': self.evaluate_refinement_process(),
            'geometric': self.evaluate_geometric_analysis()
        }
        
        total_score = 0
        max_score = 0
        
        for eval_name, eval_data in evaluations.items():
            score = eval_data.get('score', 0)
            total_score += score
            max_score += 1.0
        
        self.quality_score = (total_score / max_score) if max_score > 0 else 0
        
        return evaluations
    
    def generate_strategic_recommendations(self, evaluations):
        """Génère recommandations stratégiques"""
        recommendations = []
        
        # Analyse de la progression
        if self.quality_score > 0.8:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'CAPITALISER',
                'description': '🎯 Résultats excellents - Documenter et présenter les innovations'
            })
        elif self.quality_score > 0.6:
            recommendations.append({
                'priority': 'MEDIUM', 
                'action': 'OPTIMISER',
                'description': '🔧 Bons résultats - Affiner et étendre les analyses'
            })
        else:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'REFOCALISER',
                'description': '⚠️ Résultats mitigés - Réviser approche ou objectifs'
            })
        
        # Recommandations spécifiques
        geometric_eval = evaluations.get('geometric', {})
        if geometric_eval.get('score', 0) > 0.9:
            recommendations.append({
                'priority': 'URGENT',
                'action': 'EXPLOITER_INNOVATION',
                'description': '🔺 Innovation géométrique exceptionnelle - Publier/breveter'
            })
        
        refinement_eval = evaluations.get('refinement', {})
        if refinement_eval.get('refined_count', 0) >= 20:
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'APPLIQUER_RAFFINEMENTS',
                'description': '📚 Raffinements prêts - Retraiter corpus avec dictionnaire amélioré'
            })
        
        # État système
        process_status = self.check_running_processes()
        if process_status['dashboard']:
            recommendations.append({
                'priority': 'LOW',
                'action': 'MONITORING',
                'description': '📊 Dashboard actif - Système stable pour nouvelles analyses'
            })
        
        return recommendations
    
    def should_continue_today(self, evaluations):
        """Détermine si continuer aujourd'hui"""
        # Facteurs de décision
        high_quality_results = self.quality_score > 0.7
        innovative_breakthrough = evaluations.get('geometric', {}).get('score', 0) > 0.9
        system_stable = self.check_running_processes()['dashboard']
        
        # Fatigue algorithmique (trop d'analyses similaires)
        analysis_diversity = len([e for e in evaluations.values() if e.get('score', 0) > 0.5])
        algorithm_fatigue = analysis_diversity < 2
        
        continue_recommendation = {
            'decision': False,
            'confidence': 0.0,
            'reasoning': []
        }
        
        if innovative_breakthrough:
            continue_recommendation['decision'] = True
            continue_recommendation['confidence'] += 0.4
            continue_recommendation['reasoning'].append('🔺 Innovation majeure détectée')
        
        if high_quality_results and system_stable:
            continue_recommendation['decision'] = True
            continue_recommendation['confidence'] += 0.3
            continue_recommendation['reasoning'].append('✅ Qualité élevée + système stable')
        
        if algorithm_fatigue:
            continue_recommendation['confidence'] -= 0.2
            continue_recommendation['reasoning'].append('⚠️ Diversité algorithmique limitée')
        
        # Seuil de décision
        if continue_recommendation['confidence'] >= 0.5:
            continue_recommendation['decision'] = True
        
        return continue_recommendation
    
    def generate_final_report(self):
        """Génère rapport final avec recommandations"""
        evaluations = self.calculate_overall_progress()
        recommendations = self.generate_strategic_recommendations(evaluations)
        continuation = self.should_continue_today(evaluations)
        
        print(f"\n🎯 ÉVALUATION GLOBALE")
        print("=" * 50)
        print(f"📊 Score qualité global: {self.quality_score:.2f}/1.0")
        
        print(f"\n📈 RÉSULTATS PAR ANALYSE:")
        for analysis_name, eval_data in evaluations.items():
            print(f"   {analysis_name.upper()}: {eval_data.get('status', 'N/A')}")
            print(f"      Score: {eval_data.get('score', 0):.2f} - {eval_data.get('value', 'N/A')}")
        
        print(f"\n🎯 RECOMMANDATIONS STRATÉGIQUES:")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. [{rec['priority']}] {rec['action']}")
            print(f"      {rec['description']}")
        
        print(f"\n🤔 CONTINUER AUJOURD'HUI ?")
        decision = "OUI" if continuation['decision'] else "NON"
        print(f"   DÉCISION: {decision} (confiance: {continuation['confidence']:.2f})")
        print(f"   RAISONS:")
        for reason in continuation['reasoning']:
            print(f"      - {reason}")
        
        if continuation['decision']:
            print(f"\n🚀 PROCHAINE ÉTAPE RECOMMANDÉE:")
            if self.quality_score > 0.8:
                print("   📋 Documenter innovations et préparer présentation")
            else:
                print("   🔧 Optimiser analyses existantes ou explorer nouvelles approches")
        else:
            print(f"\n🏁 RECOMMANDATION:")
            print("   💤 Pause stratégique - Digérer résultats et planifier prochaine session")
        
        return {
            'quality_score': self.quality_score,
            'evaluations': evaluations,
            'recommendations': recommendations,
            'continue_today': continuation
        }

def main():
    """Point d'entrée évaluation"""
    print("🎯 ÉVALUATEUR PROGRESSION STRATEGIQUE")
    print("=" * 60)
    
    evaluator = ProgressionEvaluator()
    evaluator.load_analysis_results()
    
    final_assessment = evaluator.generate_final_report()
    
    # Sauvegarde évaluation
    timestamp = int(time.time())
    output_file = f"evaluation_strategique_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_assessment, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 Évaluation sauvegardée: {output_file}")
    
    return final_assessment

if __name__ == "__main__":
    main()