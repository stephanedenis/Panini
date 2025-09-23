#!/usr/bin/env python3
"""
🎯 OPTIMISATION QUALITÉ CORPUS V2 - ADAPTATION SCIENTIFIQUE MULTILINGUE
Amélioration détection dhātu pour corpus scientifiques anglais/français
Patterns spécialisés modalité épistémique scientifique
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass, asdict
import re

# Import système dhātu unifié
try:
    from integration_complete_dhatu_trio import SystemeDhatuUnifie
except ImportError as e:
    print(f"⚠️ Erreur import dhātu: {e}")
    sys.exit(1)


@dataclass
class AnalyseDhatuDocument:
    """Analyse dhātu adaptée corpus scientifique"""
    document_id: str
    langue: str
    titre: str
    abstract_extrait: str
    expressions_modales: List[str]
    expressions_aspect: List[str] 
    expressions_quant: List[str]
    score_modalite_epistemique: float
    score_aspect_temporel: float
    score_quantification: float
    score_global: float


class OptimisateurCorpusScientifique:
    """Optimisateur spécialisé corpus scientifiques multilingues"""
    
    def __init__(self):
        self.workspace = Path("/home/stephane/GitHub/PaniniFS-Research")
        self.systeme_dhatu = SystemeDhatuUnifie()
        
        # Patterns scientifiques spécialisés
        self.patterns_scientifiques = {
            # MODALITÉ ÉPISTÉMIQUE (très fréquente en sciences)
            "modal_epistemique_fr": [
                r"\b(nous montrons|nous prouvons|nous démontrons)\b",
                r"\b(il est probable|il est possible|il semble)\b",
                r"\b(supposons|admettons|considérons)\b",
                r"\b(probablement|vraisemblablement|certainement)\b",
                r"\b(peut être|pourrait être|devrait être)\b"
            ],
            "modal_epistemique_en": [
                r"\b(we show|we prove|we demonstrate|we establish)\b",
                r"\b(it is likely|it is possible|it appears|it seems)\b",
                r"\b(assume|suppose|consider|let)\b",
                r"\b(probably|likely|certainly|presumably)\b",
                r"\b(may be|could be|should be|might be)\b",
                r"\b(we believe|we conjecture|we hypothesize)\b"
            ],
            
            # ASPECT (processus scientifiques)
            "aspect_processus_fr": [
                r"\b(commencer|débuter|initier|entamer)\b",
                r"\b(continuer|poursuivre|maintenir)\b",
                r"\b(terminer|finir|conclure|achever)\b",
                r"\b(évoluer|progresser|se développer)\b",
                r"\b(en cours|en train de|sur le point de)\b"
            ],
            "aspect_processus_en": [
                r"\b(begin|start|initiate|commence)\b",
                r"\b(continue|proceed|maintain|sustain)\b",
                r"\b(finish|complete|conclude|terminate)\b",
                r"\b(evolve|progress|develop|advance)\b",
                r"\b(ongoing|in progress|in the process of)\b"
            ],
            
            # QUANTIFICATION (très présente en sciences)
            "quantification_fr": [
                r"\b(nombreux|plusieurs|quelques|peu de)\b",
                r"\b(beaucoup|énormément|considérablement)\b",
                r"\b(plus|moins|autant|davantage)\b",
                r"\b(environ|approximativement|près de)\s+\d+",
                r"\b(tous|toutes|chaque|aucun)\b"
            ],
            "quantification_en": [
                r"\b(many|several|few|some|numerous)\b",
                r"\b(much|significantly|considerably|substantially)\b",
                r"\b(more|less|most|least|as much)\b",
                r"\b(approximately|roughly|about|around)\s+\d+",
                r"\b(all|every|each|any|no|none)\b"
            ]
        }
        
    def analyser_document_scientifique(self, doc: Dict) -> AnalyseDhatuDocument:
        """Analyser document scientifique avec patterns spécialisés"""
        
        # Extraction champs
        doc_id = doc.get('id', 'unknown')
        langue = doc.get('language', 'en')
        titre = doc.get('title', '')
        abstract = doc.get('abstract', '')
        
        # Texte complet pour analyse
        texte_complet = f"{titre} {abstract}".lower()
        
        # Détection patterns selon langue
        if langue == 'fr':
            modal_patterns = self.patterns_scientifiques["modal_epistemique_fr"]
            aspect_patterns = self.patterns_scientifiques["aspect_processus_fr"]
            quant_patterns = self.patterns_scientifiques["quantification_fr"]
        else:  # Défaut anglais
            modal_patterns = self.patterns_scientifiques["modal_epistemique_en"]
            aspect_patterns = self.patterns_scientifiques["aspect_processus_en"]
            quant_patterns = self.patterns_scientifiques["quantification_en"]
        
        # Détection expressions
        expr_modales = self._detecter_expressions(texte_complet, modal_patterns)
        expr_aspect = self._detecter_expressions(texte_complet, aspect_patterns)
        expr_quant = self._detecter_expressions(texte_complet, quant_patterns)
        
        # Scores spécialisés
        score_modal = self._calculer_score_modalite_epistemique(expr_modales, texte_complet)
        score_aspect = self._calculer_score_aspect(expr_aspect, texte_complet)
        score_quant = self._calculer_score_quantification(expr_quant, texte_complet)
        
        # Score global
        score_global = (score_modal * 0.4 + score_aspect * 0.3 + score_quant * 0.3)
        
        return AnalyseDhatuDocument(
            document_id=doc_id,
            langue=langue,
            titre=titre[:100] + "..." if len(titre) > 100 else titre,
            abstract_extrait=abstract[:200] + "..." if len(abstract) > 200 else abstract,
            expressions_modales=expr_modales,
            expressions_aspect=expr_aspect,
            expressions_quant=expr_quant,
            score_modalite_epistemique=score_modal,
            score_aspect_temporel=score_aspect,
            score_quantification=score_quant,
            score_global=score_global
        )
    
    def _detecter_expressions(self, texte: str, patterns: List[str]) -> List[str]:
        """Détecter expressions selon patterns"""
        expressions = []
        for pattern in patterns:
            matches = re.findall(pattern, texte, re.IGNORECASE)
            expressions.extend(matches)
        return list(set(expressions))  # Déduplication
    
    def _calculer_score_modalite_epistemique(self, expressions: List[str], texte: str) -> float:
        """Score modalité épistémique adapté corpus scientifique"""
        if not texte:
            return 0.0
        
        # Base sur densité expressions
        nb_mots = len(texte.split())
        densite = len(expressions) / max(1, nb_mots / 100)  # Expressions per 100 words
        
        # Bonus spécifiques modalité épistémique scientifique
        bonus = 0.0
        texte_lower = texte.lower()
        
        # Marqueurs épistémiques forts
        if any(marker in texte_lower for marker in ['we prove', 'nous prouvons', 'we show', 'nous montrons']):
            bonus += 0.3
        if any(marker in texte_lower for marker in ['likely', 'probable', 'seems', 'appears']):
            bonus += 0.2
        if any(marker in texte_lower for marker in ['hypothesis', 'conjecture', 'suppose']):
            bonus += 0.15
        
        score = min(1.0, densite + bonus)
        return score
    
    def _calculer_score_aspect(self, expressions: List[str], texte: str) -> float:
        """Score aspect temporel processus scientifiques"""
        if not texte:
            return 0.0
        
        nb_mots = len(texte.split())
        densite = len(expressions) / max(1, nb_mots / 100)
        
        # Bonus processus scientifiques
        bonus = 0.0
        texte_lower = texte.lower()
        
        if any(marker in texte_lower for marker in ['begin', 'start', 'commence', 'initiate']):
            bonus += 0.2
        if any(marker in texte_lower for marker in ['continue', 'proceed', 'ongoing']):
            bonus += 0.15
        if any(marker in texte_lower for marker in ['complete', 'finish', 'conclude']):
            bonus += 0.2
        
        score = min(1.0, densite + bonus)
        return score
    
    def _calculer_score_quantification(self, expressions: List[str], texte: str) -> float:
        """Score quantification scientifique"""
        if not texte:
            return 0.0
        
        nb_mots = len(texte.split())
        densite = len(expressions) / max(1, nb_mots / 100)
        
        # Bonus quantifications numériques
        bonus = 0.0
        
        # Détection chiffres et mesures
        nb_chiffres = len(re.findall(r'\d+', texte))
        if nb_chiffres > 0:
            bonus += min(0.3, nb_chiffres / 10)
        
        # Comparatifs quantitatifs
        if any(marker in texte.lower() for marker in ['more', 'less', 'most', 'significantly']):
            bonus += 0.2
        
        score = min(1.0, densite + bonus)
        return score
    
    def optimiser_corpus_scientifique(self, chemin_corpus: str, limite_docs: int = 100) -> Dict:
        """Optimiser corpus scientifique avec analyse spécialisée"""
        print(f"\n🔬 Optimisation corpus scientifique: {chemin_corpus}")
        
        chemin_complet = self.workspace / chemin_corpus
        if not chemin_complet.exists():
            return {"erreur": "Fichier non trouvé"}
        
        # Chargement
        with open(chemin_complet, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Normalisation
        if isinstance(data, list):
            documents = data[:limite_docs]
        elif isinstance(data, dict) and 'documents' in data:
            documents = data['documents'][:limite_docs]
        else:
            documents = [data]
        
        print(f"📊 Documents scientifiques: {len(documents)}")
        
        # Analyse spécialisée
        analyses = []
        stats_langues = {}
        stats_dhatu = {"modal": 0.0, "aspect": 0.0, "quant": 0.0}
        
        for i, doc in enumerate(documents):
            if i % 20 == 0:
                print(f"   Analyse scientifique: {i}/{len(documents)}")
            
            analyse = self.analyser_document_scientifique(doc)
            analyses.append(analyse)
            
            # Stats par langue
            langue = analyse.langue
            if langue not in stats_langues:
                stats_langues[langue] = {"count": 0, "modal": 0.0, "aspect": 0.0, "quant": 0.0}
            
            stats_langues[langue]["count"] += 1
            stats_langues[langue]["modal"] += analyse.score_modalite_epistemique
            stats_langues[langue]["aspect"] += analyse.score_aspect_temporel
            stats_langues[langue]["quant"] += analyse.score_quantification
            
            # Stats globales
            stats_dhatu["modal"] += analyse.score_modalite_epistemique
            stats_dhatu["aspect"] += analyse.score_aspect_temporel
            stats_dhatu["quant"] += analyse.score_quantification
        
        # Moyennes
        nb_docs = len(analyses)
        if nb_docs > 0:
            for dhatu in stats_dhatu:
                stats_dhatu[dhatu] /= nb_docs
            
            for langue_stats in stats_langues.values():
                if langue_stats["count"] > 0:
                    langue_stats["modal"] /= langue_stats["count"]
                    langue_stats["aspect"] /= langue_stats["count"]
                    langue_stats["quant"] /= langue_stats["count"]
        
        # Top documents par dhātu
        top_modal = sorted(analyses, key=lambda x: x.score_modalite_epistemique, reverse=True)[:5]
        top_aspect = sorted(analyses, key=lambda x: x.score_aspect_temporel, reverse=True)[:5]
        top_quant = sorted(analyses, key=lambda x: x.score_quantification, reverse=True)[:5]
        
        return {
            "corpus": chemin_corpus,
            "documents_analyses": nb_docs,
            "stats_dhatu_global": stats_dhatu,
            "stats_par_langue": stats_langues,
            "top_modalite_epistemique": [asdict(doc) for doc in top_modal],
            "top_aspect_temporel": [asdict(doc) for doc in top_aspect],
            "top_quantification": [asdict(doc) for doc in top_quant],
            "sample_analyses": [asdict(analyse) for analyse in analyses[:10]]
        }

def main():
    """Optimisation corpus scientifiques avec patterns spécialisés"""
    print("🔬 OPTIMISATION CORPUS SCIENTIFIQUES V2")
    print("Patterns spécialisés modalité épistémique scientifique")
    print("="*55)
    
    optimisateur = OptimisateurCorpusScientifique()
    
    # Corpus scientifiques prioritaires
    corpus_scientifiques = [
        "corpus_unifie/panini_corpus_unifie.json",
        "corpus_multilingue_dev/dhatu_connections.json"
    ]
    
    resultats_globaux = {}
    stats_finales = {"modal": 0.0, "aspect": 0.0, "quant": 0.0}
    total_docs = 0
    
    for corpus_path in corpus_scientifiques:
        resultats = optimisateur.optimiser_corpus_scientifique(corpus_path, limite_docs=100)
        
        if "erreur" not in resultats:
            resultats_globaux[corpus_path] = resultats
            
            # Accumulation stats pondérées
            nb_docs = resultats["documents_analyses"]
            total_docs += nb_docs
            
            for dhatu in stats_finales:
                stats_finales[dhatu] += resultats["stats_dhatu_global"][dhatu] * nb_docs
    
    # Moyennes finales
    if total_docs > 0:
        for dhatu in stats_finales:
            stats_finales[dhatu] /= total_docs
    
    print(f"\n📊 RÉSULTATS OPTIMISATION SCIENTIFIQUE:")
    print("="*40)
    print(f"✅ Documents analysés: {total_docs}")
    print(f"✅ Corpus traités: {len(resultats_globaux)}")
    
    print(f"\n📈 COVERAGE DHĀTU SCIENTIFIQUE:")
    print("="*32)
    print(f"🔬 Modalité épistémique: {stats_finales['modal']:.3f}")
    print(f"⏱️ Aspect temporel: {stats_finales['aspect']:.3f}")
    print(f"📊 Quantification: {stats_finales['quant']:.3f}")
    
    coverage_moyen = sum(stats_finales.values()) / 3
    objectif_scientifique = 0.20  # Objectif adapté corpus scientifique
    
    print(f"\n🎯 VALIDATION CORPUS SCIENTIFIQUE:")
    print("="*33)
    print(f"📊 Coverage moyen: {coverage_moyen:.3f}")
    print(f"🎯 Objectif adapté: {objectif_scientifique}")
    print(f"🎯 Status: {'✅ ATTEINT' if coverage_moyen >= objectif_scientifique else '⚠️ À améliorer'}")
    
    # Sauvegarde
    rapport_final = {
        "optimisation_corpus_scientifique_v2": {
            "timestamp": "2025-09-22",
            "stats_globales": stats_finales,
            "total_documents": total_docs,
            "objectif_coverage": objectif_scientifique,
            "resultats_par_corpus": resultats_globaux
        }
    }
    
    fichier_rapport = "optimisation_corpus_scientifique_v2.json"
    with open(fichier_rapport, "w", encoding="utf-8") as f:
        json.dump(rapport_final, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Rapport scientifique: {fichier_rapport}")
    
    if coverage_moyen >= objectif_scientifique:
        print(f"\n🚀 CORPUS SCIENTIFIQUES OPTIMISÉS POUR DHĀTU!")
        print("Modalité épistémique bien détectée en contexte scientifique")
    
    return optimisateur, stats_finales

if __name__ == "__main__":
    optimisateur, stats = main()