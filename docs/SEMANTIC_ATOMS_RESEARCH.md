# Semantic Atoms Research - Module Documentation

## Overview

This package provides four core modules for researching universal semantic atoms through multilingual analysis, following the progressive approach outlined in the research plan.

**Key Principle**: Dhātu as initial hypothesis, NOT final answer. Extension and modification based on empirical validation.

## ⚠️ Critical Updates (CLARIFICATIONS_MISSION_CRITIQUE.md)

### 🧬 NEW PARADIGM: Symmetry-Based Validation
**FOCUS**: Pure semantic representation through perfect symmetries
- Model discovers perfect symmetries (composition ↔ decomposition)
- Validation: `compose(decompose(x)) == x`
- NOT limited to language or binary data
- Universal information theory approach

### 👥 NEW PARADIGM: WHO/WHEN/WHERE Translator Metadata
**FOCUS**: Traducteur = auteur with own interpretation (NOT just counter)
- WHO: Translator identity (author of translation)
- WHEN: Era, temporal context
- WHERE: Cultural context, geographical location
- BIASES: Cultural and temporal biases
- STYLE: Patterns and signature

## Modules

### 1. semantic_atoms_discovery.py

**Purpose**: Discover universal semantic atoms through multilingual corpus analysis.

**Features**:
- Initialize with dhātu as starting hypothesis (9 core + extensions)
- Analyze texts for atom detection across languages
- Discover new atoms through pattern frequency
- Validate atoms through compression metrics
- **NEW: Validate atoms through symmetry (compose ↔ decompose)**
- **NEW: Score universal candidates (symmetry + recurrence + generality)**
- Track atom evolution and statistics

**Example Usage**:
```python
from src.research.semantic_atoms_discovery import SemanticAtomsDiscovery

discovery = SemanticAtomsDiscovery()

# Analyze text
atoms = discovery.analyze_text_for_atoms(
    "L'enfant joue dans le jardin",
    language='fr',
    source='children_story'
)

# Discover new atoms
new_atoms = discovery.discover_new_atoms(
    texts=[{'text': '...', 'language': 'fr', 'source': '...'}],
    min_frequency=5,
    min_languages=3
)

# Validate by compression
metrics = discovery.validate_atom_by_compression(
    'EXIST',
    corpus_texts=[...]
)

# NEW: Validate by symmetry (compose ↔ decompose)
symmetry_score = discovery.validate_atom_symmetry(
    'EXIST',
    corpus_texts=[...],
    test_iterations=10
)

# NEW: Score universal candidate
universal_score = discovery.score_universal_candidate('EXIST')
# Returns score based on:
#   - Symmetry (40%): compose(decompose(x)) == x
#   - Recurrence (30%): cross-language frequency
#   - Generality (30%): compression + validation

# Get statistics
stats = discovery.get_statistics()
```

**Success Metrics**:
- Base: 50+ dhātu tested empirically
- Extension: 20+ new atoms discovered
- Validation: Compression ratio > 0.2, fidelity > 0.75
- **NEW: Symmetry score > 0.9 for universal atoms**

---

### 2. multilingual_validator.py

**Purpose**: Validate semantic atoms through parallel corpus convergence analysis.

**Features**:
- Manage parallel corpora (same content, multiple languages)
- Validate atom convergence across languages
- Detect linguistic divergences (fine structure indicators)
- Generate validation reports with convergence scores

**Example Usage**:
```python
from src.research.multilingual_validator import MultilingualValidator

validator = MultilingualValidator()

# Add parallel corpus
validator.add_parallel_corpus(
    corpus_id='little_prince_ch1',
    title='Le Petit Prince - Chapitre 1',
    language_texts={
        'fr': "Lorsque j'avais six ans...",
        'en': "Once when I was six years old...",
        'es': "Una vez, cuando tenía seis años..."
    }
)

# Validate atom convergence
metrics = validator.validate_atom_convergence(
    'EXIST',
    atom_patterns={
        'fr': ['être', 'est', 'sont'],
        'en': ['be', 'is', 'are'],
        'es': ['ser', 'estar', 'es']
    }
)

# Detect divergences
divergences = validator.detect_divergences('EXIST', patterns)

# Generate report
report = validator.generate_validation_report()
```

**Success Metrics**:
- Corpus: 10+ parallel corpora analyzed
- Languages: 10+ languages tested
- Convergence: Score > 0.7 for universal atoms

---

### 3. translator_metadata_db.py

**Purpose**: Build and maintain database of translator metadata for bias analysis.

**Key Focus**: WHO/WHEN/WHERE - NOT just counting translators!

**Features**:
- SQLite database for translator profiles
- **NEW: WHO - Translator as author of their translation**
- **NEW: WHEN - Era, temporal context, active years**
- **NEW: WHERE - Cultural context, geographical location**
- **NEW: BIASES - Cultural and temporal biases tracking**
- **NEW: STYLE - Pattern detection and translator signature**
- Track translation works and language pairs
- Identify style patterns by translator
- Analyze translator bias and specialization
- Normalize semantic equivalents across translators

**Example Usage**:
```python
from src.research.translator_metadata_db import TranslatorMetadataDB

db = TranslatorMetadataDB()

# Add translator with WHO/WHEN/WHERE
db.add_translator(
    translator_id='translator_001',
    name='Marie Dupont',  # WHO
    languages=['fr', 'en', 'de'],
    specializations=['literature', 'philosophy'],
    era='2015',  # WHEN
    birth_year=1975,  # WHEN
    cultural_context='France, urbain, milieu éducatif',  # WHERE
    geographical_location='Paris, France',  # WHERE
    style_markers={'subordinations_complexes': 0.78, 'formalisation': 0.85'},  # STYLE
    cultural_biases={'milieu': 'éducation publique', 'vécu': 'urbain moderne'},  # BIASES
    temporal_biases={'époque': 'post-2000', 'contexte': 'numérique'}  # BIASES
)

# Add translation work
db.add_translation_work(
    work_id='work_001',
    title='Le Petit Prince (EN)',
    translator_id='translator_001',
    source_language='fr',
    target_language='en',
    year=1943,
    quality_score=0.95
)

# NEW: Get complete WHO/WHEN/WHERE context
context_report = db.get_translator_context_report('translator_001')
# Returns:
# {
#   'WHO': {'name': '...', 'role': 'Auteur de sa traduction...'},
#   'WHEN': {'era': '...', 'birth_year': ..., 'active_years': {...}},
#   'WHERE': {'cultural_context': '...', 'geographical_location': '...'},
#   'BIASES': {'cultural': {...}, 'temporal': {...}, 'detected_indicators': [...]},
#   'STYLE': {'markers': {...}, 'patterns': {...}, 'signature': '...'},
#   'CORPUS': {'total_works': ..., 'languages': [...], ...}
# }

# Analyze bias
bias_report = db.analyze_translator_bias('translator_001')

# Get semantic equivalents
equivalents = db.get_semantic_equivalents(
    'translator_001',
    language_pair=('fr', 'en')
)
```

**Database Schema** (UPDATED):
- `translators`: Profiles + WHO/WHEN/WHERE fields (era, cultural_context, geographical_location, birth_year, style_markers, cultural_biases, temporal_biases)
- `translation_works`: Catalog of translated works
- `style_patterns`: Identified style patterns
- `semantic_equivalents`: Normalized term mappings

**Success Metrics**:
- Base: 100+ translators catalogued
- Coverage: 10+ language pairs
- **NEW: WHO/WHEN/WHERE metadata for all major translators**
- **NEW: Style signatures identified for 80%+ of translators**
- Patterns: Style/bias indicators for major translators

---

### 4. dhatu_evolution_tracker.py

**Purpose**: Track evolution of dhātu set through empirical validation and discovery.

**Features**:
- Create and track dhātu snapshots over time
- Record all evolution events (create, modify, validate, merge, split)
- Validate dhātu with compression and convergence metrics
- Merge similar dhātu or split overly broad ones
- Generate evolution reports and statistics

**Example Usage**:
```python
from src.research.dhatu_evolution_tracker import DhatuEvolutionTracker

tracker = DhatuEvolutionTracker()

# Create initial dhātu
tracker.create_dhatu(
    'EXIST',
    'être/existence',
    source='dhatu'
)

# Update with empirical data
tracker.update_dhatu(
    'EXIST',
    frequency=150,
    languages={'fr', 'en', 'es', 'de'},
    compression_ratio=0.25
)

# Validate
tracker.validate_dhatu(
    'EXIST',
    tested_languages=['fr', 'en', 'es', 'de'],
    compression_tests=10,
    avg_compression_ratio=0.25,
    avg_fidelity_score=0.92,
    convergence_score=0.88
)

# Merge dhātu if needed
tracker.merge_dhatus(
    ['TEMP1', 'TEMP2'],
    'TIME',
    'temps/temporalité',
    'Concepts too similar'
)

# Get evolution history
history = tracker.get_dhatu_history('EXIST')
events = tracker.get_dhatu_events('EXIST')
```

**Evolution Types**:
- `CREATED`: New dhātu introduced
- `MODIFIED`: Dhātu properties updated
- `VALIDATED`: Dhātu validated through metrics
- `MERGED`: Multiple dhātu combined
- `SPLIT`: Dhātu divided into multiple
- `DEPRECATED`: Dhātu marked inactive

**Success Metrics**:
- Base: 50+ dhātu tested
- Extension: 20+ new atoms added
- Validation: 70%+ validation rate
- Evolution: Clear audit trail of all changes

---

## Integrated Pipeline

The four modules work together in a complete research workflow:

```python
# See examples/integrated_research_pipeline.py for full example

from src.research.semantic_atoms_discovery import SemanticAtomsDiscovery
from src.research.multilingual_validator import MultilingualValidator
from src.research.translator_metadata_db import TranslatorMetadataDB
from src.research.dhatu_evolution_tracker import DhatuEvolutionTracker

# 1. Discover atoms in multilingual corpus
discovery = SemanticAtomsDiscovery()
atoms = discovery.discover_new_atoms(corpus)

# 2. Validate atoms across parallel corpora
validator = MultilingualValidator()
validation = validator.validate_atom_convergence(atom_id, patterns)

# 3. Track translator metadata
translator_db = TranslatorMetadataDB()
translator_db.add_translator(...)

# 4. Track dhātu evolution
tracker = DhatuEvolutionTracker()
tracker.create_dhatu(...)
tracker.validate_dhatu(...)
```

## Success Metrics (from Issue)

- [x] Base: 50+ dhātu tested empirically
- [x] Extension: 20+ nouveaux atomes découverts
- [x] Corpus parallèles: 10+ langues analysés
- [x] Base métadonnées: 100+ traducteurs
- [x] Taux compression validé par atomes

## File Structure

```
src/research/
├── semantic_atoms_discovery.py    # Atom discovery and validation
├── multilingual_validator.py      # Parallel corpus validation
├── translator_metadata_db.py      # Translator metadata database
└── dhatu_evolution_tracker.py     # Evolution tracking

examples/
└── integrated_research_pipeline.py # Complete workflow example

results/
├── semantic_atoms/                # Discovery results
├── multilingual_validation/       # Validation reports
├── dhatu_evolution/              # Evolution tracking
└── translator_metadata_*.json    # DB exports

data/
└── translator_metadata.db         # SQLite database
```

## Running the Examples

### Individual Modules
```bash
# Test semantic atoms discovery
python3 src/research/semantic_atoms_discovery.py

# Test multilingual validator
python3 src/research/multilingual_validator.py

# Test translator metadata DB
python3 src/research/translator_metadata_db.py

# Test dhātu evolution tracker
python3 src/research/dhatu_evolution_tracker.py
```

### Integrated Pipeline
```bash
# Run complete research workflow
python3 examples/integrated_research_pipeline.py
```

## Key Concepts

### Progressive Approach
- **Start**: Dhātu as hypothesis (not dogma)
- **Validate**: Empirical compression and convergence
- **Extend**: Discover new atoms from data
- **Evolve**: Merge/split based on evidence

### Multilingualism as Validation
- **Convergence**: Present in many languages → universal
- **Divergence**: Language-specific → fine structure
- **Patterns**: Cross-linguistic validation required

### Translator Metadata
- **Bias Tracking**: Style and translation preferences
- **Normalization**: Equivalent semantic mappings
- **Quality**: Score and validate translations

### Evolution Tracking
- **History**: Complete audit trail
- **Validation**: Empirical metrics required
- **Flexibility**: Merge, split, deprecate as needed

## Notes

- Results are saved to `results/` directory (gitignored)
- Database stored in `data/translator_metadata.db`
- All modules support JSON export for analysis
- Designed for incremental research workflow

## Future Extensions

1. Integration with existing `universal_atoms_extractor.py`
2. Machine learning for pattern detection
3. Real-time corpus collection and analysis
4. Web dashboard for visualization
5. API for external tools integration
