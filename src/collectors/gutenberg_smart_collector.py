#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏛️ Gutenberg Smart Collector
Collecteur intelligent utilisant les pages index officielles
"""

import requests
import re
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Tuple
from urllib.parse import urljoin
import random


class GutenbergSmartCollector:
    """Collecteur intelligent Gutenberg via pages index"""
    
    def __init__(self, output_dir: str = "data/gutenberg_smart_corpus"):
        self.base_url = "https://www.gutenberg.org"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache des livres populaires connus (pour éviter exploration)
        self.popular_books = {
            "11": {"title": "Alice's Adventures in Wonderland", "author": "Carroll"},
            "74": {"title": "The Adventures of Tom Sawyer", "author": "Twain"},
            "84": {"title": "Frankenstein", "author": "Shelley"},
            "46": {"title": "A Christmas Carol", "author": "Dickens"},
            "174": {"title": "The Picture of Dorian Gray", "author": "Wilde"},
            "35": {"title": "The Time Machine", "author": "Wells"},
            "43": {"title": "Dr. Jekyll and Mr. Hyde", "author": "Stevenson"},
            "120": {"title": "Treasure Island", "author": "Stevenson"},
            "1342": {"title": "Pride and Prejudice", "author": "Austen"},
            "345": {"title": "Dracula", "author": "Stoker"},
            "1661": {"title": "Sherlock Holmes", "author": "Doyle"},
            "1260": {"title": "Jane Eyre", "author": "Brontë"},
            "36": {"title": "The War of the Worlds", "author": "Wells"},
            "2701": {"title": "Moby Dick", "author": "Melville"},
            "768": {"title": "Wuthering Heights", "author": "Brontë"},
            "236": {"title": "The Jungle Book", "author": "Kipling"},
            "514": {"title": "Little Women", "author": "Alcott"},
            "1184": {"title": "The Count of Monte Cristo", "author": "Dumas"},
            "103": {"title": "Around the World in 80 Days", "author": "Verne"},
            "205": {"title": "Vanity Fair", "author": "Thackeray"}
        }
        
        print("🏛️ Gutenberg Smart Collector initialisé")
        print(f"   📚 {len(self.popular_books)} livres populaires en cache")
    
    def check_book_formats(self, gutenberg_id: str) -> Dict[str, Any]:
        """Vérifie formats disponibles pour un livre via page book"""
        
        book_url = f"{self.base_url}/ebooks/{gutenberg_id}"
        
        try:
            response = requests.get(book_url, timeout=15)
            if response.status_code != 200:
                return {}
            
            html_content = response.text
            
            # Extraire liens de téléchargement
            download_links = re.findall(
                r'href="([^"]*files/' + gutenberg_id + r'/[^"]*\.([^"\.]+))"',
                html_content
            )
            
            formats = {}
            for link, ext in download_links:
                full_url = urljoin(self.base_url, link)
                
                # Filtrer formats intéressants
                if ext.lower() in ['txt', 'html', 'epub', 'pdf']:
                    formats[ext.lower()] = {
                        'url': full_url,
                        'local_path': self.output_dir / gutenberg_id / f"{gutenberg_id}.{ext.lower()}"
                    }
            
            return formats
            
        except Exception as e:
            print(f"   ⚠️ Erreur check formats {gutenberg_id}: {e}")
            return {}
    
    def download_book_safe(self, gutenberg_id: str, book_info: Dict[str, str]) -> Dict[str, Any]:
        """Télécharge un livre de manière sécurisée"""
        
        title = book_info.get('title', 'Unknown')
        author = book_info.get('author', 'Unknown')
        
        print(f"📖 {title} - {author} (ID: {gutenberg_id})")
        
        # Vérifier formats disponibles
        formats = self.check_book_formats(gutenberg_id)
        
        if not formats:
            print("   ❌ Aucun format trouvé")
            return {'success': False, 'formats': {}}
        
        print(f"   🔍 Formats trouvés: {', '.join(formats.keys())}")
        
        # Créer répertoire livre
        book_dir = self.output_dir / gutenberg_id
        book_dir.mkdir(exist_ok=True)
        
        downloaded_formats = {}
        
        for format_name, format_info in formats.items():
            try:
                print(f"   📄 {format_name}...")
                
                response = requests.get(format_info['url'], timeout=20)
                response.raise_for_status()
                
                # Sauvegarder fichier
                local_path = format_info['local_path']
                local_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                
                file_size = len(response.content)
                downloaded_formats[format_name] = {
                    'path': str(local_path),
                    'size_bytes': file_size,
                    'url': format_info['url'],
                    'success': True
                }
                
                print(f"      ✅ {file_size:,} bytes")
                
                # Pause respectueuse
                time.sleep(random.uniform(1.0, 2.0))
                
            except Exception as e:
                print(f"      ❌ {e}")
                downloaded_formats[format_name] = {
                    'error': str(e),
                    'success': False
                }
        
        return {
            'success': len([f for f in downloaded_formats.values() if f.get('success', False)]) > 0,
            'formats': downloaded_formats,
            'title': title,
            'author': author
        }
    
    def collect_smart_corpus(self, max_books: int = 10) -> Dict[str, Any]:
        """Collecte corpus intelligent avec livres populaires"""
        
        print(f"🚀 COLLECTE SMART CORPUS GUTENBERG")
        print(f"=" * 50)
        
        # Sélectionner livres aléatoirement depuis cache
        selected_ids = list(self.popular_books.keys())[:max_books]
        random.shuffle(selected_ids)
        
        corpus_summary = {
            'collection_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'collection_method': 'smart_cache',
            'total_books': len(selected_ids),
            'successful_downloads': 0,
            'total_formats': 0,
            'books_data': {}
        }
        
        for gutenberg_id in selected_ids:
            book_info = self.popular_books[gutenberg_id]
            
            try:
                result = self.download_book_safe(gutenberg_id, book_info)
                
                if result['success']:
                    successful_formats = sum(1 for f in result['formats'].values() 
                                           if f.get('success', False))
                    
                    corpus_summary['books_data'][gutenberg_id] = {
                        'title': result['title'],
                        'author': result['author'],
                        'formats': result['formats'],
                        'successful_formats': successful_formats
                    }
                    
                    corpus_summary['successful_downloads'] += 1
                    corpus_summary['total_formats'] += successful_formats
                    
                    print(f"   ✅ {successful_formats} formats")
                else:
                    print("   ❌ Aucun format téléchargé")
                
            except Exception as e:
                print(f"   ❌ Erreur globale: {e}")
        
        # Sauvegarder métadonnées
        metadata_file = self.output_dir / 'smart_collection_metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(corpus_summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 RÉSUMÉ SMART COLLECTE:")
        print(f"   📚 Livres collectés: {corpus_summary['successful_downloads']}/{corpus_summary['total_books']}")
        print(f"   📄 Formats total: {corpus_summary['total_formats']}")
        print(f"   💾 Métadonnées: {metadata_file}")
        
        return corpus_summary


def main():
    """Test collecteur smart Gutenberg"""
    
    print("🏛️ TEST GUTENBERG SMART COLLECTOR")
    print("=" * 42)
    
    # Créer collecteur smart
    collector = GutenbergSmartCollector()
    
    # Collecter 5 livres populaires
    corpus = collector.collect_smart_corpus(max_books=5)
    
    print("\n✅ Test smart collector terminé")


if __name__ == "__main__":
    main()