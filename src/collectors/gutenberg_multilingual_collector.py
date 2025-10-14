#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌍 Gutenberg Multilingual Collector
Collecte automatique versions multilingues des mêmes œuvres pour mapping dhātu
"""

import json
import time
import requests
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class MultilingualBook:
    """Livre avec versions multilingues"""
    title: str
    author: str
    original_lang: str
    versions: Dict[str, Dict]  # lang -> {gutenberg_id, url, content_length}
    dhatu_mapping: Dict[str, Dict] = None  # lang -> dhatu_scores


class MultilingualCollector:
    """Collecteur versions multilingues œuvres Gutenberg"""
    
    def __init__(self):
        # Œuvres classiques disponibles en multi-langues 
        self.target_works = {
            "alice_wonderland": {
                "author": "Lewis Carroll", 
                "title": "Alice's Adventures in Wonderland",
                "versions": {
                    "en": {"id": "11", "url": "https://www.gutenberg.org/files/11/11-0.txt"},
                    "fr": {"id": "55456", "url": "https://www.gutenberg.org/files/55456/55456-0.txt"},
                    "de": {"id": "19778", "url": "https://www.gutenberg.org/files/19778/19778-0.txt"},
                    "es": {"id": "28885", "url": "https://www.gutenberg.org/files/28885/28885-0.txt"},
                    "it": {"id": "28371", "url": "https://www.gutenberg.org/files/28371/28371-0.txt"}
                }
            },
            "around_world_80_days": {
                "author": "Jules Verne",
                "title": "Around the World in Eighty Days", 
                "versions": {
                    "en": {"id": "103", "url": "https://www.gutenberg.org/files/103/103-0.txt"},
                    "fr": {"id": "800", "url": "https://www.gutenberg.org/files/800/800-0.txt"},
                    "de": {"id": "37761", "url": "https://www.gutenberg.org/files/37761/37761-0.txt"},
                    "es": {"id": "103", "url": "https://www.gutenberg.org/cache/epub/103/pg103.txt"}
                }
            },
            "frankenstein": {
                "author": "Mary Shelley",
                "title": "Frankenstein",
                "versions": {
                    "en": {"id": "84", "url": "https://www.gutenberg.org/files/84/84-0.txt"},
                    "fr": {"id": "17989", "url": "https://www.gutenberg.org/files/17989/17989-8.txt"},
                    "de": {"id": "46762", "url": "https://www.gutenberg.org/files/46762/46762-0.txt"},
                    "es": {"id": "21295", "url": "https://www.gutenberg.org/files/21295/21295-8.txt"}
                }
            },
            "dracula": {
                "author": "Bram Stoker", 
                "title": "Dracula",
                "versions": {
                    "en": {"id": "345", "url": "https://www.gutenberg.org/files/345/345-0.txt"},
                    "fr": {"id": "31311", "url": "https://www.gutenberg.org/files/31311/31311-8.txt"},
                    "de": {"id": "31284", "url": "https://www.gutenberg.org/files/31284/31284-0.txt"}
                }
            },
            "pride_prejudice": {
                "author": "Jane Austen",
                "title": "Pride and Prejudice", 
                "versions": {
                    "en": {"id": "1342", "url": "https://www.gutenberg.org/files/1342/1342-0.txt"},
                    "fr": {"id": "31100", "url": "https://www.gutenberg.org/files/31100/31100-8.txt"},
                    "de": {"id": "42671", "url": "https://www.gutenberg.org/files/42671/42671-0.txt"}
                }
            },
            "metamorphosis": {
                "author": "Franz Kafka",
                "title": "Metamorphosis",
                "versions": {
                    "en": {"id": "5200", "url": "https://www.gutenberg.org/files/5200/5200-0.txt"},
                    "fr": {"id": "7849", "url": "https://www.gutenberg.org/files/7849/7849-8.txt"},
                    "de": {"id": "915", "url": "https://www.gutenberg.org/files/915/915-0.txt"}
                }
            }
        }
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PaniniFS-Research/1.0 (Educational Research; Contact: research@example.com)'
        })
        
        print("🌍 Collecteur Multilingue initialisé")
        print(f"   📚 {len(self.target_works)} œuvres cibles")
        total_versions = sum(len(work['versions']) for work in self.target_works.values())
        print(f"   🔗 {total_versions} versions à collecter")
    
    def collect_multilingual_corpus(self, output_dir: str = "data/gutenberg_multilingual_corpus") -> Dict[str, MultilingualBook]:
        """Collecte corpus multilingue complet"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"🌍 COLLECTE CORPUS MULTILINGUE")
        print("=" * 50)
        
        collected_works = {}
        
        for work_key, work_info in self.target_works.items():
            print(f"\n📖 Collecte: {work_info['title']} - {work_info['author']}")
            
            multilingual_book = MultilingualBook(
                title=work_info['title'],
                author=work_info['author'], 
                original_lang="en",  # Assume anglais original
                versions={}
            )
            
            work_dir = output_path / work_key
            work_dir.mkdir(exist_ok=True)
            
            # Collecter chaque version linguistique
            for lang, version_info in work_info['versions'].items():
                print(f"   🔗 {lang.upper()}: ID {version_info['id']}")
                
                try:
                    # Télécharger
                    response = self.session.get(version_info['url'], timeout=30)
                    response.raise_for_status()
                    content = response.text
                    
                    # Sauvegarder
                    lang_file = work_dir / f"{work_key}_{lang}.txt"
                    with open(lang_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    # Enregistrer métadonnées
                    multilingual_book.versions[lang] = {
                        'gutenberg_id': version_info['id'],
                        'url': version_info['url'],
                        'file_path': str(lang_file),
                        'content_length': len(content),
                        'download_success': True
                    }
                    
                    print(f"      ✅ {len(content):,} caractères téléchargés")
                    
                    # Pause respectueuse
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"      ❌ Erreur: {e}")
                    multilingual_book.versions[lang] = {
                        'gutenberg_id': version_info['id'],
                        'url': version_info['url'],
                        'download_success': False,
                        'error': str(e)
                    }
            
            collected_works[work_key] = multilingual_book
        
        # Sauvegarder métadonnées collecte
        metadata_file = output_path / 'multilingual_metadata.json'
        metadata = {}
        
        for work_key, book in collected_works.items():
            metadata[work_key] = {
                'title': book.title,
                'author': book.author,
                'original_lang': book.original_lang,
                'versions': book.versions
            }
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 COLLECTE TERMINÉE:")
        successful_works = len([w for w in collected_works.values() if any(v.get('download_success', False) for v in w.versions.values())])
        print(f"   📚 Œuvres: {successful_works}/{len(collected_works)}")
        total_files = sum(sum(1 for v in w.versions.values() if v.get('download_success', False)) for w in collected_works.values())
        print(f"   📄 Fichiers: {total_files}")
        print(f"   💾 Métadonnées: {metadata_file}")
        
        return collected_works
    
    def verify_collection_integrity(self, corpus_dir: str = "data/gutenberg_multilingual_corpus") -> Dict[str, Any]:
        """Vérifie l'intégrité de la collecte multilingue"""
        
        corpus_path = Path(corpus_dir)
        if not corpus_path.exists():
            return {"error": "Corpus directory not found"}
        
        print(f"🔍 VÉRIFICATION INTÉGRITÉ CORPUS")
        print("=" * 40)
        
        verification = {
            'total_works': 0,
            'complete_works': 0,  # Toutes langues présentes
            'partial_works': 0,   # Quelques langues manquantes
            'languages_found': set(),
            'file_sizes': {},
            'integrity_score': 0.0
        }
        
        for work_dir in corpus_path.iterdir():
            if work_dir.is_dir() and work_dir.name in self.target_works:
                work_key = work_dir.name
                verification['total_works'] += 1
                
                expected_langs = set(self.target_works[work_key]['versions'].keys())
                found_files = list(work_dir.glob('*.txt'))
                found_langs = set()
                
                print(f"📖 {work_key}:")
                
                for file_path in found_files:
                    # Extraire langue du nom fichier
                    lang = file_path.stem.split('_')[-1]
                    if lang in expected_langs:
                        found_langs.add(lang)
                        verification['languages_found'].add(lang)
                        
                        file_size = file_path.stat().st_size
                        if work_key not in verification['file_sizes']:
                            verification['file_sizes'][work_key] = {}
                        verification['file_sizes'][work_key][lang] = file_size
                        
                        print(f"   ✅ {lang.upper()}: {file_size:,} bytes")
                
                missing_langs = expected_langs - found_langs
                if missing_langs:
                    print(f"   ❌ Manquant: {', '.join(missing_langs).upper()}")
                    verification['partial_works'] += 1
                else:
                    verification['complete_works'] += 1
        
        # Calcul score intégrité
        if verification['total_works'] > 0:
            verification['integrity_score'] = verification['complete_works'] / verification['total_works']
        
        print(f"\n📊 INTÉGRITÉ:")
        print(f"   📚 Œuvres complètes: {verification['complete_works']}/{verification['total_works']}")
        print(f"   🌍 Langues: {', '.join(sorted(verification['languages_found'])).upper()}")
        print(f"   📈 Score intégrité: {verification['integrity_score']:.2%}")
        
        return verification


def main():
    """Test collecte corpus multilingue"""
    
    print("🌍 TEST COLLECTE MULTILINGUE GUTENBERG")
    print("=" * 50)
    
    collector = MultilingualCollector()
    
    # Collecter corpus
    collected_works = collector.collect_multilingual_corpus()
    
    # Vérifier intégrité
    verification = collector.verify_collection_integrity()
    
    print(f"\n✅ COLLECTE MULTILINGUE TERMINÉE")
    print(f"   🎯 Score intégrité: {verification['integrity_score']:.2%}")
    
    return collected_works, verification


if __name__ == "__main__":
    main()