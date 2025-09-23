#!/usr/bin/env python3
"""
🔍 AUDIT CORPUS EXISTANT + PLANIFICATION EXTENSION
Analyse état actuel corpus organisé par niveaux
Planification extension vers 1000+ exemples validation statistique
"""

import json
import os
from pathlib import Path
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import glob

@dataclass
class AnalyseCorpus:
    """Analyse d'un corpus spécifique"""
    nom: str
    chemin: str
    taille_lignes: int
    taille_docs: int
    langues: List[str]
    type_corpus: str
    qualite_estimee: float  # 0.0-1.0
    utilisable_dhatu: bool
    coverage_estimee: Dict[str, float]  # MODAL/ASPECT/QUANT
    timestamp_creation: Optional[str]

@dataclass
class PlanificationExtension:
    """Plan d'extension vers corpus 1000+ exemples"""
    objectif_total: int
    repartition_langues: Dict[str, int]
    repartition_types: Dict[str, int]
    repartition_dhatu: Dict[str, int]
    priorites_collecte: List[str]
    timeline_semaines: int
    effort_estime: str

class AuditeurCorpusComplet:
    """Auditeur complet des corpus existants avec planification extension"""
    
    def __init__(self):
        self.workspace_root = Path("/home/stephane/GitHub/PaniniFS-Research")
        self.corpus_analyses = []
        self.corpus_patterns = {
            "corpus_files": [
                "*corpus*.json",
                "*corpus*.txt", 
                "corpus*/*.json",
                "*/corpus*.json"
            ],
            "collector_files": [
                "*collector*.py",
                "*collecteur*.py",
                "corpus*collector*.py"
            ]
        }
        
        # Statistiques globales
        self.stats_globales = {
            "nb_corpus_total": 0,
            "nb_documents_total": 0,
            "nb_langues_total": 0,
            "taille_totale_lignes": 0,
            "coverage_dhatu_moyenne": {
                "MODAL": 0.0,
                "ASPECT": 0.0, 
                "QUANT": 0.0
            },
            "qualite_moyenne": 0.0,
            "corpus_utilisables": 0
        }
        
    def analyser_fichier_corpus(self, chemin_fichier: Path) -> Optional[AnalyseCorpus]:
        """Analyser un fichier corpus spécifique"""
        try:
            if not chemin_fichier.exists():
                return None
                
            # Taille en lignes
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                lignes = f.readlines()
                taille_lignes = len(lignes)
            
            # Si JSON, analyser structure
            taille_docs = 0
            langues = []
            type_corpus = "inconnu"
            timestamp_creation = None
            
            if chemin_fichier.suffix == '.json':
                try:
                    with open(chemin_fichier, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Détection structure
                    if isinstance(data, list):
                        taille_docs = len(data)
                        # Analyser premier élément pour détecter langues
                        if data and isinstance(data[0], dict):
                            if 'language' in data[0]:
                                langues = list(set(item.get('language', 'fr') for item in data if isinstance(item, dict)))
                            if 'corpus_type' in data[0]:
                                type_corpus = data[0]['corpus_type']
                    elif isinstance(data, dict):
                        if 'documents' in data:
                            taille_docs = len(data['documents'])
                        if 'metadata' in data:
                            meta = data['metadata']
                            if 'creation' in meta:
                                timestamp_creation = meta['creation']
                            if 'sources' in meta:
                                type_corpus = '_'.join(meta['sources'])
                        if 'language' in data:
                            langues = [data['language']]
                            
                except json.JSONDecodeError:
                    pass
            
            # Détection langues par nom fichier si pas trouvé
            if not langues:
                if 'multilingue' in chemin_fichier.name:
                    langues = ['fr', 'en', 'de']
                elif 'english' in chemin_fichier.name or '_en' in chemin_fichier.name:
                    langues = ['en']
                elif 'german' in chemin_fichier.name or '_de' in chemin_fichier.name:
                    langues = ['de']
                else:
                    langues = ['fr']  # Par défaut français
            
            # Détection type corpus par nom
            if type_corpus == "inconnu":
                nom_lower = chemin_fichier.name.lower()
                if 'scientific' in nom_lower or 'scientifique' in nom_lower:
                    type_corpus = "scientifique"
                elif 'children' in nom_lower or 'prescolaire' in nom_lower:
                    type_corpus = "prescolaire"
                elif 'multilingue' in nom_lower:
                    type_corpus = "multilingue"
                elif 'dhatu' in nom_lower:
                    type_corpus = "dhatu"
                else:
                    type_corpus = "general"
            
            # Estimation qualité (heuristique)
            qualite = self._estimer_qualite_corpus(chemin_fichier, taille_docs, taille_lignes)
            
            # Coverage dhātu estimée
            coverage_dhatu = self._estimer_coverage_dhatu(type_corpus, taille_docs)
            
            # Utilisabilité pour dhātu
            utilisable = taille_docs > 10 and qualite > 0.3
            
            return AnalyseCorpus(
                nom=chemin_fichier.name,
                chemin=str(chemin_fichier),
                taille_lignes=taille_lignes,
                taille_docs=taille_docs,
                langues=langues,
                type_corpus=type_corpus,
                qualite_estimee=qualite,
                utilisable_dhatu=utilisable,
                coverage_estimee=coverage_dhatu,
                timestamp_creation=timestamp_creation
            )
            
        except Exception as e:
            print(f"⚠️ Erreur analyse {chemin_fichier}: {e}")
            return None
    
    def _estimer_qualite_corpus(self, chemin: Path, nb_docs: int, nb_lignes: int) -> float:
        """Estimer qualité corpus (0.0-1.0)"""
        score = 0.5  # Base
        
        # Bonus taille
        if nb_docs > 100:
            score += 0.2
        elif nb_docs > 50:
            score += 0.1
        
        if nb_lignes > 1000:
            score += 0.2
        elif nb_lignes > 500:
            score += 0.1
        
        # Bonus par type détecté
        nom = chemin.name.lower()
        if 'unifie' in nom:
            score += 0.1
        if 'validated' in nom or 'valide' in nom:
            score += 0.1
        if 'pilot' in nom:
            score -= 0.1  # Corpus pilote moins fiable
        
        # Pénalité si trop petit
        if nb_docs < 10:
            score -= 0.3
        if nb_lignes < 100:
            score -= 0.2
        
        return max(0.0, min(1.0, score))
    
    def _estimer_coverage_dhatu(self, type_corpus: str, nb_docs: int) -> Dict[str, float]:
        """Estimer coverage MODAL/ASPECT/QUANT selon type corpus"""
        base_coverage = {
            "MODAL": 0.1,
            "ASPECT": 0.1,
            "QUANT": 0.1
        }
        
        # Facteur taille
        facteur_taille = min(1.0, nb_docs / 100.0)
        
        # Spécialisation par type
        if type_corpus == "scientifique":
            base_coverage["MODAL"] = 0.3  # Beaucoup de modalité épistémique
            base_coverage["QUANT"] = 0.4  # Quantifications nombreuses
            base_coverage["ASPECT"] = 0.2
        elif type_corpus == "prescolaire":
            base_coverage["ASPECT"] = 0.4  # Beaucoup d'actions temporelles
            base_coverage["MODAL"] = 0.2
            base_coverage["QUANT"] = 0.3
        elif type_corpus == "multilingue":
            base_coverage["MODAL"] = 0.25
            base_coverage["ASPECT"] = 0.25
            base_coverage["QUANT"] = 0.25
        elif type_corpus == "dhatu":
            base_coverage["MODAL"] = 0.5  # Optimisé pour dhātu
            base_coverage["ASPECT"] = 0.5
            base_coverage["QUANT"] = 0.5
        
        # Application facteur taille
        return {k: v * facteur_taille for k, v in base_coverage.items()}
    
    def scanner_tous_corpus(self) -> List[AnalyseCorpus]:
        """Scanner tous les corpus dans le workspace"""
        print("🔍 SCAN COMPLET CORPUS EXISTANTS")
        print("="*35)
        
        corpus_trouves = []
        
        # Scanner selon patterns
        for pattern in self.corpus_patterns["corpus_files"]:
            chemins = list(self.workspace_root.glob(pattern))
            print(f"Pattern '{pattern}': {len(chemins)} fichiers")
            
            for chemin in chemins:
                if chemin.is_file():
                    analyse = self.analyser_fichier_corpus(chemin)
                    if analyse:
                        corpus_trouves.append(analyse)
                        print(f"  ✅ {analyse.nom}: {analyse.taille_docs} docs, qualité {analyse.qualite_estimee:.2f}")
                    else:
                        print(f"  ❌ {chemin.name}: Échec analyse")
        
        self.corpus_analyses = corpus_trouves
        return corpus_trouves
    
    def calculer_statistiques_globales(self):
        """Calculer statistiques globales des corpus"""
        if not self.corpus_analyses:
            return
        
        # Compteurs
        nb_total = len(self.corpus_analyses)
        nb_docs_total = sum(c.taille_docs for c in self.corpus_analyses)
        nb_lignes_total = sum(c.taille_lignes for c in self.corpus_analyses)
        
        # Langues uniques
        langues_uniques = set()
        for corpus in self.corpus_analyses:
            langues_uniques.update(corpus.langues)
        
        # Coverage moyenne
        coverage_moy = {"MODAL": 0.0, "ASPECT": 0.0, "QUANT": 0.0}
        for dhatu in coverage_moy.keys():
            if nb_total > 0:
                coverage_moy[dhatu] = sum(c.coverage_estimee[dhatu] for c in self.corpus_analyses) / nb_total
        
        # Qualité moyenne
        qualite_moy = sum(c.qualite_estimee for c in self.corpus_analyses) / nb_total if nb_total > 0 else 0.0
        
        # Corpus utilisables
        utilisables = sum(1 for c in self.corpus_analyses if c.utilisable_dhatu)
        
        self.stats_globales = {
            "nb_corpus_total": nb_total,
            "nb_documents_total": nb_docs_total,
            "nb_langues_total": len(langues_uniques),
            "taille_totale_lignes": nb_lignes_total,
            "coverage_dhatu_moyenne": coverage_moy,
            "qualite_moyenne": qualite_moy,
            "corpus_utilisables": utilisables,
            "langues_detectees": sorted(list(langues_uniques))
        }
    
    def identifier_gaps_corpus(self) -> Dict[str, List[str]]:
        """Identifier gaps dans la couverture corpus"""
        gaps = {
            "langues_manquantes": [],
            "types_manquantes": [],
            "dhatu_sous_representes": [],
            "qualite_insuffisante": [],
            "taille_insuffisante": []
        }
        
        # Langues importantes manquantes
        langues_cibles = ['fr', 'en', 'de', 'es', 'it']
        langues_presentes = self.stats_globales.get("langues_detectees", [])
        gaps["langues_manquantes"] = [l for l in langues_cibles if l not in langues_presentes]
        
        # Types corpus manquants
        types_presents = list(set(c.type_corpus for c in self.corpus_analyses))
        types_cibles = ['scientifique', 'prescolaire', 'multilingue', 'dhatu', 'litteraire', 'journalistique']
        gaps["types_manquantes"] = [t for t in types_cibles if t not in types_presents]
        
        # Dhātu sous-représentés (< 0.3 coverage)
        coverage = self.stats_globales["coverage_dhatu_moyenne"]
        gaps["dhatu_sous_representes"] = [dhatu for dhatu, cov in coverage.items() if cov < 0.3]
        
        # Corpus qualité insuffisante (< 0.5)
        gaps["qualite_insuffisante"] = [c.nom for c in self.corpus_analyses if c.qualite_estimee < 0.5]
        
        # Corpus taille insuffisante (< 50 docs)
        gaps["taille_insuffisante"] = [c.nom for c in self.corpus_analyses if c.taille_docs < 50]
        
        return gaps
    
    def planifier_extension_1000_plus(self, gaps: Dict) -> PlanificationExtension:
        """Planifier extension vers 1000+ exemples"""
        
        # Documents actuels utilisables
        docs_actuels = sum(c.taille_docs for c in self.corpus_analyses if c.utilisable_dhatu)
        docs_manquants = max(0, 1000 - docs_actuels)
        
        print(f"📊 Documents actuels utilisables: {docs_actuels}")
        print(f"📊 Documents manquants: {docs_manquants}")
        
        # Répartition langues (équilibré + focus français)
        repartition_langues = {
            "fr": int(docs_manquants * 0.4),    # 40% français
            "en": int(docs_manquants * 0.3),    # 30% anglais  
            "de": int(docs_manquants * 0.2),    # 20% allemand
            "es": int(docs_manquants * 0.1)     # 10% espagnol
        }
        
        # Répartition types (focus validation dhātu)
        repartition_types = {
            "dhatu_specialise": int(docs_manquants * 0.3),      # 30% optimisé dhātu
            "scientifique": int(docs_manquants * 0.25),         # 25% scientifique
            "prescolaire": int(docs_manquants * 0.2),           # 20% développemental
            "litteraire": int(docs_manquants * 0.15),           # 15% littérature
            "journalistique": int(docs_manquants * 0.1)         # 10% actualités
        }
        
        # Répartition dhātu (équilibré avec bonus MODAL)
        repartition_dhatu = {
            "MODAL": int(docs_manquants * 0.4),     # 40% modalité (priorité)
            "ASPECT": int(docs_manquants * 0.3),    # 30% aspect
            "QUANT": int(docs_manquants * 0.3)      # 30% quantité
        }
        
        # Priorités collecte
        priorites = [
            "Corpus dhātu spécialisé français (expressions modales)",
            "Corpus scientifique anglais (modalité épistémique)", 
            "Corpus développemental allemand (aspects temporels)",
            "Corpus littéraire multilingue (quantifications)",
            "Validation croisée compositions inter-dhātu"
        ]
        
        # Timeline et effort
        timeline_semaines = 4  # 4 semaines pour 1000 docs
        effort = "Moyen"  # Collecte automatisée + validation manuelle
        
        return PlanificationExtension(
            objectif_total=1000,
            repartition_langues=repartition_langues,
            repartition_types=repartition_types,
            repartition_dhatu=repartition_dhatu,
            priorites_collecte=priorites,
            timeline_semaines=timeline_semaines,
            effort_estime=effort
        )
    
    def generer_rapport_audit_complet(self) -> Dict:
        """Générer rapport complet audit + planification"""
        
        # Analyse par type corpus
        analyse_par_type = defaultdict(list)
        for corpus in self.corpus_analyses:
            analyse_par_type[corpus.type_corpus].append(corpus)
        
        # Top corpus par qualité
        top_corpus = sorted(self.corpus_analyses, key=lambda c: c.qualite_estimee, reverse=True)[:5]
        
        # Gaps identifiés
        gaps = self.identifier_gaps_corpus()
        
        # Plan extension
        plan_extension = self.planifier_extension_1000_plus(gaps)
        
        rapport = {
            "audit_corpus": {
                "timestamp": "2025-09-22",
                "statistiques_globales": self.stats_globales,
                "corpus_analyses": [
                    {
                        "nom": c.nom,
                        "taille_docs": c.taille_docs,
                        "langues": c.langues,
                        "type": c.type_corpus,
                        "qualite": round(c.qualite_estimee, 2),
                        "utilisable": c.utilisable_dhatu,
                        "coverage_dhatu": {k: round(v, 2) for k, v in c.coverage_estimee.items()}
                    }
                    for c in self.corpus_analyses
                ],
                "analyse_par_type": {
                    type_corpus: {
                        "nb_corpus": len(corpus_list),
                        "nb_docs_total": sum(c.taille_docs for c in corpus_list),
                        "qualite_moyenne": round(sum(c.qualite_estimee for c in corpus_list) / len(corpus_list), 2) if corpus_list else 0
                    }
                    for type_corpus, corpus_list in analyse_par_type.items()
                },
                "top_corpus_qualite": [
                    {"nom": c.nom, "qualite": round(c.qualite_estimee, 2), "docs": c.taille_docs}
                    for c in top_corpus
                ]
            },
            "gaps_identifies": gaps,
            "planification_extension": {
                "objectif_total": plan_extension.objectif_total,
                "documents_manquants": plan_extension.objectif_total - sum(c.taille_docs for c in self.corpus_analyses if c.utilisable_dhatu),
                "repartition_langues": plan_extension.repartition_langues,
                "repartition_types": plan_extension.repartition_types,
                "repartition_dhatu": plan_extension.repartition_dhatu,
                "priorites_collecte": plan_extension.priorites_collecte,
                "timeline_semaines": plan_extension.timeline_semaines,
                "effort_estime": plan_extension.effort_estime
            },
            "recommandations_immediates": [
                "Prioriser collecte corpus dhātu spécialisé français",
                "Enrichir corpus scientifique anglais (modalité épistémique)",
                "Développer corpus aspectuel allemand",
                "Créer corpus validation compositions inter-dhātu",
                "Automatiser pipeline collecte → validation → intégration"
            ]
        }
        
        return rapport

def main():
    """Audit complet corpus + planification extension 1000+"""
    print("🔍 AUDIT CORPUS EXISTANT + PLANIFICATION EXTENSION")
    print("Analyse état actuel et plan vers 1000+ exemples")
    print("="*55)
    
    # Initialisation auditeur
    auditeur = AuditeurCorpusComplet()
    
    # Scan complet
    corpus_trouves = auditeur.scanner_tous_corpus()
    print(f"\n📊 RÉSULTAT SCAN: {len(corpus_trouves)} corpus analysés")
    
    # Calcul statistiques
    auditeur.calculer_statistiques_globales()
    stats = auditeur.stats_globales
    
    print(f"\n📈 STATISTIQUES GLOBALES:")
    print("="*25)
    print(f"✅ Corpus total: {stats['nb_corpus_total']}")
    print(f"✅ Documents total: {stats['nb_documents_total']:,}")
    print(f"✅ Langues détectées: {stats['nb_langues_total']} {stats.get('langues_detectees', [])}")
    print(f"✅ Corpus utilisables: {stats['corpus_utilisables']}")
    print(f"✅ Qualité moyenne: {stats['qualite_moyenne']:.2f}/1.0")
    print(f"✅ Coverage MODAL: {stats['coverage_dhatu_moyenne']['MODAL']:.2f}")
    print(f"✅ Coverage ASPECT: {stats['coverage_dhatu_moyenne']['ASPECT']:.2f}")
    print(f"✅ Coverage QUANT: {stats['coverage_dhatu_moyenne']['QUANT']:.2f}")
    
    # Génération rapport complet
    rapport = auditeur.generer_rapport_audit_complet()
    
    # Affichage gaps
    gaps = rapport["gaps_identifies"]
    print(f"\n🎯 GAPS IDENTIFIÉS:")
    print("="*18)
    if gaps["langues_manquantes"]:
        print(f"❌ Langues manquantes: {gaps['langues_manquantes']}")
    if gaps["dhatu_sous_representes"]:
        print(f"❌ Dhātu sous-représentés: {gaps['dhatu_sous_representes']}")
    if gaps["qualite_insuffisante"]:
        print(f"⚠️ Qualité insuffisante: {len(gaps['qualite_insuffisante'])} corpus")
    
    # Affichage plan extension
    plan = rapport["planification_extension"]
    print(f"\n🚀 PLAN EXTENSION VERS 1000+ EXEMPLES:")
    print("="*35)
    print(f"🎯 Objectif: {plan['objectif_total']} documents")
    print(f"📊 Documents manquants: {plan['documents_manquants']}")
    print(f"⏱️ Timeline: {plan['timeline_semaines']} semaines")
    print(f"💪 Effort: {plan['effort_estime']}")
    
    print(f"\n🌍 Répartition langues:")
    for langue, nb in plan["repartition_langues"].items():
        print(f"   {langue}: {nb} docs ({nb/plan['documents_manquants']*100:.0f}%)")
    
    print(f"\n📚 Répartition types:")
    for type_c, nb in plan["repartition_types"].items():
        print(f"   {type_c}: {nb} docs")
    
    print(f"\n🔧 Priorités collecte:")
    for i, priorite in enumerate(plan["priorites_collecte"], 1):
        print(f"   {i}. {priorite}")
    
    # Sauvegarde rapport
    fichier_rapport = "audit_corpus_planification_extension.json"
    with open(fichier_rapport, "w", encoding="utf-8") as f:
        json.dump(rapport, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Rapport complet sauvegardé: {fichier_rapport}")
    
    # Conclusion
    print(f"\n🎊 AUDIT TERMINÉ - PRÊT POUR EXTENSION!")
    print("="*40)
    print("✅ État corpus actuel: Analysé complètement")
    print("✅ Gaps identifiés: Documentés avec précision")
    print("✅ Plan extension: Structuré et priorisé")
    print("✅ Prochaine étape: Lancement collecte massive")
    
    return auditeur, rapport

if __name__ == "__main__":
    auditeur, rapport = main()