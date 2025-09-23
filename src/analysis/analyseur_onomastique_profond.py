#!/usr/bin/env python3
"""
ANALYSEUR ONOMASTIQUE PROFOND - Pipeline v7.2 Enhanced

Système d'analyse complète des noms propres intégrant :
- Onomastique : Étude scientifique des noms propres
- Anthroponymie : Noms de personnes (prénoms, noms de famille)
- Toponymie : Noms de lieux (villes, régions, pays, etc.)
- Taxinomie : Noms scientifiques (espèces, classifications)
- Étymologie taxonomique : Origines et évolutions sémantiques

Principe : Chaque nom propre doit être décomposé jusqu'à ses racines
sémantiques universelles pour éviter tout emprunt aveugle.
"""

import re
import json
import time
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid

@dataclass
class RacineEtymologique:
    """Racine étymologique d'un nom"""
    racine: str
    langue_origine: str
    sens_original: str
    evolution_semantique: List[str]
    dhatu_correspondant: str
    niveau_certitude: float

@dataclass
class AnalyseOnomastique:
    """Analyse onomastique complète d'un nom propre"""
    nom_original: str
    type_onomastique: str  # anthroponyme, toponyme, taxonyme
    
    # Décomposition étymologique
    racines_etymologiques: List[RacineEtymologique]
    langues_contributives: List[str]
    
    # Analyse anthroponymique
    signification_anthroponymique: Optional[str]
    origine_culturelle: Optional[str]
    tradition_nomenclature: Optional[str]
    
    # Analyse toponymique
    signification_toponymique: Optional[str]
    caracteristiques_geographiques: Optional[Dict[str, str]]
    evolution_historique: Optional[List[str]]
    
    # Analyse taxonomique
    classification_taxonomique: Optional[Dict[str, str]]
    etymologie_scientifique: Optional[str]
    descripteurs_morphologiques: Optional[List[str]]
    
    # Synthèse sémantique universelle
    concepts_dhatu_equivalents: List[str]
    representation_universelle: str
    alternatives_non_empruntees: List[str]
    
    # Métadonnées de traçabilité
    timestamp_analyse: str
    sources_references: List[str]
    niveau_completude: float

@dataclass
class ContexteOnomastique:
    """Contexte complet d'une analyse onomastique"""
    phrase_originale: str
    noms_detectes: List[str]
    analyses_individuelles: List[AnalyseOnomastique]
    synthese_globale: Dict[str, Any]
    recommandations_langue_nouvelle: List[str]

class AnalyseurOnomastiqueProfond:
    """Analyseur spécialisé dans l'onomastique profonde"""
    
    def __init__(self):
        self.version = "v7.2-Onomastique"
        self.timestamp_init = datetime.now().isoformat()
        
        # Bases de données onomastiques
        self.base_anthroponymique = self._charger_base_anthroponymique()
        self.base_toponymique = self._charger_base_toponymique()
        self.base_taxonomique = self._charger_base_taxonomique()
        self.base_etymologique = self._charger_base_etymologique()
        
        print(f"🏛️ Analyseur Onomastique Profond {self.version} initialisé")
        print(f"📚 Bases chargées : Anthroponymie, Toponymie, Taxinomie, Étymologie")
    
    def analyser_noms_propres_complet(self, phrase: str, langue: str) -> ContexteOnomastique:
        """Analyse onomastique complète d'une phrase"""
        
        print(f"\n🔍 ANALYSE ONOMASTIQUE : '{phrase}'")
        print(f"🌍 Langue: {langue}")
        print("-" * 70)
        
        debut = time.time()
        timestamp = datetime.now().isoformat()
        
        # Détection des noms propres
        noms_detectes = self._detecter_noms_propres(phrase, langue)
        print(f"📋 Noms propres détectés : {noms_detectes}")
        
        # Analyse individuelle de chaque nom
        analyses_individuelles = []
        for nom in noms_detectes:
            analyse = self._analyser_nom_individuel(nom, langue, timestamp)
            analyses_individuelles.append(analyse)
            self._afficher_analyse_individuelle(analyse)
        
        # Synthèse globale
        synthese = self._generer_synthese_globale(analyses_individuelles)
        
        # Recommandations pour langue nouvelle
        recommandations = self._generer_recommandations_langue_nouvelle(analyses_individuelles)
        
        contexte = ContexteOnomastique(
            phrase_originale=phrase,
            noms_detectes=noms_detectes,
            analyses_individuelles=analyses_individuelles,
            synthese_globale=synthese,
            recommandations_langue_nouvelle=recommandations
        )
        
        temps_total = (time.time() - debut) * 1000
        self._afficher_synthese_complete(contexte, temps_total)
        
        return contexte
    
    def _detecter_noms_propres(self, phrase: str, langue: str) -> List[str]:
        """Détecte les noms propres dans une phrase"""
        # Pattern pour majuscules
        pattern_majuscules = r'\b[A-ZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞ][a-zàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]*\b'
        
        # Exclusion des mots en début de phrase
        mots = re.findall(pattern_majuscules, phrase)
        
        # Filtrage intelligent
        noms_propres = []
        mots_phrase = phrase.split()
        
        for i, mot in enumerate(mots_phrase):
            if re.match(pattern_majuscules, mot):
                # Si ce n'est pas le premier mot OU si c'est manifestement un nom propre
                if i > 0 or self._est_probablement_nom_propre(mot, langue):
                    noms_propres.append(mot.rstrip('.,!?;:'))
        
        return list(set(noms_propres))  # Suppression des doublons
    
    def _est_probablement_nom_propre(self, mot: str, langue: str) -> bool:
        """Détermine si un mot en majuscule est probablement un nom propre"""
        # Vérification dans les bases
        return (mot in self.base_anthroponymique or 
                mot in self.base_toponymique or
                mot in self.base_taxonomique or
                len(mot) > 3)  # Heuristique simple
    
    def _analyser_nom_individuel(self, nom: str, langue: str, timestamp: str) -> AnalyseOnomastique:
        """Analyse onomastique approfondie d'un nom individuel"""
        
        # Détermination du type onomastique
        type_ono = self._determiner_type_onomastique(nom)
        
        # Analyse étymologique
        racines = self._analyser_etymologie_profonde(nom, type_ono)
        
        # Analyses spécialisées selon le type
        sig_anthro, orig_cult, trad_nom = None, None, None
        sig_topo, carac_geo, evol_hist = None, None, None
        classif_taxo, etym_sci, desc_morph = None, None, None
        
        if type_ono == "anthroponyme":
            sig_anthro, orig_cult, trad_nom = self._analyser_anthroponymie(nom)
        elif type_ono == "toponyme":
            sig_topo, carac_geo, evol_hist = self._analyser_toponymie(nom)
        elif type_ono == "taxonyme":
            classif_taxo, etym_sci, desc_morph = self._analyser_taxinomie(nom)
        
        # Synthèse vers dhātu universels
        dhatus_equiv = self._extraire_dhatus_equivalents(racines, type_ono)
        representation_univ = self._generer_representation_universelle(dhatus_equiv, nom)
        alternatives = self._generer_alternatives_non_empruntees(dhatus_equiv, type_ono)
        
        return AnalyseOnomastique(
            nom_original=nom,
            type_onomastique=type_ono,
            racines_etymologiques=racines,
            langues_contributives=list(set([r.langue_origine for r in racines])),
            signification_anthroponymique=sig_anthro,
            origine_culturelle=orig_cult,
            tradition_nomenclature=trad_nom,
            signification_toponymique=sig_topo,
            caracteristiques_geographiques=carac_geo,
            evolution_historique=evol_hist,
            classification_taxonomique=classif_taxo,
            etymologie_scientifique=etym_sci,
            descripteurs_morphologiques=desc_morph,
            concepts_dhatu_equivalents=dhatus_equiv,
            representation_universelle=representation_univ,
            alternatives_non_empruntees=alternatives,
            timestamp_analyse=timestamp,
            sources_references=["Base_Etymologique_v1", "Base_Onomastique_v1"],
            niveau_completude=0.85
        )
    
    def _determiner_type_onomastique(self, nom: str) -> str:
        """Détermine le type onomastique du nom"""
        if nom in self.base_anthroponymique:
            return "anthroponyme"
        elif nom in self.base_toponymique:
            return "toponyme"
        elif nom in self.base_taxonomique:
            return "taxonyme"
        else:
            # Heuristiques
            if nom.endswith(('us', 'a', 'um')):  # Terminaisons latines courantes
                return "taxonyme"
            elif len(nom) > 6 and nom[0].isupper():
                return "toponyme"
            else:
                return "anthroponyme"
    
    def _analyser_etymologie_profonde(self, nom: str, type_ono: str) -> List[RacineEtymologique]:
        """Analyse étymologique approfondie"""
        racines = []
        
        # Simulation d'analyse étymologique (en réalité, nécessiterait des bases massives)
        if nom == "Smith":
            racines.append(RacineEtymologique(
                racine="smitan",
                langue_origine="vieil_anglais",
                sens_original="frapper, forger",
                evolution_semantique=["forgeron", "artisan_metal", "nom_famille"],
                dhatu_correspondant="MOVE",  # Action de frapper/forger
                niveau_certitude=0.9
            ))
        elif nom == "Paris":
            racines.append(RacineEtymologique(
                racine="par",
                langue_origine="celte_gaulois",
                sens_original="tribu, peuple",
                evolution_semantique=["tribu_parisii", "ville", "capitale"],
                dhatu_correspondant="COMMUNICATE",  # Communauté, rassemblement
                niveau_certitude=0.8
            ))
        elif nom == "Ésope":
            racines.append(RacineEtymologique(
                racine="Αἴσωπος",
                langue_origine="grec_ancien",
                sens_original="celui_qui_voit_clair",
                evolution_semantique=["sage", "conteur", "moraliste"],
                dhatu_correspondant="PERCEIVE",  # Vision, perception
                niveau_certitude=0.7
            ))
        else:
            # Analyse par décomposition morphologique
            racines.append(self._analyser_morphologie_nom(nom, type_ono))
        
        return racines
    
    def _analyser_morphologie_nom(self, nom: str, type_ono: str) -> RacineEtymologique:
        """Analyse morphologique d'un nom non répertorié"""
        return RacineEtymologique(
            racine=nom.lower()[:4],  # Simplification
            langue_origine="indeterminee",
            sens_original="à_determiner",
            evolution_semantique=["analyse_requise"],
            dhatu_correspondant="EXIST",  # Par défaut
            niveau_certitude=0.3
        )
    
    def _analyser_anthroponymie(self, nom: str) -> Tuple[str, str, str]:
        """Analyse anthroponymique spécialisée"""
        significations = {
            "Smith": "Forgeron, artisan du métal",
            "Jean": "Dieu fait grâce (hébreu)",
            "Marie": "Bien-aimée, souveraine (hébreu/égyptien)",
            "Ésope": "Celui qui voit clair, sage (grec)"
        }
        
        origines = {
            "Smith": "Anglo-saxonne",
            "Jean": "Hébraïque via grec/latin",
            "Marie": "Hébraïque/égyptienne",
            "Ésope": "Grecque antique"
        }
        
        traditions = {
            "Smith": "Nomination par métier",
            "Jean": "Tradition biblique",
            "Marie": "Tradition religieuse",
            "Ésope": "Tradition littéraire/philosophique"
        }
        
        return (significations.get(nom, "Signification à rechercher"),
                origines.get(nom, "Origine à déterminer"),
                traditions.get(nom, "Tradition à analyser"))
    
    def _analyser_toponymie(self, nom: str) -> Tuple[str, Dict[str, str], List[str]]:
        """Analyse toponymique spécialisée"""
        significations_topo = {
            "Paris": "Territoire de la tribu des Parisii",
            "Londres": "Londinium - établissement sur la Tamise",
            "Berlin": "Lieu dans les marécages"
        }
        
        caracteristiques = {
            "Paris": {"type": "urbain", "situation": "île_fluviale", "relief": "plaine"},
            "Londres": {"type": "urbain", "situation": "estuaire", "relief": "collines"},
            "Berlin": {"type": "urbain", "situation": "plaine", "relief": "marécages"}
        }
        
        evolutions = {
            "Paris": ["Lutetia_gallo-romaine", "Civitas_Parisiorum", "Paris_medieval"],
            "Londres": ["Londinium_romain", "Lundenwic_anglo-saxon", "London_moderne"],
            "Berlin": ["Village_slave", "Margraviat", "Capitale_prussienne", "Capitale_allemande"]
        }
        
        return (significations_topo.get(nom, "Signification toponymique à rechercher"),
                caracteristiques.get(nom, {"type": "à_determiner"}),
                evolutions.get(nom, ["Evolution à documenter"]))
    
    def _analyser_taxinomie(self, nom: str) -> Tuple[Dict[str, str], str, List[str]]:
        """Analyse taxonomique spécialisée"""
        # Exemple pour noms scientifiques
        classifications = {
            "Homo": {"regne": "Animalia", "embranchement": "Chordata", "classe": "Mammalia", "ordre": "Primates"},
            "Quercus": {"regne": "Plantae", "embranchement": "Spermatophyta", "classe": "Magnoliopsida", "ordre": "Fagales"}
        }
        
        etymologies_sci = {
            "Homo": "homme (latin) - caractérise l'humanité",
            "Quercus": "chêne (latin) - arbre noble et robuste"
        }
        
        descripteurs = {
            "Homo": ["bipède", "cerveau_développé", "opposable_pouce"],
            "Quercus": ["feuilles_lobées", "glands", "longévité"]
        }
        
        return (classifications.get(nom, {"classification": "à_determiner"}),
                etymologies_sci.get(nom, "Étymologie scientifique à rechercher"),
                descripteurs.get(nom, ["Descripteurs à identifier"]))
    
    def _extraire_dhatus_equivalents(self, racines: List[RacineEtymologique], type_ono: str) -> List[str]:
        """Extrait les dhātu équivalents des racines étymologiques"""
        dhatus = []
        for racine in racines:
            dhatus.append(racine.dhatu_correspondant)
        
        # Ajout de dhātu spécifiques selon le type
        if type_ono == "anthroponyme":
            dhatus.append("EXIST")  # Identité personnelle
        elif type_ono == "toponyme":
            dhatus.extend(["SPACE", "EXIST"])  # Lieu et existence
        elif type_ono == "taxonyme":
            dhatus.extend(["QUALITY", "EXIST"])  # Caractéristiques et classification
        
        return list(set(dhatus))
    
    def _generer_representation_universelle(self, dhatus: List[str], nom_original: str) -> str:
        """Génère une représentation universelle basée sur les dhātu"""
        return " + ".join(dhatus) + f" [{nom_original}_concept]"
    
    def _generer_alternatives_non_empruntees(self, dhatus: List[str], type_ono: str) -> List[str]:
        """Génère des alternatives sans emprunt basées sur les concepts universels"""
        alternatives = []
        
        # Construction à partir des dhātu
        if "MOVE" in dhatus and "EXIST" in dhatus:
            alternatives.append("CELUI-QUI-AGIT-SUR-MATIERE")  # Pour Smith/forgeron
        
        if "PERCEIVE" in dhatus and "COMMUNICATE" in dhatus:
            alternatives.append("CELUI-QUI-VOIT-ET-RACONTE")  # Pour Ésope/conteur
        
        if "COMMUNICATE" in dhatus and "SPACE" in dhatus:
            alternatives.append("LIEU-DE-RASSEMBLEMENT")  # Pour Paris/ville
        
        # Alternatives génériques selon le type
        if type_ono == "anthroponyme":
            alternatives.append("INDIVIDU-" + "-".join(dhatus))
        elif type_ono == "toponyme":
            alternatives.append("LIEU-" + "-".join(dhatus))
        elif type_ono == "taxonyme":
            alternatives.append("ESPECE-" + "-".join(dhatus))
        
        return alternatives
    
    def _generer_synthese_globale(self, analyses: List[AnalyseOnomastique]) -> Dict[str, Any]:
        """Génère une synthèse globale des analyses"""
        langues_toutes = []
        dhatus_tous = []
        types_tous = []
        
        for analyse in analyses:
            langues_toutes.extend(analyse.langues_contributives)
            dhatus_tous.extend(analyse.concepts_dhatu_equivalents)
            types_tous.append(analyse.type_onomastique)
        
        return {
            "nombre_noms_analyses": len(analyses),
            "types_onomastiques": list(set(types_tous)),
            "langues_etymologiques": list(set(langues_toutes)),
            "dhatus_universels_detectes": list(set(dhatus_tous)),
            "niveau_diversite_linguistique": len(set(langues_toutes)),
            "niveau_complexite_semantique": len(set(dhatus_tous))
        }
    
    def _generer_recommandations_langue_nouvelle(self, analyses: List[AnalyseOnomastique]) -> List[str]:
        """Génère des recommandations pour la création d'une langue nouvelle"""
        recommandations = []
        
        recommandations.append("🚫 ÉVITER tout emprunt direct de noms propres existants")
        recommandations.append("🧬 DÉCOMPOSER chaque nom jusqu'aux concepts dhātu universels")
        recommandations.append("🏗️ CONSTRUIRE de nouveaux noms à partir des dhātu identifiés")
        recommandations.append("📚 DOCUMENTER l'étymologie de chaque nom créé")
        recommandations.append("🌍 ASSURER l'universalité conceptuelle par les dhātu")
        
        # Recommandations spécifiques selon les analyses
        for analyse in analyses:
            if analyse.type_onomastique == "anthroponyme":
                recommandations.append(f"👤 Pour {analyse.nom_original}: Utiliser {analyse.representation_universelle}")
            elif analyse.type_onomastique == "toponyme":
                recommandations.append(f"🗺️ Pour {analyse.nom_original}: Utiliser {analyse.representation_universelle}")
            elif analyse.type_onomastique == "taxonyme":
                recommandations.append(f"🔬 Pour {analyse.nom_original}: Utiliser {analyse.representation_universelle}")
        
        return recommandations
    
    def _afficher_analyse_individuelle(self, analyse: AnalyseOnomastique):
        """Affiche l'analyse individuelle d'un nom"""
        print(f"\n📖 ANALYSE : {analyse.nom_original} ({analyse.type_onomastique})")
        print(f"   🌳 Racines étymologiques :")
        for racine in analyse.racines_etymologiques:
            print(f"      • {racine.racine} ({racine.langue_origine}) → {racine.sens_original}")
            print(f"        Evolution: {' → '.join(racine.evolution_semantique)}")
            print(f"        Dhātu: {racine.dhatu_correspondant} (certitude: {racine.niveau_certitude:.1f})")
        
        if analyse.signification_anthroponymique:
            print(f"   👤 Anthroponymie: {analyse.signification_anthroponymique}")
            print(f"      Origine: {analyse.origine_culturelle}")
            print(f"      Tradition: {analyse.tradition_nomenclature}")
        
        if analyse.signification_toponymique:
            print(f"   🗺️ Toponymie: {analyse.signification_toponymique}")
            print(f"      Caractéristiques: {analyse.caracteristiques_geographiques}")
        
        if analyse.etymologie_scientifique:
            print(f"   🔬 Taxinomie: {analyse.etymologie_scientifique}")
            print(f"      Classification: {analyse.classification_taxonomique}")
        
        print(f"   🧠 Dhātu équivalents: {' + '.join(analyse.concepts_dhatu_equivalents)}")
        print(f"   ✨ Représentation universelle: {analyse.representation_universelle}")
        print(f"   🔄 Alternatives non-empruntées:")
        for alt in analyse.alternatives_non_empruntees:
            print(f"      • {alt}")
    
    def _afficher_synthese_complete(self, contexte: ContexteOnomastique, temps_ms: float):
        """Affiche la synthèse complète"""
        print(f"\n🏆 SYNTHÈSE ONOMASTIQUE COMPLÈTE")
        print(f"⏱️ Temps total: {temps_ms:.2f}ms")
        print(f"📊 Synthèse globale:")
        for cle, valeur in contexte.synthese_globale.items():
            print(f"   • {cle}: {valeur}")
        
        print(f"\n💡 RECOMMANDATIONS POUR LANGUE NOUVELLE:")
        for i, rec in enumerate(contexte.recommandations_langue_nouvelle, 1):
            print(f"   {i}. {rec}")
    
    def _charger_base_anthroponymique(self) -> Dict[str, Any]:
        """Charge la base de données anthroponymique"""
        return {"Smith": {}, "Jean": {}, "Marie": {}, "Ésope": {}, "Dr": {}}
    
    def _charger_base_toponymique(self) -> Dict[str, Any]:
        """Charge la base de données toponymique"""
        return {"Paris": {}, "Londres": {}, "Berlin": {}, "France": {}}
    
    def _charger_base_taxonomique(self) -> Dict[str, Any]:
        """Charge la base de données taxonomique"""
        return {"Homo": {}, "Quercus": {}, "Felis": {}}
    
    def _charger_base_etymologique(self) -> Dict[str, Any]:
        """Charge la base de données étymologique"""
        return {"proto_indo_europeen": {}, "latin": {}, "grec": {}, "germanique": {}}


def test_analyse_onomastique():
    """Test de l'analyse onomastique complète"""
    print("🧪 TEST D'ANALYSE ONOMASTIQUE PROFONDE")
    print("=" * 80)
    
    analyseur = AnalyseurOnomastiqueProfond()
    
    # Phrases de test avec noms propres variés
    phrases_test = [
        ("Dr. Smith's cat—what a story!", "en"),
        ("Ésope racontait ses fables à Paris.", "fr"),
        ("The species Homo sapiens evolved in Africa.", "en"),
        ("Marie et Jean visitent Berlin chaque été.", "fr")
    ]
    
    for phrase, langue in phrases_test:
        print(f"\n" + "="*80)
        contexte = analyseur.analyser_noms_propres_complet(phrase, langue)
        
        # Sauvegarde de l'analyse
        nom_fichier = f"analyse_onomastique_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{langue}.json"
        with open(nom_fichier, 'w', encoding='utf-8') as f:
            contexte_dict = asdict(contexte)
            json.dump(contexte_dict, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Analyse onomastique sauvegardée: {nom_fichier}")


if __name__ == "__main__":
    test_analyse_onomastique()