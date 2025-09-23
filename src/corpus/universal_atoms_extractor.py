#!/usr/bin/env python3
"""
Extracteur d'Atomes Universaux - Noyau PaniniFS
Identification des patterns fondamentaux across langues et domaines
"""

import json
import re
import os
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import math


class UniversalAtomsExtractor:
    def __init__(self):
        self.workspace = Path('/home/stephane/GitHub/PaniniFS-Research')
        self.results_dir = self.workspace / 'universal_atoms_results'
        self.results_dir.mkdir(exist_ok=True)
        
        # Structures de données pour atomes
        self.phonetic_atoms = defaultdict(int)
        self.morpheme_atoms = defaultdict(int)
        self.syntactic_atoms = defaultdict(int)
        self.semantic_atoms = defaultdict(int)
        
        # Patterns cross-linguistiques
        self.universal_patterns = {
            'vowel_systems': defaultdict(list),
            'consonant_clusters': defaultdict(list),
            'word_boundaries': defaultdict(list),
            'semantic_roots': defaultdict(list)
        }
        
        # Métriques de validation
        self.compression_ratios = {}
        self.fidelity_scores = {}
        
        self.log("🧬 Extracteur d'Atomes Universaux initialisé")
    
    def log(self, message):
        """Logging avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def extract_phonetic_atoms(self, text):
        """Extraction atomes phonétiques de base"""
        # Patterns de voyelles universels
        vowel_patterns = [
            r'[aeiouāēīōūàèìòùáéíóúâêîôû]',  # Voyelles simples + diacritiques
            r'[aeiou]{2,3}',  # Diphtongues et triphtongues
            r'[aeiou]n[^aeiou]',  # Voyelles nasales
        ]
        
        # Patterns de consonnes universels
        consonant_patterns = [
            r'[pbtdkgfvszhjlrnm]',  # Consonnes de base
            r'[pbtdkg][lr]',  # Clusters avec liquides
            r'[fvsz][ptk]',  # Clusters fricatives + stops
            r'[mn][pbtdkg]',  # Nasales + stops
        ]
        
        for pattern in vowel_patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                self.phonetic_atoms[f"V:{match}"] += 1
        
        for pattern in consonant_patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                self.phonetic_atoms[f"C:{match}"] += 1
        
        return len(self.phonetic_atoms)
    
    def extract_morpheme_atoms(self, text):
        """Extraction atomes morphémiques"""
        # Prefixes universels
        universal_prefixes = [
            r'\b(un|in|im|ir|dis|re|pre|pro|anti|auto|co|ex|trans)',
            r'\b(sur|sous|inter|intra|extra|ultra|super|hyper)',
            r'\b(de|des|dé|non|mal|mis|over|under)'
        ]
        
        # Suffixes universels
        universal_suffixes = [
            r'(ing|ed|er|est|ly|tion|sion|ness|ment|able|ible)\b',
            r'(ique|iste|isme|aire|oire|eur|euse|ant|ent)\b',
            r'(ité|ité|age|age|eur|eux|eux|oir|oir)\b'
        ]
        
        # Racines courtes (2-4 lettres) fréquentes
        words = re.findall(r'\b\w{2,4}\b', text.lower())
        root_counter = Counter(words)
        
        for pattern in universal_prefixes:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                self.morpheme_atoms[f"PREFIX:{match}"] += 1
        
        for pattern in universal_suffixes:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                self.morpheme_atoms[f"SUFFIX:{match}"] += 1
        
        # Garder seulement les racines très fréquentes (potentiels universaux)
        frequent_roots = {word: count for word, count in root_counter.items() 
                         if count > 5}
        
        for root, count in frequent_roots.items():
            self.morpheme_atoms[f"ROOT:{root}"] += count
        
        return len(self.morpheme_atoms)
    
    def extract_syntactic_atoms(self, text):
        """Extraction patterns syntaxiques universaux"""
        # Patterns de structure universels
        syntactic_patterns = [
            r'\b\w+\s+\w+\b',  # Paires adjacentes
            r'\b\w+\s+\w+\s+\w+\b',  # Triplets
            r'\b[A-Z]\w*\s+\w+',  # Nom propre + mot
            r'\b\w+\s+[a-z]{1,3}\s+\w+',  # Mot + fonction + mot
            r'\b\w+[.!?]\s+[A-Z]',  # Fin phrase + début
        ]
        
        # Patterns de ponctuation universels
        punctuation_patterns = [
            r'[.!?]+',  # Fins de phrase
            r'[,;:]+',  # Séparateurs
            r'[()[\]{}]+',  # Groupements
            r'["-]+',  # Citations
        ]
        
        for pattern in syntactic_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # Normaliser (enlever casse, garder structure)
                normalized = re.sub(r'\b\w+', 'W', match.lower())
                self.syntactic_atoms[f"SYNT:{normalized}"] += 1
        
        for pattern in punctuation_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                self.syntactic_atoms[f"PUNCT:{match}"] += 1
        
        return len(self.syntactic_atoms)
    
    def extract_semantic_atoms(self, text):
        """Extraction atomes sémantiques (concepts universaux)"""
        # Concepts universaux de base
        universal_concepts = {
            'numbers': r'\b(one|two|three|four|five|six|seven|eight|nine|ten|un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|\d+)\b',
            'colors': r'\b(red|blue|green|yellow|black|white|rouge|bleu|vert|jaune|noir|blanc)\b',
            'family': r'\b(mother|father|parent|child|family|mère|père|enfant|famille)\b',
            'body': r'\b(hand|head|eye|foot|body|main|tête|oeil|pied|corps)\b',
            'time': r'\b(time|day|night|hour|minute|temps|jour|nuit|heure)\b',
            'space': r'\b(here|there|up|down|left|right|ici|là|haut|bas|gauche|droite)\b',
            'emotion': r'\b(happy|sad|angry|fear|love|heureux|triste|colère|peur|amour)\b',
            'action': r'\b(go|come|take|give|see|hear|aller|venir|prendre|donner|voir|entendre)\b'
        }
        
        for concept, pattern in universal_concepts.items():
            matches = re.findall(pattern, text.lower())
            for match in matches:
                self.semantic_atoms[f"SEM:{concept}:{match}"] += 1
        
        return len(self.semantic_atoms)
    
    def analyze_corpus_file(self, file_path):
        """Analyse un fichier du corpus"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extraction par type d'atome
            phonetic_count = self.extract_phonetic_atoms(content)
            morpheme_count = self.extract_morpheme_atoms(content)
            syntactic_count = self.extract_syntactic_atoms(content)
            semantic_count = self.extract_semantic_atoms(content)
            
            file_stats = {
                'file': str(file_path),
                'size': len(content),
                'phonetic_atoms': phonetic_count,
                'morpheme_atoms': morpheme_count,
                'syntactic_atoms': syntactic_count,
                'semantic_atoms': semantic_count,
                'total_atoms': phonetic_count + morpheme_count + syntactic_count + semantic_count
            }
            
            self.log(f"📄 {file_path.name}: {file_stats['total_atoms']} atomes extraits")
            return file_stats
            
        except Exception as e:
            self.log(f"❌ Erreur analyse {file_path}: {e}")
            return None
    
    def calculate_universality_score(self, atom_dict):
        """Calcule score d'universalité basé sur fréquence et distribution"""
        if not atom_dict:
            return {}
        
        total_occurrences = sum(atom_dict.values())
        universality_scores = {}
        
        for atom, count in atom_dict.items():
            # Fréquence relative
            frequency = count / total_occurrences
            
            # Score d'universalité (log pour privilégier équilibre vs dominance)
            if count > 1:
                universality = frequency * math.log(count)
            else:
                universality = frequency * 0.1
            
            universality_scores[atom] = {
                'count': count,
                'frequency': frequency,
                'universality': universality
            }
        
        return universality_scores
    
    def validate_by_synthesis(self, original_text, atom_representation):
        """Validation par synthèse - peut-on recomposer le texte ?"""
        # Simulation de recomposition (version simplifiée)
        reconstruction_quality = 0.0
        
        # Vérifier présence des atomes principaux
        key_atoms = len([atom for atom, data in atom_representation.items() 
                        if data['universality'] > 0.01])
        
        # Score basé sur densité atomique
        total_atoms = sum(data['count'] for data in atom_representation.values())
        text_length = len(original_text.split())
        
        if text_length > 0:
            atom_density = total_atoms / text_length
            reconstruction_quality = min(1.0, atom_density * 0.1)
        
        return {
            'fidelity_score': reconstruction_quality,
            'key_atoms_count': key_atoms,
            'atom_density': atom_density if text_length > 0 else 0,
            'compression_ratio': total_atoms / text_length if text_length > 0 else 0
        }
    
    def process_corpus_directory(self, corpus_dir):
        """Traite tout un répertoire de corpus"""
        corpus_path = Path(corpus_dir)
        if not corpus_path.exists():
            self.log(f"❌ Répertoire corpus non trouvé: {corpus_path}")
            return
        
        self.log(f"🔍 Analyse corpus: {corpus_path}")
        
        # Fichiers à analyser
        text_files = []
        for ext in ['*.txt', '*.md', '*.json']:
            text_files.extend(corpus_path.glob(f"**/{ext}"))
        
        self.log(f"📊 {len(text_files)} fichiers trouvés")
        
        analysis_results = []
        for file_path in text_files:
            result = self.analyze_corpus_file(file_path)
            if result:
                analysis_results.append(result)
        
        # Calcul scores d'universalité
        self.log("🧮 Calcul scores d'universalité...")
        
        phonetic_scores = self.calculate_universality_score(self.phonetic_atoms)
        morpheme_scores = self.calculate_universality_score(self.morpheme_atoms)
        syntactic_scores = self.calculate_universality_score(self.syntactic_atoms)
        semantic_scores = self.calculate_universality_score(self.semantic_atoms)
        
        # Sauvegarde résultats
        self.save_analysis_results({
            'corpus_stats': {
                'files_processed': len(analysis_results),
                'total_phonetic_atoms': len(self.phonetic_atoms),
                'total_morpheme_atoms': len(self.morpheme_atoms),
                'total_syntactic_atoms': len(self.syntactic_atoms),
                'total_semantic_atoms': len(self.semantic_atoms)
            },
            'universality_scores': {
                'phonetic': phonetic_scores,
                'morpheme': morpheme_scores,
                'syntactic': syntactic_scores,
                'semantic': semantic_scores
            },
            'file_analysis': analysis_results
        })
        
        return analysis_results
    
    def save_analysis_results(self, results):
        """Sauvegarde résultats d'analyse"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Résultats complets
        results_file = self.results_dir / f"universal_atoms_analysis_{timestamp}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Top atomes universaux
        top_atoms = {}
        for category, scores in results['universality_scores'].items():
            if scores:
                sorted_atoms = sorted(scores.items(), 
                                    key=lambda x: x[1]['universality'], 
                                    reverse=True)
                top_atoms[category] = sorted_atoms[:20]  # Top 20
        
        top_file = self.results_dir / f"top_universal_atoms_{timestamp}.json"
        with open(top_file, 'w', encoding='utf-8') as f:
            json.dump(top_atoms, f, indent=2, ensure_ascii=False)
        
        self.log(f"💾 Résultats sauvés: {results_file.name}")
        self.log(f"🏆 Top atomes: {top_file.name}")
        
        # Affichage résumé
        self.print_analysis_summary(results)
    
    def print_analysis_summary(self, results):
        """Affiche résumé de l'analyse"""
        stats = results['corpus_stats']
        
        print("\n" + "="*60)
        print("🧬 RÉSUMÉ ANALYSE ATOMES UNIVERSAUX")
        print("="*60)
        print(f"📄 Fichiers traités: {stats['files_processed']}")
        print(f"🔤 Atomes phonétiques: {stats['total_phonetic_atoms']}")
        print(f"🧩 Atomes morphémiques: {stats['total_morpheme_atoms']}")
        print(f"🏗️ Atomes syntaxiques: {stats['total_syntactic_atoms']}")
        print(f"💭 Atomes sémantiques: {stats['total_semantic_atoms']}")
        
        total_atoms = (stats['total_phonetic_atoms'] + 
                      stats['total_morpheme_atoms'] + 
                      stats['total_syntactic_atoms'] + 
                      stats['total_semantic_atoms'])
        print(f"🎯 TOTAL ATOMES: {total_atoms}")
        
        # Top 5 de chaque catégorie
        for category, scores in results['universality_scores'].items():
            if scores:
                print(f"\n🏆 TOP 5 {category.upper()}:")
                sorted_atoms = sorted(scores.items(), 
                                    key=lambda x: x[1]['universality'], 
                                    reverse=True)
                for i, (atom, data) in enumerate(sorted_atoms[:5]):
                    print(f"  {i+1}. {atom}: {data['count']} occurrences "
                          f"(universalité: {data['universality']:.4f})")
        
        print("="*60)


def main():
    print("🧬 EXTRACTEUR D'ATOMES UNIVERSAUX PANINI")
    print("="*50)
    print("Analyse des patterns fondamentaux cross-linguistiques")
    print("Identification du noyau solide d'universaux")
    print("="*50)
    
    extractor = UniversalAtomsExtractor()
    
    # Analyser les corpus existants
    corpus_directories = [
        'tech/corpus_simple',
        'tech/corpus_pilot',
        'panini/data',
        'docs'
    ]
    
    workspace = Path('/home/stephane/GitHub/PaniniFS-Research')
    
    for corpus_dir in corpus_directories:
        full_path = workspace / corpus_dir
        if full_path.exists():
            extractor.process_corpus_directory(full_path)
        else:
            extractor.log(f"⚠️ Corpus non trouvé: {full_path}")


if __name__ == '__main__':
    main()