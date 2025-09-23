#!/usr/bin/env python3
"""
Lecteur Archive Références PaniniFS
Consultation et accès au contenu original archivé
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime

class LecteurArchiveReferences:
    def __init__(self):
        self.references_dir = Path("/home/stephane/GitHub/PaniniFS-Research/panini/references")
        self.cache_dir = self.references_dir / "cache"
        self.db_file = self.references_dir / "references_database.json"
        self.index_file = self.references_dir / "sources_index.json"
        
        self.references_db = None
        self.sources_index = None
        
    def load_archives(self):
        """Charge les archives de références"""
        if not self.db_file.exists():
            print("❌ Base de données références non trouvée")
            return False
            
        with open(self.db_file, 'r', encoding='utf-8') as f:
            self.references_db = json.load(f)
            
        with open(self.index_file, 'r', encoding='utf-8') as f:
            self.sources_index = json.load(f)
            
        print(f"✅ Archive chargée: {self.references_db['total_references']} références")
        return True
        
    def show_archive_summary(self):
        """Affiche résumé archive"""
        if not self.references_db:
            return
            
        print("\n" + "=" * 60)
        print("📚 ARCHIVE RÉFÉRENCES PANINI RESEARCH")
        print("=" * 60)
        print(f"📅 Date création: {self.references_db['creation_date']}")
        print(f"📄 Total références: {self.references_db['total_references']}")
        print(f"💾 Contenu original: {self.references_db['content_preservation']['original_papers_cached']}")
        print(f"🔄 Reproductibilité: {self.references_db['reproducibility_guarantee']}")
        
        print("\n📚 RÉPARTITION PAR SOURCE:")
        for source, refs in self.sources_index.items():
            cached_count = sum(1 for ref in refs if ref['cached'])
            print(f"  {source}: {len(refs)} références ({cached_count} avec contenu)")
            
    def search_references(self, query, source=None, has_content=None):
        """Recherche dans les références"""
        if not self.references_db:
            return []
            
        results = []
        query_lower = query.lower()
        
        for ref in self.references_db['references']:
            # Filtres
            if source and ref['bibliographic_info']['source'] != source:
                continue
                
            if has_content is not None:
                if has_content != ref['cached_content']['has_cached_content']:
                    continue
                    
            # Recherche textuelle
            title = ref['bibliographic_info']['title'].lower()
            abstract = ref['original_paper'].get('abstract', '').lower()
            
            if query_lower in title or query_lower in abstract:
                results.append(ref)
                
        return results
        
    def show_reference_details(self, ref_id):
        """Affiche détails d'une référence"""
        if not self.references_db:
            return
            
        ref = None
        for r in self.references_db['references']:
            if r['reference_id'] == ref_id:
                ref = r
                break
                
        if not ref:
            print(f"❌ Référence {ref_id} non trouvée")
            return
            
        print("\n" + "=" * 60)
        print("📄 DÉTAILS RÉFÉRENCE")
        print("=" * 60)
        print(f"🔗 ID: {ref['reference_id']}")
        print(f"📰 Titre: {ref['bibliographic_info']['title']}")
        print(f"📚 Source: {ref['bibliographic_info']['source']}")
        print(f"🌍 Langue: {ref['bibliographic_info']['language']}")
        print(f"📅 Archivage: {ref['archival_date'][:10]}")
        
        if ref['cached_content']['has_cached_content']:
            print(f"💾 Contenu disponible: {ref['cached_content']['cached_file']}")
        else:
            print("⚠️  Pas de contenu original caché")
            
        print(f"\n📝 Résumé:")
        abstract = ref['original_paper'].get('abstract', 'Pas de résumé disponible')
        print(f"  {abstract[:300]}...")
        
        if ref['urls']['original_url']:
            print(f"\n🔗 URL originale: {ref['urls']['original_url']}")
            
    def open_cached_content(self, ref_id):
        """Ouvre le contenu original caché"""
        if not self.references_db:
            return
            
        ref = None
        for r in self.references_db['references']:
            if r['reference_id'] == ref_id:
                ref = r
                break
                
        if not ref:
            print(f"❌ Référence {ref_id} non trouvée")
            return
            
        if not ref['cached_content']['has_cached_content']:
            print("⚠️  Pas de contenu original disponible")
            return
            
        cached_file = ref['cached_content']['cached_file']
        
        # Ouvre selon le type de fichier
        if cached_file.endswith('.pdf'):
            try:
                subprocess.run(['xdg-open', cached_file], check=True)
                print(f"📖 Ouverture PDF: {cached_file}")
            except:
                print(f"⚠️  Impossible d'ouvrir le PDF. Fichier: {cached_file}")
        elif cached_file.endswith('.html'):
            try:
                subprocess.run(['xdg-open', cached_file], check=True)
                print(f"🌐 Ouverture HTML: {cached_file}")
            except:
                print(f"⚠️  Impossible d'ouvrir le HTML. Fichier: {cached_file}")
        else:
            print(f"📄 Fichier disponible: {cached_file}")
            
    def list_by_source(self, source):
        """Liste références par source"""
        if source not in self.sources_index:
            print(f"❌ Source '{source}' non trouvée")
            print(f"Sources disponibles: {list(self.sources_index.keys())}")
            return
            
        refs = self.sources_index[source]
        print(f"\n📚 RÉFÉRENCES SOURCE '{source}' ({len(refs)} documents)")
        print("-" * 60)
        
        for i, ref in enumerate(refs[:20], 1):  # Limite à 20
            cached_indicator = "💾" if ref['cached'] else "📄"
            title = ref['title'][:60] + "..." if len(ref['title']) > 60 else ref['title']
            print(f"{i:2}. {cached_indicator} {ref['reference_id'][:8]}... {title}")
            
        if len(refs) > 20:
            print(f"... et {len(refs) - 20} autres références")
            
    def interactive_browser(self):
        """Interface interactive de consultation"""
        if not self.load_archives():
            return
            
        self.show_archive_summary()
        
        while True:
            print("\n" + "=" * 60)
            print("🔍 CONSULTEUR ARCHIVE RÉFÉRENCES")
            print("=" * 60)
            print("1. Rechercher références")
            print("2. Lister par source") 
            print("3. Voir détails référence")
            print("4. Ouvrir contenu original")
            print("5. Résumé archive")
            print("6. Quitter")
            
            try:
                choice = input("\nChoix (1-6): ").strip()
                
                if choice == '1':
                    query = input("Terme de recherche: ").strip()
                    if query:
                        results = self.search_references(query)
                        print(f"\n🔍 {len(results)} résultats pour '{query}':")
                        for i, ref in enumerate(results[:10], 1):
                            title = ref['bibliographic_info']['title'][:50] + "..."
                            cached = "💾" if ref['cached_content']['has_cached_content'] else "📄"
                            print(f"{i}. {cached} {ref['reference_id'][:8]}... {title}")
                            
                elif choice == '2':
                    print(f"\nSources disponibles: {list(self.sources_index.keys())}")
                    source = input("Source: ").strip()
                    if source:
                        self.list_by_source(source)
                        
                elif choice == '3':
                    ref_id = input("ID référence: ").strip()
                    if ref_id:
                        self.show_reference_details(ref_id)
                        
                elif choice == '4':
                    ref_id = input("ID référence: ").strip()
                    if ref_id:
                        self.open_cached_content(ref_id)
                        
                elif choice == '5':
                    self.show_archive_summary()
                    
                elif choice == '6':
                    print("👋 Au revoir!")
                    break
                    
                else:
                    print("❌ Choix invalide")
                    
            except KeyboardInterrupt:
                print("\n👋 Au revoir!")
                break
            except Exception as e:
                print(f"❌ Erreur: {e}")

def main():
    lecteur = LecteurArchiveReferences()
    lecteur.interactive_browser()

if __name__ == "__main__":
    main()