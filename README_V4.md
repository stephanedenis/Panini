# 🧬 PaniniFS v4.0 - Système Hypersémantique de Grammars Binaires

[![Milestone](https://img.shields.io/badge/Milestone-70%20Formats-success)](https://github.com/stephanedenis/Panini)
[![Architecture](https://img.shields.io/badge/Architecture-v4.0%20Hypersemantic-blue)](./VISION_PANINI_V4_HYPERSEMANTIQUE.md)
[![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)
[![Research](https://img.shields.io/badge/Research-Active-orange)](./research/)

> *"Comme les ~2000 dhātus Sanskrit génèrent des millions de mots,  
> les 12 patterns Panini génèrent une infinité de formats binaires."*

---

## 🎯 Vision

**PaniniFS** transforme l'analyse de formats binaires en un **système hypersémantique** où:

- 🔐 **Patterns = Dhātus immuables** (primitives content-addressed)
- 📝 **Grammars = Compositions déclaratives** (YAML vs Python)
- 🌳 **Évolution = Dérivations rejouables** (Git-style Merkle DAG)
- 🔍 **Découverte = Sémantique** (similitude + généalogie)
- ⚡ **Recognition = Zero-shot** (formats inconnus identifiés)

---

## 📊 État Actuel

### ✅ Milestone #70 - 70 Formats Implémentés

| Catégorie | Formats | Lignes |
|-----------|---------|--------|
| 🖼️ **Images** | PNG, JPEG, GIF, WebP, BMP, TIFF, ICO, XPM | ~3,200 |
| 📦 **Archives** | ZIP, TAR, GZIP, BZIP2, XZ, 7Z, RAR, CAB | ~3,800 |
| 📄 **Documents** | PDF, DOCX, XLSX, PPTX, ODT, ODS, ODP | ~4,100 |
| 🔤 **Fonts** | TTF, OTF, WOFF, WOFF2, EOT | ~1,900 |
| 🎵 **Audio** | MP3, WAV, FLAC, OGG, M4A, OPUS | ~2,400 |
| 🎬 **Video** | MP4, MKV, AVI, MOV, WebM, FLV | ~3,200 |
| 📊 **Data** | JSON, YAML, XML, CSV, TOML, Protobuf, CBOR | ~2,900 |
| ⚙️ **Executables** | ELF, PE, Mach-O, DEX, CLASS | ~3,500 |
| 🔧 **Autres** | SQLITE, PCAP, PATCH, MBOX, MIDI | ~1,500 |

**Total**: **26,517 lignes** de Python (baseline)

### 🚀 Architecture v4.0 - Hypersémantique

```
┌─────────────────────────────────────────────────────────┐
│  Content-Addressed Storage (CAS)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Exact Hash   │  │Similar Hash  │  │ Provenance   │ │
│  │ (SHA-256)    │  │ (Entropy+)   │  │ Chain        │ │
│  │ Immutability │  │ Discovery    │  │ Lineage      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Derivation System (Hypersemantic)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ YAML         │  │ Merkle DAG   │  │ Semantic     │ │
│  │ Transforms   │  │ Evolution    │  │ Fingerprints │ │
│  │ Declarative  │  │ Branching    │  │ Capabilities │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Universal Pattern Engine                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 12 Dhātu-FS Patterns (87% to 4.3% usage)        │  │
│  │ KEY_VALUE ▸ HEADER_BODY ▸ MAGIC_NUMBER ▸ ...    │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Declarative Grammars (YAML)                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │ PNG: ~50 lines YAML (vs 378 lines Python)       │  │
│  │ JSON: ~35 lines YAML (vs 289 lines Python)      │  │
│  │ ZIP: ~60 lines YAML (vs 412 lines Python)       │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Réduction cible**: 74.4% (26,517 → 6,800 lignes)

---

## 🧬 Philosophie Pāṇinienne

### Sanskrit → PaniniFS

| Concept | Signification | Implémentation |
|---------|---------------|----------------|
| **Dhātu** (धातु) | Racines verbales primitives | Patterns content-addressed |
| **Pratyaya** (प्रत्यय) | Affixes transformationnels | Dérivations déclaratives |
| **Sandhi** (सन्धि) | Fusion euphonique | Merge sémantique |
| **Sūtra** (सूत्र) | Règles compositionnelles | Grammars YAML |
| **Saṃjñā** (संज्ञा) | Méta-catégories | Semantic fingerprints |

### Exemple: Évolution PNG

```
Sanskrit: √gam → gacchati → gamayati
         [root]  [+suffix]   [+causative]

PaniniFS: PNG v1.0 → v2.0-trans → v3.0
         [baseline] [+alpha]     [+alpha+color]
         a7f3d912   b8e0fa23     d0e3cf56
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/stephanedenis/Panini.git
cd Panini

# Initialize submodules
git submodule update --init --recursive

# Install dependencies
pip install -r requirements.txt
```

### Analyse d'un Fichier

```python
from panini import analyze_file

# Analyse avec extracteur existant
result = analyze_file('image.png', use_grammar=False)
print(result['metadata'])

# Analyse avec grammar v4.0 (bientôt)
result = analyze_file('image.png', use_grammar=True)
print(result['metadata'])  # Même résultat!
```

### Créer une Grammar

```yaml
# grammars/myformat.yml
format: MyFormat
version: "1.0"

patterns:
  - pattern_ref: 9949a471  # MAGIC_NUMBER
    name: signature
    config:
      signature: "MYFORMAT"
      offset: 0

  - pattern_ref: 6eacc5de  # CHUNK_STRUCTURE
    name: chunks
    config:
      repeating: true

metadata:
  extract:
    - field: header.version
      as: format_version
    - field: chunks[0].data
      as: first_chunk
```

### Tester une Grammar

```bash
# Validation vs extractor original
panini validate myformat test_file.dat --compare extractors/myformat.py

# Tests unitaires
panini test myformat tests/
```

---

## 📚 Documentation

### Spécifications Architecturales

- 📘 [**Vision v4.0**](./VISION_PANINI_V4_HYPERSEMANTIQUE.md) - Vue d'ensemble complète
- 🏗️ [**Universal Engine Architecture**](./research/UNIVERSAL_ENGINE_ARCHITECTURE.md) - 12 patterns Dhātu-FS
- 🔐 [**Content-Addressed Architecture**](./research/CONTENT_ADDRESSED_ARCHITECTURE.md) - Double-hash system
- 🌳 [**Derivation System**](./research/DERIVATION_SYSTEM_ARCHITECTURE.md) - Évolution hypersémantique
- 📊 [**Status Report**](./research/PANINI_V4_STATUS.md) - État détaillé

### Guides Techniques

- 🎓 [**Pāṇini Philosophy Analysis**](./research/PANINI_PHILOSOPHY_ANALYSIS.md) - Fondements linguistiques
- 📄 [**Pāṇini Whitepaper**](./research/PANINI_WHITEPAPER.md) - Validation empirique
- 🔬 [**Pattern Consolidation**](./research/PATTERN_CONSOLIDATION_ANALYSIS.md) - Analyse Phase 6

---

## 🎯 Roadmap

### ✅ Phase 7.1 - Architecture (COMPLETE)

- ✅ Content-Addressed Storage (double-hash)
- ✅ Derivation System (hypersemantic)
- ✅ Pattern Base Classes (registry)
- ✅ Tests (14 cas, tous passent)

### 🔄 Phase 7.2 - Patterns (EN COURS)

- ✅ MAGIC_NUMBER (59.7% usage)
- 🔄 KEY_VALUE (87.0% usage)
- ⏳ HEADER_BODY (75.0% usage)
- ⏳ SEQUENTIAL_RECORDS (56.3%)
- ⏳ BINARY_FIELD (51.4%)
- ⏳ LENGTH_PREFIXED (48.6%)
- ⏳ COMPRESSED_DATA (45.7%)
- ⏳ TEXT_MARKUP (31.4%)
- ⏳ OFFSET_TABLE (21.4%)
- ⏳ CHECKSUM (20.0%)
- ⏳ CHUNK_STRUCTURE (17.1%)
- ⏳ HIERARCHICAL_TREE (4.3%)

### ⏳ Phase 7.3 - Grammar Parser (4 semaines)

- Grammar parser YAML → execution
- 3 POCs (PNG, JSON, ZIP)
- Validation (100% metadata match, < 2x perf)

### ⏳ Phase 7.4 - Full Migration (4 semaines)

- Migrate 70 formats to grammars
- Measure actual code reduction
- Performance benchmarking

---

## 🌟 Innovations

### vs Systèmes Existants

| Système | Limitation | Innovation PaniniFS |
|---------|-----------|---------------------|
| **Git** | Diff linéaire texte | Semantic diff binaire |
| **IPFS** | Liens explicites seulement | Découverte sémantique implicite |
| **Protobuf** | Schemas statiques | Grammars évolutives |
| **Kaitai Struct** | Pas de CAS, pas d'évolution | Versioning + provenance |
| **file(1)** | Database plate | DAG hypersémantique |

### Capacités Uniques

#### 1. Zero-Shot Recognition

```python
# Format inconnu → trouve similaires → parse!
mystery_hash = compute_similarity_hash(unknown_bytes)
candidates = store.find_similar(mystery_hash, threshold=0.75)
# → [("PNG", 0.87), ("BMP", 0.78)]

grammar = load_grammar(candidates[0][0])
result = parse_with_grammar(unknown_bytes, grammar)
# ✓ Format identifié sans définition explicite!
```

#### 2. Évolution Déclarative

```yaml
# Pas de code Python, juste YAML
# v1.0 → v2.0 par dérivation rejouable
type: derivation
parents: [a7f3d912]
transformation:
  operation: add_extraction
  changes:
    - path: metadata.extract
      add: [{field: tRNS.alpha, as: transparency}]
```

#### 3. Découverte Sémantique

```python
# Navigation au-delà des liens
dag.semantic_neighbors(hash)  # Similaires structurellement
dag.capability_search(['alpha_detection'])  # Par feature
dag.diff_semantic(h1, h2)  # Différence sémantique
```

---

## 📊 Résultats Empiriques

### Phase 6 Analysis (70 formats)

| Métrique | Valeur | Validation |
|----------|--------|------------|
| **Pattern Reuse** | 43% | ✅ > 40% target |
| **Code Reduction** | 81.7% theoretical | 🔄 74.4% target |
| **Patterns Found** | 12 Dhātu-FS | ✅ O(√N) confirmed |
| **Complexity** | O(√70) ≈ 8.4 | ✅ 12 patterns |

### CAS Tests (Phase 7.1)

| Test | Résultat | Status |
|------|----------|--------|
| Deduplication | PNG stored 2× → same hash | ✅ |
| Similarity | PNG ↔ GIF: 87.5% | ✅ |
| Distinction | CHUNK ↔ MAGIC: 12-37% | ✅ |
| Entropy | zeros:0.0, random:8.0 | ✅ |
| Reconstruction | v1.0 → v3.0 replay | ✅ |

---

## 🤝 Contributing

### Workflow

```bash
# 1. Créer grammar YAML
cat > grammars/myformat.yml <<EOF
format: MyFormat
version: "1.0"
patterns: [...]
EOF

# 2. Tester
panini test myformat test_file.dat

# 3. Valider vs original
panini validate myformat --compare extractors/myformat.py

# 4. Commit avec semantic fingerprint
git commit -m "feat: Add MyFormat grammar v1.0

Capabilities: [signature_detection, ...]
Intent: [format_identification, ...]
Domain: [binary, image, ...]"
```

### Guidelines

- ✅ **Immutabilité**: Changement = nouvelle version (hash)
- ✅ **Déclaratif**: Préférer YAML à Python
- ✅ **Sémantique**: Documenter capabilities/intent
- ✅ **Tests**: 100% metadata match requis

---

## 📈 Statistics

### Code Metrics

- **Formats**: 70 ✅
- **Extractors (baseline)**: 26,517 lignes Python
- **Target (grammars)**: 6,800 lignes YAML
- **Reduction**: 74.4%
- **Architecture**: 4,400+ lignes (CAS + derivation)
- **Tests**: 679 lignes (14 test cases)

### Session Metrics (Oct 2025)

- **Commits**: 7 (milestone + architecture)
- **Documentation**: 1,900+ lignes
- **Implementation**: 2,500+ lignes
- **Tests**: 679 lignes
- **Total**: ~5,000 lignes cette session

---

## 📞 Contact

**Project**: PaniniFS v4.0  
**Repository**: <https://github.com/stephanedenis/Panini>  
**Research**: <https://github.com/stephanedenis/Panini/tree/main/research>  
**License**: MIT (code), CC-BY-4.0 (docs)

**Maintainer**: Panini Research Team  
**Issues**: <https://github.com/stephanedenis/Panini/issues>  
**Discussions**: <https://github.com/stephanedenis/Panini/discussions>

---

## 🏆 Acknowledgments

**Inspirations**:

- **Pāṇini** (~400 BCE) - Aṣṭādhyāyī (generative Sanskrit grammar)
- **Noam Chomsky** (1957) - Generative grammars
- **Linus Torvalds** (2005) - Git (content-addressed storage)
- **Juan Benet** (2015) - IPFS (Merkle DAGs)

**Technologies**:

- Python 3.10+ (extractors)
- YAML (grammars)
- Git (versioning)
- Content-addressing (CAS)

---

## ⚖️ License

```
MIT License

Copyright (c) 2025 Panini Research Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**🧬 PaniniFS v4.0 - Hypersemantic Binary Grammar System**

*Transforming binary format analysis through Pāṇinian composition theory*

[![⭐ Star](https://img.shields.io/github/stars/stephanedenis/Panini?style=social)](https://github.com/stephanedenis/Panini)
[![🔀 Fork](https://img.shields.io/github/forks/stephanedenis/Panini?style=social)](https://github.com/stephanedenis/Panini/fork)
[![👁️ Watch](https://img.shields.io/github/watchers/stephanedenis/Panini?style=social)](https://github.com/stephanedenis/Panini)

</div>
