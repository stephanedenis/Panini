#!/usr/bin/env python3
"""
🎯 IMPLÉMENTATION EXTENSIONS PRIORITAIRES : MODAL/ASPECT/QUANT
Développement des dhātu additionnels pour couverture FL étendue
Basé sur analyse domaines optimaux (Modalité 8.8/10, Aspect 7.5/10, Quantité 7.1/10)
"""

import json
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple
from enum import Enum

class TypeDhatu(Enum):
    """Types de dhātu selon fonction sémantique"""
    EXISTANT = "existant"      # Dhātu déjà implémentés
    MODAL = "modal"            # Modalité, possibilité, nécessité
    ASPECT = "aspect"          # Aspects temporels, perfectivité
    QUANT = "quantification"   # Quantification, mesure
    TEMP = "temporel"          # Relations temporelles
    INTENSE = "intensification" # Degrés d'intensité
    DISTR = "distribution"     # Distribution spatiale/temporelle
    FIGUR = "figuration"       # Métaphores, figurations

class OperateurNaire(Enum):
    """Opérateurs n-aires avec contraintes cognitives"""
    BINAIRE_NEG = "∅"          # Négation/absence
    BINAIRE_POS = "+"          # Affirmation/présence
    TRINAIRE_NEG = "!"         # Négation forte
    TRINAIRE_IND = "?"         # Indétermination
    TRINAIRE_POS = "+"         # Affirmation
    QUATERNAIRE_FAIBLE = "+·"  # Intensité faible
    QUATERNAIRE_NORMAL = "+"   # Intensité normale
    QUATERNAIRE_FORT = "++"    # Intensité forte
    QUATERNAIRE_EXTREME = "+++" # Intensité extrême

@dataclass
class DhatuEtendu:
    """Dhātu étendu avec opérateurs n-aires"""
    nom: str
    type_dhatu: TypeDhatu
    definition: str
    fonctions_lexicales: List[str]
    operateurs_supportes: List[OperateurNaire]
    exemples_usage: Dict[str, str]
    score_priorite: float
    justification_cognitive: str
    attestation_cross_linguistique: List[str]

class ExtensionDhatuImplementor:
    """Implémenteur des extensions prioritaires dhātu"""
    
    def __init__(self):
        self.dhatu_existants = self._charger_dhatu_existants()
        self.extensions_prioritaires = self._definir_extensions_prioritaires()
        self.mappings_fl = self._definir_mappings_fl()
        
    def _charger_dhatu_existants(self):
        """Charger dhātu déjà implémentés"""
        return {
            "ACTION": {"type": TypeDhatu.EXISTANT, "couverture_fl": ["Oper1", "Func1", "Labor12"]},
            "EVAL": {"type": TypeDhatu.EXISTANT, "couverture_fl": ["Bon", "Ver", "Magn"]},
            "CAUSAL": {"type": TypeDhatu.EXISTANT, "couverture_fl": ["Caus", "Liqu", "Perm"]},
            "TRANSFER": {"type": TypeDhatu.EXISTANT, "couverture_fl": ["Real1", "Fact", "Labreal"]},
            "QUALE": {"type": TypeDhatu.EXISTANT, "couverture_fl": ["Qual", "A1", "Adv1"]},
            "ORIGIN": {"type": TypeDhatu.EXISTANT, "couverture_fl": ["S2", "Demin", "Germ"]},
            "RELATED": {"type": TypeDhatu.EXISTANT, "couverture_fl": ["A2", "Adv2", "Centr"]}
        }
    
    def _definir_extensions_prioritaires(self):
        """Définir les 3 extensions prioritaires basées sur analyse optimaux"""
        return {
            "MODAL": DhatuEtendu(
                nom="MODAL",
                type_dhatu=TypeDhatu.MODAL,
                definition="Modalité épistémique, déontique, aléthique",
                fonctions_lexicales=[
                    "Poss", "Necess", "Prob", "Cert", "Dub", "Perm", "Oblig", "Inter"
                ],
                operateurs_supportes=[
                    OperateurNaire.TRINAIRE_NEG,    # ! = impossibilité
                    OperateurNaire.TRINAIRE_IND,    # ? = possibilité
                    OperateurNaire.TRINAIRE_POS,    # + = nécessité
                    OperateurNaire.QUATERNAIRE_FAIBLE,  # +· = probabilité faible
                    OperateurNaire.QUATERNAIRE_NORMAL,  # + = probabilité normale
                    OperateurNaire.QUATERNAIRE_FORT,    # ++ = probabilité forte
                    OperateurNaire.QUATERNAIRE_EXTREME  # +++ = certitude
                ],
                exemples_usage={
                    "MODAL!": "impossible, inconcevable, exclu",
                    "MODAL?": "possible, envisageable, peut-être",
                    "MODAL+": "nécessaire, obligatoire, inévitable",
                    "MODAL+·": "peu probable, douteux, improbable",
                    "MODAL++": "très probable, quasi-certain",
                    "MODAL+++": "absolument certain, indubitabl"
                },
                score_priorite=8.8,
                justification_cognitive="Modalité = catégorie cognitive universelle (Kratzer 1991)",
                attestation_cross_linguistique=[
                    "français: pouvoir/devoir/falloir",
                    "anglais: can/must/should/might",
                    "allemand: können/müssen/sollen",
                    "mandarin: 能/必须/应该",
                    "arabe: يمكن/يجب/ينبغي"
                ]
            ),
            
            "ASPECT": DhatuEtendu(
                nom="ASPECT",
                type_dhatu=TypeDhatu.ASPECT,
                definition="Aspects temporels et perfectivité",
                fonctions_lexicales=[
                    "Incep", "Cont", "Fin", "Iter", "Semel", "Degrad", "Culm", "Result"
                ],
                operateurs_supportes=[
                    OperateurNaire.TRINAIRE_NEG,    # ! = aspect privatif
                    OperateurNaire.TRINAIRE_IND,    # ? = aspect neutre
                    OperateurNaire.TRINAIRE_POS,    # + = aspect marqué
                    OperateurNaire.QUATERNAIRE_FAIBLE,  # +· = aspectualité faible
                    OperateurNaire.QUATERNAIRE_FORT,    # ++ = aspectualité marquée
                    OperateurNaire.QUATERNAIRE_EXTREME  # +++ = aspect saillant
                ],
                exemples_usage={
                    "ASPECT!": "non-aspectuel, statif, permanent",
                    "ASPECT?": "aspect neutre, non-marqué",
                    "ASPECT+": "aspectuel marqué, télique",
                    "ASPECT+·": "commencer, débuter, amorcer",
                    "ASPECT++": "continuer, poursuivre, maintenir", 
                    "ASPECT+++": "achever, accomplir, finaliser"
                },
                score_priorite=7.5,
                justification_cognitive="Aspect = structuration temporelle universelle (Comrie 1976)",
                attestation_cross_linguistique=[
                    "français: commencer/continuer/finir",
                    "anglais: begin/continue/finish",
                    "russe: prefixes по-/за-/до-",
                    "mandarin: 了/着/过",
                    "arabe: قد/كان/سوف"
                ]
            ),
            
            "QUANT": DhatuEtendu(
                nom="QUANT",
                type_dhatu=TypeDhatu.QUANT,
                definition="Quantification et mesure",
                fonctions_lexicales=[
                    "Mult", "Sing", "Plus", "Minus", "Equ", "Centr", "Distr", "Cumul"
                ],
                operateurs_supportes=[
                    OperateurNaire.TRINAIRE_NEG,    # ! = quantité nulle
                    OperateurNaire.TRINAIRE_IND,    # ? = quantité indéterminée
                    OperateurNaire.TRINAIRE_POS,    # + = quantité positive
                    OperateurNaire.QUATERNAIRE_FAIBLE,  # +· = peu, quelque
                    OperateurNaire.QUATERNAIRE_NORMAL,  # + = quantité normale
                    OperateurNaire.QUATERNAIRE_FORT,    # ++ = beaucoup, nombreux
                    OperateurNaire.QUATERNAIRE_EXTREME  # +++ = énormément, innombrable
                ],
                exemples_usage={
                    "QUANT!": "aucun, zéro, vide, néant",
                    "QUANT?": "quelque, environ, approximativement",
                    "QUANT+": "un, une unité, singulier",
                    "QUANT+·": "peu, quelques, rare",
                    "QUANT++": "beaucoup, nombreux, multiple",
                    "QUANT+++": "énormément, innombrable, infini"
                },
                score_priorite=7.1,
                justification_cognitive="Quantité = cognition numérique universelle (Dehaene 1997)",
                attestation_cross_linguistique=[
                    "français: peu/beaucoup/trop",
                    "anglais: few/many/much/lots",
                    "allemand: wenig/viel/zu_viel",
                    "japonais: 少し/たくさん/非常に",
                    "swahili: kidogo/mengi/sana"
                ]
            )
        }
    
    def _definir_mappings_fl(self):
        """Mappings précis FL → dhātu étendus"""
        return {
            # MODAL mappings
            "Poss": "MODAL?",      # Possibilité
            "Necess": "MODAL+",    # Nécessité
            "Prob": "MODAL+·",     # Probabilité
            "Cert": "MODAL+++",    # Certitude
            "Dub": "MODAL?",       # Doute
            "Perm": "MODAL+",      # Permission
            "Oblig": "MODAL+",     # Obligation
            "Inter": "MODAL!",     # Interdiction
            
            # ASPECT mappings
            "Incep": "ASPECT+·",   # Inchoatif
            "Cont": "ASPECT++",    # Continuatif
            "Fin": "ASPECT+++",    # Terminatif
            "Iter": "ASPECT++",    # Itératif
            "Semel": "ASPECT+",    # Semelfactif
            "Degrad": "ASPECT!",   # Dégradatif
            "Culm": "ASPECT+++",   # Culminatif
            "Result": "ASPECT+++", # Résultatif
            
            # QUANT mappings
            "Mult": "QUANT++",     # Multiplicatif
            "Sing": "QUANT+",      # Singulier
            "Plus": "QUANT++",     # Augmentatif
            "Minus": "QUANT+·",    # Diminutif
            "Equ": "QUANT+",       # Équitatif
            "Centr": "QUANT+",     # Central
            "Distr": "QUANT++",    # Distributif
            "Cumul": "QUANT+++"    # Cumulatif
        }
    
    def calculer_impact_couverture(self):
        """Calculer impact des extensions sur couverture FL"""
        print("🎯 CALCUL IMPACT COUVERTURE FL")
        print("="*40)
        
        # FL actuellement couvertes (dhātu existants)
        fl_actuelles = set()
        for dhatu_info in self.dhatu_existants.values():
            fl_actuelles.update(dhatu_info["couverture_fl"])
        
        # FL ajoutées par extensions
        fl_nouvelles = set()
        for extension in self.extensions_prioritaires.values():
            fl_nouvelles.update(extension.fonctions_lexicales)
        
        # FL totales Mel'čuk (estimation)
        fl_melcuk_total = 65  # Estimation basée sur littérature
        
        couverture_actuelle = len(fl_actuelles) / fl_melcuk_total * 100
        couverture_avec_extensions = (len(fl_actuelles) + len(fl_nouvelles)) / fl_melcuk_total * 100
        
        print(f"📊 FL actuellement couvertes: {len(fl_actuelles)}/{fl_melcuk_total} ({couverture_actuelle:.1f}%)")
        print(f"📊 FL avec extensions MODAL/ASPECT/QUANT: {len(fl_actuelles) + len(fl_nouvelles)}/{fl_melcuk_total} ({couverture_avec_extensions:.1f}%)")
        print(f"🚀 Amélioration: +{couverture_avec_extensions - couverture_actuelle:.1f} points")
        print(f"⚡ Facteur multiplicateur: ×{couverture_avec_extensions/couverture_actuelle:.2f}")
        
        return {
            "couverture_actuelle": couverture_actuelle,
            "couverture_nouvelle": couverture_avec_extensions,
            "amelioration": couverture_avec_extensions - couverture_actuelle,
            "facteur": couverture_avec_extensions/couverture_actuelle
        }
    
    def generer_exemples_compositionnels(self):
        """Générer exemples de compositions dhātu étendus"""
        print(f"\n🧬 EXEMPLES COMPOSITIONNELS DHĀTU ÉTENDUS")
        print("="*50)
        
        compositions = {
            # Compositions MODAL
            "probablement": {
                "decomposition": "MODAL+· + EVAL+",
                "explication": "modalité probabiliste + évaluation positive",
                "FL_cible": "Prob + Bon"
            },
            "obligatoirement": {
                "decomposition": "MODAL+ + ACTION+",
                "explication": "modalité nécessaire + action obligée",
                "FL_cible": "Oblig + Oper1"
            },
            "impossiblement": {
                "decomposition": "MODAL! + ACTION∅",
                "explication": "modalité négative + action exclue",
                "FL_cible": "Poss + Anti(Oper1)"
            },
            
            # Compositions ASPECT
            "commencer_à": {
                "decomposition": "ASPECT+· + ACTION+",
                "explication": "aspect inchoatif + action initiée",
                "FL_cible": "Incep + Oper1"
            },
            "finir_de": {
                "decomposition": "ASPECT+++ + ACTION+",
                "explication": "aspect terminatif + action achevée",
                "FL_cible": "Fin + Oper1"
            },
            "sans_cesse": {
                "decomposition": "ASPECT++ + QUANT!",
                "explication": "aspect continuatif + quantité nulle d'arrêt",
                "FL_cible": "Cont + Anti(Fin)"
            },
            
            # Compositions QUANT
            "un_peu": {
                "decomposition": "QUANT+· + EVAL?",
                "explication": "quantité faible + évaluation neutre",
                "FL_cible": "Minus + A1"
            },
            "énormément": {
                "decomposition": "QUANT+++ + INTENSE++",
                "explication": "quantité extrême + intensification forte",
                "FL_cible": "Mult + Magn"
            },
            "trop_peu": {
                "decomposition": "QUANT+· + EVAL!",
                "explication": "quantité faible + évaluation négative",
                "FL_cible": "Minus + Anti(Bon)"
            },
            
            # Compositions mixtes avancées
            "probablement_commencer": {
                "decomposition": "MODAL+· + ASPECT+· + ACTION+",
                "explication": "modalité possible + aspect inchoatif + action",
                "FL_cible": "Prob + Incep + Oper1"
            },
            "beaucoup_trop": {
                "decomposition": "QUANT++ + EVAL! + INTENSE++",
                "explication": "quantité élevée + évaluation négative + intensité",
                "FL_cible": "Mult + Anti(Bon) + Magn"
            }
        }
        
        for expression, info in compositions.items():
            print(f"\n📝 {expression}")
            print(f"   🧬 Décomposition: {info['decomposition']}")
            print(f"   💭 Explication: {info['explication']}")
            print(f"   🎯 FL équivalentes: {info['FL_cible']}")
        
        return compositions
    
    def valider_contraintes_cognitives(self):
        """Valider respect contraintes cognitives Miller 7±2"""
        print(f"\n⚠️ VALIDATION CONTRAINTES COGNITIVES")
        print("="*45)
        
        violations = []
        for nom, dhatu in self.extensions_prioritaires.items():
            nb_operateurs = len(dhatu.operateurs_supportes)
            if nb_operateurs > 7:
                violations.append(f"{nom}: {nb_operateurs} opérateurs (> limite Miller 7)")
            else:
                print(f"✅ {nom}: {nb_operateurs} opérateurs (OK)")
        
        if violations:
            print("\n🚨 VIOLATIONS DÉTECTÉES:")
            for violation in violations:
                print(f"   ❌ {violation}")
        else:
            print("\n🎊 TOUTES EXTENSIONS RESPECTENT LIMITES COGNITIVES")
        
        return len(violations) == 0
    
    def generer_plan_implementation(self):
        """Générer plan détaillé d'implémentation"""
        print(f"\n🗓️ PLAN IMPLÉMENTATION EXTENSIONS")
        print("="*40)
        
        phases = {
            "Phase 1 - MODAL (2 semaines)": {
                "taches": [
                    "Définir classe ModalDhatu avec opérateurs trinaires/quaternaires",
                    "Implémenter mappings FL → MODAL avec exemples",
                    "Tests unitaires expressions modales français/anglais",
                    "Validation contraintes cognitives"
                ],
                "delivrables": [
                    "modal_dhatu.py",
                    "tests_modal_comprehensive.py", 
                    "exemples_modal_multilingue.json"
                ]
            },
            
            "Phase 2 - ASPECT (2 semaines)": {
                "taches": [
                    "Définir classe AspectDhatu avec temporalité",
                    "Implémenter composition ASPECT + ACTION/EVAL",
                    "Tests aspects verbaux cross-linguistiques",
                    "Optimisation performance compositions"
                ],
                "delivrables": [
                    "aspect_dhatu.py",
                    "tests_aspect_temporel.py",
                    "benchmarks_composition.json"
                ]
            },
            
            "Phase 3 - QUANT (2 semaines)": {
                "taches": [
                    "Définir classe QuantDhatu avec gradations",
                    "Implémenter logique quantification floue",
                    "Tests expressions quantitatives précises",
                    "Intégration complète avec dhātu existants"
                ],
                "delivrables": [
                    "quant_dhatu.py",
                    "tests_quantification.py",
                    "integration_complete.py"
                ]
            },
            
            "Phase 4 - Validation (1 semaine)": {
                "taches": [
                    "Tests intégration complète 3 extensions",
                    "Benchmarking couverture FL vs Mel'čuk",
                    "Validation performance + mémoire",
                    "Documentation utilisateur complète"
                ],
                "delivrables": [
                    "tests_integration_complete.py",
                    "rapport_couverture_fl.md",
                    "documentation_utilisateur.md"
                ]
            }
        }
        
        for phase, info in phases.items():
            print(f"\n📅 {phase}")
            print("   🎯 Tâches:")
            for tache in info["taches"]:
                print(f"      • {tache}")
            print("   📦 Délivrables:")
            for delivrable in info["delivrables"]:
                print(f"      • {delivrable}")
        
        return phases

def main():
    """Implémentation complète extensions prioritaires"""
    implementor = ExtensionDhatuImplementor()
    
    print("🎯 IMPLÉMENTATION EXTENSIONS PRIORITAIRES MODAL/ASPECT/QUANT")
    print("Basé sur analyse scientifique domaines optimaux")
    print("="*70)
    
    # Calcul impact couverture
    impact = implementor.calculer_impact_couverture()
    
    # Exemples compositionnels
    compositions = implementor.generer_exemples_compositionnels()
    
    # Validation cognitive
    valide = implementor.valider_contraintes_cognitives()
    
    # Plan implémentation
    plan = implementor.generer_plan_implementation()
    
    print(f"\n🎊 RÉSUMÉ EXTENSIONS PRIORITAIRES")
    print("="*40)
    print(f"✅ MODAL: Modalité épistémique/déontique (Score: 8.8/10)")
    print(f"✅ ASPECT: Aspectualité temporelle (Score: 7.5/10)")
    print(f"✅ QUANT: Quantification graduée (Score: 7.1/10)")
    print(f"📊 Couverture FL: {impact['couverture_actuelle']:.1f}% → {impact['couverture_nouvelle']:.1f}%")
    print(f"🚀 Amélioration: +{impact['amelioration']:.1f} points (×{impact['facteur']:.2f})")
    print(f"⚠️ Contraintes cognitives: {'RESPECTÉES' if valide else 'VIOLATIONS DÉTECTÉES'}")
    print(f"⏱️ Délai total: 7 semaines (3×2 + 1 validation)")
    
    # Sauvegarde résultats
    resultats = {
        "extensions_prioritaires": {
            nom: {
                "definition": ext.definition,
                "fonctions_lexicales": ext.fonctions_lexicales,
                "operateurs": [op.value for op in ext.operateurs_supportes],
                "exemples": ext.exemples_usage,
                "score_priorite": ext.score_priorite,
                "justification": ext.justification_cognitive
            } for nom, ext in implementor.extensions_prioritaires.items()
        },
        "impact_couverture": impact,
        "compositions_exemples": compositions,
        "plan_implementation": plan,
        "validation_cognitive": valide
    }
    
    with open("implementation_extensions_prioritaires.json", "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Résultats sauvegardés: implementation_extensions_prioritaires.json")

if __name__ == "__main__":
    main()