#!/usr/bin/env python3
"""
ANALYSEUR DE DUMPS WIKIPEDIA POUR PRIMITIVES UNIVERSELLES
=========================================================

Analyse les dumps Wikipedia multilingues pour extraire les systèmes de 
classification et construire une base de primitives universelles.

Intégration avec encyclopedie_compositionnelle_universelle.py
"""

import requests
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import gzip
import bz2
from typing import Dict, List, Set, Tuple
import re
from dataclasses import dataclass
from datetime import datetime
import urllib.parse

@dataclass
class WikipediaSource:
    """Source Wikipedia avec métadonnées"""
    language: str
    language_name: str
    dump_url: str
    categories_file: str
    pages_file: str
    size_mb: float
    last_updated: str
    priority: int  # 1=élevée, 3=faible

class WikipediaDumpAnalyzer:
    """Analyseur des dumps Wikipedia pour extraction de primitives"""
    
    def __init__(self):
        self.base_url = "https://dumps.wikimedia.org"
        self.sources = self._initialize_sources()
        self.classification_patterns = self._initialize_patterns()
        self.output_dir = Path("wikipedia_classifications")
        self.output_dir.mkdir(exist_ok=True)
        
    def _initialize_sources(self) -> List[WikipediaSource]:
        """Initialise les sources Wikipedia pour PanLang érudite universelle"""
        return [
            # LANGUES FONDATRICES - Racines anciennes
            WikipediaSource(
                language="sa", language_name="Sanskrit", dump_url="sawiki",
                categories_file="sawiki-latest-category.sql.gz",
                pages_file="sawiki-latest-pages-articles.xml.bz2", 
                size_mb=45, last_updated="2024", priority=1  # Dhātu originels
            ),
            WikipediaSource(
                language="la", language_name="Latin", dump_url="lawiki",
                categories_file="lawiki-latest-category.sql.gz",
                pages_file="lawiki-latest-pages-articles.xml.bz2",
                size_mb=180, last_updated="2024", priority=1  # Racines européennes
            ),
            WikipediaSource(
                language="el", language_name="Grec", dump_url="elwiki",
                categories_file="elwiki-latest-category.sql.gz", 
                pages_file="elwiki-latest-pages-articles.xml.bz2",
                size_mb=420, last_updated="2024", priority=1  # Science antique
            ),
            WikipediaSource(
                language="ar", language_name="Arabe", dump_url="arwiki",
                categories_file="arwiki-latest-category.sql.gz",
                pages_file="arwiki-latest-pages-articles.xml.bz2",
                size_mb=1200, last_updated="2024", priority=1  # Sciences médiévales
            ),
            
            # LANGUES MODERNES EXHAUSTIVES
            WikipediaSource(
                language="en", language_name="English", dump_url="enwiki",
                categories_file="enwiki-latest-category.sql.gz", 
                pages_file="enwiki-latest-pages-articles.xml.bz2",
                size_mb=19000, last_updated="2024", priority=1  # Plus exhaustif
            ),
            WikipediaSource(
                language="fr", language_name="Français", dump_url="frwiki",
                categories_file="frwiki-latest-category.sql.gz",
                pages_file="frwiki-latest-pages-articles.xml.bz2",
                size_mb=2800, last_updated="2024", priority=1  # Classifications française
            ),
            WikipediaSource(
                language="de", language_name="Deutsch", dump_url="dewiki", 
                categories_file="dewiki-latest-category.sql.gz",
                pages_file="dewiki-latest-pages-articles.xml.bz2",
                size_mb=5200, last_updated="2024", priority=1  # Précision germanique
            ),
            WikipediaSource(
                language="ru", language_name="Русский", dump_url="ruwiki",
                categories_file="ruwiki-latest-category.sql.gz",
                pages_file="ruwiki-latest-pages-articles.xml.bz2", 
                size_mb=3100, last_updated="2024", priority=1  # Sciences slaves
            ),
            WikipediaSource(
                language="es", language_name="Español", dump_url="eswiki",
                categories_file="eswiki-latest-category.sql.gz",
                pages_file="eswiki-latest-pages-articles.xml.bz2",
                size_mb=4200, last_updated="2024", priority=1  # Monde ibérique
            ),
            WikipediaSource(
                language="it", language_name="Italiano", dump_url="itwiki",
                categories_file="itwiki-latest-category.sql.gz", 
                pages_file="itwiki-latest-pages-articles.xml.bz2",
                size_mb=1800, last_updated="2024", priority=1  # Renaissance italienne
            ),
            
            # LANGUES ASIATIQUES ÉRUDITES
            WikipediaSource(
                language="zh", language_name="中文", dump_url="zhwiki",
                categories_file="zhwiki-latest-category.sql.gz",
                pages_file="zhwiki-latest-pages-articles.xml.bz2",
                size_mb=2400, last_updated="2024", priority=1  # Sagesse chinoise
            ),
            WikipediaSource(
                language="ja", language_name="日本語", dump_url="jawiki",
                categories_file="jawiki-latest-category.sql.gz",
                pages_file="jawiki-latest-pages-articles.xml.bz2", 
                size_mb=3200, last_updated="2024", priority=1  # Précision japonaise
            ),
            WikipediaSource(
                language="hi", language_name="हिन्दी", dump_url="hiwiki",
                categories_file="hiwiki-latest-category.sql.gz",
                pages_file="hiwiki-latest-pages-articles.xml.bz2",
                size_mb=520, last_updated="2024", priority=1  # Continuité sanskrite
            )
        ]
        
    def _initialize_patterns(self) -> Dict[str, List[str]]:
        """Patterns de classification à rechercher dans Wikipedia"""
        return {
            # Biologie et taxonomie
            "taxonomie": [
                r"\{\{Taxobox",
                r"\{\{Infobox.*biolog",
                r"Catégorie:.*taxonomie",
                r"Category:.*taxonomy",
                r"regne\s*=",
                r"kingdom\s*=", 
                r"classe\s*=",
                r"class\s*=",
                r"ordre\s*=", 
                r"order\s*="
            ],
            
            # Chimie 
            "chimie": [
                r"\{\{Infobox.*chimi",
                r"\{\{Chembox",
                r"Catégorie:.*chimique", 
                r"Category:.*chemical",
                r"formule.*=",
                r"formula.*=",
                r"masse.*molaire", 
                r"molecular.*weight"
            ],
            
            # Géographie
            "geographie": [
                r"\{\{Infobox.*pays",
                r"\{\{Infobox.*ville", 
                r"\{\{Infobox.*country",
                r"\{\{Infobox.*city",
                r"Catégorie:.*géograph",
                r"Category:.*geography",
                r"continent\s*=",
                r"coordonnées\s*=",
                r"coordinates\s*="
            ],
            
            # Langues et linguistique
            "linguistique": [
                r"\{\{Infobox.*langue",
                r"\{\{Infobox.*language", 
                r"Catégorie:.*langue",
                r"Category:.*language",
                r"famille\s*=",
                r"family\s*=",
                r"ISO.*639",
                r"racine\s*=",
                r"root\s*="
            ],
            
            # Mathématiques
            "mathematiques": [
                r"\{\{Infobox.*math",
                r"Catégorie:.*mathém",
                r"Category:.*mathemat", 
                r"théorème",
                r"theorem",
                r"équation",
                r"equation"
            ],
            
            # Couleurs (extension du système HSL)
            "couleurs": [
                r"Catégorie:.*couleur",
                r"Category:.*color",
                r"RGB\s*=",
                r"HSL\s*=", 
                r"teinte\s*=",
                r"hue\s*=",
                r"saturation\s*=",
                r"luminosité\s*=",
                r"brightness\s*="
            ]
        }
        
    def analyze_available_dumps(self) -> Dict[str, any]:
        """Analyse les dumps Wikipedia disponibles"""
        print("🔍 ANALYSE DES DUMPS WIKIPEDIA DISPONIBLES")
        print("=" * 60)
        
        analysis = {
            "sources_prioritaires": [],
            "taille_totale_gb": 0,
            "langues_disponibles": [],
            "recommandations": []
        }
        
        for source in self.sources:
            print(f"\n📊 {source.language_name} ({source.language})")
            print(f"   📂 URL: {self.base_url}/{source.dump_url}/")
            print(f"   📏 Taille: {source.size_mb} MB")
            print(f"   ⭐ Priorité: {source.priority}/3")
            print(f"   📋 Catégories: {source.categories_file}")
            print(f"   📄 Articles: {source.pages_file}")
            
            if source.priority <= 2:
                analysis["sources_prioritaires"].append({
                    "langue": source.language,
                    "nom": source.language_name,
                    "taille_mb": source.size_mb,
                    "priorite": source.priority
                })
                
            analysis["taille_totale_gb"] += source.size_mb / 1000
            analysis["langues_disponibles"].append(source.language)
            
        # Recommandations
        analysis["recommandations"] = [
            "Commencer par Sanskrit (45 MB) - essentiel pour dhātu",
            "Français (2.8 GB) - classifications complètes", 
            "Anglais (19 GB) - plus exhaustif mais volumineux",
            "Télécharger les catégories d'abord (.sql.gz)",
            "Parser les infoboxes pour primitives structurées"
        ]
        
        print(f"\n✅ RÉSUMÉ:")
        print(f"   📊 {len(analysis['sources_prioritaires'])} sources prioritaires")
        print(f"   💾 {analysis['taille_totale_gb']:.1f} GB total")
        print(f"   🌐 {len(analysis['langues_disponibles'])} langues")
        
        return analysis
        
    def get_dump_urls(self, language: str) -> Dict[str, str]:
        """Obtient les URLs de téléchargement pour une langue"""
        source = next((s for s in self.sources if s.language == language), None)
        if not source:
            return {}
            
        base = f"{self.base_url}/{source.dump_url}/latest/"
        return {
            "categories": base + source.categories_file,
            "pages": base + source.pages_file,
            "base_url": base
        }
        
    def estimate_classification_density(self, language: str) -> Dict[str, int]:
        """Estime la densité de classifications par domaine"""
        estimates = {
            "fr": {
                "taxonomie": 45000,
                "chimie": 8000, 
                "geographie": 35000,
                "linguistique": 12000,
                "mathematiques": 15000,
                "couleurs": 500
            },
            "en": {
                "taxonomie": 180000,
                "chimie": 25000,
                "geographie": 120000, 
                "linguistique": 35000,
                "mathematiques": 45000,
                "couleurs": 1500
            },
            "sa": {
                "taxonomie": 200,
                "chimie": 50,
                "geographie": 800,
                "linguistique": 2000,  # Racines dhātu
                "mathematiques": 300,
                "couleurs": 100
            },
            "de": {
                "taxonomie": 65000,
                "chimie": 12000,
                "geographie": 45000,
                "linguistique": 18000, 
                "mathematiques": 22000,
                "couleurs": 800
            }
        }
        
        return estimates.get(language, {})
        
    def create_download_script(self, languages: List[str] = None) -> str:
        """Génère un script de téléchargement"""
        if not languages:
            languages = ["sa", "fr"]  # Commencer petit
            
        script_lines = [
            "#!/bin/bash",
            "# Script de téléchargement Wikipedia dumps", 
            "# Généré automatiquement",
            "",
            "mkdir -p wikipedia_dumps",
            "cd wikipedia_dumps", 
            ""
        ]
        
        total_size = 0
        for lang in languages:
            urls = self.get_dump_urls(lang)
            if urls:
                source = next(s for s in self.sources if s.language == lang)
                script_lines.extend([
                    f"# {source.language_name} ({source.size_mb} MB)",
                    f"echo 'Téléchargement {source.language_name}...'",
                    f"wget -c '{urls['categories']}'",
                    f"wget -c '{urls['pages']}'", 
                    ""
                ])
                total_size += source.size_mb
                
        script_lines.extend([
            f"echo 'Téléchargement terminé - {total_size} MB'",
            "ls -lah"
        ])
        
        script_content = "\n".join(script_lines)
        
        script_path = "download_wikipedia_dumps.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
            
        import os
        os.chmod(script_path, 0o755)
        
        return script_path
        
    def demonstrate_classification_extraction(self):
        """Démontre l'extraction de classifications (simulation)"""
        print("\n🔬 DÉMONSTRATION EXTRACTION DE CLASSIFICATIONS")
        print("=" * 60)
        
        # Simulation avec des exemples réels de Wikipedia
        examples = {
            "taxonomie": {
                "Chat domestique": {
                    "regne": "Animalia",
                    "embranchement": "Chordata", 
                    "classe": "Mammalia",
                    "ordre": "Carnivora",
                    "famille": "Felidae",
                    "genre": "Felis",
                    "espece": "Felis catus"
                }
            },
            "chimie": {
                "Eau": {
                    "formule": "H2O",
                    "masse_molaire": "18.015 g/mol",
                    "point_fusion": "0°C", 
                    "point_ebullition": "100°C",
                    "densite": "1 g/cm³"
                }
            },
            "geographie": {
                "Paris": {
                    "pays": "France",
                    "region": "Île-de-France", 
                    "continent": "Europe",
                    "coordonnees": "48.8566°N, 2.3522°E",
                    "population": "2161000"
                }
            }
        }
        
        for domaine, concepts in examples.items():
            print(f"\n📋 {domaine.upper()}")
            print("-" * 40)
            for concept, proprietes in concepts.items():
                print(f"🔍 {concept}:")
                for prop, valeur in proprietes.items():
                    print(f"   {prop}: {valeur}")
                    
        print("\n✅ Ces structures serviront de primitives universelles")
        print("   pour enrichir l'encyclopédie compositionnelle")

def main():
    """Fonction principale"""
    print("🌟 ANALYSEUR DUMPS WIKIPEDIA - PRIMITIVES UNIVERSELLES")
    print("=" * 70)
    
    analyzer = WikipediaDumpAnalyzer()
    
    # Analyse des dumps disponibles
    analysis = analyzer.analyze_available_dumps()
    
    # Sauvegarde de l'analyse
    with open("wikipedia_dumps_analysis.json", "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
        
    print(f"\n📄 Analyse sauvegardée: wikipedia_dumps_analysis.json")
    
    # Génération du script de téléchargement
    script_path = analyzer.create_download_script(["sa", "fr"])
    print(f"📜 Script généré: {script_path}")
    
    # Démonstration
    analyzer.demonstrate_classification_extraction()
    
    print("\n🎯 PROCHAINES ÉTAPES:")
    print("1. Exécuter ./download_wikipedia_dumps.sh")
    print("2. Parser les catégories et infoboxes") 
    print("3. Extraire les primitives taxonomiques")
    print("4. Intégrer à encyclopedie_compositionnelle_universelle.py")
    print("5. Tester reconstruction cross-linguistique")

if __name__ == "__main__":
    main()