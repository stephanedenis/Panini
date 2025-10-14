#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏛️ Projet Gutenberg API Collector
Utilise l'API officielle pour récupérer métadonnées et formats disponibles
"""

import requests
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import re


class GutenbergAPICollector:
    """Collecteur utilisant l'API officielle Gutenberg"""
    
    def __init__(self, output_dir: str = "data/gutenberg_api_corpus"):
        self.api_base = "https://gutendex.com"
        self.gutenberg_files_base = "https://www.gutenberg.org/files"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print("🏛️ Gutenberg API Collector initialisé")
        print(f"   🔗 API: {self.api_base}")
        print(f"   📂 Répertoire: {self.output_dir}")
    
    def search_books_by_language(self, languages: List[str] = ["en"], 
                                limit: int = 20) -> List[Dict[str, Any]]:
        """Recherche livres par langue via API"""
        
        print(f"🔍 Recherche livres via API: {languages} (limit: {limit})")
        
        # Construire requête API
        lang_param = ",".join(languages)
        url = f"{self.api_base}/books"
        params = {
            'languages': lang_param,
            'topic': 'fiction',  # Focus sur fiction pour cohérence
            'copyright': 'false',  # Domaine public seulement
            'page_size': limit
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            books = data.get('results', [])
            
            print(f"✅ {len(books)} livres trouvés via API")
            
            # Formater résultats
            formatted_books = []
            for book in books:
                formatted_books.append({
                    'gutenberg_id': str(book['id']),
                    'title': book.get('title', 'Unknown'),
                    'authors': [author['name'] for author in book.get('authors', [])],
                    'languages': book.get('languages', []),
                    'subjects': book.get('subjects', []),
                    'formats': book.get('formats', {}),
                    'download_count': book.get('download_count', 0)
                })
            
            return formatted_books
            
        except Exception as e:
            print(f"❌ Erreur API: {e}")
            return []
    
    def get_available_formats(self, book_info: Dict[str, Any]) -> Dict[str, str]:
        """Extrait formats disponibles depuis les métadonnées API"""
        
        formats = {}
        api_formats = book_info.get('formats', {})
        
        # Mapping formats API → extensions locales
        format_mapping = {
            'text/plain; charset=utf-8': 'txt',
            'text/plain': 'txt',
            'text/html': 'html',
            'application/epub+zip': 'epub',
            'application/pdf': 'pdf',
            'application/x-mobipocket-ebook': 'mobi'
        }
        
        for content_type, url in api_formats.items():
            # Nettoyer content-type (enlever paramètres)
            clean_type = content_type.split(';')[0].strip()
            
            if clean_type in format_mapping:
                ext = format_mapping[clean_type]
                formats[ext] = {
                    'url': url,
                    'content_type': content_type,
                    'local_path': self.output_dir / book_info['gutenberg_id'] / f"{book_info['gutenberg_id']}.{ext}"
                }
        
        return formats
    
    def download_book_formats(self, book_info: Dict[str, Any]) -> Dict[str, Any]:
        """Télécharge formats disponibles d'un livre"""
        
        gutenberg_id = book_info['gutenberg_id']
        title = book_info['title'][:50]  # Tronquer titre long
        
        print(f"📖 {title} (ID: {gutenberg_id})")
        
        # Créer répertoire livre
        book_dir = self.output_dir / gutenberg_id
        book_dir.mkdir(exist_ok=True)
        
        # Récupérer formats disponibles
        formats = self.get_available_formats(book_info)
        downloaded_formats = {}
        
        if not formats:
            print("   ⚠️ Aucun format supporté trouvé")
            return {}
        
        for format_name, format_info in formats.items():
            try:
                print(f"   📄 {format_name}...")
                
                response = requests.get(format_info['url'], timeout=30)
                response.raise_for_status()
                
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
                
                # Pause entre téléchargements
                time.sleep(0.5)
                
            except Exception as e:
                print(f"      ❌ {e}")
                downloaded_formats[format_name] = {
                    'error': str(e),
                    'success': False
                }
        
        return downloaded_formats
    
    def collect_corpus_api(self, languages: List[str] = ["en"], 
                          max_books: int = 20) -> Dict[str, Any]:
        """Collecte corpus via API Gutenberg"""
        
        print(f"🚀 COLLECTE CORPUS GUTENBERG API")
        print(f"=" * 50)
        
        # Rechercher livres via API
        books = self.search_books_by_language(languages, max_books)
        
        if not books:
            print("❌ Aucun livre trouvé via API")
            return {}
        
        corpus_summary = {
            'collection_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'languages': languages,
            'total_books': len(books),
            'successful_downloads': 0,
            'total_formats': 0,
            'books_data': {}
        }
        
        # Trier par popularité (download_count)
        books_sorted = sorted(books, key=lambda x: x.get('download_count', 0), reverse=True)
        
        for book in books_sorted:
            try:
                # Télécharger formats disponibles
                formats = self.download_book_formats(book)
                
                # Statistiques
                successful_formats = sum(1 for f in formats.values() if f.get('success', False))
                
                corpus_summary['books_data'][book['gutenberg_id']] = {
                    'title': book['title'],
                    'authors': book['authors'],
                    'languages': book['languages'],
                    'subjects': book.get('subjects', [])[:3],  # Top 3 sujets
                    'download_count': book.get('download_count', 0),
                    'formats': formats,
                    'successful_formats': successful_formats
                }
                
                if successful_formats > 0:
                    corpus_summary['successful_downloads'] += 1
                    corpus_summary['total_formats'] += successful_formats
                
                print(f"   ✅ {successful_formats} formats téléchargés")
                
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
        
        # Sauvegarder métadonnées
        metadata_file = self.output_dir / 'api_collection_metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(corpus_summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 RÉSUMÉ COLLECTE API:")
        print(f"   📚 Livres collectés: {corpus_summary['successful_downloads']}/{corpus_summary['total_books']}")
        print(f"   📄 Formats total: {corpus_summary['total_formats']}")
        print(f"   🌍 Langues: {', '.join(languages)}")
        print(f"   💾 Métadonnées: {metadata_file}")
        
        return corpus_summary
    
    def find_multilingual_books(self, max_books: int = 10) -> Dict[str, Any]:
        """Trouve livres disponibles en plusieurs langues"""
        
        print("🌍 Recherche livres multilingues...")
        
        # Rechercher par langues différentes
        languages_to_test = [
            ["en"],      # Anglais
            ["fr"],      # Français  
            ["es"],      # Espagnol
            ["de"],      # Allemand
            ["it"],      # Italien
        ]
        
        multilingual_corpus = {
            'collection_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'languages_searched': languages_to_test,
            'books_by_language': {}
        }
        
        for langs in languages_to_test:
            lang_code = langs[0]
            print(f"\n🔍 Recherche en {lang_code}...")
            
            books = self.search_books_by_language(langs, limit=5)  # 5 par langue
            multilingual_corpus['books_by_language'][lang_code] = books
            
            for book in books[:2]:  # Télécharger 2 par langue max
                formats = self.download_book_formats(book)
                print(f"   📖 {book['title'][:30]}...")
        
        # Sauvegarder
        output_file = self.output_dir / 'multilingual_corpus.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(multilingual_corpus, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Corpus multilingue: {output_file}")
        return multilingual_corpus


def main():
    """Test collecteur API Gutenberg"""
    
    print("🏛️ TEST GUTENBERG API COLLECTOR")
    print("=" * 40)
    
    # Créer collecteur API
    collector = GutenbergAPICollector()
    
    # Test collecte standard
    corpus = collector.collect_corpus_api(languages=["en"], max_books=5)
    
    print("\n✅ Test API terminé")


if __name__ == "__main__":
    main()