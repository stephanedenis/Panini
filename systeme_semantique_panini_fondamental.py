#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SYSTÈME SÉMANTIQUE PANINI FONDAMENTAL
====================================
Modélisation de la sémantique Panini comme théorie de l'information universelle :
- Universaux sémantiques (pas seulement linguistiques)
- Composition fractale multi-niveaux
- Multi-domaine (mathématiques, physique, biologie, cognition)
- Fondements théoriques avant construction PanLang

Architecture:
- SemanticUniversals: Universaux fondamentaux
- FractalComposition: Structure compositionnelle
- MultiDomainMapping: Correspondances inter-domaines
- InformationTheory: Base théorique informationnelle
"""

import json
import logging
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod


@dataclass
class SemanticUniversal:
    """Universel sémantique fondamental"""
    id: str
    name: str
    category: str  # 'relation', 'entity', 'property', 'process'
    abstract_form: str  # Représentation abstraite
    domains: List[str]  # Domaines d'application
    composition_level: int  # Niveau fractal (0=atomique, 1=composé, etc.)
    information_content: float  # Contenu informationnel (bits)
    universality_score: float  # Score d'universalité (0-1)
    
    def __post_init__(self):
        """Validation post-initialisation"""
        if not 0 <= self.universality_score <= 1:
            raise ValueError("Universality score must be between 0 and 1")


@dataclass
class FractalCompositionRule:
    """Règle de composition fractale"""
    id: str
    name: str
    input_universals: List[str]  # IDs des universaux d'entrée
    output_universal: str  # ID de l'universel de sortie
    composition_type: str  # 'linear', 'recursive', 'emergent'
    fractal_depth: int  # Profondeur fractale
    information_transform: str  # Transformation informationnelle
    domains_preserved: List[str]  # Domaines préservés
    emergence_threshold: float  # Seuil d'émergence


@dataclass
class MultiDomainCorrespondence:
    """Correspondance multi-domaine"""
    universal_id: str
    domain_mappings: Dict[str, str]  # domaine -> représentation
    isomorphisms: Dict[str, List[str]]  # domaine -> domaines isomorphes
    transformation_rules: Dict[str, str]  # domaine_source -> règle_transform


class PaniniSemanticFoundation:
    """Fondement sémantique Panini - Théorie de l'information universelle"""
    
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Structures de données principales
        self.universals: Dict[str, SemanticUniversal] = {}
        self.composition_rules: Dict[str, FractalCompositionRule] = {}
        self.domain_correspondences: Dict[str, MultiDomainCorrespondence] = {}
        
        # Domaines supportés
        self.domains = {
            'mathematics': 'Structures mathématiques',
            'physics': 'Phénomènes physiques', 
            'biology': 'Processus biologiques',
            'cognition': 'Processus cognitifs',
            'linguistics': 'Structures linguistiques',
            'computation': 'Processus computationnels',
            'social': 'Structures sociales',
            'aesthetic': 'Patterns esthétiques'
        }
        
        # Métriques du système
        self.system_metrics = {
            'universals_count': 0,
            'composition_depth': 0,
            'domain_coverage': 0.0,
            'information_density': 0.0
        }
    
    def setup_logging(self):
        """Configuration logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('panini_semantic_foundation.log'),
                logging.StreamHandler()
            ]
        )
    
    def initialize_core_universals(self):
        """Initialiser les universaux sémantiques fondamentaux"""
        self.logger.info("🏗️  INITIALISATION UNIVERSAUX FONDAMENTAUX")
        
        # Universaux de base (niveau 0 - atomiques)
        core_universals = [
            # Relations fondamentales
            SemanticUniversal(
                id="rel_containment",
                name="Containment",
                category="relation",
                abstract_form="∈(x,y)",
                domains=['mathematics', 'physics', 'cognition', 'linguistics'],
                composition_level=0,
                information_content=1.5,
                universality_score=0.95
            ),
            SemanticUniversal(
                id="rel_causation", 
                name="Causation",
                category="relation",
                abstract_form="→(x,y)",
                domains=['physics', 'biology', 'cognition', 'social'],
                composition_level=0,
                information_content=2.1,
                universality_score=0.92
            ),
            SemanticUniversal(
                id="rel_similarity",
                name="Similarity", 
                category="relation",
                abstract_form="≈(x,y)",
                domains=['mathematics', 'cognition', 'linguistics', 'aesthetic'],
                composition_level=0,
                information_content=1.8,
                universality_score=0.88
            ),
            
            # Entités fondamentales
            SemanticUniversal(
                id="ent_boundary",
                name="Boundary",
                category="entity",
                abstract_form="∂(x)",
                domains=['mathematics', 'physics', 'biology', 'cognition'],
                composition_level=0,
                information_content=1.3,
                universality_score=0.90
            ),
            SemanticUniversal(
                id="ent_pattern",
                name="Pattern",
                category="entity", 
                abstract_form="π(x)",
                domains=['mathematics', 'biology', 'cognition', 'aesthetic'],
                composition_level=0,
                information_content=2.5,
                universality_score=0.94
            ),
            
            # Propriétés fondamentales
            SemanticUniversal(
                id="prop_intensity",
                name="Intensity",
                category="property",
                abstract_form="I(x)",
                domains=['physics', 'cognition', 'linguistics', 'aesthetic'],
                composition_level=0,
                information_content=1.7,
                universality_score=0.87
            ),
            SemanticUniversal(
                id="prop_continuity",
                name="Continuity",
                category="property",
                abstract_form="C(x)",
                domains=['mathematics', 'physics', 'cognition'],
                composition_level=0,
                information_content=2.0,
                universality_score=0.89
            ),
            
            # Processus fondamentaux  
            SemanticUniversal(
                id="proc_transformation",
                name="Transformation",
                category="process",
                abstract_form="T(x→y)",
                domains=['mathematics', 'physics', 'biology', 'cognition'],
                composition_level=0,
                information_content=2.3,
                universality_score=0.93
            ),
            SemanticUniversal(
                id="proc_iteration",
                name="Iteration", 
                category="process",
                abstract_form="Iter(x)",
                domains=['mathematics', 'computation', 'biology', 'cognition'],
                composition_level=0,
                information_content=1.9,
                universality_score=0.85
            )
        ]
        
        # Ajouter au système
        for universal in core_universals:
            self.universals[universal.id] = universal
        
        self.system_metrics['universals_count'] = len(self.universals)
        self.logger.info(f"✅ {len(core_universals)} universaux fondamentaux initialisés")
    
    def create_fractal_composition_rules(self):
        """Créer règles de composition fractale"""
        self.logger.info("🔄 CRÉATION RÈGLES COMPOSITION FRACTALE")
        
        composition_rules = [
            # Composition causale-contenante
            FractalCompositionRule(
                id="comp_causal_containment",
                name="Causal Containment",
                input_universals=["rel_causation", "rel_containment"],
                output_universal="rel_causal_containment",
                composition_type="emergent",
                fractal_depth=1,
                information_transform="∈(→(x,y), z) = ∈(x,z) ∧ →(y,z)",
                domains_preserved=['physics', 'cognition'],
                emergence_threshold=0.7
            ),
            
            # Pattern-Iteration
            FractalCompositionRule(
                id="comp_iterative_pattern",
                name="Iterative Pattern",
                input_universals=["ent_pattern", "proc_iteration"],
                output_universal="ent_iterative_pattern",
                composition_type="recursive",
                fractal_depth=2,
                information_transform="π(Iter(x)) = π(x)^n",
                domains_preserved=['mathematics', 'biology', 'aesthetic'],
                emergence_threshold=0.8
            ),
            
            # Transformation-Boundary
            FractalCompositionRule(
                id="comp_boundary_transform",
                name="Boundary Transformation",
                input_universals=["proc_transformation", "ent_boundary"],
                output_universal="proc_boundary_transform",
                composition_type="linear",
                fractal_depth=1,
                information_transform="T(∂(x)) = ∂(T(x))",
                domains_preserved=['mathematics', 'physics', 'biology'],
                emergence_threshold=0.6
            ),
            
            # Similarity-Intensity
            FractalCompositionRule(
                id="comp_intensive_similarity",
                name="Intensive Similarity",
                input_universals=["rel_similarity", "prop_intensity"],
                output_universal="rel_intensive_similarity", 
                composition_type="emergent",
                fractal_depth=1,
                information_transform="≈(I(x), I(y)) → ≈(x,y)",
                domains_preserved=['cognition', 'aesthetic'],
                emergence_threshold=0.75
            )
        ]
        
        # Ajouter au système
        for rule in composition_rules:
            self.composition_rules[rule.id] = rule
        
        self.system_metrics['composition_depth'] = max(r.fractal_depth for r in composition_rules)
        self.logger.info(f"✅ {len(composition_rules)} règles de composition créées")
    
    def establish_multidomain_correspondences(self):
        """Établir correspondances multi-domaines"""
        self.logger.info("🌐 ÉTABLISSEMENT CORRESPONDANCES MULTI-DOMAINES")
        
        # Exemples de correspondances pour universaux clés
        correspondences = [
            MultiDomainCorrespondence(
                universal_id="rel_containment",
                domain_mappings={
                    'mathematics': 'x ∈ S (set membership)',
                    'physics': 'particle in field region', 
                    'cognition': 'concept in mental space',
                    'linguistics': 'morpheme in word'
                },
                isomorphisms={
                    'mathematics': ['physics', 'cognition'],
                    'physics': ['biology'],
                    'cognition': ['linguistics']
                },
                transformation_rules={
                    'mathematics->physics': 'set_membership → spatial_containment',
                    'physics->cognition': 'spatial → conceptual_space',
                    'cognition->linguistics': 'mental_space → linguistic_structure'
                }
            ),
            
            MultiDomainCorrespondence(
                universal_id="proc_transformation",
                domain_mappings={
                    'mathematics': 'f: X → Y (function)',
                    'physics': 'state transition',
                    'biology': 'metabolic process',
                    'cognition': 'mental state change',
                    'computation': 'algorithm step'
                },
                isomorphisms={
                    'mathematics': ['computation'],
                    'physics': ['biology'],
                    'cognition': ['linguistics']
                },
                transformation_rules={
                    'mathematics->computation': 'function → algorithm',
                    'physics->biology': 'physical_process → biological_process',
                    'cognition->linguistics': 'mental_change → grammatical_transform'
                }
            ),
            
            MultiDomainCorrespondence(
                universal_id="ent_pattern",
                domain_mappings={
                    'mathematics': 'mathematical structure',
                    'physics': 'wave interference',
                    'biology': 'genetic sequence',
                    'cognition': 'mental schema',
                    'aesthetic': 'artistic motif'
                },
                isomorphisms={
                    'mathematics': ['physics', 'computation'],
                    'biology': ['cognition'],
                    'aesthetic': ['cognition', 'linguistics']
                },
                transformation_rules={
                    'mathematics->physics': 'structure → wave_pattern',
                    'biology->cognition': 'genetic_pattern → mental_schema',
                    'aesthetic->linguistics': 'artistic_motif → linguistic_pattern'
                }
            )
        ]
        
        # Ajouter au système
        for correspondence in correspondences:
            self.domain_correspondences[correspondence.universal_id] = correspondence
        
        # Calculer couverture domaines
        covered_domains = set()
        for corr in correspondences:
            covered_domains.update(corr.domain_mappings.keys())
        
        self.system_metrics['domain_coverage'] = len(covered_domains) / len(self.domains)
        self.logger.info(f"✅ {len(correspondences)} correspondances établies")
        self.logger.info(f"   Couverture domaines: {self.system_metrics['domain_coverage']:.2%}")
    
    def calculate_information_metrics(self):
        """Calculer métriques informationnelles du système"""
        self.logger.info("📊 CALCUL MÉTRIQUES INFORMATIONNELLES")
        
        # Densité informationnelle totale
        total_information = sum(u.information_content for u in self.universals.values())
        total_universals = len(self.universals)
        
        if total_universals > 0:
            self.system_metrics['information_density'] = total_information / total_universals
        
        # Métriques par catégorie
        categories = {}
        for universal in self.universals.values():
            if universal.category not in categories:
                categories[universal.category] = {
                    'count': 0,
                    'total_information': 0.0,
                    'avg_universality': 0.0
                }
            
            categories[universal.category]['count'] += 1
            categories[universal.category]['total_information'] += universal.information_content
            categories[universal.category]['avg_universality'] += universal.universality_score
        
        # Moyennes par catégorie
        for category, data in categories.items():
            if data['count'] > 0:
                data['avg_information'] = data['total_information'] / data['count']
                data['avg_universality'] = data['avg_universality'] / data['count']
        
        self.system_metrics['categories'] = categories
        
        self.logger.info(f"   Densité informationnelle: {self.system_metrics['information_density']:.2f} bits/universel")
        self.logger.info(f"   Catégories: {list(categories.keys())}")
    
    def generate_semantic_foundation_report(self) -> str:
        """Générer rapport complet du fondement sémantique"""
        self.logger.info("📋 GÉNÉRATION RAPPORT FONDEMENT SÉMANTIQUE")
        
        report = f"""
🧠 SYSTÈME SÉMANTIQUE PANINI - FONDEMENT THÉORIQUE
=================================================
Généré le: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

📊 MÉTRIQUES SYSTÈME:
• Universaux fondamentaux: {self.system_metrics['universals_count']}
• Profondeur compositionnelle: {self.system_metrics['composition_depth']} niveaux
• Couverture domaines: {self.system_metrics['domain_coverage']:.1%}
• Densité informationnelle: {self.system_metrics['information_density']:.2f} bits/universel

🏗️  UNIVERSAUX PAR CATÉGORIE:
"""
        
        categories = self.system_metrics.get('categories', {})
        for category, data in categories.items():
            report += f"""
• {category.upper()}: {data['count']} universaux
  - Information moyenne: {data.get('avg_information', 0):.2f} bits
  - Universalité moyenne: {data.get('avg_universality', 0):.2f}
"""
        
        report += f"""
🌐 DOMAINES COUVERTS:
{chr(10).join(f"• {domain}: {desc}" for domain, desc in self.domains.items())}

🔄 RÈGLES COMPOSITION FRACTALE:
• Règles définies: {len(self.composition_rules)}
• Types: {list(set(r.composition_type for r in self.composition_rules.values()))}
• Profondeur maximale: {max((r.fractal_depth for r in self.composition_rules.values()), default=0)}

📡 CORRESPONDANCES MULTI-DOMAINES:
• Universaux mappés: {len(self.domain_correspondences)}
• Isomorphismes identifiés: {sum(len(c.isomorphisms) for c in self.domain_correspondences.values())}

🎯 FONDEMENTS THÉORIQUES:
1. UNIVERSAUX SÉMANTIQUES: Concepts fondamentaux trans-domaines
2. COMPOSITION FRACTALE: Structure récursive multi-niveaux  
3. MULTI-DOMAINE: Correspondances mathématiques ↔ physique ↔ cognition
4. THÉORIE INFORMATION: Quantification sémantique (bits)

🚀 IMPLICATIONS POUR PANLANG:
• Base sémantique universelle définie
• Compositionalité fractale pour morphologie
• Correspondances cross-domaines pour métaphore
• Métriques informationnelles pour optimisation

📋 PROCHAINES ÉTAPES:
1. Expansion universaux (niveau 1-2 composition)
2. Implémentation moteur inférence
3. Intégration théorie dhātu
4. Architecture PanLang basée sur fondements

✅ FONDEMENT SÉMANTIQUE PANINI ÉTABLI
Base théorique ready pour construction PanLang
"""
        
        report_file = f"PANINI_SEMANTIC_FOUNDATION_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            # Sauvegarder données JSON
            json_data = {
                'universals': {uid: asdict(u) for uid, u in self.universals.items()},
                'composition_rules': {rid: asdict(r) for rid, r in self.composition_rules.items()},
                'domain_correspondences': {cid: asdict(c) for cid, c in self.domain_correspondences.items()},
                'system_metrics': self.system_metrics,
                'domains': self.domains,
                'timestamp': datetime.now().isoformat()
            }
            
            json_file = report_file.replace('.md', '.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"✅ Rapport créé: {report_file}")
            self.logger.info(f"✅ Données JSON: {json_file}")
            
            return report_file
            
        except Exception as e:
            self.logger.error(f"❌ Erreur génération rapport: {e}")
            return ""
    
    def run_foundation_establishment(self) -> bool:
        """Exécution complète établissement fondement sémantique"""
        self.logger.info("🚀 DÉMARRAGE ÉTABLISSEMENT FONDEMENT SÉMANTIQUE PANINI")
        
        try:
            # Phase 1: Universaux fondamentaux
            self.initialize_core_universals()
            
            # Phase 2: Règles composition fractale
            self.create_fractal_composition_rules()
            
            # Phase 3: Correspondances multi-domaines
            self.establish_multidomain_correspondences()
            
            # Phase 4: Métriques informationnelles
            self.calculate_information_metrics()
            
            # Phase 5: Rapport complet
            report_file = self.generate_semantic_foundation_report()
            
            # Résultats finaux
            print("\n" + "="*70)
            print("🧠 FONDEMENT SÉMANTIQUE PANINI ÉTABLI")
            print("="*70)
            print(f"🏗️  Universaux: {self.system_metrics['universals_count']}")
            print(f"🔄 Composition: {self.system_metrics['composition_depth']} niveaux")
            print(f"🌐 Domaines: {self.system_metrics['domain_coverage']:.1%} couverture")
            print(f"📊 Information: {self.system_metrics['information_density']:.2f} bits/universel")
            print(f"📋 Rapport: {report_file}")
            print("✅ Base théorique ready pour PanLang")
            print("="*70)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur établissement fondement: {e}")
            return False


def main():
    """Point d'entrée principal"""
    print("🧠 SYSTÈME SÉMANTIQUE PANINI - FONDEMENT THÉORIQUE")
    print("==================================================")
    print("Modélisation sémantique universelle")
    print("Base théorique pour PanLang")
    print()
    
    foundation = PaniniSemanticFoundation()
    success = foundation.run_foundation_establishment()
    
    if success:
        print("\n✅ FONDEMENT SÉMANTIQUE ÉTABLI AVEC SUCCÈS")
        print("🎯 Prêt pour développement PanLang")
    else:
        print("\n❌ ÉCHEC ÉTABLISSEMENT FONDEMENT")
        print("📋 Vérifiez logs pour diagnostic")
    
    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)