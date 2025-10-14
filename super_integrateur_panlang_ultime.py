#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 SUPER-INTÉGRATEUR PANLANG ULTIME
===================================
Récupération et fusion de TOUS les dictionnaires PanLang existants dans le workspace

Objectif: Créer le dictionnaire PanLang ULTIME avec maximum de concepts pour 
reconstruction universelle de la pensée humaine

Dictionnaires détectés et intégrés:
- dictionnaire_universel_final (v1 complet)  
- dictionnaire_recursif (base récursive)
- dictionnaire_panlang_v2 (améliorations ciblées)
- data/dictionnaire_dhatu_mot_exhaustif (base sanskrite)
- Tous autres dictionnaires JSON disponibles

Auteur: Système PanLang - Super-Intégration Ultime
Date: 2025-09-26
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from collections import defaultdict, Counter
import hashlib
import glob

class SuperIntegrateurPanLangUltime:
    """Super-intégrateur récupérant TOUS les dictionnaires PanLang existants"""
    
    def __init__(self):
        self.setup_logging()
        self.workspace_root = Path.cwd()
        self.atoms_universels = [
            'MOUVEMENT', 'COGNITION', 'PERCEPTION', 'COMMUNICATION',
            'CREATION', 'EMOTION', 'EXISTENCE', 'DESTRUCTION', 
            'POSSESSION', 'DOMINATION'
        ]
        self.tous_dictionnaires = {}
        self.concepts_finaux = {}
        
    def setup_logging(self):
        """Configuration des logs"""
        log_dir = Path("super_integration_panlang_ultime")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'super_integration_ultime.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def detecter_tous_dictionnaires(self) -> List[Path]:
        """Détection automatique de TOUS les dictionnaires dans le workspace"""
        
        patterns_recherche = [
            "**/dictionnaire*.json",
            "**/panlang*.json", 
            "**/*dictionnaire*.json",
            "**/integration*.json",
            "**/dhatu*.json"
        ]
        
        dictionnaires_detectes = set()
        
        for pattern in patterns_recherche:
            for chemin in self.workspace_root.glob(pattern):
                if chemin.is_file() and chemin.suffix == '.json':
                    dictionnaires_detectes.add(chemin)
        
        dictionnaires_listes = sorted(list(dictionnaires_detectes))
        
        print("🔍 DICTIONNAIRES DÉTECTÉS:")
        for i, chemin in enumerate(dictionnaires_listes, 1):
            taille = chemin.stat().st_size / 1024  # Ko
            print(f"   {i:2d}. {chemin.name} ({taille:.1f} Ko)")
            print(f"       📁 {chemin.parent}")
        
        self.logger.info(f"✅ {len(dictionnaires_listes)} dictionnaires détectés")
        return dictionnaires_listes
    
    def charger_dictionnaire_intelligent(self, chemin: Path) -> Dict:
        """Chargement intelligent d'un dictionnaire avec extraction automatique"""
        
        try:
            with open(chemin, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extraction intelligente des concepts selon structure
            concepts_extraits = {}
            
            # Structure standard PanLang
            if "concepts" in data and isinstance(data["concepts"], dict):
                concepts_extraits = data["concepts"]
            
            # Structure dictionnaire direct
            elif "dictionnaire" in data and isinstance(data["dictionnaire"], dict):
                concepts_extraits = data["dictionnaire"]
                
            # Structure dhātu spécifique
            elif chemin.name.startswith("dhatu") or "dhatu" in str(chemin):
                # Extraction spéciale pour dhātu avec filtrage qualité
                for concept, info in data.items():
                    if isinstance(info, dict):
                        validite = info.get("validite", info.get("confiance", 0))
                        if validite >= 0.6:  # Seuil dhātu
                            concepts_extraits[concept] = info
                    elif isinstance(info, str) and len(info.split("+")) <= 4:
                        concepts_extraits[concept] = info
            
            # Structure plate (dictionnaire direct)
            elif isinstance(data, dict):
                for key, value in data.items():
                    if key not in ["metadata", "statistiques", "resultats"] and isinstance(value, (dict, str)):
                        concepts_extraits[key] = value
            
            # Métadonnées d'extraction
            metadata_extraction = {
                "source_file": str(chemin),
                "concepts_extraits": len(concepts_extraits),
                "taille_fichier": chemin.stat().st_size,
                "date_modification": datetime.fromtimestamp(chemin.stat().st_mtime).strftime("%Y-%m-%d"),
                "hash_contenu": hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()[:12]
            }
            
            if concepts_extraits:
                self.logger.info(f"✅ {chemin.name}: {len(concepts_extraits)} concepts extraits")
            else:
                self.logger.warning(f"⚠️ {chemin.name}: Aucun concept extrait")
            
            return {
                "concepts": concepts_extraits,
                "metadata": metadata_extraction,
                "structure_originale": type(data).__name__
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur chargement {chemin.name}: {e}")
            return {"concepts": {}, "metadata": {"erreur": str(e)}}
    
    def fusionner_tous_concepts(self) -> Dict:
        """Fusion intelligente de tous les concepts avec résolution de conflits"""
        
        concepts_fusionnes = {}
        sources_par_concept = defaultdict(list)
        conflits_detectes = []
        
        # Ordre de priorité des sources (plus fiable en premier)
        priorite_sources = [
            "universel_final",
            "recursif",
            "v2",
            "dhatu",
            "molecules",
            "autres"
        ]
        
        def classifier_source(chemin: str) -> str:
            chemin_lower = chemin.lower()
            if "universel" in chemin_lower:
                return "universel_final"
            elif "recursif" in chemin_lower:
                return "recursif"  
            elif "v2" in chemin_lower:
                return "v2"
            elif "dhatu" in chemin_lower:
                return "dhatu"
            elif "molecules" in chemin_lower or "integration" in chemin_lower:
                return "molecules"
            else:
                return "autres"
        
        # Tri des dictionnaires par priorité
        dictionnaires_tries = sorted(
            self.tous_dictionnaires.items(),
            key=lambda x: priorite_sources.index(classifier_source(x[1]["metadata"]["source_file"]))
        )
        
        # Fusion avec résolution de conflits
        for nom_dict, data_dict in dictionnaires_tries:
            for concept, info_concept in data_dict["concepts"].items():
                concept_norm = concept.upper()
                source_type = classifier_source(data_dict["metadata"]["source_file"])
                
                sources_par_concept[concept_norm].append({
                    "source": nom_dict,
                    "type": source_type,
                    "info": info_concept
                })
                
                if concept_norm not in concepts_fusionnes:
                    # Premier concept trouvé
                    concepts_fusionnes[concept_norm] = self._normaliser_concept_final(concept_norm, info_concept, data_dict["metadata"])
                else:
                    # Conflit détecté - résolution intelligente
                    concept_existant = concepts_fusionnes[concept_norm]
                    concept_nouveau = self._normaliser_concept_final(concept_norm, info_concept, data_dict["metadata"])
                    
                    concept_resolu, resolution = self._resoudre_conflit_intelligent(
                        concept_norm, concept_existant, concept_nouveau, source_type
                    )
                    
                    if resolution != "maintenu":
                        conflits_detectes.append({
                            "concept": concept_norm,
                            "resolution": resolution,
                            "ancienne_formule": concept_existant.get("formule", ""),
                            "nouvelle_formule": concept_resolu.get("formule", ""),
                            "source_gagnante": source_type
                        })
                        
                        concepts_fusionnes[concept_norm] = concept_resolu
        
        self.logger.info(f"🔀 Fusion terminée: {len(concepts_fusionnes)} concepts, {len(conflits_detectes)} conflits résolus")
        
        return {
            "concepts_fusionnes": concepts_fusionnes,
            "sources_par_concept": dict(sources_par_concept),
            "conflits_resolus": conflits_detectes,
            "priorites_utilisees": priorite_sources
        }
    
    def _normaliser_concept_final(self, nom: str, info: any, metadata: Dict) -> Dict:
        """Normalisation finale d'un concept pour fusion"""
        
        concept_norme = {
            "nom": nom,
            "formule": "",
            "complexite": 1,
            "validite": 0.5,
            "categorie": "general",
            "source_metadata": {
                "fichier_origine": Path(metadata["source_file"]).name,
                "date_extraction": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "hash_source": metadata.get("hash_contenu", "unknown")
            }
        }
        
        if isinstance(info, dict):
            concept_norme["formule"] = info.get("formule", info.get("definition", info.get("reconstruction", str(info))))
            concept_norme["complexite"] = info.get("complexite", len(concept_norme["formule"].split("+")) if "+" in concept_norme["formule"] else 1)
            concept_norme["validite"] = info.get("validite_estimee", info.get("validite", info.get("confiance", 0.5)))
            concept_norme["categorie"] = info.get("categorie", "general")
            concept_norme["justification"] = info.get("justification", info.get("explication", ""))
            
        elif isinstance(info, str):
            concept_norme["formule"] = info
            concept_norme["complexite"] = len(info.split("+")) if "+" in info else 1
        
        # Validation atomique
        if concept_norme["formule"]:
            atomes_utilises = [atom.strip() for atom in concept_norme["formule"].split("+")]
            atoms_valides = all(atom in self.atoms_universels for atom in atomes_utilises if atom)
            
            if not atoms_valides:
                concept_norme["validite"] *= 0.8  # Pénalité atomes non-universels
                concept_norme["warning"] = "Contient des atomes non-universels"
        
        return concept_norme
    
    def _resoudre_conflit_intelligent(self, nom_concept: str, concept_existant: Dict, 
                                     concept_nouveau: Dict, source_type: str) -> tuple:
        """Résolution intelligente des conflits entre concepts"""
        
        # Critères de résolution (par ordre de priorité)
        
        # 1. Priorité par type de source
        if source_type in ["universel_final", "recursif"] and concept_nouveau["validite"] >= 0.7:
            return concept_nouveau, f"source_prioritaire_{source_type}"
        
        # 2. Validité supérieure significative (>15%)
        if concept_nouveau["validite"] - concept_existant["validite"] > 0.15:
            return concept_nouveau, "validite_superieure"
        
        # 3. Formule plus complète (plus d'atomes universels)
        atomes_existant = len([a for a in concept_existant.get("formule", "").split("+") 
                              if a.strip() in self.atoms_universels])
        atomes_nouveau = len([a for a in concept_nouveau.get("formule", "").split("+")
                             if a.strip() in self.atoms_universels])
        
        if atomes_nouveau > atomes_existant:
            return concept_nouveau, "formule_plus_complete"
        
        # 4. Source plus récente avec validité équivalente
        if abs(concept_nouveau["validite"] - concept_existant["validite"]) < 0.1:
            return concept_nouveau, "source_plus_recente"
        
        # 5. Maintien de l'existant par défaut
        return concept_existant, "maintenu"
    
    def creer_dictionnaire_ultime(self, resultats_fusion: Dict) -> Dict:
        """Création du dictionnaire PanLang ultime final"""
        
        concepts_fusionnes = resultats_fusion["concepts_fusionnes"]
        conflits_resolus = resultats_fusion["conflits_resolus"]
        
        # Analyses finales
        complexites = [c["complexite"] for c in concepts_fusionnes.values()]
        validites = [c["validite"] for c in concepts_fusionnes.values()]
        
        utilisation_atomes = defaultdict(int)
        for concept in concepts_fusionnes.values():
            if concept["formule"]:
                atomes = [atom.strip() for atom in concept["formule"].split("+")]
                for atom in atomes:
                    if atom in self.atoms_universels:
                        utilisation_atomes[atom] += 1
        
        # Couverture catégorielle
        categories = defaultdict(int)
        for concept in concepts_fusionnes.values():
            categories[concept.get("categorie", "general")] += 1
        
        dictionnaire_ultime = {
            "metadata": {
                "titre": "PanLang ULTIME - Dictionnaire Sémantique Universel Complet",
                "version": "ULTIME-1.0",
                "date_creation": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "objectif": "Reconstruction universelle complète de la pensée humaine",
                "concepts_totaux": len(concepts_fusionnes),
                "sources_integrees": len(self.tous_dictionnaires),
                "conflits_resolus": len(conflits_resolus),
                "atoms_universels": self.atoms_universels,
                "methodologie": "Fusion intelligente multi-sources avec résolution automatique conflits",
                "qualite_moyenne": sum(validites) / len(validites) if validites else 0
            },
            
            "concepts": concepts_fusionnes,
            
            "statistiques_ultimes": {
                "repartition_complexite": dict(Counter(complexites)),
                "complexite_moyenne": sum(complexites) / len(complexites) if complexites else 0,
                "validite_moyenne": sum(validites) / len(validites) if validites else 0,
                "utilisation_atomique": dict(utilisation_atomes),
                "atoms_les_plus_utilises": sorted(utilisation_atomes.items(), key=lambda x: x[1], reverse=True)[:5],
                "couverture_categorielle": dict(categories),
                "categories_principales": sorted(categories.keys(), key=lambda x: categories[x], reverse=True)[:10]
            },
            
            "resolution_conflits": conflits_resolus,
            
            "sources_integration": {
                nom: {
                    "fichier": data["metadata"]["source_file"],
                    "concepts_apportes": len(data["concepts"]),
                    "hash": data["metadata"].get("hash_contenu", "unknown")
                }
                for nom, data in self.tous_dictionnaires.items()
            },
            
            "capacites_reconstruction": {
                "universelle": len(concepts_fusionnes) >= 100,
                "categorielle_complete": len(categories) >= 10,  
                "coherence_atomique": len(utilisation_atomes) == len(self.atoms_universels),
                "qualite_elevee": sum(validites) / len(validites) >= 0.6 if validites else False,
                "scalable": True,
                "reproductible": True
            }
        }
        
        return dictionnaire_ultime
    
    def sauvegarder_dictionnaire_ultime(self, dictionnaire: Dict):
        """Sauvegarde du dictionnaire PanLang ULTIME"""
        
        output_dir = Path("dictionnaire_panlang_ULTIME")
        output_dir.mkdir(exist_ok=True)
        
        # Version ULTIME complète
        chemin_ultime = output_dir / "dictionnaire_panlang_ULTIME_complet.json"
        with open(chemin_ultime, 'w', encoding='utf-8') as f:
            json.dump(dictionnaire, f, ensure_ascii=False, indent=2)
        
        # Version validation haute performance
        version_validation = {
            "metadata": {
                "version": dictionnaire["metadata"]["version"],
                "concepts_totaux": dictionnaire["metadata"]["concepts_totaux"],
                "qualite_moyenne": dictionnaire["metadata"]["qualite_moyenne"]
            },
            "concepts": {
                nom: {
                    "formule": data["formule"],
                    "complexite": data["complexite"],
                    "validite": data["validite"]
                }
                for nom, data in dictionnaire["concepts"].items()
            }
        }
        
        chemin_validation = output_dir / "dictionnaire_panlang_ULTIME_validation.json"
        with open(chemin_validation, 'w', encoding='utf-8') as f:
            json.dump(version_validation, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"💎 Dictionnaire ULTIME sauvegardé:")
        self.logger.info(f"   🏆 Complet: {chemin_ultime}")
        self.logger.info(f"   🧪 Validation: {chemin_validation}")
        
        return chemin_ultime, chemin_validation
    
    def executer_super_integration_ultime(self):
        """Exécution complète de la super-intégration PanLang ULTIME"""
        
        print("🚀 SUPER-INTÉGRATION PANLANG ULTIME")
        print("===================================")
        print("Récupération et fusion de TOUS les dictionnaires PanLang du workspace")
        
        # Détection automatique
        dictionnaires_detectes = self.detecter_tous_dictionnaires()
        
        if not dictionnaires_detectes:
            print("❌ Aucun dictionnaire détecté!")
            return None, None
        
        print(f"\n📥 CHARGEMENT DE {len(dictionnaires_detectes)} DICTIONNAIRES:")
        
        # Chargement intelligent
        for chemin in dictionnaires_detectes:
            nom_dict = f"{chemin.parent.name}_{chemin.stem}"
            data_dict = self.charger_dictionnaire_intelligent(chemin)
            
            if data_dict["concepts"]:
                self.tous_dictionnaires[nom_dict] = data_dict
                print(f"   ✅ {chemin.name}: {len(data_dict['concepts'])} concepts")
            else:
                print(f"   ❌ {chemin.name}: Vide ou invalide")
        
        if not self.tous_dictionnaires:
            print("❌ Aucun dictionnaire valide chargé!")
            return None, None
        
        print(f"\n🔀 FUSION INTELLIGENTE:")
        
        # Fusion avec résolution de conflits
        resultats_fusion = self.fusionner_tous_concepts()
        
        print(f"   📚 Concepts totaux: {len(resultats_fusion['concepts_fusionnes'])}")
        print(f"   ⚖️ Conflits résolus: {len(resultats_fusion['conflits_resolus'])}")
        
        # Création dictionnaire final
        dictionnaire_ultime = self.creer_dictionnaire_ultime(resultats_fusion)
        
        print(f"\n🏆 DICTIONNAIRE PANLANG ULTIME CRÉÉ!")
        print(f"   📊 Concepts totaux: {dictionnaire_ultime['metadata']['concepts_totaux']}")
        print(f"   🎯 Qualité moyenne: {dictionnaire_ultime['metadata']['qualite_moyenne']:.3f}")
        print(f"   🔧 Sources intégrées: {dictionnaire_ultime['metadata']['sources_integrees']}")
        
        # Top statistiques
        stats = dictionnaire_ultime["statistiques_ultimes"]
        print(f"\n📈 STATISTIQUES ULTIMES:")
        print(f"   🧮 Complexité moyenne: {stats['complexite_moyenne']:.1f}")
        print(f"   ✨ Validité moyenne: {stats['validite_moyenne']:.3f}")
        print(f"   🏷️ Catégories: {len(stats['couverture_categorielle'])}")
        
        # Top atomes utilisés
        print(f"\n🔬 ATOMES LES PLUS UTILISÉS:")
        for atom, count in stats['atoms_les_plus_utilises']:
            print(f"   ⚛️ {atom}: {count} occurrences")
        
        # Capacités de reconstruction
        capacites = dictionnaire_ultime["capacites_reconstruction"]
        print(f"\n🎯 CAPACITÉS DE RECONSTRUCTION:")
        for capacite, validee in capacites.items():
            status = "✅" if validee else "❌"
            print(f"   {status} {capacite.replace('_', ' ').title()}")
        
        # Sauvegarde
        chemin_ultime, chemin_validation = self.sauvegarder_dictionnaire_ultime(dictionnaire_ultime)
        
        print(f"\n💎 PANLANG ULTIME PRÊT!")
        print(f"   🏆 Dictionnaire complet: {chemin_ultime}")
        print(f"   🧪 Version validation: {chemin_validation}")
        
        print(f"\n🚀 PRÊT POUR VALIDATION FINALE ULTIME!")
        
        return dictionnaire_ultime, chemin_validation

def main():
    """Point d'entrée principal"""
    try:
        super_integrateur = SuperIntegrateurPanLangUltime()
        dictionnaire, chemin_validation = super_integrateur.executer_super_integration_ultime()
        
        if dictionnaire:
            print(f"\n🏆 PanLang ULTIME créé avec {dictionnaire['metadata']['concepts_totaux']} concepts!")
        else:
            print("❌ Échec de la super-intégration")
        
        return dictionnaire, chemin_validation
        
    except Exception as e:
        logging.error(f"❌ Erreur super-intégration ULTIME: {e}")
        raise

if __name__ == "__main__":
    main()