#!/usr/bin/env python3
"""
🌐 EXTENSION CROSS-LINGUISTIQUE POLYSÉMIE DHĀTU
Adaptations allemand/chinois avec patterns linguistiques spécifiques
Support multi-langues pour résolution polysémie contextuelle
"""

import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import Counter

# Import algorithme base
try:
    from resolution_polysemie_contextuelle import ResolveurPolysemieContextuelle, CandidatDecomposition, AnalysePolysemie
    from integration_complete_dhatu_trio import SystemeDhatuUnifie
except ImportError as e:
    print(f"⚠️ Erreur import: {e}")
    print("Modules base requis")
    exit(1)


@dataclass
class AdaptationLinguistique:
    """Configuration adaptation linguistique spécifique"""
    langue: str
    code_iso: str
    patterns_modaux: Dict[str, List[str]]
    patterns_aspectuels: Dict[str, List[str]] 
    patterns_quantitatifs: Dict[str, List[str]]
    structures_syntaxiques: List[str]
    ordre_mots: str  # SOV, SVO, VSO, etc.
    specificites_culturelles: List[str]


@dataclass
class ResultatCrossLinguistique:
    """Résultat analyse cross-linguistique"""
    expression_originale: str
    langue: str
    traductions_equivalentes: Dict[str, str]  # langue -> traduction
    analyses_par_langue: Dict[str, AnalysePolysemie]
    coherence_cross_linguistique: float
    divergences_culturelles: List[str]
    recommandations_adaptation: List[str]


class ExtensionCrossLinguistique:
    """Extension multilingue pour résolution polysémie dhātu"""
    
    def __init__(self):
        self.resolveur_base = ResolveurPolysemieContextuelle()
        
        # Adaptations linguistiques
        self.adaptations = {
            "fr": self._creer_adaptation_francais(),
            "de": self._creer_adaptation_allemand(), 
            "zh": self._creer_adaptation_chinois(),
            "en": self._creer_adaptation_anglais()
        }
        
        # Dictionnaires traduction concepts dhātu
        self.lexiques_dhatu = {
            "MODAL": {
                "fr": ["modal", "possible", "probable", "certain", "nécessaire"],
                "de": ["modal", "möglich", "wahrscheinlich", "sicher", "notwendig"],
                "zh": ["可能", "大概", "肯定", "必须", "应该"],
                "en": ["modal", "possible", "probable", "certain", "necessary"]
            },
            "ASPECT": {
                "fr": ["aspect", "commencer", "continuer", "finir", "progresser"],
                "de": ["aspekt", "anfangen", "fortsetzen", "beenden", "fortschreiten"],
                "zh": ["开始", "继续", "完成", "进行", "结束"],
                "en": ["aspect", "begin", "continue", "finish", "progress"]
            },
            "QUANT": {
                "fr": ["quantité", "beaucoup", "peu", "plusieurs", "nombreux"],
                "de": ["quantität", "viel", "wenig", "mehrere", "zahlreich"],
                "zh": ["数量", "很多", "很少", "几个", "许多"],
                "en": ["quantity", "much", "little", "several", "numerous"]
            }
        }
        
        # Patterns polysémie cross-linguistiques
        self.patterns_universels = {
            "modal_quant": {
                "fr": ["probablement beaucoup", "certainement nombreux", "peut-être plusieurs"],
                "de": ["wahrscheinlich viel", "sicher zahlreich", "vielleicht mehrere"],
                "zh": ["大概很多", "肯定许多", "可能几个"],
                "en": ["probably much", "certainly numerous", "maybe several"]
            },
            "aspect_modal": {
                "fr": ["commence peut-être", "va certainement", "pourrait continuer"],
                "de": ["fängt vielleicht an", "wird sicher", "könnte fortsetzen"],
                "zh": ["可能开始", "肯定会", "可能继续"],
                "en": ["maybe begins", "will certainly", "might continue"]
            },
            "aspect_quant": {
                "fr": ["de plus en plus", "plusieurs fois", "beaucoup progresser"],
                "de": ["immer mehr", "mehrmals", "viel fortschreiten"],
                "zh": ["越来越多", "多次", "很多进步"],
                "en": ["more and more", "several times", "much progress"]
            }
        }
        
        # Métriques validation
        self.metriques_cross = {
            "coherence_totale": 0.0,
            "divergences_par_langue": {},
            "patterns_universels_valides": 0,
            "adaptations_reussies": 0
        }
    
    def _creer_adaptation_francais(self) -> AdaptationLinguistique:
        """Adaptation base français (référence)"""
        return AdaptationLinguistique(
            langue="Français",
            code_iso="fr",
            patterns_modaux={
                "epistemique": ["semble", "paraît", "suggère", "indique", "montre"],
                "deontique": ["doit", "faut", "nécessaire", "requis", "obligatoire"],
                "dynamique": ["peut", "capable", "parvient", "réussit", "arrive"]
            },
            patterns_aspectuels={
                "inceptif": ["commence", "débute", "entame", "initie", "démarre"],
                "progressif": ["continue", "poursuit", "progresse", "avance", "développe"],
                "conclusif": ["termine", "finit", "achève", "conclut", "finalise"]
            },
            patterns_quantitatifs={
                "cardinale": ["un", "deux", "trois", "dix", "cent", "exactement"],
                "approximative": ["environ", "vers", "près de", "autour de", "approximativement"],
                "comparative": ["plus", "moins", "autant", "davantage", "supérieur"]
            },
            structures_syntaxiques=["SVO", "complément_postposé"],
            ordre_mots="SVO",
            specificites_culturelles=["politesse_conditionnelle", "nuances_subtiles"]
        )
    
    def _creer_adaptation_allemand(self) -> AdaptationLinguistique:
        """Adaptation spécifique allemand"""
        return AdaptationLinguistique(
            langue="Deutsch",
            code_iso="de",
            patterns_modaux={
                "epistemique": ["scheint", "erscheint", "deutet", "zeigt", "weist"],
                "deontique": ["muss", "soll", "notwendig", "erforderlich", "verpflichtend"],
                "dynamique": ["kann", "vermag", "imstande", "fähig", "schafft"]
            },
            patterns_aspectuels={
                "inceptif": ["beginnt", "fängt an", "startet", "initiiert", "eröffnet"],
                "progressif": ["setzt fort", "macht weiter", "entwickelt", "schreitet fort"],
                "conclusif": ["beendet", "schließt ab", "vollendet", "finalisiert", "komplettiert"]
            },
            patterns_quantitatifs={
                "cardinale": ["eins", "zwei", "drei", "zehn", "hundert", "genau"],
                "approximative": ["etwa", "ungefähr", "rund", "circa", "annähernd"],
                "comparative": ["mehr", "weniger", "gleich", "größer", "kleiner"]
            },
            structures_syntaxiques=["SOV_subordonnée", "V2_principale", "séparable_verbes"],
            ordre_mots="V2/SOV",
            specificites_culturelles=["précision_technique", "composés_complexes", "modalité_forte"]
        )
    
    def _creer_adaptation_chinois(self) -> AdaptationLinguistique:
        """Adaptation spécifique chinois"""
        return AdaptationLinguistique(
            langue="中文",
            code_iso="zh",
            patterns_modaux={
                "epistemique": ["似乎", "好像", "可能", "大概", "也许"],
                "deontique": ["必须", "应该", "需要", "得", "要"],
                "dynamique": ["能", "会", "可以", "能够", "敢"]
            },
            patterns_aspectuels={
                "inceptif": ["开始", "起", "始", "初", "启"],
                "progressif": ["正在", "继续", "进行", "发展", "推进"],
                "conclusif": ["完成", "结束", "终", "毕", "了"]
            },
            patterns_quantitatifs={
                "cardinale": ["一", "二", "三", "十", "百", "确切"],
                "approximative": ["大约", "左右", "差不多", "约", "几乎"],
                "comparative": ["更", "较", "比", "超", "不如"]
            },
            structures_syntaxiques=["SVO", "classificateurs", "particules_aspectuelles"],
            ordre_mots="SVO",
            specificites_culturelles=["contexte_implicit", "harmonie_sociale", "hiérarchie_respect"]
        )
    
    def _creer_adaptation_anglais(self) -> AdaptationLinguistique:
        """Adaptation spécifique anglais"""
        return AdaptationLinguistique(
            langue="English",
            code_iso="en",
            patterns_modaux={
                "epistemique": ["seems", "appears", "suggests", "indicates", "shows"],
                "deontique": ["must", "should", "necessary", "required", "mandatory"],
                "dynamique": ["can", "able", "capable", "manages", "succeeds"]
            },
            patterns_aspectuels={
                "inceptif": ["begins", "starts", "initiates", "commences", "launches"],
                "progressif": ["continues", "progresses", "develops", "advances", "proceeds"],
                "conclusif": ["finishes", "completes", "concludes", "finalizes", "accomplishes"]
            },
            patterns_quantitatifs={
                "cardinale": ["one", "two", "three", "ten", "hundred", "exactly"],
                "approximative": ["about", "around", "roughly", "approximately", "nearly"],
                "comparative": ["more", "less", "as much", "greater", "fewer"]
            },
            structures_syntaxiques=["SVO", "auxiliaires_modaux", "progressif_continu"],
            ordre_mots="SVO",
            specificites_culturelles=["directness", "efficiency", "pragmatic_focus"]
        )
    
    def adapter_contextes_discriminants(self, langue: str) -> Dict[str, List[str]]:
        """Adapter contextes discriminants pour langue spécifique"""
        
        if langue not in self.adaptations:
            return self.resolveur_base.contextes_discriminants  # Fallback français
        
        adaptation = self.adaptations[langue]
        contextes_adaptes = {}
        
        # Modal
        contextes_adaptes["modal_epistemique"] = adaptation.patterns_modaux["epistemique"]
        contextes_adaptes["modal_deontique"] = adaptation.patterns_modaux["deontique"] 
        contextes_adaptes["modal_dynamique"] = adaptation.patterns_modaux["dynamique"]
        
        # Aspect
        contextes_adaptes["aspect_inceptif"] = adaptation.patterns_aspectuels["inceptif"]
        contextes_adaptes["aspect_progressif"] = adaptation.patterns_aspectuels["progressif"]
        contextes_adaptes["aspect_conclusif"] = adaptation.patterns_aspectuels["conclusif"]
        
        # Quant
        contextes_adaptes["quant_cardinale"] = adaptation.patterns_quantitatifs["cardinale"]
        contextes_adaptes["quant_approximative"] = adaptation.patterns_quantitatifs["approximative"]
        contextes_adaptes["quant_comparative"] = adaptation.patterns_quantitatifs["comparative"]
        
        return contextes_adaptes
    
    def detecter_langue_expression(self, expression: str, contexte: str = "") -> str:
        """Détection automatique langue d'une expression"""
        
        texte_complet = f"{expression} {contexte}".lower()
        scores_langues = {}
        
        # Scoring par langue
        for code_langue, adaptation in self.adaptations.items():
            score = 0.0
            
            # Patterns modaux
            for pattern_list in adaptation.patterns_modaux.values():
                for pattern in pattern_list:
                    if pattern.lower() in texte_complet:
                        score += 2.0
            
            # Patterns aspectuels
            for pattern_list in adaptation.patterns_aspectuels.values():
                for pattern in pattern_list:
                    if pattern.lower() in texte_complet:
                        score += 2.0
            
            # Patterns quantitatifs
            for pattern_list in adaptation.patterns_quantitatifs.values():
                for pattern in pattern_list:
                    if pattern.lower() in texte_complet:
                        score += 2.0
            
            # Lexique dhātu
            for dhatu_type, lexique_dhatu in self.lexiques_dhatu.items():
                if code_langue in lexique_dhatu:
                    for terme in lexique_dhatu[code_langue]:
                        if terme.lower() in texte_complet:
                            score += 1.0
            
            scores_langues[code_langue] = score
        
        # Langue avec score maximal
        if scores_langues and max(scores_langues.values()) > 0:
            return max(scores_langues, key=scores_langues.get)
        
        return "fr"  # Défaut français
    
    def resoudre_polysemie_multilingue(self, expression: str, contexte: str = "", 
                                     langue_forcee: Optional[str] = None) -> ResultatCrossLinguistique:
        """Résolution polysémie avec support multilingue"""
        
        # Détection langue
        langue_detectee = langue_forcee or self.detecter_langue_expression(expression, contexte)
        
        # Adaptation contextes
        contextes_adaptes = self.adapter_contextes_discriminants(langue_detectee)
        
        # Résolveur adapté
        resolveur_adapte = ResolveurPolysemieContextuelle()
        resolveur_adapte.contextes_discriminants = contextes_adaptes
        
        # Analyse principale
        analyse_principale = resolveur_adapte.resoudre_polysemie(expression, contexte)
        
        # Traductions dans autres langues
        traductions = self._generer_traductions_equivalentes(expression, langue_detectee)
        
        # Analyses cross-linguistiques
        analyses_par_langue = {langue_detectee: analyse_principale}
        
        for code_langue, traduction in traductions.items():
            if code_langue != langue_detectee:
                contextes_trad = self.adapter_contextes_discriminants(code_langue)
                resolveur_trad = ResolveurPolysemieContextuelle()
                resolveur_trad.contextes_discriminants = contextes_trad
                
                analyse_trad = resolveur_trad.resoudre_polysemie(traduction, contexte)
                analyses_par_langue[code_langue] = analyse_trad
        
        # Calcul cohérence cross-linguistique
        coherence = self._calculer_coherence_cross_linguistique(analyses_par_langue)
        
        # Détection divergences
        divergences = self._detecter_divergences_culturelles(analyses_par_langue, langue_detectee)
        
        # Recommandations
        recommandations = self._generer_recommandations_adaptation(analyses_par_langue, langue_detectee)
        
        return ResultatCrossLinguistique(
            expression_originale=expression,
            langue=langue_detectee,
            traductions_equivalentes=traductions,
            analyses_par_langue=analyses_par_langue,
            coherence_cross_linguistique=coherence,
            divergences_culturelles=divergences,
            recommandations_adaptation=recommandations
        )
    
    def _generer_traductions_equivalentes(self, expression: str, langue_source: str) -> Dict[str, str]:
        """Générer traductions équivalentes dans autres langues"""
        
        traductions = {langue_source: expression}
        
        # Recherche dans patterns universels
        for pattern_type, patterns_par_langue in self.patterns_universels.items():
            if langue_source in patterns_par_langue:
                for expr_pattern in patterns_par_langue[langue_source]:
                    if self._expressions_similaires(expression, expr_pattern):
                        # Traduction dans autres langues
                        for code_langue, patterns_cible in patterns_par_langue.items():
                            if code_langue != langue_source:
                                # Prendre première traduction correspondante
                                idx = patterns_par_langue[langue_source].index(expr_pattern)
                                if idx < len(patterns_cible):
                                    traductions[code_langue] = patterns_cible[idx]
                        break
        
        # Traductions par substitution lexique dhātu
        if len(traductions) == 1:  # Pas trouvé dans patterns
            traductions.update(self._traduire_par_substitution_dhatu(expression, langue_source))
        
        return traductions
    
    def _expressions_similaires(self, expr1: str, expr2: str, seuil: float = 0.6) -> bool:
        """Vérifier similarité entre expressions"""
        mots1 = set(expr1.lower().split())
        mots2 = set(expr2.lower().split())
        
        if not mots1 or not mots2:
            return False
        
        intersection = mots1.intersection(mots2)
        union = mots1.union(mots2)
        
        similarite = len(intersection) / len(union)
        return similarite >= seuil
    
    def _traduire_par_substitution_dhatu(self, expression: str, langue_source: str) -> Dict[str, str]:
        """Traduction par substitution lexique dhātu"""
        
        traductions = {}
        mots_expression = expression.lower().split()
        
        for code_langue in self.adaptations:
            if code_langue == langue_source:
                continue
            
            mots_traduits = []
            for mot in mots_expression:
                mot_traduit = mot  # Défaut: garder original
                
                # Recherche dans lexiques dhātu
                for dhatu_type, lexique in self.lexiques_dhatu.items():
                    if langue_source in lexique and code_langue in lexique:
                        if mot in lexique[langue_source]:
                            idx = lexique[langue_source].index(mot)
                            if idx < len(lexique[code_langue]):
                                mot_traduit = lexique[code_langue][idx]
                                break
                
                mots_traduits.append(mot_traduit)
            
            traductions[code_langue] = " ".join(mots_traduits)
        
        return traductions
    
    def _calculer_coherence_cross_linguistique(self, analyses: Dict[str, AnalysePolysemie]) -> float:
        """Calculer cohérence entre analyses multilingues"""
        
        if len(analyses) < 2:
            return 1.0
        
        scores_coherence = []
        analyses_liste = list(analyses.values())
        
        # Comparaison paires d'analyses
        for i in range(len(analyses_liste)):
            for j in range(i + 1, len(analyses_liste)):
                analyse1 = analyses_liste[i]
                analyse2 = analyses_liste[j]
                
                # Cohérence dhātu impliqués
                if (analyse1.candidat_optimal and analyse2.candidat_optimal):
                    dhatu1 = set(analyse1.candidat_optimal.dhatu_impliques)
                    dhatu2 = set(analyse2.candidat_optimal.dhatu_impliques)
                    
                    if dhatu1 and dhatu2:
                        coherence_dhatu = len(dhatu1.intersection(dhatu2)) / len(dhatu1.union(dhatu2))
                        scores_coherence.append(coherence_dhatu)
                
                # Cohérence types polysémie
                if analyse1.type_polysemie == analyse2.type_polysemie:
                    scores_coherence.append(0.5)  # Bonus type identique
        
        return sum(scores_coherence) / len(scores_coherence) if scores_coherence else 0.0
    
    def _detecter_divergences_culturelles(self, analyses: Dict[str, AnalysePolysemie], langue_ref: str) -> List[str]:
        """Détecter divergences culturelles entre langues"""
        
        divergences = []
        
        if langue_ref not in analyses:
            return divergences
        
        analyse_ref = analyses[langue_ref]
        
        for code_langue, analyse in analyses.items():
            if code_langue == langue_ref:
                continue
            
            adaptation = self.adaptations.get(code_langue)
            if not adaptation:
                continue
            
            # Divergence confiance
            if analyse_ref.candidat_optimal and analyse.candidat_optimal:
                diff_confiance = abs(analyse_ref.confiance_resolution - analyse.confiance_resolution)
                if diff_confiance > 0.3:
                    divergences.append(f"Confiance divergente {langue_ref}↔{code_langue}: {diff_confiance:.2f}")
            
            # Divergence dhātu
            if (analyse_ref.candidat_optimal and analyse.candidat_optimal):
                dhatu_ref = set(analyse_ref.candidat_optimal.dhatu_impliques)
                dhatu_cible = set(analyse.candidat_optimal.dhatu_impliques)
                
                if dhatu_ref != dhatu_cible:
                    divergences.append(f"Dhātu divergents {langue_ref}↔{code_langue}: {dhatu_ref} vs {dhatu_cible}")
            
            # Divergences spécificités culturelles
            for spec in adaptation.specificites_culturelles:
                if "précision" in spec and analyse.confiance_resolution > analyse_ref.confiance_resolution:
                    divergences.append(f"Précision culturelle {code_langue}: +{analyse.confiance_resolution - analyse_ref.confiance_resolution:.2f}")
        
        return divergences
    
    def _generer_recommandations_adaptation(self, analyses: Dict[str, AnalysePolysemie], langue_ref: str) -> List[str]:
        """Générer recommandations adaptation cross-linguistique"""
        
        recommandations = []
        
        # Cohérence globale
        coherence = self._calculer_coherence_cross_linguistique(analyses)
        
        if coherence < 0.5:
            recommandations.append("Améliorer cohérence cross-linguistique (patterns universels)")
        
        if coherence > 0.8:
            recommandations.append("Excellente cohérence - système transférable")
        
        # Recommendations par langue
        for code_langue, analyse in analyses.items():
            if code_langue == langue_ref:
                continue
            
            adaptation = self.adaptations.get(code_langue)
            if not adaptation:
                continue
            
            # Confiance faible
            if analyse.confiance_resolution < 0.3:
                recommandations.append(f"Enrichir contextes discriminants {adaptation.langue}")
            
            # Polysémie non résolue
            if analyse.type_polysemie == "ambigue":
                recommandations.append(f"Ajouter patterns spécifiques {adaptation.langue}")
            
            # Adaptation syntaxique
            if adaptation.ordre_mots != "SVO":
                recommandations.append(f"Adapter ordre mots {adaptation.langue}: {adaptation.ordre_mots}")
        
        return recommandations
    
    def tester_extension_multilingue(self, expressions_test: List[Tuple[str, str, str]]) -> Dict:
        """Test extension multilingue sur corpus d'expressions"""
        
        resultats = []
        stats_globales = {
            "total_expressions": len(expressions_test),
            "langues_detectees": Counter(),
            "coherence_moyenne": 0.0,
            "divergences_totales": 0,
            "adaptations_reussies": 0
        }
        
        print(f"🌐 Test extension cross-linguistique: {len(expressions_test)} expressions")
        
        for i, (expression, contexte, langue_attendue) in enumerate(expressions_test):
            if i % 10 == 0:
                print(f"   Progression: {i}/{len(expressions_test)}")
            
            resultat = self.resoudre_polysemie_multilingue(expression, contexte)
            resultats.append(asdict(resultat))
            
            # Stats
            stats_globales["langues_detectees"][resultat.langue] += 1
            stats_globales["coherence_moyenne"] += resultat.coherence_cross_linguistique
            stats_globales["divergences_totales"] += len(resultat.divergences_culturelles)
            
            if resultat.coherence_cross_linguistique > 0.6:
                stats_globales["adaptations_reussies"] += 1
        
        # Moyennes
        if stats_globales["total_expressions"] > 0:
            stats_globales["coherence_moyenne"] /= stats_globales["total_expressions"]
        
        stats_globales["taux_adaptation"] = (stats_globales["adaptations_reussies"] / 
                                           stats_globales["total_expressions"]) * 100
        
        return {
            "statistiques_globales": stats_globales,
            "resultats_detailles": resultats[:20],  # Sample
            "metriques_cross": self.metriques_cross
        }


def main():
    """Test extension cross-linguistique polysémie dhātu"""
    print("🌐 EXTENSION CROSS-LINGUISTIQUE POLYSÉMIE DHĀTU")
    print("Adaptations allemand/chinois + patterns universels")
    print("="*60)
    
    # Initialisation extension
    extension = ExtensionCrossLinguistique()
    
    # Expressions test multilingues
    expressions_test = [
        # Français
        ("probablement beaucoup", "Dans cette recherche scientifique", "fr"),
        ("commence peut-être", "Le processus d'analyse", "fr"),
        ("certainement nombreux", "Les participants sont", "fr"),
        
        # Allemand
        ("wahrscheinlich viel", "In dieser wissenschaftlichen Forschung", "de"),
        ("fängt vielleicht an", "Der Analyseprozess", "de"),
        ("sicher zahlreich", "Die Teilnehmer sind", "de"),
        
        # Chinois
        ("大概很多", "在这个科学研究中", "zh"),
        ("可能开始", "分析过程", "zh"),
        ("肯定许多", "参与者", "zh"),
        
        # Anglais
        ("probably much", "In this scientific research", "en"),
        ("maybe begins", "The analysis process", "en"),
        ("certainly numerous", "The participants are", "en"),
        
        # Expressions mixtes/ambiguës
        ("很可能 beaucoup", "Contexte mixte", "zh"),
        ("peut-être 多", "Mixed context", "fr")
    ]
    
    print(f"📊 Test sur {len(expressions_test)} expressions multilingues")
    
    # Test extension massive
    resultats = extension.tester_extension_multilingue(expressions_test)
    
    # Affichage résultats
    stats = resultats["statistiques_globales"]
    print(f"\n📈 RÉSULTATS EXTENSION CROSS-LINGUISTIQUE:")
    print("="*43)
    print(f"✅ Expressions testées: {stats['total_expressions']}")
    print(f"✅ Adaptations réussies: {stats['adaptations_reussies']} ({stats['taux_adaptation']:.1f}%)")
    print(f"✅ Cohérence moyenne: {stats['coherence_moyenne']:.3f}")
    print(f"✅ Divergences totales: {stats['divergences_totales']}")
    
    print(f"\n🌍 LANGUES DÉTECTÉES:")
    print("="*18)
    for langue, count in stats["langues_detectees"].items():
        pourcentage = (count / stats['total_expressions']) * 100
        langue_nom = extension.adaptations[langue].langue if langue in extension.adaptations else langue
        print(f"   {langue_nom} ({langue}): {count} ({pourcentage:.1f}%)")
    
    # Exemples réussites cross-linguistiques
    print(f"\n🎯 EXEMPLES COHÉRENCE CROSS-LINGUISTIQUE:")
    print("="*39)
    exemples_coherents = [r for r in resultats["resultats_detailles"] 
                         if r['coherence_cross_linguistique'] > 0.7][:3]
    
    for exemple in exemples_coherents:
        expr = exemple['expression_originale']
        langue = exemple['langue']
        coherence = exemple['coherence_cross_linguistique']
        traductions = exemple['traductions_equivalentes']
        
        print(f"✅ '{expr}' ({langue}) - Cohérence: {coherence:.2f}")
        for lang_code, trad in traductions.items():
            if lang_code != langue:
                lang_nom = extension.adaptations[lang_code].langue if lang_code in extension.adaptations else lang_code
                print(f"   → {lang_nom}: '{trad}'")
    
    # Sauvegarde
    fichier_resultats = "extension_cross_linguistique_resultats.json"
    with open(fichier_resultats, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Résultats sauvegardés: {fichier_resultats}")
    
    # Validation objectifs
    taux_adaptation = stats['taux_adaptation']
    coherence_moyenne = stats['coherence_moyenne']
    objectif_adaptation = 60.0  # 60% adaptations réussies
    objectif_coherence = 0.5   # 50% cohérence cross-linguistique
    
    print(f"\n🎊 VALIDATION EXTENSION CROSS-LINGUISTIQUE:")
    print("="*42)
    print(f"🎯 Taux adaptation: {taux_adaptation:.1f}%")
    print(f"🎯 Objectif adaptation: {objectif_adaptation}%")
    print(f"🎯 Cohérence moyenne: {coherence_moyenne:.3f}")
    print(f"🎯 Objectif cohérence: {objectif_coherence}")
    
    success_adaptation = taux_adaptation >= objectif_adaptation
    success_coherence = coherence_moyenne >= objectif_coherence
    
    print(f"🎯 Status adaptation: {'✅ OBJECTIF ATTEINT' if success_adaptation else '⚠️ À améliorer'}")
    print(f"🎯 Status cohérence: {'✅ OBJECTIF ATTEINT' if success_coherence else '⚠️ À améliorer'}")
    
    if success_adaptation and success_coherence:
        print(f"\n🚀 EXTENSION CROSS-LINGUISTIQUE OPÉRATIONNELLE!")
        print("Support multilingue prêt pour production")
    else:
        print(f"\n⚠️ Optimisations recommandées:")
        if not success_adaptation:
            print("- Enrichir patterns linguistiques spécifiques")
            print("- Améliorer détection automatique langue")
        if not success_coherence:
            print("- Développer patterns universels")
            print("- Calibrer weights cross-linguistiques")
    
    return extension, resultats

if __name__ == "__main__":
    extension, resultats = main()