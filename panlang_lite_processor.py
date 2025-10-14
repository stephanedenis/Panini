#!/usr/bin/env python3
"""
PANLANG LITE - EXTRACTEUR RAPIDE DE PRIMITIVES
==============================================

Version optimisée pour extraire les primitives essentielles
sans décompresser tous les gros fichiers en même temps.
"""

import bz2
import gzip
import json
import re
from pathlib import Path
from typing import Dict, List
import sqlite3
import time

class PanLangLiteProcessor:
    """Processeur léger pour PanLang"""
    
    def __init__(self, dumps_dir: str = "wikipedia_dumps"):
        self.dumps_dir = Path(dumps_dir)
        self.output_dir = Path("panlang_primitives")
        self.output_dir.mkdir(exist_ok=True)
        
        self.db_path = self.output_dir / "panlang_primitives.db"
        self.init_database()
        
    def init_database(self):
        """Initialise la base de données SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS primitives (
            id INTEGER PRIMARY KEY,
            terme_original TEXT,
            langue_source TEXT,
            domaine TEXT,
            contexte TEXT,
            certitude_score REAL,
            extraction_date TEXT
        )
        """)
        
        conn.commit()
        conn.close()
    
    def extract_sanskrit_dhatus_compressed(self) -> List[Dict]:
        """Extrait dhātu directement du fichier compressé"""
        print("🕉️  EXTRACTION DHĀTU SANSKRIT (sans décompression)")
        print("-" * 50)
        
        sanskrit_file = self.dumps_dir / "sawiki-latest-pages-articles.xml.bz2"
        dhatus = []
        
        if not sanskrit_file.exists():
            print("❌ Fichier Sanskrit non trouvé")
            return dhatus
            
        try:
            with bz2.open(sanskrit_file, 'rt', encoding='utf-8', errors='ignore') as f:
                chunk_size = 1000000  # 1MB par chunk
                chunk_count = 0
                dhatu_patterns = [
                    r'धातु[:\s]*([^\s\n।]+)',
                    r'dhatu[:\s]*([a-zA-Z]+)',
                    r'verb.*root[:\s]*([a-zA-Z]+)'
                ]
                
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                        
                    chunk_count += 1
                    
                    # Recherche dhātu dans le chunk
                    for pattern in dhatu_patterns:
                        matches = re.findall(pattern, chunk, re.IGNORECASE)
                        for match in matches:
                            if len(match.strip()) > 1:  # Éviter les faux positifs
                                dhatu = {
                                    "terme": match.strip(),
                                    "langue": "sa",
                                    "domaine": "dhatu_racine",
                                    "contexte": f"Sanskrit chunk {chunk_count}",
                                    "certitude": 0.9
                                }
                                dhatus.append(dhatu)
                    
                    if chunk_count % 10 == 0:
                        print(f"   📄 Chunk {chunk_count}, dhātu trouvés: {len(dhatus)}")
                    
                    # Limite pour éviter saturation mémoire
                    if chunk_count > 100 or len(dhatus) > 500:
                        break
                        
        except Exception as e:
            print(f"⚠️  Erreur extraction Sanskrit: {e}")
            
        print(f"✅ Dhātu extraits: {len(dhatus)}")
        return dhatus
    
    def extract_french_taxonomies_compressed(self) -> List[Dict]:
        """Extrait taxonomies françaises du fichier compressé"""
        print("🇫🇷 EXTRACTION TAXONOMIES FRANÇAISES")
        print("-" * 40)
        
        french_file = self.dumps_dir / "frwiki-latest-pages-articles.xml.bz2"
        taxonomies = []
        
        if not french_file.exists():
            print("❌ Fichier Français non trouvé")
            return taxonomies
            
        try:
            with bz2.open(french_file, 'rt', encoding='utf-8', errors='ignore') as f:
                chunk_size = 2000000  # 2MB par chunk
                chunk_count = 0
                
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                        
                    chunk_count += 1
                    
                    # Recherche Taxobox
                    taxobox_matches = re.finditer(
                        r'\{\{Taxobox.*?règne\s*=\s*([^|\n}]+).*?classe\s*=\s*([^|\n}]+)', 
                        chunk, re.DOTALL | re.IGNORECASE
                    )
                    
                    for match in taxobox_matches:
                        regne = match.group(1).strip()
                        classe = match.group(2).strip()
                        
                        if regne and classe:
                            taxonomie = {
                                "terme": f"{regne}→{classe}",
                                "langue": "fr",
                                "domaine": "taxonomie_biologique",
                                "contexte": f"Règne: {regne}, Classe: {classe}",
                                "certitude": 0.8
                            }
                            taxonomies.append(taxonomie)
                    
                    if chunk_count % 5 == 0:
                        print(f"   📄 Chunk {chunk_count}, taxonomies: {len(taxonomies)}")
                    
                    # Limite
                    if chunk_count > 50 or len(taxonomies) > 200:
                        break
                        
        except Exception as e:
            print(f"⚠️  Erreur extraction Français: {e}")
            
        print(f"✅ Taxonomies extraites: {len(taxonomies)}")
        return taxonomies
    
    def extract_english_concepts_compressed(self) -> List[Dict]:
        """Extrait concepts anglais essentiels"""
        print("🇺🇸 EXTRACTION CONCEPTS ANGLAIS")
        print("-" * 35)
        
        english_file = self.dumps_dir / "enwiki-latest-pages-articles.xml.bz2"
        concepts = []
        
        if not english_file.exists():
            print("❌ Fichier Anglais non trouvé")
            return concepts
            
        try:
            with bz2.open(english_file, 'rt', encoding='utf-8', errors='ignore') as f:
                chunk_size = 3000000  # 3MB par chunk
                chunk_count = 0
                
                patterns = [
                    (r'etymology.*?from\s+([A-Za-z]+)', "etymologie"),
                    (r'chemical\s+formula.*?([A-Z][a-z]*[0-9]*)', "chimie"),
                    (r'kingdom\s*=\s*([^|\n}]+)', "biologie")
                ]
                
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                        
                    chunk_count += 1
                    
                    for pattern, domaine in patterns:
                        matches = re.findall(pattern, chunk, re.IGNORECASE)
                        for match in matches[:10]:  # Limite par chunk
                            concept = {
                                "terme": match.strip(),
                                "langue": "en", 
                                "domaine": domaine,
                                "contexte": f"English {domaine} chunk {chunk_count}",
                                "certitude": 0.7
                            }
                            concepts.append(concept)
                    
                    if chunk_count % 10 == 0:
                        print(f"   📄 Chunk {chunk_count}, concepts: {len(concepts)}")
                    
                    # Limite pour éviter surcharge
                    if chunk_count > 30 or len(concepts) > 300:
                        break
                        
        except Exception as e:
            print(f"⚠️  Erreur extraction Anglais: {e}")
            
        print(f"✅ Concepts extraits: {len(concepts)}")
        return concepts
    
    def save_all_primitives(self, primitives_lists: List[List[Dict]]):
        """Sauvegarde toutes les primitives"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        total_saved = 0
        for primitives in primitives_lists:
            for primitive in primitives:
                cursor.execute("""
                INSERT INTO primitives (terme_original, langue_source, domaine, contexte, certitude_score, extraction_date)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    primitive["terme"],
                    primitive["langue"],
                    primitive["domaine"], 
                    primitive["contexte"],
                    primitive["certitude"],
                    time.strftime("%Y-%m-%d %H:%M:%S")
                ))
                total_saved += 1
        
        conn.commit()
        conn.close()
        
        print(f"💾 Sauvegardé: {total_saved} primitives totales")
        return total_saved
    
    def generate_panlang_lite_report(self) -> Dict:
        """Génère le rapport PanLang Lite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Statistiques
        cursor.execute("SELECT COUNT(*) FROM primitives")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT domaine, COUNT(*) FROM primitives GROUP BY domaine")
        domaines = dict(cursor.fetchall())
        
        cursor.execute("SELECT langue_source, COUNT(*) FROM primitives GROUP BY langue_source")
        langues = dict(cursor.fetchall())
        
        conn.close()
        
        rapport = {
            "titre": "PanLang Lite - Primitives Essentielles",
            "description": "Extraction rapide des primitives fondamentales",
            "total_primitives": total,
            "domaines": domaines,
            "langues": langues,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "base_donnees": str(self.db_path)
        }
        
        # Sauvegarde
        with open(self.output_dir / "panlang_lite_report.json", "w", encoding="utf-8") as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
            
        return rapport

def main():
    """Création PanLang Lite - Version optimisée"""
    print("🚀 PANLANG LITE - EXTRACTION RAPIDE DE PRIMITIVES")
    print("=" * 55)
    print("Approche: Extraction directe sur fichiers compressés")
    print("Objectif: Primitives essentielles sans décompression massive")
    print()
    
    processor = PanLangLiteProcessor()
    
    # Extraction par langue (sans décompresser tout)
    primitives_all = []
    
    # 1. Sanskrit - Priorité absolue (racines dhātu)
    dhatus = processor.extract_sanskrit_dhatus_compressed()
    primitives_all.append(dhatus)
    
    # 2. Français - Classifications taxonomiques
    taxonomies_fr = processor.extract_french_taxonomies_compressed()
    primitives_all.append(taxonomies_fr)
    
    # 3. Anglais - Concepts scientifiques
    concepts_en = processor.extract_english_concepts_compressed()
    primitives_all.append(concepts_en)
    
    # Sauvegarde
    total_primitives = processor.save_all_primitives(primitives_all)
    
    # Rapport final
    rapport = processor.generate_panlang_lite_report()
    
    print("\n📊 RAPPORT PANLANG LITE")
    print("=" * 25)
    print(f"🌟 Total primitives: {rapport['total_primitives']}")
    print(f"🌐 Langues: {list(rapport['langues'].keys())}")
    print(f"🔬 Domaines: {list(rapport['domaines'].keys())}")
    print()
    
    for domaine, count in rapport["domaines"].items():
        print(f"   📋 {domaine}: {count} primitives")
    
    for langue, count in rapport["langues"].items():
        print(f"   🌍 {langue}: {count} termes")
    
    print(f"\n💾 Base de données: {rapport['base_donnees']}")
    print(f"📄 Rapport: {processor.output_dir}/panlang_lite_report.json")
    print("\n🎯 PanLang Lite - Fondations établies pour la langue érudite!")
    print("   → Racines sanskrites dhātu intégrées")
    print("   → Taxonomies biologiques françaises") 
    print("   → Concepts scientifiques anglais")
    print("   → Base solide pour développement PanLang complet")

if __name__ == "__main__":
    main()