#!/usr/bin/env python3
"""
SYSTÈME DE DÉTECTION AUTOMATIQUE D'AMBIGUÏTÉS v2.0
===============================================

Système intelligent qui score et classe automatiquement les conflits
sémantiques pour prioriser les raffinements de dictionnaire.

Basé sur l'analyse des 154 conflits détectés dans notre dictionnaire.
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Any, Set
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import re
import math

@dataclass
class ConflictScore:
    """Score d'un conflit avec métriques détaillées"""
    conflict_id: str
    severity_raw: float
    semantic_coherence_score: float  # 0-1, plus bas = plus incohérent
    frequency_impact_score: float   # Fréquence usage estimée 
    resolution_difficulty: float    # Difficulté résolution 0-1
    priority_score: float           # Score final priorité
    resolution_type: str            # 'critical', 'high', 'medium', 'low'

@dataclass
class AutomaticRefinementSuggestion:
    """Suggestion automatique de raffinement"""
    concept_name: str
    current_definition: List[str]
    conflict_type: str
    suggested_refinement: Dict[str, Any]
    confidence_score: float
    linguistic_analysis: Dict[str, Any]
    contextual_dimensions: List[str]

class AutomaticAmbiguityDetector:
    """Détecteur automatique d'ambiguïtés avec scoring intelligent"""
    
    def __init__(self, analysis_report_path: str):
        self.report_path = analysis_report_path
        self.analysis_data = self._load_analysis_report()
        self.conflicts = self.analysis_data.get('detailed_conflicts', [])
        
        # Métriques linguistiques pour scoring
        self.semantic_coherence_patterns = self._build_coherence_patterns()
        self.frequency_estimates = self._build_frequency_estimates()
        
        print(f"🤖 Détecteur automatique initialisé")
        print(f"📊 {len(self.conflicts)} conflits à analyser")
    
    def _load_analysis_report(self) -> Dict:
        """Charge le rapport d'analyse des ambiguïtés"""
        try:
            with open(self.report_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Erreur chargement rapport: {e}")
            return {}
    
    def _build_coherence_patterns(self) -> Dict[str, float]:
        """Patterns de cohérence sémantique par type atome"""
        return {
            # Combinaisons cohérentes (score élevé)
            ('EMOTION', 'CREATION'): 0.9,      # JOIE
            ('EMOTION', 'DESTRUCTION'): 0.8,   # TRISTESSE  
            ('COGNITION', 'COMMUNICATION'): 0.9, # EXPLIQUER
            ('MOUVEMENT', 'PERCEPTION'): 0.8,    # EXPLORER
            ('POSSESSION', 'EMOTION'): 0.7,      # DÉSIRER
            
            # Combinaisons incohérentes (score bas)
            ('DESTRUCTION', 'PERCEPTION', 'EXISTENCE'): 0.2,  # AMOUR problématique
            ('DESTRUCTION', 'MOUVEMENT'): 0.3,                 # MUSIQUE réducteur
            ('COMMUNICATION',): 0.1,                           # ÉTOILE bizarre
            ('EXISTENCE',): 0.2,                               # Trop vague
        }
    
    def _build_frequency_estimates(self) -> Dict[str, float]:
        """Estimations fréquence usage par concept"""
        # Concepts fréquents dans usage quotidien
        high_frequency = ['AMOUR', 'JOIE', 'TRISTESSE', 'PEUR', 'COMPRENDRE', 
                         'APPRENDRE', 'COMMUNICATION', 'MOUVEMENT']
        
        # Concepts moyens
        medium_frequency = ['NOSTALGIE', 'MÉLANCOLIE', 'EUPHORIE', 'ARCHITECTURE',
                           'MUSIQUE', 'ART', 'PHILOSOPHIE']
        
        # Concepts rares/techniques  
        low_frequency = ['ÉTOILE', 'FENÊTRE', 'RÉCIT', 'LÉGENDE', 'RACINE']
        
        estimates = {}
        for concept in high_frequency:
            estimates[concept] = 0.8
        for concept in medium_frequency:
            estimates[concept] = 0.5  
        for concept in low_frequency:
            estimates[concept] = 0.2
            
        return estimates
    
    def calculate_semantic_coherence(self, atoms: List[str]) -> float:
        """Calcule cohérence sémantique d'une combinaison d'atomes"""
        
        # Cas spéciaux problématiques identifiés
        atoms_tuple = tuple(sorted(atoms))
        if atoms_tuple in self.semantic_coherence_patterns:
            return self.semantic_coherence_patterns[atoms_tuple]
        
        # Heuristiques générales
        if len(atoms) == 1:
            return 0.3  # Concepts mono-atomiques souvent sous-spécifiés
        
        if len(atoms) > 4:
            return 0.4  # Sur-complexité
        
        # Combinaisons problématiques détectées
        if 'DESTRUCTION' in atoms and 'CREATION' not in atoms:
            if any(emotion in atoms for emotion in ['EMOTION', 'PERCEPTION']):
                return 0.2  # Émotions positives avec destruction pure
        
        if set(atoms) == {'DESTRUCTION', 'MOUVEMENT'}:
            return 0.3  # Trop réducteur pour concepts riches
            
        if 'EXISTENCE' in atoms and len(atoms) == 1:
            return 0.1  # Trop vague
            
        # Score par défaut basé sur diversité
        unique_categories = set()
        atom_categories = {
            'EMOTION': 'affect',
            'COGNITION': 'mental', 
            'PERCEPTION': 'sensory',
            'COMMUNICATION': 'social',
            'MOUVEMENT': 'physical',
            'CREATION': 'generative',
            'DESTRUCTION': 'transformative',
            'EXISTENCE': 'ontological',
            'POSSESSION': 'relational',
            'DOMINATION': 'power'
        }
        
        for atom in atoms:
            if atom in atom_categories:
                unique_categories.add(atom_categories[atom])
        
        diversity_score = len(unique_categories) / len(atoms) if atoms else 0
        return min(0.8, 0.4 + diversity_score * 0.4)
    
    def calculate_resolution_difficulty(self, conflict: Dict) -> float:
        """Estime difficulté de résolution d'un conflit"""
        
        conflict_type = conflict.get('conflict_type', '')
        concept1 = conflict.get('concept_1', '')
        concept2 = conflict.get('concept_2', '')
        
        # Conflits identiques = très difficile à résoudre
        if conflict_type == 'identical_decomposition':
            return 0.9
            
        # Définitions incohérentes = moyennement difficile  
        if conflict_type == 'incoherent_definition':
            atoms = conflict.get('decomposition_1', [])
            
            # Cas particulièrement problématiques
            if concept1 == 'AMOUR' and 'DESTRUCTION' in atoms:
                return 0.8  # Refonte conceptuelle majeure nécessaire
                
            if len(atoms) == 1 and atoms[0] in ['EXISTENCE', 'COMMUNICATION']:
                return 0.6  # Ajout dimensions requises
                
            return 0.7
        
        # Synonymes partiels = plus facile
        if conflict_type == 'partial_synonym':
            return 0.4
            
        return 0.5
    
    def score_all_conflicts(self) -> List[ConflictScore]:
        """Score tous les conflits avec priorités"""
        
        print("\n🎯 SCORING AUTOMATIQUE DES CONFLITS")
        print("=" * 50)
        
        scored_conflicts = []
        
        for conflict in self.conflicts:
            concept1 = conflict.get('concept_1', '')
            atoms = conflict.get('decomposition_1', [])
            severity = conflict.get('severity', 0.5)
            
            # Calculer métriques
            coherence = self.calculate_semantic_coherence(atoms)
            frequency = self.frequency_estimates.get(concept1, 0.3)
            difficulty = self.calculate_resolution_difficulty(conflict)
            
            # Score priorité combiné
            # Formule: impact élevé si incohérent + fréquent + pas trop difficile
            priority = (
                (1.0 - coherence) * 0.4 +     # Plus incohérent = plus prioritaire
                frequency * 0.3 +              # Plus fréquent = plus prioritaire  
                severity * 0.2 +               # Plus sévère = plus prioritaire
                (1.0 - difficulty) * 0.1       # Moins difficile = plus prioritaire
            )
            
            # Classification priorité
            if priority >= 0.7:
                resolution_type = 'critical'
            elif priority >= 0.5:
                resolution_type = 'high'
            elif priority >= 0.3:
                resolution_type = 'medium'
            else:
                resolution_type = 'low'
            
            score = ConflictScore(
                conflict_id=conflict.get('conflict_id', ''),
                severity_raw=severity,
                semantic_coherence_score=coherence,
                frequency_impact_score=frequency,
                resolution_difficulty=difficulty,
                priority_score=priority,
                resolution_type=resolution_type
            )
            
            scored_conflicts.append(score)
        
        # Trier par priorité
        scored_conflicts.sort(key=lambda x: x.priority_score, reverse=True)
        
        # Statistiques
        by_priority = Counter(s.resolution_type for s in scored_conflicts)
        print(f"📊 Répartition priorités: {dict(by_priority)}")
        
        # Top 10 conflits prioritaires
        print(f"\n🔥 TOP 10 CONFLITS PRIORITAIRES:")
        for i, score in enumerate(scored_conflicts[:10]):
            concept = score.conflict_id.split('_')[-2] if '_' in score.conflict_id else 'N/A'
            print(f"   {i+1:2d}. {concept} ({score.resolution_type}, priorité: {score.priority_score:.2f})")
        
        return scored_conflicts
    
    def generate_automatic_refinements(self, top_conflicts: List[ConflictScore]) -> List[AutomaticRefinementSuggestion]:
        """Génère suggestions automatiques de raffinement"""
        
        print(f"\n⚙️ GÉNÉRATION RAFFINEMENTS AUTOMATIQUES")
        print("=" * 50)
        
        suggestions = []
        
        # Dictionnaire de correspondances concepts -> conflits
        conflict_map = {}
        for conflict in self.conflicts:
            concept = conflict.get('concept_1', '')
            if concept:
                conflict_map[concept] = conflict
        
        for score in top_conflicts[:20]:  # Top 20 prioritaires
            
            concept_name = score.conflict_id.split('_')[-2] if '_' in score.conflict_id else ''
            if not concept_name or concept_name not in conflict_map:
                continue
                
            conflict_data = conflict_map[concept_name]
            atoms = conflict_data.get('decomposition_1', [])
            conflict_type = conflict_data.get('conflict_type', '')
            
            # Suggestion selon type conflit
            refinement = self._generate_refinement_for_concept(
                concept_name, atoms, conflict_type, score
            )
            
            if refinement:
                suggestions.append(refinement)
        
        print(f"✨ {len(suggestions)} suggestions générées")
        return suggestions
    
    def _generate_refinement_for_concept(self, concept: str, atoms: List[str], 
                                       conflict_type: str, score: ConflictScore) -> AutomaticRefinementSuggestion:
        """Génère raffinement spécifique pour un concept"""
        
        # Analyses linguistiques par concept
        refinements = {
            'AMOUR': {
                'atoms': ['EMOTION', 'COMMUNICATION', 'POSSESSION', 'CREATION'],
                'contextual_dimensions': ['romantique', 'familial', 'platonique', 'universel'],
                'description': 'Sentiment d\'attachement profond incluant dimensions affective, communicative et créatrice',
                'confidence': 0.9
            },
            'MUSIQUE': {
                'atoms': ['COMMUNICATION', 'CREATION', 'EMOTION', 'MOUVEMENT'],
                'contextual_dimensions': ['artistique', 'rythmique', 'harmonique', 'culturel'],
                'description': 'Art sonore combinant expression créative, communication émotionnelle et organisation temporelle',
                'confidence': 0.8
            },
            'ÉTOILE': {
                'atoms': ['EXISTENCE', 'PERCEPTION', 'MOUVEMENT'],
                'contextual_dimensions': ['astronomique', 'symbolique', 'navigationnel', 'métaphorique'],
                'description': 'Corps céleste perceptible servant de référence spatiale et symbolique',
                'confidence': 0.7
            },
            'DÉGOÛT': {
                'atoms': ['EMOTION', 'DESTRUCTION', 'PERCEPTION'],
                'contextual_dimensions': ['physiologique', 'moral', 'esthétique', 'social'],
                'description': 'Répulsion émotionnelle face à stimulus perçu comme négatif ou contaminant',
                'confidence': 0.8
            }
        }
        
        if concept not in refinements:
            # Raffinement générique
            suggested_refinement = {
                'atoms': atoms + ['CONTEXTE'],  # Ajout dimension contextuelle
                'contextual_dimensions': ['général', 'spécialisé'],
                'description': f'Concept {concept} nécessitant spécification contextuelle',
                'confidence': 0.4
            }
        else:
            suggested_refinement = refinements[concept]
        
        return AutomaticRefinementSuggestion(
            concept_name=concept,
            current_definition=atoms,
            conflict_type=conflict_type,
            suggested_refinement=suggested_refinement,
            confidence_score=suggested_refinement['confidence'],
            linguistic_analysis={
                'semantic_field': self._identify_semantic_field(concept),
                'etymology_hints': self._get_etymology_hints(concept),
                'cross_cultural_variants': []
            },
            contextual_dimensions=suggested_refinement['contextual_dimensions']
        )
    
    def _identify_semantic_field(self, concept: str) -> str:
        """Identifie champ sémantique principal"""
        emotion_concepts = ['AMOUR', 'JOIE', 'TRISTESSE', 'PEUR', 'COLÈRE', 'DÉGOÛT']
        if concept in emotion_concepts:
            return 'émotions'
        
        art_concepts = ['MUSIQUE', 'ART', 'LITTÉRATURE', 'ARCHITECTURE']
        if concept in art_concepts:
            return 'arts'
            
        return 'général'
    
    def _get_etymology_hints(self, concept: str) -> str:
        """Indices étymologiques pour affiner définition"""
        etymologies = {
            'AMOUR': 'latin amor - attachement, désir',
            'MUSIQUE': 'grec mousikē - art des Muses', 
            'ÉTOILE': 'latin stella - point lumineux',
            'DÉGOÛT': 'dé-goût - perte du goût/plaisir'
        }
        return etymologies.get(concept, '')
    
    def generate_full_detection_report(self) -> Dict[str, Any]:
        """Génère rapport complet de détection automatique"""
        
        print(f"\n🎯 RAPPORT FINAL DÉTECTION AUTOMATIQUE")
        print("=" * 60)
        
        # Scoring complet
        scored_conflicts = self.score_all_conflicts()
        
        # Suggestions raffinement
        suggestions = self.generate_automatic_refinements(scored_conflicts)
        
        # Analyse globale
        total_conflicts = len(scored_conflicts)
        critical_conflicts = [s for s in scored_conflicts if s.resolution_type == 'critical']
        
        avg_coherence = np.mean([s.semantic_coherence_score for s in scored_conflicts])
        
        report = {
            'timestamp': '2025-09-27T13:45:00Z',
            'detection_method': 'automatic_scoring_v2.0',
            'analysis_summary': {
                'total_conflicts_analyzed': total_conflicts,
                'critical_conflicts': len(critical_conflicts),
                'average_semantic_coherence': float(avg_coherence),
                'refinement_suggestions_generated': len(suggestions)
            },
            'conflict_scores': [asdict(score) for score in scored_conflicts],
            'automatic_refinements': [asdict(sugg) for sugg in suggestions],
            'priority_actions': [
                'Traiter immédiatement conflits CRITICAL (priorité >= 0.7)',
                'Réviser définitions incohérentes majeures (AMOUR, MUSIQUE, etc.)',
                'Ajouter dimensions contextuelles aux concepts sous-spécifiés',
                'Tester raffinements sur corpus de validation'
            ],
            'methodology_notes': {
                'coherence_scoring': 'Basé sur patterns linguistiques et cohérence sémantique',
                'frequency_weighting': 'Concepts fréquents prioritaires pour impact utilisateur',
                'difficulty_assessment': 'Estimation complexité raffinement requis',
                'confidence_levels': 'Suggestions avec scores confiance pour validation'
            }
        }
        
        print(f"📊 RÉSULTATS FINAUX:")
        print(f"   • Conflits analysés: {total_conflicts}")
        print(f"   • Conflits critiques: {len(critical_conflicts)}")
        print(f"   • Cohérence moyenne: {avg_coherence:.2f}")
        print(f"   • Suggestions: {len(suggestions)}")
        
        return report
    
    def save_detection_report(self, report: Dict[str, Any], output_path: str):
        """Sauvegarde rapport de détection"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 Rapport détection sauvegardé: {output_path}")
            print(f"📏 Taille: {len(json.dumps(report, ensure_ascii=False))} caractères")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")

def main():
    """Test système détection automatique"""
    import glob
    import os
    
    # Trouver dernier rapport d'analyse
    reports = glob.glob("analyse_ambiguites_dictionnaire_*.json")
    if not reports:
        print("❌ Aucun rapport d'analyse trouvé")
        return
    
    latest_report = max(reports, key=os.path.getctime)
    print(f"📄 Utilisation rapport: {latest_report}")
    
    # Initialiser détecteur
    detector = AutomaticAmbiguityDetector(latest_report)
    
    # Générer rapport complet
    report = detector.generate_full_detection_report()
    
    # Sauvegarder
    output_path = "rapport_detection_automatique_ambiguites.json"
    detector.save_detection_report(report, output_path)
    
    print(f"\n✅ DÉTECTION AUTOMATIQUE TERMINÉE")

if __name__ == "__main__":
    main()