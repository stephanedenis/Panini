#!/usr/bin/env python3
"""
ANALYSEUR D'AMBIGUÏTÉS SÉMANTIQUES ULTIME
=======================================

Détecte et analyse les ambiguïtés, synonymies partielles et chevauchements
conceptuels dans nos dictionnaires PanLang pour affiner les définitions.

Problèmes identifiés :
- AMOUR = DESTRUCTION + PERCEPTION + EXISTENCE (incohérent sémantiquement)  
- Multiples concepts avec même décomposition atomique
- Synonymes partiels sans distinction connotative
- Définitions vides ou sous-spécifiées
"""

import json
import re
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
from pathlib import Path
import itertools
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AmbiguityConflict:
    """Conflit d'ambiguïté détecté entre concepts"""
    conflict_id: str
    concept_1: str
    concept_2: str
    conflict_type: str  # 'identical_decomposition', 'partial_synonym', 'incoherent_definition', 'missing_description'
    severity: float  # 0.0 = mineur, 1.0 = critique
    decomposition_1: List[str]
    decomposition_2: List[str]
    overlap_atoms: List[str]
    semantic_distance: float
    evidence: List[str]
    suggested_refinements: List[str]

@dataclass 
class ConceptAnalysis:
    """Analyse complète d'un concept"""
    concept_name: str
    atomic_decomposition: List[str]
    complexity_level: int
    validity_score: float
    source_type: str
    description_quality: str  # 'empty', 'minimal', 'adequate', 'rich'
    potential_issues: List[str]
    similar_concepts: List[Tuple[str, float]]  # (concept, similarity_score)
    contextual_variants: Dict[str, Any]

class UltimateAmbiguityAnalyzer:
    """Analyseur ultime d'ambiguïtés sémantiques"""
    
    def __init__(self, dictionnaire_path: str):
        self.dictionnaire_path = dictionnaire_path
        self.dictionnaire_data = self._load_dictionnaire()
        self.concepts = self._extract_concepts()
        self.atomic_decompositions = self._build_decomposition_index()
        self.conflicts = []
        
        logger.info(f"🔍 Chargé {len(self.concepts)} concepts pour analyse d'ambiguïtés")
    
    def _load_dictionnaire(self) -> Dict:
        """Charge le dictionnaire complet"""
        try:
            with open(self.dictionnaire_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ Erreur chargement dictionnaire: {e}")
            return {}
    
    def _extract_concepts(self) -> Dict[str, Dict]:
        """Extrait tous les concepts du dictionnaire"""
        concepts = {}
        
        if 'concepts' not in self.dictionnaire_data:
            logger.error("❌ Pas de section 'concepts' dans le dictionnaire")
            return concepts
            
        for concept_name, concept_data in self.dictionnaire_data['concepts'].items():
            if concept_name == 'CONCEPTS_ECHANTILLON':
                # Traiter l'échantillon spécial
                if isinstance(concept_data.get('formule'), str):
                    # Parse la formule JSON embedée
                    try:
                        formule_data = eval(concept_data['formule'])
                        if isinstance(formule_data, dict):
                            for sub_concept, sub_data in formule_data.items():
                                concepts[sub_concept] = sub_data
                    except Exception as e:
                        logger.warning(f"⚠️ Problème parsing CONCEPTS_ECHANTILLON: {e}")
                continue
            
            concepts[concept_name] = concept_data
            
        logger.info(f"📊 Extrait {len(concepts)} concepts individuels")
        return concepts
    
    def _build_decomposition_index(self) -> Dict[tuple, List[str]]:
        """Index des décompositions atomiques identiques"""
        index = defaultdict(list)
        
        for concept_name, concept_data in self.concepts.items():
            # Extraire atomes finaux
            if isinstance(concept_data, dict):
                if 'atomes_finaux' in concept_data:
                    atomes = tuple(sorted(concept_data['atomes_finaux']))
                    index[atomes].append(concept_name)
                elif 'decomposition' in concept_data:
                    atomes = tuple(sorted(concept_data['decomposition']))
                    index[atomes].append(concept_name)
        
        # Garder seulement les décompositions partagées
        shared_decompositions = {k: v for k, v in index.items() if len(v) > 1}
        
        logger.info(f"🔄 Identifié {len(shared_decompositions)} décompositions partagées")
        return shared_decompositions
    
    def analyze_identical_decompositions(self) -> List[AmbiguityConflict]:
        """Analyse les concepts avec décompositions identiques"""
        conflicts = []
        
        print("\n🔍 ANALYSE DES DÉCOMPOSITIONS IDENTIQUES")
        print("=" * 50)
        
        for decomposition, concept_list in self.atomic_decompositions.items():
            if len(concept_list) < 2:
                continue
                
            print(f"\n⚠️ Décomposition {list(decomposition)} partagée par:")
            for concept in concept_list:
                concept_data = self.concepts[concept]
                validite = concept_data.get('validite', 0)
                source = concept_data.get('source', 'inconnu')
                print(f"   • {concept} (validité: {validite:.2f}, source: {source})")
            
            # Créer conflit pour chaque paire
            for i, concept_1 in enumerate(concept_list):
                for concept_2 in concept_list[i+1:]:
                    conflict = AmbiguityConflict(
                        conflict_id=f"identical_{concept_1}_{concept_2}",
                        concept_1=concept_1,
                        concept_2=concept_2,
                        conflict_type="identical_decomposition",
                        severity=0.9,  # Très sévère
                        decomposition_1=list(decomposition),
                        decomposition_2=list(decomposition),
                        overlap_atoms=list(decomposition),
                        semantic_distance=0.0,
                        evidence=[f"Décomposition identique: {list(decomposition)}"],
                        suggested_refinements=[
                            f"Distinguer {concept_1} vs {concept_2} avec dimensions supplémentaires",
                            "Ajouter aspects contextuels/connotatifs",
                            "Réviser décompositions pour capturer nuances"
                        ]
                    )
                    conflicts.append(conflict)
        
        return conflicts
    
    def analyze_incoherent_definitions(self) -> List[AmbiguityConflict]:
        """Détecte définitions sémantiquement incohérentes"""
        conflicts = []
        incoherent_patterns = []
        
        print("\n💥 ANALYSE DES DÉFINITIONS INCOHÉRENTES")
        print("=" * 50)
        
        for concept_name, concept_data in self.concepts.items():
            if not isinstance(concept_data, dict):
                continue
                
            atomes = concept_data.get('atomes_finaux', concept_data.get('decomposition', []))
            
            # Patterns incohérents détectés
            if 'AMOUR' in concept_name.upper():
                if 'DESTRUCTION' in atomes:
                    evidence = f"AMOUR contient DESTRUCTION - contradiction sémantique"
                    incoherent_patterns.append((concept_name, evidence))
            
            if 'JOIE' in concept_name.upper() or 'BONHEUR' in concept_name.upper():
                if 'DESTRUCTION' in atomes and 'CREATION' not in atomes:
                    evidence = f"Émotion positive {concept_name} avec DESTRUCTION sans CREATION"
                    incoherent_patterns.append((concept_name, evidence))
            
            if 'MUSIQUE' in concept_name.upper():
                if set(atomes) == {'DESTRUCTION', 'MOUVEMENT'}:
                    evidence = f"MUSIQUE = DESTRUCTION + MOUVEMENT - réduction excessive"
                    incoherent_patterns.append((concept_name, evidence))
            
            if 'ÉTOILE' in concept_name.upper():
                if atomes == ['COMMUNICATION']:
                    evidence = f"ÉTOILE = COMMUNICATION - analogie douteuse"
                    incoherent_patterns.append((concept_name, evidence))
            
            # Descriptions vides
            description = concept_data.get('description', '')
            if not description or description.strip() == '':
                evidence = f"Définition vide pour {concept_name}"
                incoherent_patterns.append((concept_name, evidence))
        
        # Créer conflits
        for concept_name, evidence in incoherent_patterns:
            concept_data = self.concepts[concept_name]
            atomes = concept_data.get('atomes_finaux', concept_data.get('decomposition', []))
            
            conflict = AmbiguityConflict(
                conflict_id=f"incoherent_{concept_name}",
                concept_1=concept_name,
                concept_2="",
                conflict_type="incoherent_definition",
                severity=0.8,
                decomposition_1=atomes,
                decomposition_2=[],
                overlap_atoms=[],
                semantic_distance=1.0,
                evidence=[evidence],
                suggested_refinements=[
                    "Réviser décomposition atomique",
                    "Ajouter description sémantique riche",
                    "Considérer aspects métaphoriques/culturels"
                ]
            )
            conflicts.append(conflict)
            print(f"💥 {evidence}")
        
        return conflicts
    
    def analyze_partial_synonyms(self) -> List[AmbiguityConflict]:
        """Identifie synonymes partiels nécessitant distinction"""
        conflicts = []
        
        print("\n🔀 ANALYSE DES SYNONYMES PARTIELS")
        print("=" * 50)
        
        # Groupes sémantiques à examiner
        emotion_concepts = [name for name in self.concepts.keys() 
                          if any(atom in self.concepts[name].get('atomes_finaux', []) 
                                for atom in ['EMOTION'])]
        
        movement_concepts = [name for name in self.concepts.keys()
                           if any(atom in self.concepts[name].get('atomes_finaux', [])
                                 for atom in ['MOUVEMENT'])]
        
        communication_concepts = [name for name in self.concepts.keys()
                                if any(atom in self.concepts[name].get('atomes_finaux', [])
                                      for atom in ['COMMUNICATION'])]
        
        print(f"📊 Émotions: {len(emotion_concepts)}, Mouvements: {len(movement_concepts)}, Communications: {len(communication_concepts)}")
        
        # Analyser émotions similaires
        for i, concept_1 in enumerate(emotion_concepts):
            for concept_2 in emotion_concepts[i+1:]:
                data_1 = self.concepts[concept_1]
                data_2 = self.concepts[concept_2]
                
                atoms_1 = set(data_1.get('atomes_finaux', []))
                atoms_2 = set(data_2.get('atomes_finaux', []))
                
                overlap = atoms_1.intersection(atoms_2)
                similarity = len(overlap) / max(len(atoms_1), len(atoms_2), 1)
                
                if similarity > 0.6 and concept_1 != concept_2:
                    conflict = AmbiguityConflict(
                        conflict_id=f"partial_synonym_{concept_1}_{concept_2}",
                        concept_1=concept_1,
                        concept_2=concept_2,
                        conflict_type="partial_synonym",
                        severity=similarity,
                        decomposition_1=list(atoms_1),
                        decomposition_2=list(atoms_2),
                        overlap_atoms=list(overlap),
                        semantic_distance=1.0 - similarity,
                        evidence=[f"Similarité atomique: {similarity:.2f}"],
                        suggested_refinements=[
                            "Ajouter dimensions aspectuelles distinctives",
                            "Spécifier contextes d'usage différents",
                            "Enrichir avec connotations culturelles"
                        ]
                    )
                    conflicts.append(conflict)
                    print(f"🔀 {concept_1} ↔ {concept_2} (similarité: {similarity:.2f})")
        
        return conflicts
    
    def analyze_concept_quality(self) -> Dict[str, ConceptAnalysis]:
        """Analyse qualité de chaque concept"""
        analyses = {}
        
        print("\n📈 ANALYSE QUALITÉ DES CONCEPTS")
        print("=" * 50)
        
        quality_stats = {'empty': 0, 'minimal': 0, 'adequate': 0, 'rich': 0}
        
        for concept_name, concept_data in self.concepts.items():
            if not isinstance(concept_data, dict):
                continue
                
            # Évaluer qualité description
            description = concept_data.get('description', '')
            if not description or description.strip() == '':
                desc_quality = 'empty'
            elif len(description) < 20:
                desc_quality = 'minimal'  
            elif len(description) < 100:
                desc_quality = 'adequate'
            else:
                desc_quality = 'rich'
            
            quality_stats[desc_quality] += 1
            
            # Identifier issues
            issues = []
            atomes = concept_data.get('atomes_finaux', concept_data.get('decomposition', []))
            
            if len(atomes) == 1 and desc_quality == 'empty':
                issues.append("Concept atomique sans description")
            
            if len(atomes) > 4:
                issues.append("Décomposition potentiellement sur-complexe")
            
            validity = concept_data.get('validite', 0)
            if validity < 0.5:
                issues.append(f"Validité faible: {validity}")
            
            if concept_data.get('source') == 'wikipedia_directe_optimisee' and validity < 0.4:
                issues.append("Source automatique + validité faible")
            
            analysis = ConceptAnalysis(
                concept_name=concept_name,
                atomic_decomposition=atomes,
                complexity_level=len(atomes),
                validity_score=validity,
                source_type=concept_data.get('source', 'inconnu'),
                description_quality=desc_quality,
                potential_issues=issues,
                similar_concepts=[],
                contextual_variants={}
            )
            
            analyses[concept_name] = analysis
        
        print(f"📊 Qualité descriptions: {quality_stats}")
        return analyses
    
    def generate_ambiguity_report(self) -> Dict[str, Any]:
        """Génère rapport complet des ambiguïtés"""
        print("\n🎯 GÉNÉRATION RAPPORT D'AMBIGUÏTÉS COMPLET")
        print("=" * 60)
        
        # Analyses individuelles
        identical_conflicts = self.analyze_identical_decompositions()
        incoherent_conflicts = self.analyze_incoherent_definitions()
        partial_synonym_conflicts = self.analyze_partial_synonyms()
        quality_analyses = self.analyze_concept_quality()
        
        all_conflicts = identical_conflicts + incoherent_conflicts + partial_synonym_conflicts
        
        # Statistiques globales
        total_concepts = len(self.concepts)
        high_severity_conflicts = [c for c in all_conflicts if c.severity > 0.7]
        empty_descriptions = [name for name, analysis in quality_analyses.items() 
                            if analysis.description_quality == 'empty']
        
        low_validity_concepts = [name for name, data in self.concepts.items()
                               if isinstance(data, dict) and data.get('validite', 0) < 0.3]
        
        print(f"\n📊 STATISTIQUES FINALES:")
        print(f"   • Total concepts: {total_concepts}")
        print(f"   • Conflits détectés: {len(all_conflicts)}")
        print(f"   • Conflits sévères: {len(high_severity_conflicts)}")
        print(f"   • Descriptions vides: {len(empty_descriptions)}")
        print(f"   • Concepts faible validité: {len(low_validity_concepts)}")
        
        # Top conflits par sévérité
        sorted_conflicts = sorted(all_conflicts, key=lambda x: x.severity, reverse=True)
        print(f"\n🔥 TOP 10 CONFLITS LES PLUS SÉVÈRES:")
        for i, conflict in enumerate(sorted_conflicts[:10]):
            print(f"   {i+1:2d}. {conflict.concept_1} ({conflict.conflict_type}, sévérité: {conflict.severity:.2f})")
        
        return {
            'timestamp': '2025-01-21T10:00:00Z',
            'total_concepts': total_concepts,
            'conflicts': {
                'identical_decompositions': len(identical_conflicts),
                'incoherent_definitions': len(incoherent_conflicts), 
                'partial_synonyms': len(partial_synonym_conflicts),
                'total': len(all_conflicts)
            },
            'quality_issues': {
                'empty_descriptions': len(empty_descriptions),
                'low_validity_concepts': len(low_validity_concepts),
                'high_severity_conflicts': len(high_severity_conflicts)
            },
            'detailed_conflicts': [asdict(conflict) for conflict in sorted_conflicts],
            'quality_analyses': {name: asdict(analysis) for name, analysis in quality_analyses.items()},
            'recommendations': {
                'priority_1': [
                    "Résoudre conflits identiques (décompositions exactement égales)",
                    "Corriger définitions incohérentes (AMOUR=DESTRUCTION, etc.)",
                    "Ajouter descriptions pour concepts vides"
                ],
                'priority_2': [
                    "Distinguer synonymes partiels avec contexte/connotation",
                    "Réviser concepts Wikipedia faible validité",
                    "Simplifier décompositions sur-complexes"
                ],
                'methodology': [
                    "Analyse linguistique différentielle pour synonymes",
                    "Validation experte pour incohérences",
                    "Tests corpus pour vérifier améliorations"
                ]
            }
        }
    
    def save_report(self, report: Dict[str, Any], output_path: str):
        """Sauvegarde rapport d'analyse"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 Rapport sauvegardé: {output_path}")
            print(f"📏 Taille: {len(json.dumps(report, ensure_ascii=False))} caractères")
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde rapport: {e}")

def main():
    """Analyseur ambiguïtés avec protection processus"""
    import time
    import os
    
    print("🚀 DÉMARRAGE ANALYSEUR AMBIGUÏTÉS (mode sécurisé)")
    
    # Vérification registre processus
    registre_path = "registre_processus_actifs.json"
    if os.path.exists(registre_path):
        print("📋 Registre processus détecté - mode coordonné")
    
    try:
        # Chemin dictionnaire
        dictionnaire_path = "/home/stephane/GitHub/PaniniFS-Research/dictionnaire_panlang_ULTIME/dictionnaire_panlang_ULTIME_complet.json"
        
        # Vérifier existence fichier
        if not os.path.exists(dictionnaire_path):
            print(f"❌ Fichier dictionnaire non trouvé: {dictionnaire_path}")
            return
        
        print(f"📚 Dictionnaire trouvé: {dictionnaire_path}")
        
        # Initialiser analyseur
        print("🔧 Initialisation analyseur...")
        analyzer = UltimateAmbiguityAnalyzer(dictionnaire_path)
        
        # Générer rapport complet
        print("🔍 Génération rapport ambiguïtés...")
        report = analyzer.generate_ambiguity_report()
        
        # Sauvegarder avec timestamp
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_path = f"analyse_ambiguites_dictionnaire_{timestamp}.json"
        analyzer.save_report(report, output_path)
        
        print(f"\n✅ ANALYSE TERMINÉE - Rapport: {output_path}")
        print(f"📊 Conflits détectés: {report['conflicts']['total']}")
        print(f"🎯 Concepts analysés: {report['total_concepts']}")
        
        return output_path
        
    except Exception as e:
        print(f"❌ ERREUR ANALYSEUR: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()