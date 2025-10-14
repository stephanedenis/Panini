#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏛️ Gutenberg Direct Collector
Collecteur utilisant URLs directes vérifiées (zéro 404)
"""

import requests
import json
import time
from pathlib import Path
from typing import Dict, List, Any
import random


class GutenbergDirectCollector:
    """Collecteur direct avec URLs vérifiées"""
    
    def __init__(self, output_dir: str = "data/gutenberg_direct_corpus"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # URLs directes vérifiées (format txt UTF-8)
        self.verified_books = {
            "11": {
                "title": "Alice's Adventures in Wonderland",
                "author": "Carroll, Lewis",
                "txt_url": "https://www.gutenberg.org/files/11/11-0.txt"
            },
            "74": {
                "title": "The Adventures of Tom Sawyer", 
                "author": "Twain, Mark",
                "txt_url": "https://www.gutenberg.org/files/74/74-0.txt"
            },
            "84": {
                "title": "Frankenstein",
                "author": "Shelley, Mary",
                "txt_url": "https://www.gutenberg.org/files/84/84-0.txt"
            },
            "1342": {
                "title": "Pride and Prejudice",
                "author": "Austen, Jane", 
                "txt_url": "https://www.gutenberg.org/files/1342/1342-0.txt"
            },
            "174": {
                "title": "The Picture of Dorian Gray",
                "author": "Wilde, Oscar",
                "txt_url": "https://www.gutenberg.org/files/174/174-0.txt"
            },
            "46": {
                "title": "A Christmas Carol",
                "author": "Dickens, Charles",
                "txt_url": "https://www.gutenberg.org/files/46/46-0.txt"
            },
            "345": {
                "title": "Dracula",
                "author": "Stoker, Bram",
                "txt_url": "https://www.gutenberg.org/files/345/345-0.txt"
            },
            "120": {
                "title": "Treasure Island", 
                "author": "Stevenson, Robert Louis",
                "txt_url": "https://www.gutenberg.org/files/120/120-0.txt"
            },
            "35": {
                "title": "The Time Machine",
                "author": "Wells, H. G.",
                "txt_url": "https://www.gutenberg.org/files/35/35-0.txt"
            },
            "43": {
                "title": "The Strange Case of Dr. Jekyll and Mr. Hyde",
                "author": "Stevenson, Robert Louis", 
                "txt_url": "https://www.gutenberg.org/files/43/43-0.txt"
            },
            "768": {
                "title": "Wuthering Heights",
                "author": "Brontë, Emily",
                "txt_url": "https://www.gutenberg.org/files/768/768-0.txt"
            },
            "1260": {
                "title": "Jane Eyre",
                "author": "Brontë, Charlotte",
                "txt_url": "https://www.gutenberg.org/files/1260/1260-0.txt"
            },
            "2701": {
                "title": "Moby Dick",
                "author": "Melville, Herman",
                "txt_url": "https://www.gutenberg.org/files/2701/2701-0.txt"
            },
            "514": {
                "title": "Little Women",
                "author": "Alcott, Louisa May",
                "txt_url": "https://www.gutenberg.org/files/514/514-0.txt"
            },
            "36": {
                "title": "The War of the Worlds",
                "author": "Wells, H. G.",
                "txt_url": "https://www.gutenberg.org/files/36/36-0.txt"
            }
        }
        
        print("🏛️ Gutenberg Direct Collector initialisé")
        print(f"   📚 {len(self.verified_books)} URLs vérifiées")
    
    def download_book_direct(self, gutenberg_id: str) -> Dict[str, Any]:
        """Télécharge un livre via URL directe"""
        
        book_info = self.verified_books[gutenberg_id]
        title = book_info['title']
        author = book_info['author']
        
        print(f"📖 {title[:40]}... - {author}")
        
        try:
            response = requests.get(book_info['txt_url'], timeout=20)
            response.raise_for_status()
            
            # Créer répertoire livre
            book_dir = self.output_dir / gutenberg_id
            book_dir.mkdir(exist_ok=True)
            
            # Sauvegarder fichier
            local_path = book_dir / f"{gutenberg_id}.txt"
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            file_size = len(response.content)
            
            result = {
                'success': True,
                'title': title,
                'author': author,
                'file_path': str(local_path),
                'file_size': file_size,
                'url': book_info['txt_url']
            }
            
            print(f"   ✅ {file_size:,} bytes téléchargés")
            return result
            
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            return {
                'success': False,
                'title': title,
                'author': author,
                'error': str(e)
            }
    
    def collect_verified_corpus(self, max_books: int = 10) -> Dict[str, Any]:
        """Collecte corpus avec URLs vérifiées (zéro 404)"""
        
        print(f"🚀 COLLECTE CORPUS GUTENBERG DIRECT")
        print(f"=" * 50)
        
        # Sélectionner livres aléatoirement
        available_ids = list(self.verified_books.keys())
        selected_ids = random.sample(available_ids, min(max_books, len(available_ids)))
        
        corpus_summary = {
            'collection_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'collection_method': 'direct_verified_urls',
            'total_books': len(selected_ids),
            'successful_downloads': 0,
            'total_bytes': 0,
            'books_data': {}
        }
        
        for gutenberg_id in selected_ids:
            result = self.download_book_direct(gutenberg_id)
            
            corpus_summary['books_data'][gutenberg_id] = result
            
            if result['success']:
                corpus_summary['successful_downloads'] += 1
                corpus_summary['total_bytes'] += result['file_size']
            
            # Pause respectueuse entre téléchargements
            time.sleep(random.uniform(1.5, 2.5))
        
        # Sauvegarder métadonnées
        metadata_file = self.output_dir / 'direct_collection_metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(corpus_summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 RÉSUMÉ COLLECTE DIRECTE:")
        print(f"   📚 Livres collectés: {corpus_summary['successful_downloads']}/{corpus_summary['total_books']}")
        print(f"   📄 Taille total: {corpus_summary['total_bytes']:,} bytes")
        print(f"   💾 Métadonnées: {metadata_file}")
        
        return corpus_summary


def main():
    """Test collecteur direct Gutenberg"""
    
    print("🏛️ TEST GUTENBERG DIRECT COLLECTOR")
    print("=" * 42)
    
    # Créer collecteur direct
    collector = GutenbergDirectCollector()
    
    # Collecter 8 livres avec URLs vérifiées
    corpus = collector.collect_verified_corpus(max_books=8)
    
    print("\n✅ Test direct collector terminé")


if __name__ == "__main__":
    main()