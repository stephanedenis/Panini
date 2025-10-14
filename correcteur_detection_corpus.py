#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 CORRECTEUR DETECTION CORPUS - HILL CLIMBING PANLANG
=====================================================
Répare la détection des corpus disponibles pour l'optimisation continue

PROBLÈME IDENTIFIÉ:
- 32+ corpus JSON disponibles dans le workspace  
- Système détecte 0 nouveaux corpus
- Patterns de recherche défaillants

SOLUTION:
- Révision complète de la détection
- Expansion des patterns de recherche
- Logique de filtrage améliorée
- Test immédiat et intégration

Auteur: Diagnostic & Réparation Système PanLang
Date: 2025-09-27
"""

import json
import logging
from pathlib import Path
from typing import List, Set
import glob

class CorrecteurDetectionCorpus:
    """Correcteur pour la détection de corpus disponibles"""
    
    def __init__(self):
        self.workspace_root = Path.cwd()
        self.corpus_integres = set()  # Pour simulation
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Configuration logging pour diagnostic"""
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)
    
    def detecter_tous_corpus_disponibles(self) -> List[str]:
        """Détection exhaustive de TOUS les corpus disponibles"""
        
        self.logger.info("🔍 DIAGNOSTIC COMPLET - Détection corpus")
        
        # 1. PATTERNS EXHAUSTIFS - Plus large que l'original
        patterns_exhaustifs = [
            # Patterns originaux (possiblement défaillants)
            "corpus_*.json",
            "data/*corpus*.json", 
            "**/*corpus*.json",
            
            # Patterns supplémentaires basés sur file_search
            "**/corpus.json",                    # Fichiers nommés simplement "corpus.json"
            "**/corpus_*.json",                  # Variantes avec préfixes
            "**/*_corpus_*.json",               # Variantes avec corpus au milieu
            "**/integration_corpus_*.json",     # Corpus d'intégration spécifiques
            "**/scientific_corpus_*.json",      # Corpus scientifiques
            "**/toy_corpus.json",               # Corpus de test
            
            # Données brutes détectées
            "data/*.json",                      # Tous JSON dans data/
            "**/data/*.json",                   # Tous JSON dans sous-dossiers data/
            "PaniniFS-Research/**/*.json",      # Sous-répertoire PaniniFS-Research
            "tech/**/*.json",                   # Répertoire technique
            
            # Formats alternatifs
            "*.txt",                            # Fichiers texte
            "data/*.txt",                       # Textes dans data/
            "**/*.md",                          # Markdown avec potentiel contenu
            
            # Patterns spécialisés découverts
            "**/*multilingue*.json",
            "**/*scientifique*.json", 
            "**/*prescolaire*.json",
            "**/*unifie*.json",
            "expansion_*/**/*.json"
        ]
        
        tous_corpus = []
        corpus_par_pattern = {}
        
        for pattern in patterns_exhaustifs:
            corpus_pattern = []
            
            try:
                # Utilisation de glob pour recherche récursive
                chemins_trouves = list(self.workspace_root.glob(pattern))
                
                for chemin in chemins_trouves:
                    if self._est_corpus_valide(chemin):
                        chemin_str = str(chemin)
                        if chemin_str not in tous_corpus:
                            tous_corpus.append(chemin_str)
                            corpus_pattern.append(chemin_str)
                
                if corpus_pattern:
                    corpus_par_pattern[pattern] = len(corpus_pattern)
                    
            except Exception as e:
                self.logger.error(f"❌ Erreur pattern {pattern}: {e}")
        
        # 2. RAPPORT DIAGNOSTIC DÉTAILLÉ
        self.logger.info(f"📊 RÉSULTATS DÉTECTION:")
        self.logger.info(f"   🎯 Total corpus trouvés: {len(tous_corpus)}")
        
        for pattern, nb in corpus_par_pattern.items():
            self.logger.info(f"   📁 {pattern}: {nb} corpus")
        
        # 3. AFFICHAGE DES PREMIERS CORPUS TROUVÉS
        self.logger.info(f"🔍 ÉCHANTILLON CORPUS DÉTECTÉS:")
        for i, corpus in enumerate(tous_corpus[:10]):
            self.logger.info(f"   {i+1:2d}. {Path(corpus).name} ({Path(corpus).parent})")
        
        if len(tous_corpus) > 10:
            self.logger.info(f"   ... et {len(tous_corpus) - 10} autres")
        
        return tous_corpus
    
    def _est_corpus_valide(self, chemin: Path) -> bool:
        """Validation améliorée d'un corpus"""
        
        try:
            if not chemin.is_file():
                return False
            
            # Filtrage des fichiers système/temporaires
            nom_fichier = chemin.name.lower()
            if any(exclusion in nom_fichier for exclusion in [
                'node_modules', '.git', '__pycache__', '.pytest_cache',
                'package-lock', '.log', '.tmp', '.cache'
            ]):
                return False
            
            # Validation JSON
            if chemin.suffix == '.json':
                with open(chemin, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Corpus valide = dict avec contenu substantiel
                if isinstance(data, dict) and len(data) >= 3:
                    # Vérification contenu non-vide
                    contenu_total = sum(len(str(v)) for v in data.values() if isinstance(v, (str, dict, list)))
                    return contenu_total > 100  # Minimum 100 caractères de contenu
            
            # Validation TXT/MD
            elif chemin.suffix in ['.txt', '.md']:
                taille = chemin.stat().st_size
                return 500 <= taille <= 10_000_000  # Entre 500 bytes et 10MB
            
            return False
            
        except Exception as e:
            self.logger.debug(f"⚠️ Erreur validation {chemin}: {e}")
            return False
    
    def simuler_detection_originale(self) -> List[str]:
        """Simulation de la détection originale défaillante"""
        
        self.logger.info("🔄 SIMULATION DÉTECTION ORIGINALE")
        
        # Code original approximatif
        sources_potentielles = [
            "corpus_*.json",
            "data/*corpus*.json", 
            "**/*corpus*.json",
            "*.txt",
            "data/*.txt",
            "corpus_*/**/*.json"
        ]
        
        nouveaux_corpus = []
        workspace_root = Path.cwd()
        
        for pattern in sources_potentielles:
            for chemin in workspace_root.glob(pattern):
                if chemin.is_file() and str(chemin) not in self.corpus_integres:
                    try:
                        if chemin.suffix == '.json':
                            with open(chemin, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                if isinstance(data, dict) and len(data) > 5:
                                    nouveaux_corpus.append(str(chemin))
                        elif chemin.suffix == '.txt':
                            if chemin.stat().st_size > 1000:
                                nouveaux_corpus.append(str(chemin))
                    except:
                        continue
        
        self.logger.info(f"📊 Simulation originale: {len(nouveaux_corpus)} corpus")
        return nouveaux_corpus[:5]
    
    def comparer_detections(self):
        """Comparaison entre détection exhaustive et originale"""
        
        print("🆚 COMPARAISON MÉTHODES DÉTECTION")
        print("="*50)
        
        # Détection exhaustive
        corpus_exhaustifs = self.detecter_tous_corpus_disponibles()
        
        # Simulation originale  
        corpus_originaux = self.simuler_detection_originale()
        
        print(f"📊 RÉSULTATS:")
        print(f"   🔍 Détection exhaustive: {len(corpus_exhaustifs)} corpus")
        print(f"   🔄 Simulation originale: {len(corpus_originaux)} corpus")
        print(f"   📈 Différence: +{len(corpus_exhaustifs) - len(corpus_originaux)} corpus")
        
        # Analyse de la différence
        if len(corpus_exhaustifs) > len(corpus_originaux):
            print(f"\n✅ PROBLÈME IDENTIFIÉ: Détection originale TROP RESTRICTIVE")
            print(f"💡 SOLUTION: Utiliser détection exhaustive")
        else:
            print(f"\n❓ Problème non évident - investigation approfondie requise")
        
        return corpus_exhaustifs, corpus_originaux
    
    def generer_correcteur_integration(self, corpus_disponibles: List[str]):
        """Génère le code correcteur pour l'intégration"""
        
        code_correcteur = f'''
def detecter_nouveaux_corpus_CORRIGE(self) -> List[str]:
    """Détection CORRIGÉE des nouveaux corpus disponibles"""
    
    # PATTERNS EXHAUSTIFS (vs originaux restrictifs)
    patterns_exhaustifs = [
        "**/*corpus*.json",     # Récursif tous corpus
        "**/corpus.json",       # Fichiers corpus simples  
        "data/**/*.json",       # Tous JSON dans data/
        "**/*multilingue*.json", # Corpus spécialisés
        "**/*scientifique*.json",
        "**/*prescolaire*.json",
        "**/*unifie*.json",
        "tech/**/*.json",       # Corpus techniques
        "*.txt",                # Fichiers texte racine
        "data/*.txt"            # Textes dans data/
    ]
    
    nouveaux_corpus = []
    workspace_root = Path.cwd()
    
    for pattern in patterns_exhaustifs:
        for chemin in workspace_root.glob(pattern):
            if chemin.is_file() and str(chemin) not in self.corpus_integres:
                if self._valider_corpus_ameliore(chemin):
                    nouveaux_corpus.append(str(chemin))
    
    # Limite raisonnable pour éviter surcharge
    return nouveaux_corpus[:15]  # vs 5 original

def _valider_corpus_ameliore(self, chemin: Path) -> bool:
    """Validation améliorée vs originale trop stricte"""
    
    try:
        # Exclusions système
        if any(excl in str(chemin) for excl in ['node_modules', '.git', '__pycache__']):
            return False
            
        if chemin.suffix == '.json':
            with open(chemin, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Seuil abaissé: 3 vs 5 original
                return isinstance(data, dict) and len(data) >= 3
                
        elif chemin.suffix == '.txt':
            # Seuil abaissé: 500 vs 1000 original  
            return chemin.stat().st_size >= 500
            
        return False
        
    except:
        return False

# 🎯 CORPUS IMMÉDIATEMENT DISPONIBLES:
# {len(corpus_disponibles)} corpus détectés !
# 
# Premiers 10:
{chr(10).join(f"# - {Path(c).name}" for c in corpus_disponibles[:10])}
'''
        
        print("🔧 CODE CORRECTEUR GÉNÉRÉ:")
        print(code_correcteur)
        
        return code_correcteur
    
    def recommandations_integration(self):
        """Recommandations pour corriger le système hill-climbing"""
        
        print(f"\n💡 RECOMMANDATIONS CORRECTION:")
        print(f"="*40)
        print(f"1. 🔄 REMPLACER detecter_nouveaux_corpus() dans optimiseur")
        print(f"2. 📈 UTILISER patterns exhaustifs vs restrictifs") 
        print(f"3. 🎯 ABAISSER seuils validation (3 vs 5, 500 vs 1000)")
        print(f"4. 🚀 REDÉMARRER optimisation avec correction")
        print(f"5. ✅ VÉRIFIER intégration effective des nouveaux corpus")

def main():
    """Test du correcteur de détection"""
    
    correcteur = CorrecteurDetectionCorpus()
    
    print("🔧 DIAGNOSTIC COMPLET - DÉTECTION CORPUS")
    print("="*50)
    
    # Comparaison des méthodes
    corpus_exhaustifs, corpus_originaux = correcteur.comparer_detections()
    
    # Génération du correcteur
    correcteur.generer_correcteur_integration(corpus_exhaustifs)
    
    # Recommandations
    correcteur.recommandations_integration()
    
    print(f"\n🎯 RÉSUMÉ:")
    print(f"   Problem: Système détecte 0 corpus sur {len(corpus_exhaustifs)} disponibles")
    print(f"   Cause: Patterns restrictifs + seuils trop élevés")
    print(f"   Solution: Code correcteur généré ☝️")

if __name__ == "__main__":
    main()