#!/usr/bin/env python3
"""
DÉCOMPRESSEUR ET ANALYSEUR WIKIPEDIA POUR PANLANG
=================================================

Décompresse et analyse tous les dumps Wikipedia pour créer PanLang,
la langue érudite universelle qui infuse toute la connaissance humaine.

PanLang forge une intuition correcte pour son époque en intégrant :
- Racines dhātu sanskrites originelles
- Classifications taxonomiques exhaustives
- Concepts scientifiques multilingues
- Sagesse culturelle pan-mondiale
"""

import bz2
import gzip
import xml.etree.ElementTree as ET
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
import concurrent.futures
import time
from dataclasses import dataclass, asdict
import sqlite3

@dataclass
class ConceptPrimitive:
    """Primitive conceptuelle extraite de Wikipedia"""
    terme_original: str
    langue_source: str
    domaine: str
    hierarchie: List[str]
    proprietes: Dict[str, str]
    racines_etymologiques: List[str]
    certitude_score: float
    occurrences_multilingues: Dict[str, str]

class PanLangWikipediaProcessor:
    """Processeur pour créer PanLang à partir de Wikipedia"""
    
    def __init__(self, dumps_dir: str = "wikipedia_dumps"):
        self.dumps_dir = Path(dumps_dir)
        self.output_dir = Path("panlang_primitives")
        self.output_dir.mkdir(exist_ok=True)
        
        # Base de données pour primitives
        self.db_path = self.output_dir / "panlang_primitives.db"
        self.init_database()
        
        # Patterns d'extraction
        self.extraction_patterns = self._init_extraction_patterns()
        
        # Statistiques
        self.stats = {
            "files_processed": 0,
            "primitives_extracted": 0,
            "languages_covered": set(),
            "domains_covered": set()
        }
    
    def init_database(self):
        """Initialise la base de données SQLite pour les primitives"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS primitives (
            id INTEGER PRIMARY KEY,
            terme_original TEXT,
            langue_source TEXT,
            domaine TEXT,
            hierarchie TEXT,  -- JSON
            proprietes TEXT,  -- JSON
            racines_etymologiques TEXT,  -- JSON
            certitude_score REAL,
            occurrences_multilingues TEXT,  -- JSON
            date_extraction TEXT
        )
        """)
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_domaine ON primitives(domaine)
        """)
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_langue ON primitives(langue_source)
        """)
        
        conn.commit()
        conn.close()
    
    def _init_extraction_patterns(self) -> Dict[str, Dict]:
        """Patterns d'extraction par domaine et par langue"""
        return {
            # BIOLOGIE - Taxonomies universelles
            "taxonomie": {
                "patterns": [
                    r"\{\{Taxobox",
                    r"\{\{Infobox.*biolog",  
                    r"regne\s*=\s*([^|\n]+)",
                    r"kingdom\s*=\s*([^|\n]+)",
                    r"класс\s*=\s*([^|\n]+)",  # Russe
                    r"界\s*=\s*([^|\n]+)",      # Chinois
                ],
                "hierarchie": ["regne", "embranchement", "classe", "ordre", "famille", "genre", "espece"]
            },
            
            # LINGUISTIQUE - Racines étymologiques
            "etymologie": {
                "patterns": [
                    r"étymologie.*?([A-Za-z\u0900-\u097F\u0100-\u017F]+)",  # Sanskrit/Latin
                    r"racine.*?([A-Za-z\u0900-\u097F]+)",
                    r"धातु.*?([^\s]+)",  # Dhātu sanskrit
                    r"root.*?([A-Za-z]+)",
                    r"词根.*?([^。]+)",    # Chinois
                ],
                "langues_anciennes": ["sa", "la", "el", "ar"]
            },
            
            # CHIMIE - Formules et propriétés
            "chimie": {
                "patterns": [
                    r"formule.*?([A-Z][a-z]*[0-9]*)",
                    r"formula.*?([A-Z][a-z]*[0-9]*)",
                    r"masse.*molaire.*?([0-9]+\.?[0-9]*)",
                    r"化学式.*?([A-Z][a-z0-9]+)",  # Chinois
                ],
                "proprietes": ["masse_molaire", "point_fusion", "point_ebullition", "densite"]
            },
            
            # GÉOGRAPHIE - Localisation hiérarchique
            "geographie": {
                "patterns": [
                    r"pays\s*=\s*([^|\n]+)",
                    r"country\s*=\s*([^|\n]+)",
                    r"continent\s*=\s*([^|\n]+)",
                    r"координаты\s*=\s*([^|\n]+)",  # Russe
                ],
                "hierarchie": ["continent", "pays", "region", "ville"]
            }
        }
    
    def decompress_files(self) -> Dict[str, List[Path]]:
        """Décompresse tous les fichiers Wikipedia"""
        print("🗜️  DÉCOMPRESSION DES ARCHIVES WIKIPEDIA")
        print("=" * 50)
        
        decompressed = {"xml": [], "sql": []}
        
        for compressed_file in self.dumps_dir.glob("*.bz2"):
            print(f"📦 Décompression: {compressed_file.name}")
            decompressed_path = compressed_file.with_suffix('')
            
            if not decompressed_path.exists():
                with bz2.open(compressed_file, 'rb') as src, \
                     open(decompressed_path, 'wb') as dst:
                    dst.write(src.read())
            
            if decompressed_path.suffix == '.xml':
                decompressed["xml"].append(decompressed_path)
            
        for compressed_file in self.dumps_dir.glob("*.gz"):
            print(f"📦 Décompression: {compressed_file.name}")
            decompressed_path = compressed_file.with_suffix('')
            
            if not decompressed_path.exists():
                with gzip.open(compressed_file, 'rb') as src, \
                     open(decompressed_path, 'wb') as dst:
                    dst.write(src.read())
            
            if decompressed_path.suffix == '.sql':
                decompressed["sql"].append(decompressed_path)
                
        print(f"✅ Décompressé: {len(decompressed['xml'])} XML + {len(decompressed['sql'])} SQL")
        return decompressed
    
    def extract_sanskrit_dhatus(self, sanskrit_xml: Path) -> List[ConceptPrimitive]:
        """Extrait les racines dhātu du Sanskrit - PRIORITÉ ABSOLUE"""
        print("🕉️  EXTRACTION RACINES DHĀTU SANSKRITES")
        print("-" * 40)
        
        dhatus = []
        
        try:
            # Parser XML progressif pour gros fichiers
            context = ET.iterparse(sanskrit_xml, events=('start', 'end'))
            context = iter(context)
            event, root = next(context)
            
            page_count = 0
            dhatu_count = 0
            
            for event, elem in context:
                if event == 'end' and elem.tag.endswith('page'):
                    title = elem.find('.//title')
                    text = elem.find('.//text')
                    
                    if title is not None and text is not None:
                        title_text = title.text or ""
                        content = text.text or ""
                        
                        # Détection dhātu
                        if any(marker in content.lower() for marker in 
                               ['धातु', 'dhatu', 'racine', 'root', 'verb']):
                            
                            # Extraction patterns dhātu
                            dhatu_matches = re.findall(
                                r'धातु[:\s]*([^\s\n।]+)', content, re.IGNORECASE
                            )
                            
                            for dhatu_root in dhatu_matches:
                                primitive = ConceptPrimitive(
                                    terme_original=dhatu_root,
                                    langue_source="sa",
                                    domaine="etymologie_dhatu",
                                    hierarchie=["racine", "verbale", "sanskrit"],
                                    proprietes={
                                        "source_title": title_text,
                                        "context": content[:200] + "..."
                                    },
                                    racines_etymologiques=[dhatu_root],
                                    certitude_score=0.9,
                                    occurrences_multilingues={"sa": dhatu_root}
                                )
                                dhatus.append(primitive)
                                dhatu_count += 1
                        
                        page_count += 1
                        if page_count % 100 == 0:
                            print(f"   📄 {page_count} pages, {dhatu_count} dhātu trouvés")
                    
                    # Libération mémoire
                    elem.clear()
                    
        except ET.ParseError as e:
            print(f"⚠️  Erreur parsing XML: {e}")
        
        print(f"✅ Extraits: {dhatu_count} racines dhātu")
        return dhatus
    
    def extract_taxonomies(self, xml_files: List[Path]) -> List[ConceptPrimitive]:
        """Extrait les taxonomies biologiques multilingues"""
        print("🧬 EXTRACTION TAXONOMIES BIOLOGIQUES")
        print("-" * 40)
        
        taxonomies = []
        
        for xml_file in xml_files:
            lang = xml_file.name[:2]  # Code langue
            print(f"   🔍 Langue: {lang}")
            
            # Extraction rapide par regex pour démo
            try:
                with open(xml_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content_sample = f.read(10000000)  # 10MB échantillon
                    
                # Recherche Taxobox
                taxobox_matches = re.finditer(
                    r'\{\{Taxobox.*?(?=\{\{|\n\n)', 
                    content_sample, re.DOTALL | re.IGNORECASE
                )
                
                for match in list(taxobox_matches)[:50]:  # Limite pour démo
                    taxobox = match.group(0)
                    
                    # Extraction hiérarchie
                    regne = re.search(r'regne\s*=\s*([^|\n]+)', taxobox, re.IGNORECASE)
                    classe = re.search(r'classe\s*=\s*([^|\n]+)', taxobox, re.IGNORECASE)
                    
                    if regne and classe:
                        primitive = ConceptPrimitive(
                            terme_original=regne.group(1).strip(),
                            langue_source=lang,
                            domaine="taxonomie",
                            hierarchie=["regne", regne.group(1).strip(), classe.group(1).strip()],
                            proprietes={"source": "taxobox"},
                            racines_etymologiques=[],
                            certitude_score=0.8,
                            occurrences_multilingues={lang: regne.group(1)}
                        )
                        taxonomies.append(primitive)
                        
            except Exception as e:
                print(f"⚠️  Erreur {xml_file.name}: {e}")
                
        return taxonomies
    
    def save_primitives(self, primitives: List[ConceptPrimitive]):
        """Sauvegarde les primitives dans la base de données"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for primitive in primitives:
            cursor.execute("""
            INSERT INTO primitives (
                terme_original, langue_source, domaine, hierarchie,
                proprietes, racines_etymologiques, certitude_score,
                occurrences_multilingues, date_extraction
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """, (
                primitive.terme_original,
                primitive.langue_source, 
                primitive.domaine,
                json.dumps(primitive.hierarchie),
                json.dumps(primitive.proprietes),
                json.dumps(primitive.racines_etymologiques),
                primitive.certitude_score,
                json.dumps(primitive.occurrences_multilingues)
            ))
        
        conn.commit()
        conn.close()
        
        print(f"💾 Sauvegardé: {len(primitives)} primitives")
    
    def generate_panlang_report(self) -> Dict:
        """Génère le rapport PanLang"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Statistiques par domaine
        cursor.execute("""
        SELECT domaine, COUNT(*), AVG(certitude_score)
        FROM primitives GROUP BY domaine
        """)
        domaines = cursor.fetchall()
        
        # Statistiques par langue
        cursor.execute("""
        SELECT langue_source, COUNT(*)
        FROM primitives GROUP BY langue_source
        """)
        langues = cursor.fetchall()
        
        conn.close()
        
        rapport = {
            "titre": "PANLANG - Langue Érudite Universelle",
            "description": "Primitives extraites de Wikipedia multilingue pour forge d'intuition correcte",
            "domaines": {domaine: {"count": count, "certitude_moy": round(cert, 3)} 
                        for domaine, count, cert in domaines},
            "langues": {lang: count for lang, count in langues},
            "total_primitives": sum(count for _, count in langues),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Sauvegarde rapport
        with open(self.output_dir / "panlang_report.json", "w", encoding="utf-8") as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
            
        return rapport

def main():
    """Fonction principale - Création de PanLang"""
    print("🌍 CRÉATION PANLANG - LANGUE ÉRUDITE UNIVERSELLE")
    print("=" * 60)
    print("Vision: Infuser toute la connaissance humaine")
    print("Objectif: Forger une intuition correcte pour l'époque")
    print()
    
    processor = PanLangWikipediaProcessor()
    
    # 1. Décompression
    files = processor.decompress_files()
    
    # 2. Extraction prioritaire Sanskrit (dhātu)
    sanskrit_files = [f for f in files["xml"] if "sawiki" in f.name]
    if sanskrit_files:
        dhatus = processor.extract_sanskrit_dhatus(sanskrit_files[0])
        processor.save_primitives(dhatus)
        print(f"✅ Racines dhātu intégrées: {len(dhatus)}")
    
    # 3. Extraction taxonomies multilingues
    other_xml = [f for f in files["xml"] if "sawiki" not in f.name]
    if other_xml:
        taxonomies = processor.extract_taxonomies(other_xml[:3])  # 3 langues pour démo
        processor.save_primitives(taxonomies)
        print(f"✅ Taxonomies intégrées: {len(taxonomies)}")
    
    # 4. Rapport final
    rapport = processor.generate_panlang_report()
    
    print("\n📊 RAPPORT PANLANG")
    print("-" * 20)
    print(f"📚 Total primitives: {rapport['total_primitives']}")
    print(f"🌐 Langues couvertes: {len(rapport['langues'])}")
    print(f"🔬 Domaines: {len(rapport['domaines'])}")
    
    for domaine, stats in rapport["domaines"].items():
        print(f"   {domaine}: {stats['count']} primitives (certitude: {stats['certitude_moy']})")
    
    print(f"\n💾 Base de données: {processor.db_path}")
    print(f"📄 Rapport complet: {processor.output_dir}/panlang_report.json")
    print("\n🎯 PanLang - Fondations établies pour la langue érudite universelle!")

if __name__ == "__main__":
    main()