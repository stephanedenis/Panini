# 🦀 Roadmap: PaniniFS Rust Production-Quality Implementation

**Date**: 2025-01-12  
**Objectif**: Porter le décomposeur sémantique Python mature (1527 lignes, 44 formats) vers Rust avec qualité production  
**Contexte**: Rust archivé = squelette vide, Python = code production mature

---

## 📊 État Actuel

### ✅ Assets Existants (Python)
- **`research/panini-fs/prototypes/decomposers/generic_decomposer.py`**: 1527 lignes
- **Architecture mature**:
  - `PatternProcessor` base class + 18+ processeurs spécialisés
  - `GenericDecomposer` orchestrateur principal
  - Support récursif et hiérarchique
- **44+ Grammaires JSON** dans `research/panini-fs/format_grammars/`:
  - Images: PNG, JPEG, GIF, WebP, TIFF, BMP, ICO
  - Audio: WAV, MP3, FLAC, OGG
  - Vidéo: MP4, AVI, WebM, MKV
  - Documents: PDF, ZIP, GZIP, TAR, 7Z, RAR
  - Exotiques: WASM, ELF, MIDI, etc.

### ❌ Rust Status
- **Squelette vide** dans archives (`CORE/panini-fs/`)
- Seulement `lib.rs` avec modules déclarés
- Tous les fichiers `.rs` sont vides
- `Cargo.toml` minimal sans dépendances

### 🎯 Workspace Rust Existant
- **`modules/core/filesystem/Cargo.toml`**: Workspace configuré
- Crates déclarées: `panini-core`, `panini-api`
- Dépendances workspace: tokio, serde, sha2, bytes, petgraph, axum

---

## 🏗️ Architecture Cible

### Crate Structure
```
modules/core/filesystem/
├── Cargo.toml (workspace root)
├── crates/
│   ├── panini-core/
│   │   ├── Cargo.toml
│   │   ├── src/
│   │   │   ├── lib.rs
│   │   │   ├── semantic/
│   │   │   │   ├── mod.rs
│   │   │   │   ├── decomposer.rs       ⭐ Core engine
│   │   │   │   ├── patterns/           ⭐ Pattern processors
│   │   │   │   │   ├── mod.rs
│   │   │   │   │   ├── base.rs         (PatternProcessor trait)
│   │   │   │   │   ├── magic_number.rs
│   │   │   │   │   ├── length_prefixed.rs
│   │   │   │   │   ├── typed_chunk.rs
│   │   │   │   │   ├── crc_checksum.rs
│   │   │   │   │   ├── riff.rs
│   │   │   │   │   ├── jpeg_segment.rs
│   │   │   │   │   ├── gif.rs
│   │   │   │   │   ├── tiff.rs
│   │   │   │   │   ├── pdf.rs
│   │   │   │   │   └── ...
│   │   │   │   ├── grammar.rs          (Grammar loader/parser)
│   │   │   │   └── atom.rs             (Dhātu atom structures)
│   │   │   ├── storage/
│   │   │   │   ├── mod.rs
│   │   │   │   ├── chunk_store.rs      (Content-addressed storage)
│   │   │   │   └── index.rs            (Semantic index)
│   │   │   └── validation/
│   │   │       ├── mod.rs
│   │   │       └── reconstruction.rs   (Bit-perfect validation)
│   │   └── tests/
│   │       ├── fixtures/               (Binary test files)
│   │       └── integration_tests.rs
│   │
│   └── panini-api/
│       ├── Cargo.toml
│       └── src/
│           ├── main.rs                 (HTTP API avec Axum)
│           └── routes/
│               ├── decompose.rs
│               └── query.rs
```

---

## 🎯 Phase 1: Infrastructure de Base (2-3 jours)

### Objectifs
- ✅ Structures de données fondamentales
- ✅ Système de grammaires JSON
- ✅ Pattern processor trait de base
- ✅ Tests unitaires infrastructuraux

### Livrables

#### 1.1. `panini-core/src/semantic/atom.rs`
```rust
/// Représente un atome sémantique (chunk décomposé)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SemanticAtom {
    pub offset: u64,
    pub size: u64,
    pub pattern: String,
    pub interpretation: String,
    pub data_hash: [u8; 32],  // SHA-256
    pub metadata: HashMap<String, serde_json::Value>,
    pub children: Vec<SemanticAtom>,  // Récursif
}
```

#### 1.2. `panini-core/src/semantic/grammar.rs`
```rust
/// Chargeur de grammaires JSON
pub struct GrammarLoader {
    grammars: HashMap<String, FormatGrammar>,
}

#[derive(Debug, Deserialize)]
pub struct FormatGrammar {
    pub format: String,
    pub version: String,
    pub patterns: Vec<PatternSpec>,
}

impl GrammarLoader {
    pub fn load_from_directory(path: &Path) -> Result<Self>;
    pub fn get_grammar(&self, format: &str) -> Option<&FormatGrammar>;
}
```

#### 1.3. `panini-core/src/semantic/patterns/base.rs`
```rust
/// Trait pour tous les pattern processors
pub trait PatternProcessor: Send + Sync {
    fn pattern_name(&self) -> &'static str;
    fn process(
        &self,
        data: &[u8],
        offset: u64,
        spec: &PatternSpec,
    ) -> Result<ProcessResult>;
}

pub struct ProcessResult {
    pub atom: SemanticAtom,
    pub bytes_consumed: u64,
    pub next_offset: Option<u64>,
}
```

#### 1.4. Tests
```rust
#[test]
fn test_grammar_loader() {
    let loader = GrammarLoader::load_from_directory("../../../research/panini-fs/format_grammars").unwrap();
    assert!(loader.get_grammar("png").is_some());
}
```

---

## 🎯 Phase 2: Pattern Processors Universels (3-5 jours)

### Priorité: Patterns Universels Réutilisables

#### 2.1. `patterns/magic_number.rs`
- Lecture magic number (signatures)
- Support multi-valeurs (GIF87a/GIF89a)
- Validation stricte

#### 2.2. `patterns/length_prefixed.rs`
- Length-prefixed data (uint16/uint32)
- Endianness configurable (big/little)
- Lecture données associées

#### 2.3. `patterns/typed_chunk.rs`
- Chunks typés (PNG, RIFF)
- Type + Length + Data + CRC
- Validation intégrité

#### 2.4. `patterns/crc_checksum.rs`
- CRC-32, Adler-32
- Validation checksums
- Calcul et vérification

#### 2.5. Tests par Pattern
```rust
#[test]
fn test_magic_number_png() {
    let png_header = b"\x89PNG\r\n\x1a\n";
    let processor = MagicNumberProcessor::new();
    let result = processor.process(png_header, 0, &spec).unwrap();
    assert_eq!(result.atom.pattern, "MAGIC_NUMBER");
    assert!(result.atom.metadata["valid"].as_bool().unwrap());
}
```

---

## 🎯 Phase 3: Format-Specific Processors (5-7 jours)

### Formats Prioritaires (MVP)

#### 3.1. **PNG** (Référence Gold Standard)
- `patterns/png.rs`
- Chunks IHDR, PLTE, IDAT, IEND
- CRC validation
- Compression DEFLATE awareness

#### 3.2. **JPEG**
- `patterns/jpeg_segment.rs`
- Segments SOI, APP0-APP15, DQT, DHT, SOS, EOI
- Huffman tables
- Quantization tables

#### 3.3. **GIF**
- `patterns/gif.rs`
- Logical Screen Descriptor
- Image Descriptor
- LZW compression blocks
- Extension blocks

#### 3.4. **RIFF (WAV/AVI)**
- `patterns/riff.rs`
- RIFF header
- Chunks récursifs
- Format variations (WAVE, AVI, WebP)

#### 3.5. **PDF**
- `patterns/pdf.rs`
- Object streams
- Cross-reference table
- Trailer parsing

---

## 🎯 Phase 4: Décomposeur Principal (3-4 jours)

### `semantic/decomposer.rs`

```rust
pub struct GenericDecomposer {
    grammars: GrammarLoader,
    processors: HashMap<String, Box<dyn PatternProcessor>>,
}

impl GenericDecomposer {
    pub fn new(grammar_path: &Path) -> Result<Self>;
    
    pub fn decompose(&self, data: &[u8], grammar_name: &str) -> Result<Vec<SemanticAtom>> {
        let grammar = self.grammars.get_grammar(grammar_name)
            .ok_or_else(|| Error::GrammarNotFound)?;
        
        let mut atoms = Vec::new();
        let mut offset = 0u64;
        
        for pattern_spec in &grammar.patterns {
            let processor = self.processors.get(&pattern_spec.pattern)
                .ok_or_else(|| Error::ProcessorNotFound)?;
            
            let result = processor.process(data, offset, pattern_spec)?;
            atoms.push(result.atom);
            offset = result.next_offset.unwrap_or(offset + result.bytes_consumed);
        }
        
        Ok(atoms)
    }
    
    /// Décomposition récursive
    pub fn decompose_recursive(&self, atom: &mut SemanticAtom, data: &[u8]) -> Result<()>;
}
```

---

## 🎯 Phase 5: Storage & Validation (2-3 jours)

### 5.1. Content-Addressed Storage
```rust
pub struct ChunkStore {
    path: PathBuf,
}

impl ChunkStore {
    pub fn store_atom(&self, atom: &SemanticAtom, data: &[u8]) -> Result<[u8; 32]>;
    pub fn retrieve_atom(&self, hash: &[u8; 32]) -> Result<Vec<u8>>;
}
```

### 5.2. Reconstruction Validator
```rust
pub struct ReconstructionValidator;

impl ReconstructionValidator {
    pub fn validate_bit_perfect(&self, original: &[u8], atoms: &[SemanticAtom]) -> Result<bool> {
        let reconstructed = self.reconstruct(atoms)?;
        Ok(original == reconstructed.as_slice())
    }
}
```

---

## 🎯 Phase 6: API REST (2 jours)

### `panini-api/src/main.rs`
```rust
use axum::{Router, routing::post};

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/decompose", post(routes::decompose))
        .route("/query", post(routes::query));
    
    axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}
```

### Endpoints
- **POST /decompose**: Upload binary + grammar → JSON atoms
- **POST /query**: Semantic query → matching atoms

---

## 🎯 Phase 7: Testing & Benchmarks (3-4 jours)

### 7.1. Test Corpus
```
tests/fixtures/
├── images/
│   ├── test_png_1.png
│   ├── test_jpeg_1.jpg
│   └── test_gif_1.gif
├── audio/
│   └── test_wav_1.wav
└── documents/
    └── test_pdf_1.pdf
```

### 7.2. Integration Tests
```rust
#[test]
fn test_png_decomposition_bit_perfect() {
    let data = include_bytes!("fixtures/images/test_png_1.png");
    let decomposer = GenericDecomposer::new("grammars").unwrap();
    let atoms = decomposer.decompose(data, "png").unwrap();
    
    let validator = ReconstructionValidator;
    assert!(validator.validate_bit_perfect(data, &atoms).unwrap());
}
```

### 7.3. Benchmarks
```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn bench_png_decomposition(c: &mut Criterion) {
    let data = include_bytes!("fixtures/images/test_png_1.png");
    let decomposer = GenericDecomposer::new("grammars").unwrap();
    
    c.bench_function("decompose_png", |b| {
        b.iter(|| decomposer.decompose(black_box(data), "png"))
    });
}
```

---

## 📦 Dépendances Cargo

### `panini-core/Cargo.toml`
```toml
[dependencies]
# Serialization
serde = { workspace = true }
serde_json = { workspace = true }

# Hashing
sha2 = { workspace = true }

# Data structures
bytes = { workspace = true }
byteorder = { workspace = true }

# Error handling
anyhow = { workspace = true }
thiserror = { workspace = true }

# Compression
flate2 = "1.0"  # DEFLATE pour PNG
crc32fast = "1.3"  # CRC-32 rapide

[dev-dependencies]
tempfile = { workspace = true }
criterion = "0.5"

[[bench]]
name = "decomposition_bench"
harness = false
```

---

## 🎯 Qualité Production: Checklist

### Code Quality
- [ ] **Zero unsafe** sauf si absolument nécessaire + justifié
- [ ] **Error handling**: `Result<T, Error>` partout, pas de `.unwrap()`
- [ ] **Documentation**: `///` doc comments sur tous les items publics
- [ ] **Tests unitaires**: 80%+ coverage par module
- [ ] **Integration tests**: Top 10 formats testés bit-perfect
- [ ] **Benchmarks**: Comparaison Python vs Rust

### Performance
- [ ] **Streaming**: Pas de chargement complet en mémoire
- [ ] **Zero-copy**: `&[u8]` slices, pas de clones inutiles
- [ ] **Parallel**: Support décomposition parallèle (Rayon)
- [ ] **Async**: API REST non-bloquante (Tokio)

### Maintenance
- [ ] **CI/CD**: GitHub Actions (build, test, bench, clippy, fmt)
- [ ] **Versioning**: SemVer strict
- [ ] **Changelog**: Maintenu à jour
- [ ] **Examples**: Au moins 3 exemples fonctionnels

### Security
- [ ] **Bounds checking**: Toutes les lectures validées
- [ ] **Integer overflow**: Checked arithmetic
- [ ] **Fuzzing**: Cargo-fuzz sur top 5 formats
- [ ] **Audit**: `cargo audit` en CI

---

## 📊 Métriques de Succès

### Fonctionnel
1. **44+ formats supportés** (parité Python)
2. **Reconstruction bit-perfect** à 100%
3. **Grammaires JSON compatibles** avec version Python
4. **API REST fonctionnelle** (<100ms p99 pour PNG 1MB)

### Performance
1. **5-10x plus rapide que Python** sur décomposition PNG
2. **Mémoire**: <10MB pour décomposer 100MB fichier
3. **Throughput**: >100MB/s sur formats simples (PNG, JPEG)

### Qualité
1. **Zero warnings** `cargo clippy`
2. **100% formatted** `cargo fmt`
3. **80%+ test coverage**
4. **Documentation complète** `cargo doc --open`

---

## 🚀 Timeline Estimé

| Phase | Durée | Dépendances |
|-------|-------|-------------|
| Phase 1: Infrastructure | 2-3 jours | - |
| Phase 2: Pattern Processors | 3-5 jours | Phase 1 |
| Phase 3: Format Processors | 5-7 jours | Phase 2 |
| Phase 4: Décomposeur Principal | 3-4 jours | Phase 3 |
| Phase 5: Storage & Validation | 2-3 jours | Phase 4 |
| Phase 6: API REST | 2 jours | Phase 5 |
| Phase 7: Testing & Benchmarks | 3-4 jours | Phase 6 |
| **Total** | **20-28 jours** | - |

### Approche Agile
- **Sprints de 1 semaine**
- **Review après chaque phase**
- **Integration continue** dès Phase 1

---

## 🔄 Migration Strategy

### Option A: Big Bang (Non Recommandé)
- Tout porter d'un coup
- Risque élevé
- Long feedback loop

### Option B: Incrémental (Recommandé) ⭐
1. **Semaine 1**: Phase 1 + 2 → Pattern processors universels
2. **Semaine 2**: Phase 3 → PNG + JPEG (formats critiques)
3. **Semaine 3**: Phase 4 + 5 → Décomposeur + validation
4. **Semaine 4**: Phase 6 + 7 → API + tests complets
5. **Semaine 5+**: Formats additionnels progressivement

### Option C: Hybrid Python/Rust
- FFI binding temporaire
- Python appelle Rust pour formats critiques
- Migration progressive

---

## 📝 Next Actions

### Immédiat (Aujourd'hui)
1. ✅ Lire roadmap complète
2. ⬜ Créer structure crates (`panini-core/src/`)
3. ⬜ Implémenter `SemanticAtom` struct
4. ⬜ Implémenter `GrammarLoader`
5. ⬜ Premier test unitaire

### Cette Semaine
- [ ] Phase 1 complète
- [ ] 3 pattern processors universels
- [ ] Test PNG magic number

### Ce Mois
- [ ] Phases 1-4 complètes
- [ ] PNG + JPEG décomposition bit-perfect
- [ ] API REST fonctionnelle

---

## 🎓 Références

### Rust Resources
- [The Rust Book](https://doc.rust-lang.org/book/)
- [Async Book](https://rust-lang.github.io/async-book/)
- [Cargo Book](https://doc.rust-lang.org/cargo/)

### Format Specs
- PNG: [RFC 2083](https://www.rfc-editor.org/rfc/rfc2083)
- JPEG: [ITU T.81](https://www.w3.org/Graphics/JPEG/itu-t81.pdf)
- GIF: [GIF89a Spec](https://www.w3.org/Graphics/GIF/spec-gif89a.txt)

### PaniniFS Theory
- `/home/stephane/GitHub/Panini/research/panini-fs/prototypes/decomposers/generic_decomposer.py`
- `/home/stephane/GitHub/Panini/docs/architecture/ASYNC_SEMANTIC_COMPRESSION_PIPELINE.md`

---

**🎯 Philosophie**: "Make it work, make it right, make it fast" - Kent Beck

1. **Make it work**: Implémentation fonctionnelle (Phases 1-4)
2. **Make it right**: Tests, validation, documentation (Phase 7)
3. **Make it fast**: Optimisations, benchmarks (continu)
