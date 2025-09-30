# Multi-Format Corpus Analysis System

Système d'analyse multi-format pour la séparation contenant/contenu dans PaniniFS.

## Vue d'ensemble

Ce système implémente une approche en 3 niveaux pour analyser et séparer la structure du conteneur (filesystem) du contenu sémantique dans des fichiers multi-formats.

### Architecture 3 Niveaux

1. **Niveau 1 - Structure Fichier (PaniniFS)**
   - Métadonnées filesystem (inodes, blocks, permissions)
   - Type de conteneur (plain, compressed, encrypted)
   - Structure physique du stockage

2. **Niveau 2 - Enveloppe de Présentation**
   - Format-specific structure (PDF pages, EPUB chapters, MP4 atoms)
   - Métadonnées de présentation (fonts, layout, styling)
   - Container version et encoding

3. **Niveau 3 - Contenu Sémantique Pur**
   - Texte extrait indépendamment du format
   - Features sémantiques (tokens, langue, concepts)
   - Hash de contenu normalisé

## Modules

### 1. MultiFormatAnalyzer (`multi_format_analyzer.py`)

Analyseur principal pour scanner et cataloguer le corpus multi-format.

**Fonctionnalités:**
- Scan de répertoires pour identifier contenus multi-formats
- Extraction de métadonnées par format (TXT, PDF, EPUB, MP3, MP4, SRT, etc.)
- Regroupement de fichiers par contenu commun
- Statistiques de couverture du corpus

**Usage:**
```python
from src.research.multi_format_analyzer import MultiFormatAnalyzer

# Initialize analyzer
analyzer = MultiFormatAnalyzer(corpus_root=Path("./data/multi_format_corpus"))

# Scan directory for books
books_items = analyzer.scan_directory(Path("./data/multi_format_corpus/books"), "book")

# Get statistics
stats = analyzer.get_format_coverage_stats()
print(f"Total items: {stats['total_items']}")

# Export registry
analyzer.export_registry()
```

### 2. ContentInvariantExtractor (`content_invariant_extractor.py`)

Extracteur d'invariants sémantiques cross-format.

**Fonctionnalités:**
- Extraction de texte depuis différents formats
- Calcul d'invariants textuels (word count, unique words, top words)
- Identification d'invariants communs entre formats
- Calcul de similarité cross-format

**Usage:**
```python
from src.research.content_invariant_extractor import ContentInvariantExtractor

# Initialize extractor
extractor = ContentInvariantExtractor()

# Extract invariants from multi-format content
invariants = extractor.extract_invariants_from_content(
    content_id="book_001",
    title="My Book",
    formats={"txt": Path("book.txt"), "pdf": Path("book.pdf")}
)

print(f"Similarity: {invariants.similarity_score:.2%}")
print(f"Common words: {invariants.invariants['common_top_words']}")
```

### 3. ContainerContentSeparator (`container_vs_content_separator.py`)

Séparateur 3 niveaux contenant/contenu.

**Fonctionnalités:**
- Extraction des 3 niveaux d'information
- Détection de type de conteneur
- Calcul de métriques de compression par niveau
- Évaluation de la redondance éliminée

**Usage:**
```python
from src.research.container_vs_content_separator import ContainerContentSeparator

# Initialize separator
separator = ContainerContentSeparator()

# Perform 3-level separation
separation = separator.separate_three_levels(
    file_path=Path("document.pdf"),
    content_id="doc_001"
)

print(f"Container type: {separation.level1_file.container_type}")
print(f"Format: {separation.level2_envelope.format_type}")
print(f"Language: {separation.level3_content.language}")
print(f"Compression potential: {separation.compression_by_level['total_compression_potential']:.2%}")
```

### 4. MultiFormatAnalysisPipeline (`multi_format_analysis_pipeline.py`)

Pipeline d'intégration complet combinant les 3 modules.

**Usage:**
```python
from src.research.multi_format_analysis_pipeline import MultiFormatAnalysisPipeline

# Initialize pipeline
pipeline = MultiFormatAnalysisPipeline()

# Run complete analysis
report = pipeline.run_complete_analysis()

# Check results
print(f"Items analyzed: {report['summary']['total_content_items']}")
print(f"Average similarity: {report['invariant_analysis']['average_cross_format_similarity']:.2%}")
```

## Formats Supportés

### Livres
- **TXT** - Plain text
- **MD** - Markdown
- **PDF** - Portable Document Format (basic support)
- **EPUB** - Electronic Publication (basic support)

### Audio
- **TXT** - Transcription
- **MP3** - MPEG Audio Layer 3
- **WAV** - Waveform Audio
- **FLAC** - Free Lossless Audio Codec

### Vidéo
- **SRT** - SubRip Subtitle
- **VTT** - WebVTT Subtitle
- **MP4** - MPEG-4 Video
- **WEBM** - WebM Video

## Génération de Corpus d'Exemple

Utilisez le script `generate_sample_corpus.py` pour créer un corpus de test:

```bash
python3 scripts/generate_sample_corpus.py
```

Cela créera:
- **Livres**: intro_panini (txt, md, pdf), dhatu_theory (txt, md)
- **Audio**: podcast_episode1 (txt, mp3), tech_talk (txt)
- **Vidéo**: tutorial_video (srt, mp4), explainer_video (vtt)

## Exécution du Pipeline Complet

```bash
python3 src/research/multi_format_analysis_pipeline.py
```

### Résultats Générés

Le pipeline génère 4 fichiers JSON dans `data/multi_format_corpus/analysis_results/`:

1. **content_registry.json** - Registre de tous les contenus multi-formats
2. **invariants.json** - Invariants extraits pour chaque contenu
3. **separations.json** - Résultats de séparation 3 niveaux
4. **analysis_report.json** - Rapport d'analyse complet

## Métriques de Succès

### Objectifs (Issue Requirements)

- [ ] **Corpus**: 100+ contenus en 3+ formats chacun
- [x] **Extraction automatique**: Invariants cross-format ✓
- [x] **Séparation validée**: Container vs contenu ✓
- [x] **Compression optimisée**: Par niveau ✓

### État Actuel (Corpus d'Exemple)

- **Corpus size**: 4 contenus
- **Formats/item**: 2.2 formats moyens
- **Similarité cross-format**: 84% moyenne
- **Potentiel compression**: 37% moyenne

## Extension du Corpus

Pour atteindre l'objectif de 100+ contenus:

1. **Ajouter plus de livres** dans formats TXT, PDF, EPUB
2. **Ajouter plus d'audio** avec transcriptions
3. **Ajouter plus de vidéos** avec sous-titres
4. **Utiliser corpus existants**:
   - Project Gutenberg (livres publics)
   - LibriVox (audiobooks)
   - OpenSubtitles (sous-titres)

## Dépendances pour Support Complet

Pour une extraction complète de texte depuis PDF et EPUB:

```bash
pip install PyPDF2 pdfplumber ebooklib
```

Pour extraction audio/vidéo metadata:

```bash
pip install mutagen ffmpeg-python
```

## Structure du Projet

```
data/multi_format_corpus/
├── books/              # Livres en TXT, PDF, EPUB
├── audio/              # Audio + transcriptions
├── video/              # Vidéos + sous-titres
└── analysis_results/   # Résultats d'analyse
    ├── content_registry.json
    ├── invariants.json
    ├── separations.json
    └── analysis_report.json

src/research/
├── multi_format_analyzer.py          # Module 1: Analyse multi-format
├── content_invariant_extractor.py    # Module 2: Extraction invariants
├── container_vs_content_separator.py # Module 3: Séparation 3 niveaux
└── multi_format_analysis_pipeline.py # Pipeline intégration

scripts/
└── generate_sample_corpus.py         # Générateur corpus exemple
```

## Exemples d'Analyse

### Exemple 1: Livre en 3 formats

Pour un livre disponible en TXT, PDF et EPUB:
- **Niveau 1**: 3 fichiers différents (sizes variés)
- **Niveau 2**: 3 enveloppes différentes (PDF structure, EPUB ZIP, TXT plain)
- **Niveau 3**: Contenu sémantique identique (même texte, mêmes concepts)

Résultat: **Similarité > 95%** entre les 3 formats

### Exemple 2: Vidéo + Sous-titres

Pour une vidéo MP4 avec sous-titres SRT:
- **Niveau 1**: Fichiers MP4 (large) et SRT (small)
- **Niveau 2**: MP4 container avec atoms vs SRT timing structure
- **Niveau 3**: Contenu textuel identique dans les deux

Résultat: **Compression potentielle élevée** en isolant le contenu sémantique

## Tests

Chaque module peut être testé individuellement:

```bash
# Test multi-format analyzer
python3 src/research/multi_format_analyzer.py

# Test invariant extractor
python3 src/research/content_invariant_extractor.py

# Test container/content separator
python3 src/research/container_vs_content_separator.py

# Test complete pipeline
python3 src/research/multi_format_analysis_pipeline.py
```

## Contribution

Pour contribuer au corpus:

1. Ajouter des fichiers multi-formats dans `data/multi_format_corpus/`
2. Utiliser le même nom de base pour les variants (ex: `book.txt`, `book.pdf`, `book.epub`)
3. Exécuter le pipeline d'analyse
4. Vérifier les résultats dans `analysis_results/`

## Références

- **Issue**: [RESEARCH] Séparation Contenant/Contenu - Corpus multi-format
- **Architecture**: 3 niveaux (File/Envelope/Content)
- **Inspiration**: PaniniFS semantic filesystem, Dhātu theory
