#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translator Metadata Database - Base de Métadonnées des Traducteurs
====================================================================

Colliger noms traducteurs chaque corpus pour anticiper style/biais traduction.

Fonctionnalités:
- Base métadonnées traducteurs
- Anticiper style/biais traduction
- Patterns récurrents par traducteur
- Normalisation équivalents sémantiques
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict, Counter
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TranslatorProfile:
    """Profil d'un traducteur - WHO/WHEN/WHERE"""
    translator_id: str
    name: str  # WHO: Nom du traducteur (auteur de sa traduction)
    languages: Set[str]  # Langues de travail
    specializations: List[str]  # Domaines de spécialisation
    era: Optional[str] = None  # WHEN: Époque (ex: "2015", "1950s", "contemporary")
    cultural_context: Optional[str] = None  # WHERE: Contexte culturel (ex: "France, urbain")
    geographical_location: Optional[str] = None  # WHERE: Localisation géographique
    birth_year: Optional[int] = None  # Année de naissance
    works_count: int = 0
    style_markers: Dict[str, float] = field(default_factory=dict)  # Patterns stylistiques
    cultural_biases: Dict[str, str] = field(default_factory=dict)  # Biais culturels
    temporal_biases: Dict[str, str] = field(default_factory=dict)  # Biais temporels
    bias_indicators: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


@dataclass
class TranslationWork:
    """Œuvre traduite"""
    work_id: str
    title: str
    translator_id: str
    source_language: str
    target_language: str
    year: Optional[int] = None
    domain: Optional[str] = None
    quality_score: Optional[float] = None
    metadata: Dict = field(default_factory=dict)


@dataclass
class StylePattern:
    """Pattern de style identifié"""
    pattern_id: str
    translator_id: str
    pattern_type: str  # 'lexical', 'syntactic', 'semantic'
    description: str
    frequency: float
    examples: List[str] = field(default_factory=list)


class TranslatorMetadataDB:
    """Base de données des métadonnées de traducteurs"""
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialisation de la base de données
        
        Args:
            db_path: Chemin vers la base SQLite
        """
        if db_path is None:
            db_path = Path('/home/runner/work/Panini/Panini/data/translator_metadata.db')
        
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialiser la base de données
        self._init_database()
        
        # Cache en mémoire
        self.translators_cache = {}
        self.works_cache = {}
        
        # Statistiques
        self.stats = {
            'total_translators': 0,
            'total_works': 0,
            'total_patterns': 0,
            'languages_covered': set()
        }
        
        self._load_stats()
        
        self.log("📚 Translator Metadata Database initialized")
    
    def _init_database(self):
        """Initialise les tables de la base de données"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Table des traducteurs - WHO/WHEN/WHERE
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS translators (
                    translator_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    languages TEXT,
                    specializations TEXT,
                    era TEXT,
                    cultural_context TEXT,
                    geographical_location TEXT,
                    birth_year INTEGER,
                    works_count INTEGER DEFAULT 0,
                    style_markers TEXT,
                    cultural_biases TEXT,
                    temporal_biases TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Table des œuvres traduites
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS translation_works (
                    work_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    translator_id TEXT NOT NULL,
                    source_language TEXT NOT NULL,
                    target_language TEXT NOT NULL,
                    year INTEGER,
                    domain TEXT,
                    quality_score REAL,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (translator_id) REFERENCES translators(translator_id)
                )
            """)
            
            # Table des patterns de style
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS style_patterns (
                    pattern_id TEXT PRIMARY KEY,
                    translator_id TEXT NOT NULL,
                    pattern_type TEXT NOT NULL,
                    description TEXT,
                    frequency REAL,
                    examples TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (translator_id) REFERENCES translators(translator_id)
                )
            """)
            
            # Table des équivalents sémantiques normalisés
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS semantic_equivalents (
                    equiv_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    translator_id TEXT NOT NULL,
                    source_term TEXT NOT NULL,
                    target_term TEXT NOT NULL,
                    source_language TEXT NOT NULL,
                    target_language TEXT NOT NULL,
                    frequency INTEGER DEFAULT 1,
                    confidence REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (translator_id) REFERENCES translators(translator_id)
                )
            """)
            
            # Index pour performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_works_translator 
                ON translation_works(translator_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_patterns_translator 
                ON style_patterns(translator_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_equiv_translator 
                ON semantic_equivalents(translator_id)
            """)
            
            conn.commit()
        
        self.log("✅ Database initialized")
    
    def add_translator(self, translator_id: str, name: str,
                      languages: List[str],
                      specializations: Optional[List[str]] = None,
                      era: Optional[str] = None,
                      cultural_context: Optional[str] = None,
                      geographical_location: Optional[str] = None,
                      birth_year: Optional[int] = None,
                      style_markers: Optional[Dict[str, float]] = None,
                      cultural_biases: Optional[Dict[str, str]] = None,
                      temporal_biases: Optional[Dict[str, str]] = None,
                      metadata: Optional[Dict] = None) -> TranslatorProfile:
        """
        Ajoute un traducteur à la base - WHO/WHEN/WHERE
        
        Args:
            translator_id: ID unique du traducteur
            name: WHO - Nom du traducteur (auteur de sa traduction)
            languages: Liste des langues de travail
            specializations: Domaines de spécialisation
            era: WHEN - Époque (ex: "2015", "1950s", "contemporary")
            cultural_context: WHERE - Contexte culturel (ex: "France, urbain")
            geographical_location: WHERE - Localisation géographique
            birth_year: Année de naissance
            style_markers: Patterns stylistiques (ex: {'subordinations_complexes': 0.78})
            cultural_biases: Biais culturels (description milieu/vécu)
            temporal_biases: Biais temporels (contexte époque)
            metadata: Métadonnées additionnelles
            
        Returns:
            TranslatorProfile créé
        """
        profile = TranslatorProfile(
            translator_id=translator_id,
            name=name,
            languages=set(languages),
            specializations=specializations or [],
            era=era,
            cultural_context=cultural_context,
            geographical_location=geographical_location,
            birth_year=birth_year,
            style_markers=style_markers or {},
            cultural_biases=cultural_biases or {},
            temporal_biases=temporal_biases or {},
            metadata=metadata or {}
        )
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO translators 
                (translator_id, name, languages, specializations, era, cultural_context,
                 geographical_location, birth_year, style_markers, cultural_biases,
                 temporal_biases, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                translator_id,
                name,
                json.dumps(list(languages)),
                json.dumps(specializations or []),
                era,
                cultural_context,
                geographical_location,
                birth_year,
                json.dumps(style_markers or {}),
                json.dumps(cultural_biases or {}),
                json.dumps(temporal_biases or {}),
                json.dumps(metadata or {})
            ))
            conn.commit()
        
        self.translators_cache[translator_id] = profile
        self.stats['total_translators'] += 1
        self.stats['languages_covered'].update(languages)
        
        context_info = f" ({era or 'unknown era'}, {cultural_context or 'unknown context'})"
        self.log(f"👤 Added translator: {name}{context_info} ({len(languages)} languages)")
        
        return profile
    
    def add_translation_work(self, work_id: str, title: str,
                            translator_id: str,
                            source_language: str,
                            target_language: str,
                            year: Optional[int] = None,
                            domain: Optional[str] = None,
                            quality_score: Optional[float] = None,
                            metadata: Optional[Dict] = None) -> TranslationWork:
        """
        Ajoute une œuvre traduite
        
        Args:
            work_id: ID unique de l'œuvre
            title: Titre de l'œuvre
            translator_id: ID du traducteur
            source_language: Langue source
            target_language: Langue cible
            year: Année de publication
            domain: Domaine (littérature, technique, etc.)
            quality_score: Score de qualité (0-1)
            metadata: Métadonnées additionnelles
            
        Returns:
            TranslationWork créé
        """
        work = TranslationWork(
            work_id=work_id,
            title=title,
            translator_id=translator_id,
            source_language=source_language,
            target_language=target_language,
            year=year,
            domain=domain,
            quality_score=quality_score,
            metadata=metadata or {}
        )
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO translation_works 
                (work_id, title, translator_id, source_language, target_language, 
                 year, domain, quality_score, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                work_id, title, translator_id, source_language, target_language,
                year, domain, quality_score, json.dumps(metadata or {})
            ))
            
            # Mettre à jour le compteur de travaux du traducteur
            cursor.execute("""
                UPDATE translators 
                SET works_count = works_count + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE translator_id = ?
            """, (translator_id,))
            
            conn.commit()
        
        self.works_cache[work_id] = work
        self.stats['total_works'] += 1
        
        self.log(f"📖 Added work: {title} by {translator_id}")
        
        return work
    
    def add_style_pattern(self, pattern_id: str, translator_id: str,
                         pattern_type: str, description: str,
                         frequency: float,
                         examples: Optional[List[str]] = None) -> StylePattern:
        """
        Ajoute un pattern de style identifié
        
        Args:
            pattern_id: ID unique du pattern
            translator_id: ID du traducteur
            pattern_type: Type ('lexical', 'syntactic', 'semantic')
            description: Description du pattern
            frequency: Fréquence d'occurrence
            examples: Exemples du pattern
            
        Returns:
            StylePattern créé
        """
        pattern = StylePattern(
            pattern_id=pattern_id,
            translator_id=translator_id,
            pattern_type=pattern_type,
            description=description,
            frequency=frequency,
            examples=examples or []
        )
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO style_patterns 
                (pattern_id, translator_id, pattern_type, description, frequency, examples)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                pattern_id, translator_id, pattern_type, description, frequency,
                json.dumps(examples or [])
            ))
            conn.commit()
        
        self.stats['total_patterns'] += 1
        
        self.log(f"🎨 Added style pattern: {pattern_id} ({pattern_type})")
        
        return pattern
    
    def add_semantic_equivalent(self, translator_id: str,
                               source_term: str, target_term: str,
                               source_language: str, target_language: str,
                               frequency: int = 1,
                               confidence: float = 1.0):
        """
        Ajoute un équivalent sémantique normalisé
        
        Args:
            translator_id: ID du traducteur
            source_term: Terme source
            target_term: Terme cible
            source_language: Langue source
            target_language: Langue cible
            frequency: Nombre d'occurrences
            confidence: Confiance (0-1)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Vérifier si existe déjà
            cursor.execute("""
                SELECT equiv_id, frequency FROM semantic_equivalents
                WHERE translator_id = ? AND source_term = ? AND target_term = ?
                AND source_language = ? AND target_language = ?
            """, (translator_id, source_term, target_term, source_language, target_language))
            
            existing = cursor.fetchone()
            
            if existing:
                # Mettre à jour fréquence
                cursor.execute("""
                    UPDATE semantic_equivalents
                    SET frequency = frequency + ?
                    WHERE equiv_id = ?
                """, (frequency, existing[0]))
            else:
                # Insérer nouveau
                cursor.execute("""
                    INSERT INTO semantic_equivalents
                    (translator_id, source_term, target_term, source_language, 
                     target_language, frequency, confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (translator_id, source_term, target_term, source_language,
                      target_language, frequency, confidence))
            
            conn.commit()
        
        self.log(f"🔗 Added semantic equivalent: {source_term} → {target_term}")
    
    def get_translator_profile(self, translator_id: str) -> Optional[TranslatorProfile]:
        """Récupère le profil d'un traducteur"""
        if translator_id in self.translators_cache:
            return self.translators_cache[translator_id]
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM translators WHERE translator_id = ?
            """, (translator_id,))
            
            row = cursor.fetchone()
            if row:
                profile = TranslatorProfile(
                    translator_id=row['translator_id'],
                    name=row['name'],
                    languages=set(json.loads(row['languages'])),
                    specializations=json.loads(row['specializations']),
                    era=row.get('era'),
                    cultural_context=row.get('cultural_context'),
                    geographical_location=row.get('geographical_location'),
                    birth_year=row.get('birth_year'),
                    works_count=row['works_count'],
                    style_markers=json.loads(row['style_markers']) if row.get('style_markers') else {},
                    cultural_biases=json.loads(row['cultural_biases']) if row.get('cultural_biases') else {},
                    temporal_biases=json.loads(row['temporal_biases']) if row.get('temporal_biases') else {},
                    metadata=json.loads(row['metadata'])
                )
                self.translators_cache[translator_id] = profile
                return profile
        
        return None
    
    def get_translator_works(self, translator_id: str) -> List[TranslationWork]:
        """Récupère toutes les œuvres d'un traducteur"""
        works = []
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM translation_works WHERE translator_id = ?
                ORDER BY year DESC
            """, (translator_id,))
            
            for row in cursor.fetchall():
                work = TranslationWork(
                    work_id=row['work_id'],
                    title=row['title'],
                    translator_id=row['translator_id'],
                    source_language=row['source_language'],
                    target_language=row['target_language'],
                    year=row['year'],
                    domain=row['domain'],
                    quality_score=row['quality_score'],
                    metadata=json.loads(row['metadata'])
                )
                works.append(work)
        
        return works
    
    def get_translator_style_patterns(self, translator_id: str) -> List[StylePattern]:
        """Récupère les patterns de style d'un traducteur"""
        patterns = []
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM style_patterns WHERE translator_id = ?
                ORDER BY frequency DESC
            """, (translator_id,))
            
            for row in cursor.fetchall():
                pattern = StylePattern(
                    pattern_id=row['pattern_id'],
                    translator_id=row['translator_id'],
                    pattern_type=row['pattern_type'],
                    description=row['description'],
                    frequency=row['frequency'],
                    examples=json.loads(row['examples'])
                )
                patterns.append(pattern)
        
        return patterns
    
    def analyze_translator_bias(self, translator_id: str) -> Dict:
        """
        Analyse les biais potentiels d'un traducteur
        
        Args:
            translator_id: ID du traducteur
            
        Returns:
            Rapport d'analyse des biais
        """
        works = self.get_translator_works(translator_id)
        patterns = self.get_translator_style_patterns(translator_id)
        
        # Analyser la distribution des langues
        lang_pairs = Counter()
        domains = Counter()
        
        for work in works:
            lang_pairs[f"{work.source_language}→{work.target_language}"] += 1
            if work.domain:
                domains[work.domain] += 1
        
        # Analyser patterns de style
        pattern_types = Counter()
        for pattern in patterns:
            pattern_types[pattern.pattern_type] += 1
        
        bias_report = {
            'translator_id': translator_id,
            'total_works': len(works),
            'language_pairs': dict(lang_pairs.most_common()),
            'dominant_pair': lang_pairs.most_common(1)[0] if lang_pairs else None,
            'domains': dict(domains.most_common()),
            'dominant_domain': domains.most_common(1)[0] if domains else None,
            'style_patterns': {
                'total': len(patterns),
                'by_type': dict(pattern_types)
            },
            'bias_indicators': []
        }
        
        # Identifier biais potentiels
        if lang_pairs:
            dominant_count = lang_pairs.most_common(1)[0][1]
            if dominant_count / len(works) > 0.7:
                bias_report['bias_indicators'].append(
                    f"Strong specialization in {lang_pairs.most_common(1)[0][0]} (>70%)"
                )
        
        if domains:
            dominant_domain_count = domains.most_common(1)[0][1]
            if dominant_domain_count / len(works) > 0.6:
                bias_report['bias_indicators'].append(
                    f"Domain specialization in {domains.most_common(1)[0][0]} (>60%)"
                )
        
        return bias_report
    
    def get_translator_context_report(self, translator_id: str) -> Dict:
        """
        Génère rapport contextuel WHO/WHEN/WHERE pour traducteur.
        
        Focus: QUI traduit, QUAND, OÙ, avec quels BIAIS.
        Traducteur = auteur de sa traduction avec interprétation propre.
        
        Args:
            translator_id: ID du traducteur
            
        Returns:
            Rapport contextuel complet
        """
        profile = self.get_translator_profile(translator_id)
        if not profile:
            return {'error': f'Translator {translator_id} not found'}
        
        works = self.get_translator_works(translator_id)
        patterns = self.get_translator_style_patterns(translator_id)
        
        # Construire rapport WHO/WHEN/WHERE
        report = {
            'WHO': {
                'name': profile.name,
                'translator_id': translator_id,
                'role': 'Auteur de sa traduction avec interprétation propre'
            },
            'WHEN': {
                'era': profile.era or 'unknown',
                'birth_year': profile.birth_year,
                'active_years': self._get_active_years(works),
                'temporal_context': 'Contemporary' if not profile.era or 'contemporary' in profile.era.lower() else profile.era
            },
            'WHERE': {
                'cultural_context': profile.cultural_context or 'unknown',
                'geographical_location': profile.geographical_location or 'unknown',
                'cultural_influence': self._analyze_cultural_influence(profile)
            },
            'BIASES': {
                'cultural': profile.cultural_biases,
                'temporal': profile.temporal_biases,
                'detected_indicators': self._detect_bias_patterns(works, patterns)
            },
            'STYLE': {
                'markers': profile.style_markers,
                'patterns': self._summarize_style_patterns(patterns),
                'signature': self._generate_style_signature(profile, patterns)
            },
            'CORPUS': {
                'total_works': len(works),
                'languages': list(profile.languages),
                'specializations': profile.specializations,
                'domains': self._get_work_domains(works)
            },
            'METADATA': {
                'works_count': profile.works_count,
                'style_patterns_count': len(patterns),
                'languages_covered': len(profile.languages)
            }
        }
        
        return report
    
    def _get_active_years(self, works: List[TranslationWork]) -> Dict:
        """Détermine les années d'activité du traducteur"""
        years = [w.year for w in works if w.year]
        if not years:
            return {'first': None, 'last': None, 'span': 0}
        
        return {
            'first': min(years),
            'last': max(years),
            'span': max(years) - min(years) if len(years) > 1 else 0
        }
    
    def _analyze_cultural_influence(self, profile: TranslatorProfile) -> str:
        """Analyse l'influence culturelle basée sur le contexte"""
        if not profile.cultural_context:
            return "unknown"
        
        context = profile.cultural_context.lower()
        influences = []
        
        if 'urban' in context or 'urbain' in context:
            influences.append('urban_perspective')
        if 'rural' in context or 'rural' in context:
            influences.append('rural_perspective')
        if any(country in context for country in ['france', 'uk', 'usa', 'germany']):
            influences.append('western_cultural_lens')
        
        return ', '.join(influences) if influences else profile.cultural_context
    
    def _detect_bias_patterns(self, works: List[TranslationWork], 
                             patterns: List[StylePattern]) -> List[str]:
        """Détecte patterns de biais dans les traductions"""
        bias_patterns = []
        
        # Analyser spécialisation langue
        lang_pairs = Counter()
        for work in works:
            lang_pairs[f"{work.source_language}→{work.target_language}"] += 1
        
        if lang_pairs:
            most_common = lang_pairs.most_common(1)[0]
            if most_common[1] / len(works) > 0.7:
                bias_patterns.append(f"Language pair specialization: {most_common[0]} ({most_common[1]/len(works):.0%})")
        
        # Analyser patterns stylistiques récurrents
        if patterns:
            high_freq_patterns = [p for p in patterns if p.frequency > 0.7]
            if high_freq_patterns:
                bias_patterns.append(f"Strong stylistic signature: {len(high_freq_patterns)} recurring patterns")
        
        return bias_patterns
    
    def _summarize_style_patterns(self, patterns: List[StylePattern]) -> Dict:
        """Résume les patterns stylistiques"""
        by_type = defaultdict(list)
        for pattern in patterns:
            by_type[pattern.pattern_type].append({
                'description': pattern.description,
                'frequency': pattern.frequency
            })
        
        return {ptype: plist for ptype, plist in by_type.items()}
    
    def _generate_style_signature(self, profile: TranslatorProfile, 
                                  patterns: List[StylePattern]) -> str:
        """Génère une signature stylistique du traducteur"""
        signature_elements = []
        
        # Style markers
        if profile.style_markers:
            top_markers = sorted(profile.style_markers.items(), 
                               key=lambda x: x[1], reverse=True)[:3]
            for marker, value in top_markers:
                signature_elements.append(f"{marker}={value:.2f}")
        
        # Pattern types dominants
        if patterns:
            pattern_types = Counter(p.pattern_type for p in patterns)
            dominant = pattern_types.most_common(1)[0]
            signature_elements.append(f"dominant_{dominant[0]}")
        
        return "; ".join(signature_elements) if signature_elements else "neutral"
    
    def _get_work_domains(self, works: List[TranslationWork]) -> Dict:
        """Liste les domaines de travaux"""
        domains = Counter(w.domain for w in works if w.domain)
        return dict(domains.most_common())
    
    def get_semantic_equivalents(self, translator_id: str,
                                language_pair: Optional[Tuple[str, str]] = None) -> List[Dict]:
        """
        Récupère les équivalents sémantiques pour un traducteur
        
        Args:
            translator_id: ID du traducteur
            language_pair: Paire de langues optionnelle (source, target)
            
        Returns:
            Liste des équivalents sémantiques
        """
        equivalents = []
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if language_pair:
                cursor.execute("""
                    SELECT * FROM semantic_equivalents 
                    WHERE translator_id = ? AND source_language = ? AND target_language = ?
                    ORDER BY frequency DESC
                """, (translator_id, language_pair[0], language_pair[1]))
            else:
                cursor.execute("""
                    SELECT * FROM semantic_equivalents 
                    WHERE translator_id = ?
                    ORDER BY frequency DESC
                """, (translator_id,))
            
            for row in cursor.fetchall():
                equivalents.append({
                    'source_term': row['source_term'],
                    'target_term': row['target_term'],
                    'source_language': row['source_language'],
                    'target_language': row['target_language'],
                    'frequency': row['frequency'],
                    'confidence': row['confidence']
                })
        
        return equivalents
    
    def _load_stats(self):
        """Charge les statistiques depuis la base"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM translators")
            self.stats['total_translators'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM translation_works")
            self.stats['total_works'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM style_patterns")
            self.stats['total_patterns'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT DISTINCT languages FROM translators")
            for row in cursor.fetchall():
                if row[0]:
                    self.stats['languages_covered'].update(json.loads(row[0]))
    
    def get_statistics(self) -> Dict:
        """Retourne les statistiques globales"""
        return {
            'total_translators': self.stats['total_translators'],
            'total_works': self.stats['total_works'],
            'total_patterns': self.stats['total_patterns'],
            'languages_covered': len(self.stats['languages_covered']),
            'language_list': sorted(self.stats['languages_covered'])
        }
    
    def export_to_json(self, output_file: Optional[Path] = None) -> Path:
        """Exporte la base complète en JSON"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = Path(f"/home/runner/work/Panini/Panini/results/translator_metadata_{timestamp}.json")
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        export_data = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'statistics': self.get_statistics()
            },
            'translators': [],
            'works': [],
            'patterns': []
        }
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Export translators
            cursor.execute("SELECT * FROM translators")
            for row in cursor.fetchall():
                export_data['translators'].append(dict(row))
            
            # Export works
            cursor.execute("SELECT * FROM translation_works")
            for row in cursor.fetchall():
                export_data['works'].append(dict(row))
            
            # Export patterns
            cursor.execute("SELECT * FROM style_patterns")
            for row in cursor.fetchall():
                export_data['patterns'].append(dict(row))
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        self.log(f"💾 Database exported to {output_file}")
        return output_file
    
    def log(self, message: str):
        """Log avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")


def main():
    """Example usage and testing"""
    print("📚 TRANSLATOR METADATA DATABASE")
    print("=" * 60)
    
    db = TranslatorMetadataDB()
    
    # Example: Add translators
    db.add_translator(
        translator_id='translator_001',
        name='Marie Dupont',
        languages=['fr', 'en', 'de'],
        specializations=['literature', 'philosophy'],
        metadata={'birth_year': 1965, 'country': 'France'}
    )
    
    db.add_translator(
        translator_id='translator_002',
        name='John Smith',
        languages=['en', 'fr', 'es'],
        specializations=['technical', 'scientific'],
        metadata={'birth_year': 1970, 'country': 'UK'}
    )
    
    # Example: Add translation works
    db.add_translation_work(
        work_id='work_001',
        title='Le Petit Prince (EN)',
        translator_id='translator_001',
        source_language='fr',
        target_language='en',
        year=1943,
        domain='literature',
        quality_score=0.95
    )
    
    db.add_translation_work(
        work_id='work_002',
        title='The Little Prince (ES)',
        translator_id='translator_002',
        source_language='en',
        target_language='es',
        year=1945,
        domain='literature',
        quality_score=0.88
    )
    
    # Example: Add style patterns
    db.add_style_pattern(
        pattern_id='pattern_001',
        translator_id='translator_001',
        pattern_type='lexical',
        description='Prefers "child" over "kid"',
        frequency=0.85,
        examples=['the child walked', 'a young child']
    )
    
    # Example: Add semantic equivalents
    db.add_semantic_equivalent(
        translator_id='translator_001',
        source_term='enfant',
        target_term='child',
        source_language='fr',
        target_language='en',
        frequency=25,
        confidence=0.98
    )
    
    # Analyze bias
    bias_report = db.analyze_translator_bias('translator_001')
    print(f"\n📊 Bias Analysis for translator_001:")
    print(f"  Total works: {bias_report['total_works']}")
    print(f"  Dominant pair: {bias_report['dominant_pair']}")
    print(f"  Bias indicators: {len(bias_report['bias_indicators'])}")
    
    # Statistics
    stats = db.get_statistics()
    print(f"\n📈 DATABASE STATISTICS:")
    print(f"  Total translators: {stats['total_translators']}")
    print(f"  Total works: {stats['total_works']}")
    print(f"  Total patterns: {stats['total_patterns']}")
    print(f"  Languages covered: {stats['languages_covered']}")
    
    # Export
    export_path = db.export_to_json()
    print(f"\n✅ Database exported to: {export_path}")
    
    return 0


if __name__ == "__main__":
    main()
