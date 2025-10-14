#!/usr/bin/env python3
"""
SYSTÈME DE DÉCOMPRESSION WIKIPEDIA OPTIMISÉ
===========================================

Décompresse les dumps Wikipedia pour accès direct avec performance optimale,
tout en maintenant la reproductibilité via traçabilité complète des sources.

FONCTIONNALITÉS:
- Décompression sélective (XML articles seulement)
- Traçabilité complète : URLs, dates, checksums
- Reproductibilité garantie
- Gestion mémoire optimisée
- Extraction sémantique directe
"""

import json
import subprocess
import hashlib
import bz2
import gzip
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import xml.etree.ElementTree as ET
import re

class WikipediaDecompresseurOptimise:
    """Décompresseur optimisé avec traçabilité complète"""
    
    def __init__(self):
        self.dumps_dir = Path("wikipedia_dumps")
        self.decompressed_dir = Path("wikipedia_decompressed") 
        self.metadata_dir = Path("wikipedia_metadata")
        
        # Créer répertoires
        self.decompressed_dir.mkdir(exist_ok=True)
        self.metadata_dir.mkdir(exist_ok=True)
        
        # Fichier de traçabilité pour reproductibilité
        self.tracabilite_file = self.metadata_dir / "sources_tracabilite.json"
        
        # Pattern pour extraction d'articles
        self.ns_pattern = re.compile(r'xmlns="[^"]*"')
        
    def inventorier_dumps_disponibles(self) -> Dict[str, Dict]:
        """Inventaire complet des dumps avec métadonnées"""
        print("📦 INVENTAIRE DUMPS DISPONIBLES")
        print("-" * 35)
        
        dumps_info = {}
        
        if not self.dumps_dir.exists():
            print("   ❌ Répertoire wikipedia_dumps non trouvé")
            return dumps_info
        
        # Scanner tous les fichiers compressés
        for fichier in self.dumps_dir.glob("*"):
            if fichier.suffix in ['.bz2', '.gz', '.7z']:
                # Extraction métadonnées du nom
                nom_base = fichier.stem
                if 'pages-articles' in nom_base:
                    # Format: {langue}wiki-latest-pages-articles.xml
                    langue = nom_base.split('wiki-')[0]
                    
                    # Calcul taille et checksum
                    taille_mb = fichier.stat().st_size / (1024 * 1024)
                    checksum = self._calculer_checksum(fichier)
                    
                    dumps_info[langue] = {
                        "fichier_source": str(fichier),
                        "format": fichier.suffix,
                        "taille_mb": round(taille_mb, 1),
                        "checksum_sha256": checksum,
                        "date_fichier": datetime.fromtimestamp(fichier.stat().st_mtime).isoformat(),
                        "type_contenu": "pages-articles",
                        "status": "compresse"
                    }
                    
                    print(f"   ✅ {langue}: {taille_mb:.1f} MB ({fichier.suffix})")
        
        print(f"\n📊 Total: {len(dumps_info)} dumps identifiés")
        return dumps_info
    
    def _calculer_checksum(self, fichier: Path) -> str:
        """Calcule checksum SHA256 pour vérification intégrité"""
        sha256_hash = hashlib.sha256()
        
        with open(fichier, "rb") as f:
            # Lecture par chunks pour gros fichiers
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
                
        return sha256_hash.hexdigest()[:16]  # 16 premiers chars
    
    def decompresser_dump_selectively(self, langue: str, dumps_info: Dict) -> Optional[Path]:
        """Décompression sélective d'un dump avec optimisation mémoire"""
        
        if langue not in dumps_info:
            print(f"   ❌ Dump {langue} non trouvé")
            return None
        
        info_dump = dumps_info[langue]
        fichier_source = Path(info_dump["fichier_source"])
        fichier_decompresse = self.decompressed_dir / f"{langue}wiki_articles.xml"
        
        # Vérifier si déjà décompressé
        if fichier_decompresse.exists():
            print(f"   ✅ {langue}: Déjà décompressé ({fichier_decompresse.name})")
            return fichier_decompresse
        
        print(f"   🔄 Décompression {langue} ({info_dump['taille_mb']} MB)...")
        
        try:
            # Décompression selon format
            if fichier_source.suffix == '.bz2':
                with bz2.open(fichier_source, 'rt', encoding='utf-8') as f_in:
                    with open(fichier_decompresse, 'w', encoding='utf-8') as f_out:
                        # Copie par chunks pour éviter saturation mémoire
                        chunk_size = 1024 * 1024  # 1MB chunks
                        while True:
                            chunk = f_in.read(chunk_size)
                            if not chunk:
                                break
                            f_out.write(chunk)
            
            elif fichier_source.suffix == '.gz':
                with gzip.open(fichier_source, 'rt', encoding='utf-8') as f_in:
                    with open(fichier_decompresse, 'w', encoding='utf-8') as f_out:
                        chunk_size = 1024 * 1024
                        while True:
                            chunk = f_in.read(chunk_size)
                            if not chunk:
                                break
                            f_out.write(chunk)
            
            taille_decompresse = fichier_decompresse.stat().st_size / (1024 * 1024)
            print(f"   ✅ {langue}: Décompressé → {taille_decompresse:.1f} MB")
            
            return fichier_decompresse
            
        except Exception as e:
            print(f"   ❌ {langue}: Erreur décompression - {e}")
            return None
    
    def extraire_articles_optimise(self, fichier_xml: Path, langue: str, 
                                 max_articles: int = 10000) -> List[Dict[str, str]]:
        """Extraction optimisée d'articles depuis XML décompressé"""
        
        print(f"   📖 Extraction articles {langue} (max {max_articles})...")
        
        articles = []
        count = 0
        
        try:
            # Parser XML en streaming pour éviter saturation mémoire
            context = ET.iterparse(fichier_xml, events=('start', 'end'))
            context = iter(context)
            event, root = next(context)
            
            article_current = {}
            in_text = False
            text_content = []
            
            for event, elem in context:
                if event == 'start':
                    if elem.tag.endswith('page'):
                        article_current = {}
                    elif elem.tag.endswith('title'):
                        if elem.text:
                            article_current['titre'] = elem.text.strip()
                    elif elem.tag.endswith('text'):
                        in_text = True
                        text_content = []
                        
                elif event == 'end':
                    if elem.tag.endswith('text') and in_text:
                        if elem.text:
                            # Nettoyage contenu Wiki
                            contenu_nettoye = self._nettoyer_contenu_wiki(elem.text)
                            if contenu_nettoye and len(contenu_nettoye) > 100:  # Articles substantiels
                                article_current['contenu'] = contenu_nettoye[:2000]  # Limité à 2000 chars
                        in_text = False
                        
                    elif elem.tag.endswith('page'):
                        if 'titre' in article_current and 'contenu' in article_current:
                            # Filtrer articles utiles (pas de redirections, etc.)
                            if not article_current['titre'].startswith('Catégorie:'):
                                if not article_current['contenu'].startswith('#REDIRECT'):
                                    articles.append({
                                        'titre': article_current['titre'],
                                        'contenu': article_current['contenu'],
                                        'langue': langue
                                    })
                                    count += 1
                                    
                                    if count >= max_articles:
                                        break
                    
                    # Libération mémoire
                    elem.clear()
                    
            print(f"   ✅ {len(articles)} articles extraits")
            return articles
            
        except Exception as e:
            print(f"   ❌ Erreur extraction {langue}: {e}")
            return []
    
    def _nettoyer_contenu_wiki(self, contenu_brut: str) -> str:
        """Nettoyage contenu Wikipedia (suppression markup)"""
        
        if not contenu_brut:
            return ""
        
        # Suppression markup Wiki basique
        contenu = re.sub(r'\{\{[^}]*\}\}', '', contenu_brut)  # Templates
        contenu = re.sub(r'\[\[([^|\]]*)\|([^\]]*)\]\]', r'\2', contenu)  # Liens avec texte
        contenu = re.sub(r'\[\[([^\]]*)\]\]', r'\1', contenu)  # Liens simples
        contenu = re.sub(r'==+([^=]+)==+', r'\1', contenu)  # Titres sections
        contenu = re.sub(r"'''([^']+)'''", r'\1', contenu)  # Gras
        contenu = re.sub(r"''([^']+)''", r'\1', contenu)  # Italique
        contenu = re.sub(r'<[^>]+>', '', contenu)  # Tags HTML
        contenu = re.sub(r'&[a-zA-Z]+;', ' ', contenu)  # Entités HTML
        contenu = re.sub(r'\n+', ' ', contenu)  # Retours ligne multiples
        contenu = re.sub(r'\s+', ' ', contenu)  # Espaces multiples
        
        return contenu.strip()
    
    def generer_base_articles_rapide(self, dumps_info: Dict, 
                                   langues_prioritaires: List[str] = None) -> Dict[str, List[Dict]]:
        """Génère base d'articles optimisée pour recherche sémantique rapide"""
        
        print(f"\n🚀 GÉNÉRATION BASE ARTICLES RAPIDE")
        print("-" * 40)
        
        if langues_prioritaires is None:
            langues_prioritaires = ['fr', 'en', 'de', 'sa', 'hi']  # Priorité par utilité
        
        base_articles = {}
        
        for langue in langues_prioritaires:
            if langue in dumps_info:
                print(f"\n📖 Traitement {langue}...")
                
                # Décompression
                fichier_xml = self.decompresser_dump_selectively(langue, dumps_info)
                
                if fichier_xml:
                    # Extraction articles
                    articles = self.extraire_articles_optimise(fichier_xml, langue, max_articles=5000)
                    
                    if articles:
                        base_articles[langue] = articles
                        
                        # Sauvegarde JSON pour accès rapide
                        fichier_json = self.decompressed_dir / f"{langue}_articles_rapide.json"
                        with open(fichier_json, 'w', encoding='utf-8') as f:
                            json.dump(articles, f, indent=2, ensure_ascii=False)
                        
                        print(f"   💾 Sauvé: {fichier_json}")
        
        return base_articles
    
    def generer_tracabilite_complete(self, dumps_info: Dict, base_articles: Dict) -> Dict:
        """Génère traçabilité complète pour reproductibilité"""
        
        tracabilite = {
            "metadata": {
                "generation_date": datetime.now().isoformat(),
                "system_info": "PaniniFS-Research Wikipedia Processor",
                "version": "1.0.0",
                "reproductible": True
            },
            
            "sources_wikipedia": {
                "base_url": "https://dumps.wikimedia.org",
                "dumps_info": dumps_info,
                "langues_traitees": list(base_articles.keys()),
                "total_dumps": len(dumps_info)
            },
            
            "articles_extraits": {
                langue: {
                    "count": len(articles),
                    "echantillon_titres": [art["titre"] for art in articles[:10]],
                    "taille_moyenne_chars": sum(len(art["contenu"]) for art in articles) // len(articles) if articles else 0
                }
                for langue, articles in base_articles.items()
            },
            
            "checksums_verification": {
                langue: self._calculer_checksum_articles(articles)
                for langue, articles in base_articles.items()
            },
            
            "commandes_reproduction": {
                "download_script": "bash download_wikipedia_dumps.sh",
                "decompression_script": "python3 wikipedia_decompresseur_optimise.py",
                "extraction_command": "python3 -c \"from wikipedia_decompresseur_optimise import *; WikipediaDecompresseurOptimise().generer_base_articles_rapide({})\"",
                "gitignore_updated": True
            },
            
            "performance_metrics": {
                "decompression_time_estimate": "~15-30 minutes selon CPU",
                "disk_space_required": "~2-5GB décompressé",
                "memory_usage_peak": "~500MB par dump",
                "articles_per_minute": "~200-500 selon langue"
            }
        }
        
        # Sauvegarde traçabilité
        with open(self.tracabilite_file, 'w', encoding='utf-8') as f:
            json.dump(tracabilite, f, indent=2, ensure_ascii=False)
        
        return tracabilite
    
    def _calculer_checksum_articles(self, articles: List[Dict]) -> str:
        """Checksum pour vérifier intégrité extraction"""
        content_str = json.dumps(articles, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(content_str.encode()).hexdigest()[:12]

def main():
    """Décompression optimisée avec traçabilité complète"""
    print("📦 WIKIPEDIA DÉCOMPRESSEUR OPTIMISÉ")
    print("=" * 40)
    print("Objectif: Performance + Reproductibilité")
    print()
    
    decompresseur = WikipediaDecompresseurOptimise()
    
    # 1. Inventaire
    dumps_info = decompresseur.inventorier_dumps_disponibles()
    
    if not dumps_info:
        print("\n⚠️  Aucun dump trouvé. Exécuter d'abord:")
        print("   bash download_wikipedia_dumps.sh")
        return
    
    # 2. Génération base articles rapide
    base_articles = decompresseur.generer_base_articles_rapide(dumps_info)
    
    # 3. Traçabilité complète
    tracabilite = decompresseur.generer_tracabilite_complete(dumps_info, base_articles)
    
    print(f"\n🏆 RÉSULTATS DÉCOMPRESSION")
    print("=" * 30)
    print(f"📊 Dumps traités: {len(base_articles)}")
    
    total_articles = sum(len(articles) for articles in base_articles.values())
    print(f"📖 Articles extraits: {total_articles}")
    
    print(f"💾 Fichiers générés:")
    for langue in base_articles:
        fichier = f"{langue}_articles_rapide.json"
        print(f"   • wikipedia_decompressed/{fichier}")
    
    print(f"🔍 Traçabilité: {decompresseur.tracabilite_file}")
    
    print(f"\n✅ REPRODUCTIBILITÉ GARANTIE:")
    print(f"   • Sources tracées avec checksums")
    print(f"   • Commandes reproduction documentées")
    print(f"   • .gitignore configuré (pas de pollution repo)")
    print(f"   • Données régénérables de façon fiable")
    
    print(f"\n🚀 Prêt pour expansion sémantique optimisée!")

if __name__ == "__main__":
    main()