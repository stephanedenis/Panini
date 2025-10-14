#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌍 Gutenberg Multilingual Collector (URLs Vérifiées)
Collecte versions multilingues avec URLs directement validées
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


class VerifiedMultilingualCollector:
    """Collecteur URLs vérifiées multilingues Gutenberg"""
    
    def __init__(self):
        # URLs vérifiées manuellement pour versions multilingues
        self.verified_works = {
            "alice_wonderland": {
                "author": "Lewis Carroll",
                "title": "Alice's Adventures in Wonderland",
                "versions": {
                    "en": {
                        "id": "11", 
                        "url": "https://www.gutenberg.org/files/11/11-0.txt"
                    },
                    "fr": {
                        "id": "55456", 
                        "url": "https://www.gutenberg.org/cache/epub/55456/pg55456.txt"
                    }
                }
            },
            "frankenstein": {
                "author": "Mary Shelley", 
                "title": "Frankenstein",
                "versions": {
                    "en": {
                        "id": "84",
                        "url": "https://www.gutenberg.org/files/84/84-0.txt"
                    },
                    "de": {
                        "id": "21264",
                        "url": "https://www.gutenberg.org/files/21264/21264-0.txt"
                    }
                }
            },
            "pride_prejudice": {
                "author": "Jane Austen",
                "title": "Pride and Prejudice", 
                "versions": {
                    "en": {
                        "id": "1342",
                        "url": "https://www.gutenberg.org/files/1342/1342-0.txt"
                    },
                    "de": {
                        "id": "42671", 
                        "url": "https://www.gutenberg.org/files/42671/42671-0.txt"
                    }
                }
            },
            "around_world_80_days": {
                "author": "Jules Verne",
                "title": "Around the World in Eighty Days",
                "versions": {
                    "en": {
                        "id": "103",
                        "url": "https://www.gutenberg.org/files/103/103-0.txt"  
                    },
                    "fr": {
                        "id": "800",
                        "url": "https://www.gutenberg.org/cache/epub/800/pg800.txt"
                    }
                }
            },
            "metamorphosis": {
                "author": "Franz Kafka",
                "title": "Metamorphosis",
                "versions": {
                    "en": {
                        "id": "5200",
                        "url": "https://www.gutenberg.org/files/5200/5200-0.txt"
                    },
                    "de": {
                        "id": "915",
                        "url": "https://www.gutenberg.org/cache/epub/915/pg915.txt"
                    }
                }
            },
            "dracula": {
                "author": "Bram Stoker",
                "title": "Dracula", 
                "versions": {
                    "en": {
                        "id": "345",
                        "url": "https://www.gutenberg.org/files/345/345-0.txt"
                    },
                    "fr": {
                        "id": "31311",
                        "url": "https://www.gutenberg.org/cache/epub/31311/pg31311.txt"
                    }
                }
            }
        }
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PaniniFS-Research/1.0 (Educational Research)'
        })
        
        print("🌍 Collecteur Multilingue Vérifié initialisé")
        print(f"   📚 {len(self.verified_works)} œuvres cibles")
        total = sum(len(w['versions']) for w in self.verified_works.values())
        print(f"   🔗 {total} versions vérifiées")
    
    def collect_verified_multilingual_corpus(self, output_dir: str = "data/gutenberg_multilingual_verified") -> Dict[str, MultilingualBook]:
        """Collecte corpus multilingue avec URLs vérifiées"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"🌍 COLLECTE CORPUS MULTILINGUE VÉRIFIÉ")
        print("=" * 50)
        
        collected_works = {}
        total_chars = 0
        
        for work_key, work_info in self.verified_works.items():
            print(f"\n📖 {work_info['title']} - {work_info['author']}")
            
            multilingual_book = MultilingualBook(
                title=work_info['title'],
                author=work_info['author'],
                original_lang="en",
                versions={}
            )
            
            work_dir = output_path / work_key
            work_dir.mkdir(exist_ok=True)
            
            # Collecter chaque version linguistique
            for lang, version_info in work_info['versions'].items():
                print(f"   🔗 {lang.upper()}: ID {version_info['id']}")
                
                try:
                    # Télécharger avec vérification
                    response = self.session.get(version_info['url'], timeout=30)
                    response.raise_for_status()
                    content = response.text
                    
                    # Vérifier contenu valide (pas d'erreur 404 HTML)
                    if '<title>404 Not Found</title>' in content or len(content) < 1000:
                        raise Exception(f"Contenu invalide: {len(content)} chars")
                    
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
                    
                    total_chars += len(content)
                    print(f"      ✅ {len(content):,} caractères")
                    
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
        metadata_file = output_path / 'multilingual_verified_metadata.json'
        metadata = {
            'collection_summary': {
                'total_works': len(collected_works),
                'total_characters': total_chars,
                'languages': ['en', 'fr', 'de']
            },
            'works': {}
        }
        
        for work_key, book in collected_works.items():
            metadata['works'][work_key] = {
                'title': book.title,
                'author': book.author,
                'original_lang': book.original_lang,
                'versions': book.versions
            }
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 COLLECTE TERMINÉE:")
        successful = sum(1 for w in collected_works.values() 
                        if any(v.get('download_success', False) 
                              for v in w.versions.values()))
        print(f"   📚 Œuvres: {successful}/{len(collected_works)}")
        total_files = sum(sum(1 for v in w.versions.values() 
                             if v.get('download_success', False)) 
                         for w in collected_works.values())
        print(f"   📄 Fichiers: {total_files}")
        print(f"   📝 Caractères: {total_chars:,}")
        print(f"   💾 Métadonnées: {metadata_file}")
        
        return collected_works


def main():
    """Test collecte corpus multilingue vérifié"""
    
    print("🌍 TEST COLLECTE MULTILINGUE VÉRIFIÉ")
    print("=" * 50)
    
    collector = VerifiedMultilingualCollector()
    
    # Collecter corpus
    collected_works = collector.collect_verified_multilingual_corpus()
    
    print(f"\n✅ COLLECTE MULTILINGUE VÉRIFIÉE TERMINÉE")
    
    return collected_works


if __name__ == "__main__":
    main()