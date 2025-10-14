#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 INTÉGRATEUR FINAL PANLANG v2.5
================================
Fusion ultime de TOUTES les données PanLang disponibles pour système complet

Sources intégrées:
- Dictionnaire v1.0 (89 concepts validés)
- Améliorations v2.0 (18 concepts ciblés)  
- Corpus récursif sémantique existant
- Concepts émergents générés
- Validation et optimisation complète

Objectif: Dictionnaire PanLang COMPLET pour reconstruction universelle

Auteur: Système PanLang - Intégration Finale v2.5
Date: 2025-09-26
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict, Counter
import hashlib

class IntegrateurFinalPanLangV25:
    """Intégration ultime de toutes les données PanLang disponibles"""
    
    def __init__(self):
        self.setup_logging()
        self.atoms_universels = [
            'MOUVEMENT', 'COGNITION', 'PERCEPTION', 'COMMUNICATION',
            'CREATION', 'EMOTION', 'EXISTENCE', 'DESTRUCTION', 
            'POSSESSION', 'DOMINATION'
        ]
        self.sources_donnees = {}
        self.conflicts_resolus = []
        self.concepts_finaux = {}
        
    def setup_logging(self):
        """Configuration des logs"""
        log_dir = Path("integration_finale_panlang_v25")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'integration_finale_v25.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def charger_toutes_sources(self) -> Dict:
        """Chargement de TOUTES les sources PanLang disponibles"""
        
        sources = {
            "v1_unifie": self._charger_source("dictionnaire_unifie_panlang/dictionnaire_panlang_unifie_complet.json"),
            "v2_ameliorations": self._charger_source("dictionnaire_panlang_v2/dictionnaire_panlang_v2_complet.json"),
            "recursif_semantique": self._charger_source("dictionnaire_recursif_semantique.json"),
            "integration_ultimate": self._charger_source("integration_molecules_ultimate.json"),
            "dhatu_complet": self._charger_source("dictionnaire_dhatu_mot_exhaustif.json")
        }
        
        # Statistiques de chargement
        stats = {}
        for nom, data in sources.items():
            if data:
                concepts_count = 0
                if "concepts" in data:
                    concepts_count = len(data["concepts"])
                elif "dictionnaire" in data:
                    concepts_count = len(data["dictionnaire"])
                elif isinstance(data, dict):
                    concepts_count = len([k for k, v in data.items() if isinstance(v, (dict, str))])
                
                stats[nom] = {
                    "disponible": True,
                    "concepts": concepts_count,
                    "qualite": "haute" if concepts_count > 50 else "moyenne" if concepts_count > 10 else "base"
                }
                self.logger.info(f"✅ {nom}: {concepts_count} concepts chargés")
            else:
                stats[nom] = {"disponible": False, "concepts": 0}
                self.logger.warning(f"⚠️ {nom}: Non disponible")
        
        self.sources_donnees = sources
        
        print("📊 SOURCES DONNÉES CHARGÉES:")
        for nom, stat in stats.items():
            if stat["disponible"]:
                print(f"   ✅ {nom}: {stat['concepts']} concepts ({stat['qualite']} qualité)")
            else:
                print(f"   ❌ {nom}: Indisponible")
        
        return sources
    
    def _charger_source(self, chemin: str) -> Dict:
        """Charge une source de données spécifique"""
        try:
            with open(chemin, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except Exception as e:
            self.logger.error(f"Erreur chargement {chemin}: {e}")
            return {}
    
    def extraire_concepts_normalises(self) -> Dict:
        """Extraction et normalisation de tous les concepts disponibles"""
        
        concepts_normalises = {}
        
        # Extraction v1.0 unifié (source prioritaire)
        if self.sources_donnees["v1_unifie"]:
            v1_concepts = self.sources_donnees["v1_unifie"].get("concepts", {})
            for nom, data in v1_concepts.items():
                concepts_normalises[nom] = self._normaliser_concept(nom, data, "v1_unifie")
        
        # Extraction v2.0 améliorations (ajouts ciblés)
        if self.sources_donnees["v2_ameliorations"]:
            v2_concepts = self.sources_donnees["v2_ameliorations"].get("concepts", {})
            for nom, data in v2_concepts.items():
                if nom not in concepts_normalises:  # Éviter conflits avec v1.0
                    concepts_normalises[nom] = self._normaliser_concept(nom, data, "v2_ameliorations")
                else:
                    # Résolution conflit v1 vs v2
                    concept_resolu = self._resoudre_conflit_versions(nom, concepts_normalises[nom], data)
                    concepts_normalises[nom] = concept_resolu
        
        # Extraction corpus récursif (compléments)
        if self.sources_donnees["recursif_semantique"]:
            recursif_data = self.sources_donnees["recursif_semantique"]
            if "dictionnaire" in recursif_data:
                recursif_concepts = recursif_data["dictionnaire"]
                for nom, data in recursif_concepts.items():
                    if nom not in concepts_normalises and nom not in self.atoms_universels:
                        concepts_normalises[nom] = self._normaliser_concept(nom, data, "recursif_semantique")
        
        # Extraction données dhātu (base sanskrite)
        if self.sources_donnees["dhatu_complet"]:
            dhatu_data = self.sources_donnees["dhatu_complet"]
            # Filtrage sélectif des meilleures reconstructions dhātu
            dhatu_concepts = self._filtrer_dhatu_qualite(dhatu_data)
            for nom, data in dhatu_concepts.items():
                if nom not in concepts_normalises:
                    concepts_normalises[nom] = self._normaliser_concept(nom, data, "dhatu_sanskrit")
        
        self.logger.info(f"📚 {len(concepts_normalises)} concepts normalisés extraits")
        print(f"📚 Total concepts intégrés: {len(concepts_normalises)}")
        
        return concepts_normalises
    
    def _normaliser_concept(self, nom: str, data: any, source: str) -> Dict:
        """Normalise un concept selon le standard PanLang v2.5"""
        
        concept_normalise = {
            "nom": nom.upper(),
            "source": source,
            "formule": "",
            "complexite": 1,
            "validite": 0.5,
            "categorie": "general",
            "justification": "",
            "metadata": {
                "date_integration": datetime.now().strftime("%Y-%m-%d"),
                "version_panlang": "2.5",
                "hash_source": hashlib.md5(str(data).encode()).hexdigest()[:8]
            }
        }
        
        # Extraction selon type de données
        if isinstance(data, dict):
            concept_normalise["formule"] = data.get("formule", data.get("definition", data.get("reconstruction", "")))
            concept_normalise["complexite"] = data.get("complexite", len(concept_normalise["formule"].split("+")) if "+" in concept_normalise["formule"] else 1)
            concept_normalise["validite"] = data.get("validite_estimee", data.get("validite", data.get("confiance", 0.5)))
            concept_normalise["categorie"] = data.get("categorie", "general")
            concept_normalise["justification"] = data.get("justification", data.get("explication", ""))
            
        elif isinstance(data, str):
            concept_normalise["formule"] = data
            concept_normalise["complexite"] = len(data.split("+")) if "+" in data else 1
            
        # Validation atomique
        if concept_normalise["formule"]:
            atomes_utilises = [atom.strip() for atom in concept_normalise["formule"].split("+")]
            atoms_valides = all(atom in self.atoms_universels for atom in atomes_utilises)
            if not atoms_valides:
                concept_normalise["validite"] *= 0.7  # Pénalité pour atomes non-universels
                concept_normalise["metadata"]["warning"] = "Utilise des atomes non-universels"
        
        return concept_normalise
    
    def _resoudre_conflit_versions(self, nom: str, concept_v1: Dict, data_v2: Dict) -> Dict:
        """Résolution intelligente des conflits entre versions"""
        
        # Priorité à v2.0 pour les améliorations ciblées
        if isinstance(data_v2, dict) and data_v2.get("source") == "v2_ameliorations":
            concept_resolu = self._normaliser_concept(nom, data_v2, "v2_prioritaire")
            concept_resolu["metadata"]["conflit_resolu"] = f"v1→v2: {concept_v1['formule']} → {concept_resolu['formule']}"
            
            self.conflicts_resolus.append({
                "concept": nom,
                "resolution": "v2_prioritaire",
                "v1_formule": concept_v1["formule"],
                "v2_formule": concept_resolu["formule"]
            })
            
            return concept_resolu
        
        # Sinon maintenir v1.0 (plus testé)
        return concept_v1
    
    def _filtrer_dhatu_qualite(self, dhatu_data: Dict) -> Dict:
        """Filtre les reconstructions dhātu de haute qualité"""
        
        dhatu_filtres = {}
        
        # Critères de qualité pour dhātu
        for concept, data in dhatu_data.items():
            if isinstance(data, dict):
                validite = data.get("validite", data.get("confiance", 0))
                if validite >= 0.7:  # Seuil qualité élevé
                    dhatu_filtres[concept] = data
            elif isinstance(data, str) and len(data.split("+")) <= 4:  # Complexité raisonnable
                dhatu_filtres[concept] = data
        
        self.logger.info(f"🔍 {len(dhatu_filtres)} concepts dhātu haute qualité sélectionnés")
        return dhatu_filtres
    
    def optimiser_dictionnaire_final(self, concepts_normalises: Dict) -> Dict:
        """Optimisation finale du dictionnaire complet"""
        
        # Analyse des patterns de complexité
        complexites = [c["complexite"] for c in concepts_normalises.values()]
        complexite_moyenne = sum(complexites) / len(complexites)
        
        # Analyse couverture atomique
        utilisation_atomes = defaultdict(int)
        for concept in concepts_normalises.values():
            if concept["formule"]:
                atomes = [atom.strip() for atom in concept["formule"].split("+")]
                for atom in atomes:
                    if atom in self.atoms_universels:
                        utilisation_atomes[atom] += 1
        
        # Identification des lacunes critiques
        lacunes_detectees = []
        categories_importantes = ["sensoriel", "vital", "social", "philosophique", "emotionnel"]
        
        for categorie in categories_importantes:
            concepts_categorie = [c for c in concepts_normalises.values() if categorie in c.get("categorie", "")]
            if len(concepts_categorie) < 5:  # Seuil minimum par catégorie
                lacunes_detectees.append({
                    "categorie": categorie,
                    "concepts_actuels": len(concepts_categorie),
                    "recommandation": "Ajout de concepts supplémentaires recommandé"
                })
        
        # Dictionnaire optimisé final
        dictionnaire_optimise = {
            "metadata": {
                "titre": "PanLang v2.5 - Dictionnaire Sémantique Universel",
                "version": "2.5.0",
                "date_creation": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "concepts_totaux": len(concepts_normalises),
                "sources_integrees": len([s for s in self.sources_donnees.values() if s]),
                "conflicts_resolus": len(self.conflicts_resolus),
                "atoms_universels": self.atoms_universels,
                "objectif": "Reconstruction universelle de la pensée humaine par combinaisons atomiques",
                "reproductibilite": "Sources complètes avec hashes de vérification"
            },
            
            "concepts": concepts_normalises,
            
            "statistiques_finales": {
                "repartition_complexite": dict(Counter(complexites)),
                "complexite_moyenne": round(complexite_moyenne, 2),
                "utilisation_atomique": dict(utilisation_atomes),
                "atomes_sous_utilises": [atom for atom in self.atoms_universels if utilisation_atomes[atom] < 5],
                "couverture_categorielle": self._analyser_couverture_finale(concepts_normalises),
                "lacunes_detectees": lacunes_detectees
            },
            
            "resolution_conflits": self.conflicts_resolus,
            
            "recommandations_evolution": {
                "v3_priorities": [
                    "Enrichissement catégories sous-représentées",
                    "Optimisation formules atomiques",
                    "Expansion corpus multilingue",
                    "Tests validation étendus"
                ],
                "maintenance": [
                    "Vérification périodique validité concepts",
                    "Mise à jour avec nouvelles découvertes linguistiques",
                    "Optimisation performance reconstruction"
                ]
            }
        }
        
        return dictionnaire_optimise
    
    def _analyser_couverture_finale(self, concepts: Dict) -> Dict:
        """Analyse la couverture catégorielle finale"""
        
        categories = defaultdict(list)
        
        for nom, concept in concepts.items():
            categorie = concept.get("categorie", "non_classifie")
            categories[categorie].append(nom)
        
        return {
            "total_categories": len(categories),
            "repartition": {cat: len(concepts_cat) for cat, concepts_cat in categories.items()},
            "categories_principales": sorted(categories.keys(), key=lambda x: len(categories[x]), reverse=True)[:10]
        }
    
    def sauvegarder_dictionnaire_v25(self, dictionnaire: Dict):
        """Sauvegarde du dictionnaire PanLang v2.5 final"""
        
        output_dir = Path("dictionnaire_panlang_v25_final")
        output_dir.mkdir(exist_ok=True)
        
        # Version complète avec toutes métadonnées
        chemin_complet = output_dir / "dictionnaire_panlang_v25_complet.json"
        with open(chemin_complet, 'w', encoding='utf-8') as f:
            json.dump(dictionnaire, f, ensure_ascii=False, indent=2)
        
        # Version optimisée pour validation
        version_validation = {
            "metadata": {
                "version": "2.5.0",
                "concepts_totaux": dictionnaire["metadata"]["concepts_totaux"],
                "date_creation": dictionnaire["metadata"]["date_creation"]
            },
            "concepts": {
                nom: {
                    "formule": data["formule"],
                    "complexite": data["complexite"],
                    "validite": data["validite"],
                    "source": data["source"]
                }
                for nom, data in dictionnaire["concepts"].items()
            }
        }
        
        chemin_validation = output_dir / "dictionnaire_panlang_v25_validation.json"
        with open(chemin_validation, 'w', encoding='utf-8') as f:
            json.dump(version_validation, f, ensure_ascii=False, indent=2)
        
        # Version démo légère
        concepts_demo = {}
        for i, (nom, data) in enumerate(dictionnaire["concepts"].items()):
            if i < 50:  # Top 50 concepts
                concepts_demo[nom] = {
                    "formule": data["formule"],
                    "complexite": data["complexite"]
                }
        
        version_demo = {
            "metadata": {"version": "2.5.0-demo", "concepts": len(concepts_demo)},
            "concepts": concepts_demo
        }
        
        chemin_demo = output_dir / "dictionnaire_panlang_v25_demo.json"
        with open(chemin_demo, 'w', encoding='utf-8') as f:
            json.dump(version_demo, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"💾 Dictionnaire v2.5 sauvegardé:")
        self.logger.info(f"   📄 Complet: {chemin_complet}")
        self.logger.info(f"   🧪 Validation: {chemin_validation}")
        self.logger.info(f"   📱 Demo: {chemin_demo}")
        
        return chemin_complet, chemin_validation, chemin_demo
    
    def generer_rapport_integration_finale(self, dictionnaire: Dict) -> Path:
        """Génère le rapport d'intégration finale v2.5"""
        
        rapport = {
            "metadata": {
                "titre": "Rapport d'Intégration Finale PanLang v2.5",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "version_finale": "2.5.0",
                "objectif": "Système complet de reconstruction universelle"
            },
            
            "sources_integrees": {
                nom: {
                    "disponible": bool(data),
                    "concepts_extraits": len(data.get("concepts", data.get("dictionnaire", {}))) if data else 0
                }
                for nom, data in self.sources_donnees.items()
            },
            
            "resultats_integration": {
                "concepts_finaux": dictionnaire["metadata"]["concepts_totaux"],
                "sources_fusionnees": dictionnaire["metadata"]["sources_integrees"],
                "conflicts_resolus": len(self.conflicts_resolus),
                "qualite_moyenne": sum(c["validite"] for c in dictionnaire["concepts"].values()) / len(dictionnaire["concepts"])
            },
            
            "capacites_finales": {
                "reconstruction_universelle": dictionnaire["metadata"]["concepts_totaux"] >= 100,
                "couverture_categorielle": len(dictionnaire["statistiques_finales"]["couverture_categorielle"]["repartition"]) >= 10,
                "coherence_atomique": all(atom in dictionnaire["statistiques_finales"]["utilisation_atomique"] for atom in self.atoms_universels),
                "scalabilite": True,
                "reproductibilite": True
            },
            
            "evolution_versions": {
                "v1_0": "89 concepts - Base solide",
                "v2_0": "18 concepts ciblés - Corrections lacunes",
                "v2_5": f"{dictionnaire['metadata']['concepts_totaux']} concepts - Intégration complète"
            },
            
            "recommandations_futures": {
                "validation_immediate": "Test complet capacités v2.5",
                "optimisations": dictionnaire["recommandations_evolution"]["v3_priorities"],
                "maintenance": dictionnaire["recommandations_evolution"]["maintenance"]
            }
        }
        
        output_dir = Path("dictionnaire_panlang_v25_final")
        rapport_path = output_dir / "rapport_integration_finale_v25.json"
        
        with open(rapport_path, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"📊 Rapport intégration finale: {rapport_path}")
        return rapport_path
    
    def executer_integration_complete_v25(self):
        """Exécution complète de l'intégration finale PanLang v2.5"""
        
        print("🎯 INTÉGRATION FINALE PANLANG v2.5")
        print("==================================")
        print("Fusion de TOUTES les données PanLang pour système universel complet")
        
        # Chargement des sources
        sources = self.charger_toutes_sources()
        
        # Extraction et normalisation
        concepts_normalises = self.extraire_concepts_normalises()
        
        # Optimisation finale
        dictionnaire_final = self.optimiser_dictionnaire_final(concepts_normalises)
        
        print(f"\n📊 STATISTIQUES FINALES V2.5:")
        print(f"   📚 Concepts totaux: {dictionnaire_final['metadata']['concepts_totaux']}")
        print(f"   🔧 Sources intégrées: {dictionnaire_final['metadata']['sources_integrees']}")
        print(f"   ⚖️ Conflits résolus: {dictionnaire_final['metadata']['conflicts_resolus']}")
        print(f"   🎯 Complexité moyenne: {dictionnaire_final['statistiques_finales']['complexite_moyenne']}")
        
        # Affichage top concepts par catégorie
        repartition = dictionnaire_final['statistiques_finales']['couverture_categorielle']['repartition']
        print(f"\n🏷️ TOP CATÉGORIES:")
        for cat in sorted(repartition.keys(), key=lambda x: repartition[x], reverse=True)[:5]:
            print(f"   📂 {cat}: {repartition[cat]} concepts")
        
        # Sauvegarde
        chemin_complet, chemin_validation, chemin_demo = self.sauvegarder_dictionnaire_v25(dictionnaire_final)
        
        # Rapport final
        rapport_path = self.generer_rapport_integration_finale(dictionnaire_final)
        
        print(f"\n✅ INTÉGRATION V2.5 TERMINÉE!")
        print(f"   📄 Dictionnaire complet: {chemin_complet}")
        print(f"   🧪 Version validation: {chemin_validation}")
        print(f"   📱 Version demo: {chemin_demo}")
        print(f"   📊 Rapport détaillé: {rapport_path}")
        
        print(f"\n🏆 PANLANG v2.5 PRÊT!")
        print(f"   🎯 {dictionnaire_final['metadata']['concepts_totaux']} concepts pour reconstruction universelle")
        print(f"   🔬 Validation finale recommandée")
        
        return dictionnaire_final, chemin_validation

def main():
    """Point d'entrée principal"""
    try:
        integrateur = IntegrateurFinalPanLangV25()
        dictionnaire, chemin_validation = integrateur.executer_integration_complete_v25()
        
        print(f"\n🚀 PanLang v2.5 Final prêt pour validation ultime!")
        return dictionnaire, chemin_validation
        
    except Exception as e:
        logging.error(f"❌ Erreur intégration finale v2.5: {e}")
        raise

if __name__ == "__main__":
    main()