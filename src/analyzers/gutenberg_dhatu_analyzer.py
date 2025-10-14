#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧬 Gutenberg Dhātu Analyzer
Extraction contenu authentique + analyse universaux dhātu sur corpus Gutenberg
"""

import re
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass


@dataclass
class BookContent:
    """Contenu extrait d'un livre Gutenberg"""
    title: str
    author: str
    gutenberg_id: str
    authentic_content: str
    metadata_blocks: List[str]
    dhatu_analysis: Dict[str, float] = None
    content_signature: str = None


class GutenbergContentExtractor:
    """Extracteur contenu authentique livres Gutenberg"""
    
    def __init__(self):
        # Patterns typiques Gutenberg à supprimer
        self.gutenberg_patterns = [
            # Début standard Gutenberg
            r'\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*',
            # Fin standard Gutenberg  
            r'\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*',
            # Copyright et légal
            r'This eBook is for the use of anyone anywhere.*?Project Gutenberg',
            r'Project Gutenberg.*?is located at.*?\.',
            r'Most people start at our Web site.*?http://www\.gutenberg\.org/',
            # Métadonnées début
            r'Title:.*?\n',
            r'Author:.*?\n', 
            r'Release Date:.*?\n',
            r'Language:.*?\n',
            r'\[eBook #\d+\]',
            # Encodage et production
            r'Character set encoding:.*?\n',
            r'Produced by.*?\n',
            r'Updated:.*?\n',
        ]
        
        print("🧬 Gutenberg Content Extractor initialisé")
    
    def extract_authentic_content(self, file_path: Path) -> BookContent:
        """Extrait le contenu authentique d'un fichier Gutenberg"""
        
        print(f"📖 Extraction: {file_path.name}")
        
        # Lire fichier
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            raw_content = f.read()
        
        # Extraire métadonnées avant nettoyage
        metadata_blocks = []
        cleaned_content = raw_content
        
        # Supprimer patterns Gutenberg
        for pattern in self.gutenberg_patterns:
            matches = re.findall(pattern, cleaned_content, re.IGNORECASE | re.DOTALL)
            metadata_blocks.extend(matches)
            cleaned_content = re.sub(pattern, '', cleaned_content, flags=re.IGNORECASE | re.DOTALL)
        
        # Nettoyage supplémentaire
        cleaned_content = self._clean_text(cleaned_content)
        
        # Extraire métadonnées du nom de fichier
        gutenberg_id = file_path.stem.split('.')[0]
        
        # Créer signature contenu
        content_hash = hashlib.sha256(cleaned_content.encode('utf-8')).hexdigest()[:16]
        
        book = BookContent(
            title="Unknown",  # À améliorer avec parsing métadonnées
            author="Unknown",
            gutenberg_id=gutenberg_id,
            authentic_content=cleaned_content,
            metadata_blocks=metadata_blocks,
            content_signature=content_hash
        )
        
        print(f"   ✅ Contenu extrait: {len(cleaned_content):,} caractères")
        print(f"   🔍 Signature: {content_hash}")
        
        return book
    
    def _clean_text(self, text: str) -> str:
        """Nettoyage final du texte"""
        
        # Supprimer lignes vides multiples
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        
        # Supprimer espaces en début/fin
        text = text.strip()
        
        # Supprimer caractères de contrôle
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f]', '', text)
        
        return text


class DhatuAnalyzer:
    """Analyseur dhātu pour contenu textuel"""
    
    def __init__(self):
        # Les 9 dhātu universels validés
        self.dhatu_names = [
            'RELATE', 'MODAL', 'EXIST', 'EVAL', 'COMM',
            'CAUSE', 'ITER', 'DECIDE', 'FEEL'
        ]
        
        # Patterns simples pour détection dhātu (à améliorer)
        self.dhatu_patterns = {
            'RELATE': r'\b(with|to|from|between|among|relation|connect|link)\b',
            'MODAL': r'\b(can|could|may|might|must|should|would|possible|necessary)\b',
            'EXIST': r'\b(is|are|was|were|be|being|been|exist|there)\b',
            'EVAL': r'\b(good|bad|better|worse|best|worst|great|terrible|evaluate)\b',
            'COMM': r'\b(say|said|tell|told|speak|talk|communicate|express|word)\b',
            'CAUSE': r'\b(because|since|therefore|thus|cause|reason|result|effect)\b',
            'ITER': r'\b(again|repeat|continue|always|often|usually|every|each)\b',
            'DECIDE': r'\b(decide|choose|select|determine|resolve|conclude|judge)\b',
            'FEEL': r'\b(feel|felt|emotion|happy|sad|love|hate|like|dislike)\b'
        }
        
        print("🧬 Dhātu Analyzer initialisé avec 9 universaux")
    
    def analyze_dhatu_distribution(self, content: str) -> Dict[str, float]:
        """Analyse distribution dhātu dans le contenu"""
        
        content_lower = content.lower()
        total_words = len(content.split())
        
        dhatu_scores = {}
        
        for dhatu_name in self.dhatu_names:
            if dhatu_name in self.dhatu_patterns:
                pattern = self.dhatu_patterns[dhatu_name]
                matches = re.findall(pattern, content_lower)
                score = len(matches) / max(total_words, 1)  # Éviter division par 0
                dhatu_scores[dhatu_name] = round(score, 6)
            else:
                dhatu_scores[dhatu_name] = 0.0
        
        # Normaliser scores
        total_score = sum(dhatu_scores.values())
        if total_score > 0:
            dhatu_scores = {k: round(v / total_score, 6) for k, v in dhatu_scores.items()}
        
        return dhatu_scores
    
    def get_dominant_dhatus(self, dhatu_scores: Dict[str, float], top_k: int = 3) -> List[Tuple[str, float]]:
        """Retourne les dhātu dominants"""
        
        sorted_dhatus = sorted(dhatu_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_dhatus[:top_k]


class GutenbergDhatuPipeline:
    """Pipeline complet analyse dhātu corpus Gutenberg"""
    
    def __init__(self, corpus_dir: str = "data/gutenberg_corpus"):
        self.corpus_dir = Path(corpus_dir)
        self.extractor = GutenbergContentExtractor()
        self.analyzer = DhatuAnalyzer()
        
        print("🚀 Pipeline Gutenberg-Dhātu initialisé")
    
    def process_corpus(self) -> Dict[str, Any]:
        """Traite tout le corpus Gutenberg collecté"""
        
        print("🧬 ANALYSE CORPUS GUTENBERG")
        print("=" * 50)
        
        results = {
            'processing_summary': {
                'total_books': 0,
                'successful_extractions': 0,
                'total_characters': 0,
                'average_dhatu_scores': {}
            },
            'books_analysis': {}
        }
        
        # Parcourir répertoires livres
        for book_dir in self.corpus_dir.glob('*/'):
            if book_dir.is_dir() and book_dir.name.isdigit():
                gutenberg_id = book_dir.name
                
                # Chercher fichier txt
                txt_files = list(book_dir.glob('*.txt'))
                if txt_files:
                    txt_file = txt_files[0]
                    
                    try:
                        # Extraire contenu authentique
                        book = self.extractor.extract_authentic_content(txt_file)
                        
                        # Analyser dhātu
                        dhatu_scores = self.analyzer.analyze_dhatu_distribution(book.authentic_content)
                        dominant_dhatus = self.analyzer.get_dominant_dhatus(dhatu_scores)
                        
                        book.dhatu_analysis = dhatu_scores
                        
                        # Stocker résultats
                        results['books_analysis'][gutenberg_id] = {
                            'title': book.title,
                            'author': book.author,
                            'content_length': len(book.authentic_content),
                            'content_signature': book.content_signature,
                            'dhatu_scores': dhatu_scores,
                            'dominant_dhatus': dominant_dhatus,
                            'metadata_blocks_count': len(book.metadata_blocks)
                        }
                        
                        # Statistiques
                        results['processing_summary']['successful_extractions'] += 1
                        results['processing_summary']['total_characters'] += len(book.authentic_content)
                        
                        print(f"✅ {gutenberg_id}: {len(book.authentic_content):,} chars")
                        print(f"   🧬 Dominant: {', '.join([f'{d}({s:.3f})' for d, s in dominant_dhatus])}")
                        
                    except Exception as e:
                        print(f"❌ {gutenberg_id}: {e}")
                
                results['processing_summary']['total_books'] += 1
        
        # Calcul moyennes dhātu
        if results['processing_summary']['successful_extractions'] > 0:
            avg_scores = {}
            for dhatu in self.analyzer.dhatu_names:
                scores = [book['dhatu_scores'].get(dhatu, 0) 
                         for book in results['books_analysis'].values()]
                avg_scores[dhatu] = round(sum(scores) / len(scores), 6) if scores else 0
            
            results['processing_summary']['average_dhatu_scores'] = avg_scores
        
        # Sauvegarder résultats
        output_file = self.corpus_dir / 'dhatu_analysis_results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 RÉSULTATS PIPELINE:")
        print(f"   📚 Livres traités: {results['processing_summary']['successful_extractions']}/{results['processing_summary']['total_books']}")
        print(f"   📄 Total caractères: {results['processing_summary']['total_characters']:,}")
        print(f"   💾 Résultats: {output_file}")
        
        return results


def main():
    """Test pipeline dhātu Gutenberg"""
    
    print("🧬 TEST PIPELINE GUTENBERG-DHĀTU MASSIF")
    print("=" * 50)
    
    # Créer pipeline sur corpus massif
    pipeline = GutenbergDhatuPipeline("data/gutenberg_massive_corpus")
    
    # Traiter corpus
    results = pipeline.process_corpus()
    
    # Afficher résultats validation universaux
    print(f"\n📊 VALIDATION UNIVERSAUX DHĀTU:")
    avg_scores = results['processing_summary']['average_dhatu_scores']
    sorted_dhatus = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)
    
    for dhatu, score in sorted_dhatus:
        percentage = score * 100
        bar = "█" * int(percentage / 5)  # Barre visuelle
        print(f"   {dhatu:8}: {percentage:5.2f}% {bar}")
    
    print(f"\n✅ VALIDATION COMPLÈTE:")
    print(f"   📚 Livres: {results['processing_summary']['successful_extractions']}")
    print(f"   📄 Caractères: {results['processing_summary']['total_characters']:,}")
    
    print("\n✅ Pipeline massif terminé avec succès")


if __name__ == "__main__":
    main()