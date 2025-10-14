#!/usr/bin/env python3
"""
PROCESSUS DE RAFFINEMENT DÉFINITIONS SÉMANTIQUES v3.0
===================================================

Pipeline intelligent pour corriger les ambiguïtés détectées et enrichir
les définitions avec dimensions contextuelles, connotatives et pragmatiques.

Basé sur l'analyse des 154 conflits et suggestions automatiques générées.
"""

import json
import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import time
import os

@dataclass
class RefinedConcept:
    """Concept raffiné avec définition enrichie"""
    original_name: str
    refined_atoms: List[str]
    contextual_dimensions: Dict[str, Any]
    connotative_aspects: Dict[str, float]
    pragmatic_constraints: List[str]
    usage_patterns: Dict[str, List[str]]
    confidence_score: float
    linguistic_justification: str

@dataclass
class RefinementOperation:
    """Opération de raffinement appliquée"""
    concept_name: str
    operation_type: str  # 'add_dimension', 'replace_atoms', 'split_concept', 'merge_concepts'
    before_state: Dict[str, Any]
    after_state: Dict[str, Any]
    rationale: str
    validation_tests: List[str]

class DefinitionRefinementProcessor:
    """Processeur principal de raffinement des définitions"""
    
    def __init__(self, ambiguity_report_path: str, detection_report_path: str):
        self.ambiguity_report_path = ambiguity_report_path
        self.detection_report_path = detection_report_path
        
        # Charger données d'analyse
        self.ambiguity_data = self._load_json_report(ambiguity_report_path)
        self.detection_data = self._load_json_report(detection_report_path)
        
        # Données raffinement
        self.current_concepts = self._extract_current_concepts()
        self.conflict_priorities = self._extract_conflict_priorities()
        
        # Bibliothèques de raffinement
        self.contextual_dimensions_db = self._build_contextual_dimensions()
        self.connotative_profiles_db = self._build_connotative_profiles()
        self.pragmatic_constraints_db = self._build_pragmatic_constraints()
        
        print(f"🔧 Processeur raffinement initialisé")
        print(f"📊 {len(self.current_concepts)} concepts à traiter")
        print(f"🎯 {len(self.conflict_priorities)} conflits prioritaires")
    
    def _load_json_report(self, path: str) -> Dict:
        """Charge rapport JSON avec gestion erreurs"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Erreur chargement {path}: {e}")
            return {}
    
    def _extract_current_concepts(self) -> Dict[str, Dict]:
        """Extrait concepts actuels avec leurs définitions"""
        concepts = {}
        
        # Depuis analyse ambiguïtés
        quality_analyses = self.ambiguity_data.get('quality_analyses', {})
        
        for concept_name, analysis in quality_analyses.items():
            if isinstance(analysis, dict):
                concepts[concept_name] = {
                    'atoms': analysis.get('atomic_decomposition', []),
                    'complexity': analysis.get('complexity_level', 0),
                    'validity': analysis.get('validity_score', 0.5),
                    'quality': analysis.get('description_quality', 'unknown'),
                    'issues': analysis.get('potential_issues', [])
                }
        
        return concepts
    
    def _extract_conflict_priorities(self) -> List[Dict]:
        """Extrait conflits avec priorités du système détection"""
        conflicts = self.detection_data.get('conflict_scores', [])
        
        # Filtrer conflits haute priorité
        high_priority = [
            c for c in conflicts 
            if c.get('resolution_type') in ['critical', 'high'] and 
               c.get('priority_score', 0) > 0.5
        ]
        
        return sorted(high_priority, key=lambda x: x.get('priority_score', 0), reverse=True)
    
    def _build_contextual_dimensions(self) -> Dict[str, Dict]:
        """Base de données dimensions contextuelles par domaine sémantique"""
        return {
            'emotions': {
                'AMOUR': {
                    'romantic': {'weight': 0.4, 'markers': ['passion', 'intimité', 'exclusivité']},
                    'familial': {'weight': 0.3, 'markers': ['protection', 'inconditionalité', 'permanence']},
                    'platonique': {'weight': 0.2, 'markers': ['admiration', 'respect', 'spiritualité']},
                    'universel': {'weight': 0.1, 'markers': ['compassion', 'humanité', 'altruisme']}
                },
                'JOIE': {
                    'euphoric': {'weight': 0.2, 'markers': ['extase', 'débordement', 'temporaire']},
                    'contentement': {'weight': 0.4, 'markers': ['satisfaction', 'sérénité', 'durable']},
                    'social': {'weight': 0.3, 'markers': ['partage', 'contagion', 'célébration']},
                    'achievement': {'weight': 0.1, 'markers': ['fierté', 'accomplissement', 'mérite']}
                },
                'TRISTESSE': {
                    'melancholic': {'weight': 0.3, 'markers': ['nostalgie', 'poésie', 'douce-amère']},
                    'grief': {'weight': 0.4, 'markers': ['deuil', 'perte', 'profonde']},
                    'disappointment': {'weight': 0.2, 'markers': ['déception', 'attente', 'temporaire']},
                    'existential': {'weight': 0.1, 'markers': ['vide', 'sens', 'métaphysique']}
                }
            },
            'arts': {
                'MUSIQUE': {
                    'performance': {'weight': 0.3, 'markers': ['exécution', 'virtuosité', 'live']},
                    'composition': {'weight': 0.2, 'markers': ['création', 'harmonie', 'structure']},
                    'reception': {'weight': 0.3, 'markers': ['écoute', 'émotion', 'interprétation']},
                    'cultural': {'weight': 0.2, 'markers': ['tradition', 'identité', 'social']}
                },
                'ART': {
                    'visual': {'weight': 0.4, 'markers': ['image', 'forme', 'couleur']},
                    'conceptual': {'weight': 0.2, 'markers': ['idée', 'concept', 'critique']},
                    'expressive': {'weight': 0.3, 'markers': ['émotion', 'personnel', 'subjectif']},
                    'social': {'weight': 0.1, 'markers': ['société', 'politique', 'message']}
                }
            },
            'nature': {
                'ÉTOILE': {
                    'astronomical': {'weight': 0.4, 'markers': ['cosmos', 'physique', 'distance']},
                    'navigational': {'weight': 0.2, 'markers': ['orientation', 'guide', 'reference']},
                    'symbolic': {'weight': 0.3, 'markers': ['destin', 'espoir', 'rêve']},
                    'mythological': {'weight': 0.1, 'markers': ['légende', 'divinité', 'ancestral']}
                }
            }
        }
    
    def _build_connotative_profiles(self) -> Dict[str, Dict[str, float]]:
        """Profils connotatifs (valence émotionnelle) par concept"""
        return {
            'AMOUR': {'positive': 0.8, 'intensity': 0.9, 'complexity': 0.7, 'universality': 0.8},
            'JOIE': {'positive': 0.9, 'intensity': 0.7, 'complexity': 0.3, 'universality': 0.9},
            'TRISTESSE': {'positive': 0.1, 'intensity': 0.6, 'complexity': 0.5, 'universality': 0.8},
            'MUSIQUE': {'positive': 0.7, 'intensity': 0.6, 'complexity': 0.8, 'universality': 0.9},
            'ÉTOILE': {'positive': 0.6, 'intensity': 0.4, 'complexity': 0.6, 'universality': 0.7},
            'DÉGOÛT': {'positive': 0.1, 'intensity': 0.8, 'complexity': 0.4, 'universality': 0.6}
        }
    
    def _build_pragmatic_constraints(self) -> Dict[str, List[str]]:
        """Contraintes pragmatiques d'usage par concept"""
        return {
            'AMOUR': [
                'Nécessite réciprocité contextuelle',
                'Intensité variable selon relation', 
                'Aspectuel: peut être processuel ou statique',
                'Culturellement variable dans expression'
            ],
            'MUSIQUE': [
                'Nécessite support/medium',
                'Temporellement structurée',
                'Socialement partageable',
                'Techniquement produire'
            ],
            'ÉTOILE': [
                'Référence visuelle nécessaire',
                'Distance conceptuelle importante',
                'Usage métaphorique fréquent',
                'Contexte observation requis'
            ]
        }
    
    def process_high_priority_refinements(self) -> List[RefinedConcept]:
        """Traite raffinements haute priorité"""
        
        print(f"\n🎯 TRAITEMENT RAFFINEMENTS HAUTE PRIORITÉ")
        print("=" * 55)
        
        refined_concepts = []
        
        # Traiter top 20 conflits prioritaires
        top_conflicts = self.conflict_priorities[:20]
        
        for i, conflict in enumerate(top_conflicts):
            concept_name = self._extract_concept_from_conflict_id(conflict.get('conflict_id', ''))
            
            if not concept_name or concept_name not in self.current_concepts:
                continue
            
            print(f"\n🔧 Raffinement {i+1}/20: {concept_name}")
            
            # Appliquer raffinement spécialisé
            refined_concept = self._refine_specific_concept(concept_name, conflict)
            
            if refined_concept:
                refined_concepts.append(refined_concept)
                print(f"   ✅ Raffiné (confiance: {refined_concept.confidence_score:.2f})")
            else:
                print(f"   ❌ Échec raffinement")
        
        return refined_concepts
    
    def _extract_concept_from_conflict_id(self, conflict_id: str) -> str:
        """Extrait nom concept depuis ID conflit"""
        # Format: "incoherent_CONCEPT" ou "semantic_conflict_CONCEPT1_CONCEPT2"
        parts = conflict_id.split('_')
        if len(parts) >= 2:
            # Pour "incoherent_CONCEPT", retourner CONCEPT
            if parts[0] == 'incoherent' and len(parts) == 2:
                return parts[1]
            # Pour "semantic_conflict_X_Y", retourner le premier concept
            elif 'conflict' in conflict_id and len(parts) >= 3:
                return parts[-2]
            # Cas général: dernier élément
            else:
                return parts[-1]
        return ''
    
    def _refine_specific_concept(self, concept_name: str, conflict: Dict) -> Optional[RefinedConcept]:
        """Raffine concept spécifique selon conflit détecté"""
        
        current_def = self.current_concepts.get(concept_name, {})
        current_atoms = current_def.get('atoms', [])
        
        # Raffinements spécialisés par concept problématique
        if concept_name == 'AMOUR':
            return self._refine_amour_concept(current_atoms, conflict)
        elif concept_name == 'MUSIQUE':
            return self._refine_musique_concept(current_atoms, conflict)
        elif concept_name == 'ÉTOILE':
            return self._refine_etoile_concept(current_atoms, conflict)
        elif concept_name == 'DÉGOÛT':
            return self._refine_degout_concept(current_atoms, conflict)
        else:
            # Raffinement générique
            return self._refine_generic_concept(concept_name, current_atoms, conflict)
    
    def _refine_amour_concept(self, current_atoms: List[str], conflict: Dict) -> RefinedConcept:
        """Raffinement spécialisé pour AMOUR"""
        
        # Nouvelles dimensions atomiques cohérentes
        refined_atoms = ['EMOTION', 'COMMUNICATION', 'POSSESSION', 'CREATION']
        
        # Dimensions contextuelles riches
        contextual_dims = self.contextual_dimensions_db['emotions']['AMOUR']
        
        return RefinedConcept(
            original_name='AMOUR',
            refined_atoms=refined_atoms,
            contextual_dimensions=contextual_dims,
            connotative_aspects=self.connotative_profiles_db['AMOUR'],
            pragmatic_constraints=self.pragmatic_constraints_db['AMOUR'],
            usage_patterns={
                'romantic': ['aimer passionnément', 'être amoureux de', 'éprouver de l\'amour'],
                'familial': ['amour maternel', 'amour filial', 'amour fraternel'],
                'platonique': ['amour spirituel', 'amour pur', 'amour désintéressé'],
                'universel': ['amour de l\'humanité', 'amour universel', 'amour divin']
            },
            confidence_score=0.9,
            linguistic_justification="Remplacement DESTRUCTION par CREATION + ajout dimensions contextuelles multiples pour capturer richesse sémantique"
        )
    
    def _refine_musique_concept(self, current_atoms: List[str], conflict: Dict) -> RefinedConcept:
        """Raffinement spécialisé pour MUSIQUE"""
        
        refined_atoms = ['COMMUNICATION', 'CREATION', 'EMOTION', 'MOUVEMENT']
        contextual_dims = self.contextual_dimensions_db['arts']['MUSIQUE']
        
        return RefinedConcept(
            original_name='MUSIQUE',
            refined_atoms=refined_atoms,
            contextual_dimensions=contextual_dims,
            connotative_aspects=self.connotative_profiles_db['MUSIQUE'],
            pragmatic_constraints=self.pragmatic_constraints_db['MUSIQUE'],
            usage_patterns={
                'performance': ['jouer de la musique', 'interpréter', 'exécuter'],
                'composition': ['composer', 'créer', 'arranger'],
                'reception': ['écouter', 'apprécier', 'ressentir'],
                'cultural': ['tradition musicale', 'identité culturelle', 'patrimoine']
            },
            confidence_score=0.8,
            linguistic_justification="Ajout COMMUNICATION/CREATION/EMOTION pour capturer art complet vs DESTRUCTION/MOUVEMENT réducteur"
        )
    
    def _refine_etoile_concept(self, current_atoms: List[str], conflict: Dict) -> RefinedConcept:
        """Raffinement spécialisé pour ÉTOILE"""
        
        refined_atoms = ['EXISTENCE', 'PERCEPTION', 'MOUVEMENT']
        contextual_dims = self.contextual_dimensions_db['nature']['ÉTOILE']
        
        return RefinedConcept(
            original_name='ÉTOILE',
            refined_atoms=refined_atoms,
            contextual_dimensions=contextual_dims,
            connotative_aspects=self.connotative_profiles_db['ÉTOILE'],
            pragmatic_constraints=self.pragmatic_constraints_db['ÉTOILE'],
            usage_patterns={
                'astronomical': ['étoile fixe', 'magnitude', 'constellation'],
                'navigational': ['étoile polaire', 's\'orienter', 'navigation'],
                'symbolic': ['étoile du destin', 'étoile filante', 'étoile de l\'espoir'],
                'mythological': ['étoile des bergers', 'étoile du matin', 'voûte céleste']
            },
            confidence_score=0.7,
            linguistic_justification="Ajout EXISTENCE/PERCEPTION/MOUVEMENT pour corps céleste vs COMMUNICATION seule inadéquate"
        )
    
    def _refine_degout_concept(self, current_atoms: List[str], conflict: Dict) -> RefinedConcept:
        """Raffinement spécialisé pour DÉGOÛT"""
        
        refined_atoms = ['EMOTION', 'DESTRUCTION', 'PERCEPTION']
        
        return RefinedConcept(
            original_name='DÉGOÛT',
            refined_atoms=refined_atoms,
            contextual_dimensions={
                'physiological': {'weight': 0.4, 'markers': ['nausée', 'répulsion', 'corporel']},
                'moral': {'weight': 0.3, 'markers': ['indignation', 'éthique', 'valeurs']},
                'aesthetic': {'weight': 0.2, 'markers': ['laideur', 'dysharmonie', 'goût']},
                'social': {'weight': 0.1, 'markers': ['rejet', 'exclusion', 'norme']}
            },
            connotative_aspects=self.connotative_profiles_db['DÉGOÛT'],
            pragmatic_constraints=[
                'Réaction involontaire à stimulus',
                'Gradable en intensité',
                'Peut être culturellement conditionné',
                'Aspect protecteur évolutionnaire'
            ],
            usage_patterns={
                'physiological': ['avoir des nausées', 'répugner', 'écœurer'],
                'moral': ['être indigné', 'réprouver', 'condamner'],
                'aesthetic': ['trouver laid', 'déplaire', 'choquer'],
                'social': ['rejeter', 'mépriser', 'exclure']
            },
            confidence_score=0.8,
            linguistic_justification="Ajout EMOTION/PERCEPTION pour capturer aspect réactionnel vs EXISTENCE seule insuffisante"
        )
    
    def _refine_generic_concept(self, concept_name: str, current_atoms: List[str], 
                               conflict: Dict) -> Optional[RefinedConcept]:
        """Raffinement générique pour concepts non spécialisés"""
        
        # Stratégie générique: ajouter dimension contextuelle
        refined_atoms = current_atoms + ['CONTEXT'] if 'CONTEXT' not in current_atoms else current_atoms
        
        return RefinedConcept(
            original_name=concept_name,
            refined_atoms=refined_atoms,
            contextual_dimensions={'generic': {'weight': 1.0, 'markers': ['contextuel', 'variable']}},
            connotative_aspects={'neutral': 0.5},
            pragmatic_constraints=['Nécessite spécification contextuelle'],
            usage_patterns={'generic': [f'utilisation de {concept_name}']},
            confidence_score=0.4,
            linguistic_justification="Raffinement générique avec ajout dimension contextuelle"
        )
    
    def generate_refined_dictionary(self, refined_concepts: List[RefinedConcept]) -> Dict[str, Any]:
        """Génère dictionnaire raffiné avec concepts améliorés"""
        
        print(f"\n📚 GÉNÉRATION DICTIONNAIRE RAFFINÉ")
        print("=" * 45)
        
        refined_dict = {
            'metadata': {
                'version': 'RAFFINÉ-v3.0',
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                'source_analysis': self.ambiguity_report_path,
                'refinement_count': len(refined_concepts),
                'methodology': 'ambiguity_resolution_with_contextual_enrichment'
            },
            'concepts_raffines': {},
            'operations_applied': [],
            'validation_tests': []
        }
        
        # Ajouter concepts raffinés
        for concept in refined_concepts:
            refined_dict['concepts_raffines'][concept.original_name] = asdict(concept)
        
        # Statistiques raffinement
        avg_confidence = np.mean([c.confidence_score for c in refined_concepts])
        print(f"📊 Concepts raffinés: {len(refined_concepts)}")
        print(f"📊 Confiance moyenne: {avg_confidence:.2f}")
        
        return refined_dict
    
    def run_complete_refinement_process(self) -> str:
        """Lance processus complet de raffinement"""
        
        print(f"\n🚀 DÉMARRAGE PROCESSUS COMPLET RAFFINEMENT")
        print("=" * 60)
        
        start_time = time.time()
        
        try:
            # Étape 1: Raffinements haute priorité
            refined_concepts = self.process_high_priority_refinements()
            
            # Étape 2: Génération dictionnaire raffiné
            refined_dictionary = self.generate_refined_dictionary(refined_concepts)
            
            # Étape 3: Sauvegarde
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = f"dictionnaire_raffine_{timestamp}.json"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(refined_dictionary, f, ensure_ascii=False, indent=2)
            
            duration = time.time() - start_time
            
            print(f"\n✅ RAFFINEMENT TERMINÉ")
            print(f"⏱️  Durée: {duration:.1f}s")
            print(f"💾 Dictionnaire raffiné: {output_path}")
            print(f"📊 Concepts traités: {len(refined_concepts)}")
            
            return output_path
            
        except Exception as e:
            print(f"❌ ERREUR RAFFINEMENT: {e}")
            import traceback
            traceback.print_exc()
            return ""

def main():
    """Lance processus raffinement définitions"""
    import glob
    
    print("🔧 DÉMARRAGE PROCESSUS RAFFINEMENT DÉFINITIONS")
    
    # Trouver rapports d'analyse
    ambiguity_reports = glob.glob("analyse_ambiguites_dictionnaire_*.json")
    detection_reports = glob.glob("rapport_detection_automatique_*.json")
    
    if not ambiguity_reports:
        print("❌ Aucun rapport d'ambiguïtés trouvé")
        return
        
    if not detection_reports:
        print("❌ Aucun rapport de détection trouvé")  
        return
    
    latest_ambiguity = max(ambiguity_reports, key=os.path.getctime)
    latest_detection = max(detection_reports, key=os.path.getctime)
    
    print(f"📄 Rapport ambiguïtés: {latest_ambiguity}")
    print(f"📄 Rapport détection: {latest_detection}")
    
    # Initialiser processeur
    processor = DefinitionRefinementProcessor(latest_ambiguity, latest_detection)
    
    # Lancer raffinement complet
    result_path = processor.run_complete_refinement_process()
    
    if result_path:
        print(f"\n🎯 SUCCÈS - Dictionnaire raffiné disponible: {result_path}")
    else:
        print(f"\n❌ ÉCHEC - Voir logs pour détails")

if __name__ == "__main__":
    main()