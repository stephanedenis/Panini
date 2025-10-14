#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏛️ Projet Gutenberg Collector
Collecte et préparation corpus multilingue/multiformat pour validation dhātu
"""

import requests
import re
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urlparse, urljoin
import mimetypes


class GutenbergCollector:
    """Collecteur intelligent Projet Gutenberg pour recherche dhātu"""
    
    def __init__(self, output_dir: str = "data/gutenberg_corpus"):
        self.base_url = "https://www.gutenberg.org"
        self.mirror_urls = [
            "https://www.gutenberg.org",
            "http://aleph.gutenberg.org",
            "https://gutenberg.pglaf.org"
        ]
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Métadonnées collectées
        self.collected_books = {}
        self.format_stats = {}
        
        print(f"🏛️ Gutenberg Collector initialisé")
        print(f"   📂 Répertoire: {self.output_dir}")
    
    def search_multilingual_books(self, max_books: int = 20) -> List[Dict[str, Any]]:
        """Recherche livres disponibles en plusieurs langues"""
        
        print(f"🔍 Recherche livres multilingues (max {max_books})")
        
        # Titres classiques souvent traduits (IDs avec txt disponible)
        multilingual_candidates = [
            {"title": "Alice's Adventures in Wonderland", "author": "Carroll", "gutenberg_id": "11"},
            {"title": "Pride and Prejudice", "author": "Austen", "gutenberg_id": "1342"},
            {"title": "The Adventures of Tom Sawyer", "author": "Twain", "gutenberg_id": "74"},
            {"title": "Frankenstein", "author": "Shelley", "gutenberg_id": "84"},
            {"title": "A Christmas Carol", "author": "Dickens", "gutenberg_id": "46"},
            {"title": "The Picture of Dorian Gray", "author": "Wilde", "gutenberg_id": "174"},
            {"title": "The Time Machine", "author": "Wells", "gutenberg_id": "35"},
            {"title": "Around the World in Eighty Days", "author": "Verne", "gutenberg_id": "103"},
            {"title": "The Strange Case of Dr. Jekyll and Mr. Hyde", "author": "Stevenson", "gutenberg_id": "43"},
            {"title": "Dracula", "author": "Stoker", "gutenberg_id": "345"},
            {"title": "The Adventures of Sherlock Holmes", "author": "Doyle", "gutenberg_id": "1661"},
            {"title": "Jane Eyre", "author": "Brontë", "gutenberg_id": "1260"},
            {"title": "The War of the Worlds", "author": "Wells", "gutenberg_id": "36"},
            {"title": "Treasure Island", "author": "Stevenson", "gutenberg_id": "120"},
            {"title": "The Count of Monte Cristo", "author": "Dumas", "gutenberg_id": "1184"},
            {"title": "Moby Dick", "author": "Melville", "gutenberg_id": "2701"},
            {"title": "The Great Gatsby", "author": "Fitzgerald", "gutenberg_id": "64317"},
            {"title": "Wuthering Heights", "author": "Brontë", "gutenberg_id": "768"},
            {"title": "The Jungle Book", "author": "Kipling", "gutenberg_id": "236"},
            {"title": "Little Women", "author": "Alcott", "gutenberg_id": "514"},
        ]
        
        return multilingual_candidates[:max_books]
    
    def get_book_formats(self, gutenberg_id: str) -> Dict[str, str]:
        """Récupère les formats disponibles pour un livre"""
        
        formats = {}
        base_url = f"https://www.gutenberg.org/ebooks/{gutenberg_id}"
        
        # Formats standards Gutenberg
        format_extensions = {
            'txt': 'Plain Text UTF-8',
            'txt.utf-8': 'Plain Text UTF-8',
            'html': 'HTML',
            'epub.noimages': 'EPUB (no images)',
            'epub.images': 'EPUB (with images)',
            'kindle.noimages': 'Kindle (no images)',
            'pdf': 'PDF'
        }
        
        for ext, description in format_extensions.items():
            # URL pattern Gutenberg
            if gutenberg_id.startswith('1'):
                # IDs starting with 1: files/1342/1342-0.txt
                url = f"https://www.gutenberg.org/files/{gutenberg_id}/{gutenberg_id}-0.{ext}"
            else:
                # Other IDs: files/74/74-0.txt  
                url = f"https://www.gutenberg.org/files/{gutenberg_id}/{gutenberg_id}-0.{ext}"
            
            formats[ext] = {
                'url': url,
                'description': description,
                'local_path': self.output_dir / f"{gutenberg_id}" / f"{gutenberg_id}.{ext}"
            }
        
        return formats
    
    def download_book_formats(self, book_info: Dict[str, Any]) -> Dict[str, Any]:
        """Télécharge tous les formats disponibles d'un livre"""
        
        gutenberg_id = book_info['gutenberg_id']
        title = book_info['title']
        
        print(f"📖 Téléchargement: {title} (ID: {gutenberg_id})")
        
        # Créer répertoire livre
        book_dir = self.output_dir / gutenberg_id
        book_dir.mkdir(exist_ok=True)
        
        formats = self.get_book_formats(gutenberg_id)
        downloaded_formats = {}
        
        for format_name, format_info in formats.items():
            try:
                print(f"   📄 Format {format_name}...")
                
                response = requests.get(format_info['url'], timeout=30)
                
                if response.status_code == 200:
                    # Sauvegarder fichier
                    local_path = format_info['local_path']
                    local_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(local_path, 'wb') as f:
                        f.write(response.content)
                    
                    # Statistiques
                    file_size = len(response.content)
                    downloaded_formats[format_name] = {
                        'path': str(local_path),
                        'size_bytes': file_size,
                        'url': format_info['url'],
                        'success': True
                    }
                    
                    print(f"      ✅ {file_size:,} bytes")
                
                else:
                    print(f"      ❌ HTTP {response.status_code}")
                    downloaded_formats[format_name] = {
                        'error': f"HTTP {response.status_code}",
                        'success': False
                    }
                
                # Pause entre téléchargements
                time.sleep(1)
                
            except Exception as e:
                print(f"      ❌ Erreur: {e}")
                downloaded_formats[format_name] = {
                    'error': str(e),
                    'success': False
                }
        
        return downloaded_formats
    
    def collect_test_corpus(self, max_books: int = 5) -> Dict[str, Any]:
        """Collecte corpus test pour validation dhātu"""
        
        print(f"🚀 COLLECTE CORPUS GUTENBERG")
        print(f"=" * 50)
        
        # Rechercher livres multilingues
        books = self.search_multilingual_books(max_books)
        
        corpus_summary = {
            'collection_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_books': len(books),
            'successful_downloads': 0,
            'total_formats': 0,
            'books_data': {}
        }
        
        for book in books:
            try:
                # Télécharger formats disponibles
                formats = self.download_book_formats(book)
                
                # Statistiques
                successful_formats = sum(1 for f in formats.values() if f.get('success', False))
                
                corpus_summary['books_data'][book['gutenberg_id']] = {
                    'title': book['title'],
                    'author': book['author'],
                    'formats': formats,
                    'successful_formats': successful_formats
                }
                
                if successful_formats > 0:
                    corpus_summary['successful_downloads'] += 1
                    corpus_summary['total_formats'] += successful_formats
                
                print(f"   ✅ {book['title']}: {successful_formats} formats")
                
            except Exception as e:
                print(f"   ❌ {book['title']}: {e}")
        
        # Sauvegarder métadonnées
        metadata_file = self.output_dir / 'collection_metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(corpus_summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 RÉSUMÉ COLLECTE:")
        print(f"   📚 Livres collectés: {corpus_summary['successful_downloads']}/{corpus_summary['total_books']}")
        print(f"   📄 Formats total: {corpus_summary['total_formats']}")
        print(f"   💾 Métadonnées: {metadata_file}")
        
        return corpus_summary


def main():
    """Test collecteur Gutenberg"""
    
    print("🏛️ TEST GUTENBERG COLLECTOR")
    print("=" * 40)
    
    # Créer collecteur
    collector = GutenbergCollector()
    
    # Collecter corpus test
    corpus = collector.collect_test_corpus(max_books=3)  # Test avec 3 livres
    
    print("\n✅ Test collecteur terminé")


if __name__ == "__main__":
    main()