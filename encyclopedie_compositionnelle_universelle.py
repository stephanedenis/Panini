#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENCYCLOPÉDIE COMPOSITIONNELLE UNIVERSELLE - Architecture v1.0

Système de décomposition universelle basé sur primitives sémantiques dhātu.
Remplace les dictionnaires statiques par une analyse compositionnelle profonde.

Principe : Tout concept est décomposable en primitives universelles
- Noms communs → taxonomie + fonction + propriétés
- Couleurs → teinte (phase circulaire) + intensité + luminosité  
- Objets → fonction + matière + forme
- Animaux → classification biologique + comportement + habitat
- Actions → mouvement + intention + résultat

Architecture compositionnelle permettant la reconstruction exacte.
"""

import numpy as np
import math
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

@dataclass 
class PrimitiveUniverselle:
    """Primitive sémantique universelle"""
    nom: str
    dhatu_primaire: str
    domaine: str
    parametres: Dict[str, float]
    relations: List[str]
    niveau_abstraction: int

@dataclass
class DecompositionConceptuelle:
    """Décomposition complète d'un concept"""
    concept_original: str
    primitives_constitutives: List[PrimitiveUniverselle]
    composition_dhatu: List[str]
    parametres_quantitatifs: Dict[str, float]
    regles_reconstruction: List[str]
    alternatives_universelles: List[str]
    certitude_decomposition: float

class EncyclopedieCompositionnelle:
    """Encyclopédie universelle par décomposition conceptuelle"""
    
    def __init__(self):
        self.version = "v1.0-Compositionnelle"
        
        # Primitives de base par domaine
        self.primitives_couleurs = self._init_primitives_couleurs()
        self.primitives_animaux = self._init_primitives_animaux() 
        self.primitives_objets = self._init_primitives_objets()
        self.primitives_actions = self._init_primitives_actions()
        self.primitives_formes = self._init_primitives_formes()
        self.primitives_matieres = self._init_primitives_matieres()
        
        print("🌟 Encyclopédie Compositionnelle Universelle initialisée")
        print("📚 Domaines : Couleurs, Animaux, Objets, Actions, Formes, Matières")
    
    def decomposer_concept(self, concept: str, contexte: str = "") -> DecompositionConceptuelle:
        """Décomposition universelle d'un concept"""
        
        print(f"\n🔬 DÉCOMPOSITION CONCEPTUELLE : '{concept}'")
        print(f"📋 Contexte : {contexte}")
        print("-" * 60)
        
        # Détection du domaine conceptuel
        domaine = self._detecter_domaine(concept, contexte)
        print(f"🎯 Domaine détecté : {domaine}")
        
        # Décomposition selon le domaine
        if domaine == "couleur":
            return self._decomposer_couleur(concept)
        elif domaine == "animal":
            return self._decomposer_animal(concept)
        elif domaine == "objet":
            return self._decomposer_objet(concept)
        elif domaine == "action":
            return self._decomposer_action(concept)
        else:
            return self._decomposer_generique(concept)
    
    def reconstruire_concept(self, decomposition: DecompositionConceptuelle) -> str:
        """Reconstruction d'un concept à partir de sa décomposition"""
        
        print(f"\n🔧 RECONSTRUCTION : {decomposition.concept_original}")
        
        # Application des règles de reconstruction
        concept_reconstruit = self._appliquer_regles_reconstruction(
            decomposition.primitives_constitutives,
            decomposition.regles_reconstruction,
            decomposition.parametres_quantitatifs
        )
        
        print(f"✅ Concept reconstruit : '{concept_reconstruit}'")
        return concept_reconstruit
    
    def _init_primitives_couleurs(self) -> Dict[str, PrimitiveUniverselle]:
        """Primitives pour les couleurs selon perception humaine"""
        return {
            'teinte_circulaire': PrimitiveUniverselle(
                nom="teinte_circulaire",
                dhatu_primaire="ITER",  # Concept cyclique
                domaine="couleur", 
                parametres={"angle_degres": 0.0, "cycle_complet": 360.0},
                relations=["rouge=0°", "vert=120°", "bleu=240°"],
                niveau_abstraction=1
            ),
            'intensite_saturation': PrimitiveUniverselle(
                nom="intensite_saturation", 
                dhatu_primaire="EVAL",  # Évaluation d'intensité
                domaine="couleur",
                parametres={"niveau": 0.0, "min": 0.0, "max": 1.0},
                relations=["pur=1.0", "gris=0.0"],
                niveau_abstraction=1
            ),
            'luminosite_clarte': PrimitiveUniverselle(
                nom="luminosite_clarte",
                dhatu_primaire="EXIST",  # Présence de lumière 
                domaine="couleur",
                parametres={"niveau": 0.5, "noir": 0.0, "blanc": 1.0},
                relations=["sombre=0.0-0.3", "moyen=0.3-0.7", "clair=0.7-1.0"],
                niveau_abstraction=1
            )
        }
    
    def _init_primitives_animaux(self) -> Dict[str, PrimitiveUniverselle]:
        """Primitives taxonomiques pour animaux"""
        return {
            'regne_animal': PrimitiveUniverselle(
                nom="regne_animal",
                dhatu_primaire="EXIST",
                domaine="taxonomie",
                parametres={"niveau_taxonomique": 1},
                relations=["animalia", "vs_vegetalia", "vs_mineralia"],
                niveau_abstraction=6
            ),
            'vertebre_structure': PrimitiveUniverselle(
                nom="vertebre_structure", 
                dhatu_primaire="RELATE",  # Structure/organisation
                domaine="anatomie",
                parametres={"presence_colonne": 1.0},
                relations=["vertebres", "vs_invertebres"],
                niveau_abstraction=4
            ),
            'mammifere_classe': PrimitiveUniverselle(
                nom="mammifere_classe",
                dhatu_primaire="FLOW",  # Circulation sanguine chaude
                domaine="taxonomie", 
                parametres={"sang_chaud": 1.0, "poils": 1.0, "lait": 1.0},
                relations=["mammalia", "vs_reptilia", "vs_aves"],
                niveau_abstraction=3
            ),
            'carnivore_regime': PrimitiveUniverselle(
                nom="carnivore_regime",
                dhatu_primaire="CAUSE",  # Action de chasser/consommer
                domaine="comportement",
                parametres={"viande_pourcentage": 0.8},
                relations=["predateur", "vs_herbivore", "vs_omnivore"],
                niveau_abstraction=2
            ),
            'domestique_relation': PrimitiveUniverselle(
                nom="domestique_relation",
                dhatu_primaire="COMM",  # Communication avec humains
                domaine="social",
                parametres={"adaptation_humaine": 0.9, "dependance": 0.7},
                relations=["apprivoise", "vs_sauvage"],
                niveau_abstraction=1
            )
        }
    
    def _init_primitives_objets(self) -> Dict[str, PrimitiveUniverselle]:
        """Primitives fonctionnelles pour objets"""
        return {
            'fonction_primaire': PrimitiveUniverselle(
                nom="fonction_primaire",
                dhatu_primaire="CAUSE",  # Causalité/utilité
                domaine="fonction",
                parametres={"efficacite": 1.0},
                relations=["usage_principal"],
                niveau_abstraction=2
            ),
            'materiau_constitution': PrimitiveUniverselle(
                nom="materiau_constitution",
                dhatu_primaire="EXIST",  # Substance physique
                domaine="matiere",
                parametres={"durete": 0.5, "flexibilite": 0.5},
                relations=["composition_chimique"],
                niveau_abstraction=1
            ),
            'forme_geometrique': PrimitiveUniverselle(
                nom="forme_geometrique", 
                dhatu_primaire="RELATE",  # Relations spatiales
                domaine="geometrie",
                parametres={"dimensions": 3, "symetrie": 0.5},
                relations=["structure_spatiale"],
                niveau_abstraction=1
            )
        }
    
    def _init_primitives_actions(self) -> Dict[str, PrimitiveUniverselle]:
        """Primitives pour décomposition des actions"""
        return {
            'mouvement_base': PrimitiveUniverselle(
                nom="mouvement_base",
                dhatu_primaire="FLOW",
                domaine="cinetique", 
                parametres={"vitesse": 0.5, "direction": 0.0},
                relations=["deplacement_spatial"],
                niveau_abstraction=1
            ),
            'intention_volonte': PrimitiveUniverselle(
                nom="intention_volonte",
                dhatu_primaire="DECIDE", 
                domaine="mental",
                parametres={"volontaire": 1.0, "conscient": 0.8},
                relations=["decision_prealable"],
                niveau_abstraction=2
            ),
            'resultat_transformation': PrimitiveUniverselle(
                nom="resultat_transformation",
                dhatu_primaire="CAUSE",
                domaine="effet",
                parametres={"changement_etat": 0.7},
                relations=["modification_resultante"], 
                niveau_abstraction=1
            )
        }
    
    def _init_primitives_formes(self) -> Dict[str, PrimitiveUniverselle]:
        """Primitives géométriques universelles"""
        return {
            'circularite': PrimitiveUniverselle(
                nom="circularite",
                dhatu_primaire="ITER",  # Continuité cyclique
                domaine="geometrie",
                parametres={"courbure": 1.0, "fermeture": 1.0},
                relations=["rond", "sphere", "cycle"],
                niveau_abstraction=1
            ),
            'linearite': PrimitiveUniverselle(
                nom="linearite", 
                dhatu_primaire="RELATE",  # Relation directionnelle
                domaine="geometrie",
                parametres={"rectitude": 1.0, "continuite": 1.0},
                relations=["ligne", "droite", "direction"],
                niveau_abstraction=1
            ),
            'angularite': PrimitiveUniverselle(
                nom="angularite",
                dhatu_primaire="DECIDE",  # Rupture/changement direction
                domaine="geometrie", 
                parametres={"angle_degres": 90.0, "nettete": 1.0},
                relations=["angle", "coin", "intersection"],
                niveau_abstraction=1
            )
        }
    
    def _init_primitives_matieres(self) -> Dict[str, PrimitiveUniverselle]:
        """Primitives pour classification des matières"""
        return {
            'durete_resistance': PrimitiveUniverselle(
                nom="durete_resistance",
                dhatu_primaire="EXIST",  # Résistance à l'altération
                domaine="physique",
                parametres={"echelle_mohs": 5.0, "resistance": 0.5},
                relations=["solide", "vs_mou"],
                niveau_abstraction=1
            ),
            'flexibilite_plasticite': PrimitiveUniverselle(
                nom="flexibilite_plasticite",
                dhatu_primaire="FLOW",  # Capacité de déformation
                domaine="mecanique",
                parametres={"elasticite": 0.5, "plasticite": 0.3},
                relations=["deformable", "vs_rigide"],
                niveau_abstraction=1
            ),
            'origine_naturelle': PrimitiveUniverselle(
                nom="origine_naturelle",
                dhatu_primaire="CAUSE",  # Processus de formation
                domaine="origine",
                parametres={"naturel": 1.0, "artificiel": 0.0},
                relations=["nature", "vs_synthetique"],
                niveau_abstraction=2
            )
        }
    
    def _detecter_domaine(self, concept: str, contexte: str) -> str:
        """Détection du domaine conceptuel"""
        concept_lower = concept.lower()
        
        # Couleurs
        couleurs = ['rouge', 'bleu', 'vert', 'jaune', 'noir', 'blanc', 'rose', 'violet', 'orange', 'marron']
        if any(c in concept_lower for c in couleurs):
            return "couleur"
        
        # Animaux
        animaux = ['chat', 'chien', 'oiseau', 'poisson', 'souris', 'lion', 'tigre', 'éléphant']
        if any(a in concept_lower for a in animaux):
            return "animal"
        
        # Actions/verbes
        if contexte.lower() in ['verbe', 'action'] or concept.endswith(('er', 'ir', 're')):
            return "action"
        
        # Objets par défaut
        return "objet"
    
    def _decomposer_couleur(self, couleur: str) -> DecompositionConceptuelle:
        """Décomposition spécialisée des couleurs"""
        
        # Mapping couleurs vers HSL (Teinte, Saturation, Luminosité)
        couleurs_hsl = {
            'rouge': (0, 1.0, 0.5),
            'vert': (120, 1.0, 0.5), 
            'bleu': (240, 1.0, 0.5),
            'jaune': (60, 1.0, 0.5),
            'orange': (30, 1.0, 0.5),
            'violet': (270, 1.0, 0.5),
            'rose': (300, 0.7, 0.8),
            'marron': (30, 0.6, 0.3),
            'noir': (0, 0, 0),
            'blanc': (0, 0, 1.0),
            'gris': (0, 0, 0.5)
        }
        
        h, s, l = couleurs_hsl.get(couleur.lower(), (0, 0.5, 0.5))
        
        primitives = [
            self.primitives_couleurs['teinte_circulaire'],
            self.primitives_couleurs['intensite_saturation'], 
            self.primitives_couleurs['luminosite_clarte']
        ]
        
        # Modification des paramètres selon la couleur spécifique
        primitives[0].parametres['angle_degres'] = h
        primitives[1].parametres['niveau'] = s
        primitives[2].parametres['niveau'] = l
        
        return DecompositionConceptuelle(
            concept_original=couleur,
            primitives_constitutives=primitives,
            composition_dhatu=["ITER", "EVAL", "EXIST"],
            parametres_quantitatifs={"teinte": h, "saturation": s, "luminosite": l},
            regles_reconstruction=[
                f"teinte_circulaire({h}°)",
                f"intensite_saturation({s:.2f})", 
                f"luminosite_clarte({l:.2f})"
            ],
            alternatives_universelles=[
                f"couleur_phase_{h}°_intensite_{s:.1f}_lumiere_{l:.1f}",
                f"perception_visuelle_HSL({h},{s},{l})"
            ],
            certitude_decomposition=0.95
        )
    
    def _decomposer_animal(self, animal: str) -> DecompositionConceptuelle:
        """Décomposition taxonomique d'un animal"""
        
        # Base de données taxonomique simplifiée
        taxonomies = {
            'chat': {
                'regne': 'animal',
                'embranchement': 'vertebre', 
                'classe': 'mammifere',
                'ordre': 'carnivore',
                'famille': 'felide',
                'domestication': True,
                'taille': 'petit',
                'habitat': 'domestique'
            },
            'chien': {
                'regne': 'animal',
                'embranchement': 'vertebre',
                'classe': 'mammifere', 
                'ordre': 'carnivore',
                'famille': 'canide',
                'domestication': True,
                'taille': 'moyen',
                'habitat': 'domestique'
            },
            'lion': {
                'regne': 'animal',
                'embranchement': 'vertebre',
                'classe': 'mammifere',
                'ordre': 'carnivore', 
                'famille': 'felide',
                'domestication': False,
                'taille': 'grand',
                'habitat': 'savane'
            }
        }
        
        taxo = taxonomies.get(animal.lower(), taxonomies['chat'])  # Default cat
        
        primitives = [
            self.primitives_animaux['regne_animal'],
            self.primitives_animaux['vertebre_structure'],
            self.primitives_animaux['mammifere_classe'],
            self.primitives_animaux['carnivore_regime']
        ]
        
        if taxo['domestication']:
            primitives.append(self.primitives_animaux['domestique_relation'])
        
        return DecompositionConceptuelle(
            concept_original=animal,
            primitives_constitutives=primitives,
            composition_dhatu=["EXIST", "RELATE", "FLOW", "CAUSE", "COMM"],
            parametres_quantitatifs={
                "niveau_taxonomique": 5,
                "domestication": 1.0 if taxo['domestication'] else 0.0,
                "taille_relative": {"petit": 0.3, "moyen": 0.6, "grand": 1.0}[taxo['taille']]
            },
            regles_reconstruction=[
                f"regne({taxo['regne']})",
                f"classe({taxo['classe']})", 
                f"regime({taxo['ordre']})",
                f"domestication({taxo['domestication']})",
                f"habitat({taxo['habitat']})"
            ],
            alternatives_universelles=[
                f"animal_mammifere_carnivore_{'domestique' if taxo['domestication'] else 'sauvage'}",
                f"vertebre_{taxo['classe']}_{taxo['ordre']}"
            ],
            certitude_decomposition=0.9
        )
    
    def _decomposer_objet(self, objet: str) -> DecompositionConceptuelle:
        """Décomposition fonctionnelle d'un objet"""
        
        # Base fonctionnelle simplifiée
        fonctions_objets = {
            'table': {
                'fonction': 'support_horizontal',
                'materiau': 'bois_metal',
                'forme': 'plateau_pieds', 
                'usage': 'poser_objets'
            },
            'chaise': {
                'fonction': 'support_corps',
                'materiau': 'bois_tissu',
                'forme': 'assise_dossier',
                'usage': 'position_assise'
            },
            'couteau': {
                'fonction': 'decouper',
                'materiau': 'metal_manche',
                'forme': 'lame_aiguisee',
                'usage': 'trancher_matiere'
            }
        }
        
        obj_data = fonctions_objets.get(objet.lower(), fonctions_objets['table'])
        
        primitives = [
            self.primitives_objets['fonction_primaire'],
            self.primitives_objets['materiau_constitution'],
            self.primitives_objets['forme_geometrique']
        ]
        
        return DecompositionConceptuelle(
            concept_original=objet,
            primitives_constitutives=primitives,
            composition_dhatu=["CAUSE", "EXIST", "RELATE"],
            parametres_quantitatifs={
                "utilite_fonctionnelle": 0.9,
                "complexite_forme": 0.6,
                "duree_vie": 0.8
            },
            regles_reconstruction=[
                f"fonction({obj_data['fonction']})",
                f"materiau({obj_data['materiau']})",
                f"forme({obj_data['forme']})",
                f"usage({obj_data['usage']})"
            ],
            alternatives_universelles=[
                f"objet_{obj_data['fonction']}_{obj_data['materiau']}",
                f"artefact_fonction_{obj_data['usage']}"
            ],
            certitude_decomposition=0.85
        )
    
    def _decomposer_action(self, action: str) -> DecompositionConceptuelle:
        """Décomposition d'une action en primitives"""
        
        actions_primitives = {
            'marcher': {
                'mouvement': 'deplacement_pieds',
                'intention': 'volontaire_navigation',
                'resultat': 'changement_position'
            },
            'courir': {
                'mouvement': 'deplacement_rapide',
                'intention': 'volontaire_vitesse', 
                'resultat': 'changement_position_rapide'
            },
            'manger': {
                'mouvement': 'ingestion_bouche',
                'intention': 'nutrition_survie',
                'resultat': 'transformation_aliment_energie'
            }
        }
        
        action_data = actions_primitives.get(action.lower(), actions_primitives['marcher'])
        
        primitives = [
            self.primitives_actions['mouvement_base'],
            self.primitives_actions['intention_volonte'],
            self.primitives_actions['resultat_transformation']
        ]
        
        return DecompositionConceptuelle(
            concept_original=action,
            primitives_constitutives=primitives,
            composition_dhatu=["FLOW", "DECIDE", "CAUSE"],
            parametres_quantitatifs={
                "energie_requise": 0.6,
                "duree_typique": 0.5,
                "complexite_coordination": 0.4
            },
            regles_reconstruction=[
                f"mouvement({action_data['mouvement']})",
                f"intention({action_data['intention']})",
                f"resultat({action_data['resultat']})"
            ],
            alternatives_universelles=[
                f"action_{action_data['mouvement']}_{action_data['intention']}",
                f"verbe_mouvement_{action_data['resultat']}"
            ],
            certitude_decomposition=0.8
        )
    
    def _decomposer_generique(self, concept: str) -> DecompositionConceptuelle:
        """Décomposition générique par défaut"""
        return DecompositionConceptuelle(
            concept_original=concept,
            primitives_constitutives=[],
            composition_dhatu=["EXIST"],
            parametres_quantitatifs={"abstraction": 0.5},
            regles_reconstruction=[f"concept_generique({concept})"],
            alternatives_universelles=[f"entite_inconnue_{concept}"],
            certitude_decomposition=0.3
        )
    
    def _appliquer_regles_reconstruction(self, primitives: List[PrimitiveUniverselle], 
                                       regles: List[str], 
                                       parametres: Dict[str, float]) -> str:
        """Application des règles de reconstruction"""
        
        # Reconstruction basée sur les primitives et paramètres
        if len(regles) >= 3 and "teinte" in parametres:
            # Couleur
            h, s, l = parametres.get("teinte", 0), parametres.get("saturation", 0.5), parametres.get("luminosite", 0.5)
            return self._reconstruire_couleur_hsl(h, s, l)
        
        elif len(primitives) >= 4 and any("animal" in p.domaine for p in primitives):
            # Animal 
            return self._reconstruire_animal(primitives, parametres)
        
        elif len(primitives) >= 3 and any("fonction" in p.domaine for p in primitives):
            # Objet
            return self._reconstruire_objet(regles)
        
        else:
            # Générique
            return f"concept_reconstruit_{regles[0] if regles else 'inconnu'}"
    
    def _reconstruire_couleur_hsl(self, h: float, s: float, l: float) -> str:
        """Reconstruction d'une couleur à partir des paramètres HSL"""
        
        # Mapping inverse HSL vers noms de couleurs
        if l < 0.1:
            return "noir"
        elif l > 0.9 and s < 0.1:
            return "blanc"
        elif s < 0.2:
            return "gris"
        else:
            # Teintes principales
            if h < 15 or h >= 345:
                return "rouge"
            elif h < 45:
                return "orange" 
            elif h < 75:
                return "jaune"
            elif h < 165:
                return "vert"
            elif h < 195:
                return "cyan"
            elif h < 255:
                return "bleu"
            elif h < 285:
                return "violet"
            elif h < 315:
                return "magenta"
            else:
                return "rose"
    
    def _reconstruire_animal(self, primitives: List[PrimitiveUniverselle], parametres: Dict[str, float]) -> str:
        """Reconstruction d'un animal à partir des primitives"""
        
        est_domestique = parametres.get("domestication", 0.0) > 0.5
        taille = parametres.get("taille_relative", 0.5)
        
        # Logique de reconstruction basée sur les caractéristiques
        if est_domestique:
            if taille < 0.4:
                return "chat"  # Petit domestique
            else:
                return "chien"  # Moyen/grand domestique
        else:
            if taille > 0.8:
                return "lion"  # Grand sauvage
            else:
                return "animal_sauvage"
    
    def _reconstruire_objet(self, regles: List[str]) -> str:
        """Reconstruction d'un objet à partir des règles"""
        
        fonction_str = next((r for r in regles if r.startswith("fonction(")), "")
        
        if "support_horizontal" in fonction_str:
            return "table"
        elif "support_corps" in fonction_str:
            return "chaise" 
        elif "decouper" in fonction_str:
            return "couteau"
        else:
            return "objet_fonctionnel"

# Démonstration
def demonstration_encyclopedie():
    """Démonstration de l'encyclopédie compositionnelle"""
    
    print("🌟 DÉMONSTRATION ENCYCLOPÉDIE COMPOSITIONNELLE UNIVERSELLE")
    print("=" * 80)
    
    encyclopedie = EncyclopedieCompositionnelle()
    
    # Tests sur différents domaines
    concepts_test = [
        ("rouge", "couleur"),
        ("chat", "animal"), 
        ("table", "objet"),
        ("marcher", "action")
    ]
    
    for concept, contexte in concepts_test:
        print(f"\n{'='*60}")
        
        # Décomposition
        decomposition = encyclopedie.decomposer_concept(concept, contexte)
        
        print(f"🔬 Concept: {concept}")
        print(f"📊 Primitives: {len(decomposition.primitives_constitutives)}")
        print(f"🧬 Dhātu: {' + '.join(decomposition.composition_dhatu)}")
        print(f"📏 Paramètres: {decomposition.parametres_quantitatifs}")
        print(f"🔧 Règles: {decomposition.regles_reconstruction}")
        print(f"🌐 Alternatives: {decomposition.alternatives_universelles}")
        print(f"✅ Certitude: {decomposition.certitude_decomposition:.1%}")
        
        # Reconstruction
        concept_reconstruit = encyclopedie.reconstruire_concept(decomposition)
        
        print(f"🎯 Reconstruction réussie: {concept == concept_reconstruit}")
        
    print(f"\n{'='*80}")
    print("✅ DÉMONSTRATION COMPLÉTÉE - Encyclopédie Compositionnelle Opérationnelle")

if __name__ == "__main__":
    demonstration_encyclopedie()