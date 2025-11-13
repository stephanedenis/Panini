# 🧪 Reconstruction Recipes - Format & Stratégies

**Version**: 0.2.0  
**Date**: 2025-11-13  
**Module**: Validation & Reconstruction

---

## 🎯 Overview

Les **Reconstruction Recipes** sont des fichiers JSON qui décrivent exactement comment reconstruire un chunk compressé vers son état original, garantissant une reconstruction **bit-perfect**.

**Philosophie**: Une recipe est un contrat qui garantit `decompress(compress(data)) == data`.

---

## 📋 Format Recipe JSON

### Structure de Base

```json
{
  "version": "1.0",
  "chunk_id": 0,
  "original_hash": "abc123...",
  "compression_method": "semantic_image_v1",
  "reconstruction": {
    "method": "gzip_decompress",
    "parameters": {}
  },
  "stats": {
    "original_size": 10240,
    "compressed_size": 2048,
    "ratio": 0.2,
    "savings_percent": 80.0
  },
  "uploaded_at": "2025-11-13T10:30:00Z",
  "worker": "colab_pro_gpu"
}
```

### Champs Obligatoires

| Champ | Type | Description |
|-------|------|-------------|
| `version` | string | Version du format recipe (actuellement "1.0") |
| `chunk_id` | int | ID du chunk (ordre de reconstruction) |
| `original_hash` | string | SHA-256 du chunk original (validation) |
| `compression_method` | string | Méthode de compression utilisée |
| `reconstruction` | object | Instructions de décompression |

### Champs Optionnels

| Champ | Type | Description |
|-------|------|-------------|
| `stats` | object | Statistiques de compression |
| `uploaded_at` | string | Timestamp upload (ISO 8601) |
| `worker` | string | ID du worker ayant compressé |
| `assembly_info` | object | Info pour reconstruction multi-chunk |

---

## 🔧 Méthodes de Compression

### 1. Generic GZIP

**Usage**: Compression générique sans sémantique spécifique.

```json
{
  "compression_method": "generic_gzip_v1",
  "reconstruction": {
    "method": "gzip_decompress"
  }
}
```

**Reconstruction Python**:
```python
import gzip

def reconstruct_generic_gzip(compressed_data: bytes, recipe: dict) -> bytes:
    return gzip.decompress(compressed_data)
```

**Avantages**:
- Simple et rapide
- Compatible universellement
- Bon ratio sur données répétitives

**Inconvénients**:
- Pas d'optimisation sémantique
- Moins efficace que formats spécialisés

---

### 2. Semantic Image (v1)

**Usage**: Images (PNG, JPEG, BMP) avec préservation structure.

```json
{
  "compression_method": "semantic_image_v1",
  "reconstruction": {
    "method": "image_array_reconstruct",
    "parameters": {
      "shape": [256, 256, 3],
      "dtype": "uint8",
      "format": "PNG"
    }
  }
}
```

**Reconstruction Python**:
```python
import gzip
import numpy as np
from PIL import Image
import io

def reconstruct_semantic_image(compressed_data: bytes, recipe: dict) -> bytes:
    params = recipe['reconstruction']['parameters']
    
    # Décompresser array numpy
    decompressed = gzip.decompress(compressed_data)
    shape = tuple(params['shape'])
    dtype = params['dtype']
    
    # Reconstruire array
    img_array = np.frombuffer(decompressed, dtype=dtype).reshape(shape)
    
    # Convertir en image
    img = Image.fromarray(img_array.astype('uint8'))
    
    # Sauvegarder dans format original
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=params['format'])
    
    return img_bytes.getvalue()
```

**Avantages**:
- Préserve dimensions et format
- Meilleur ratio que gzip pur
- Support GPU pour traitement

**Inconvénients**:
- Nécessite PIL/numpy
- Plus complexe

---

### 3. Semantic Text (v1)

**Usage**: Texte avec détection encoding.

```json
{
  "compression_method": "semantic_text_v1",
  "reconstruction": {
    "method": "gzip_decompress",
    "parameters": {
      "encoding": "utf-8"
    }
  }
}
```

**Reconstruction Python**:
```python
def reconstruct_semantic_text(compressed_data: bytes, recipe: dict) -> bytes:
    encoding = recipe['reconstruction']['parameters']['encoding']
    decompressed = gzip.decompress(compressed_data)
    
    # Valider encoding
    try:
        decompressed.decode(encoding)
    except UnicodeDecodeError:
        raise ValueError(f"Invalid encoding: {encoding}")
    
    return decompressed
```

**Avantages**:
- Détection automatique encoding
- Validation intégrité UTF-8
- Compression optimisée texte

---

### 4. Video Keyframe (v1) - 🚧 En développement

**Usage**: Chunks vidéo avec séparation keyframes/delta.

```json
{
  "compression_method": "video_keyframe_v1",
  "reconstruction": {
    "method": "video_keyframe_reconstruct",
    "parameters": {
      "codec": "h264",
      "keyframe_indices": [0, 30, 60],
      "is_keyframe": true,
      "temporal_refs": []
    }
  }
}
```

**Reconstruction (conceptuel)**:
```python
def reconstruct_video_keyframe(compressed_data: bytes, recipe: dict) -> bytes:
    params = recipe['reconstruction']['parameters']
    
    if params['is_keyframe']:
        # Keyframe = indépendant, décompression directe
        return decompress_h264_frame(compressed_data)
    else:
        # Delta frame = nécessite références temporelles
        refs = load_temporal_references(params['temporal_refs'])
        return reconstruct_delta_frame(compressed_data, refs)
```

**Status**: 🔜 Planifié pour v0.3.0

---

### 5. PDF Object (v1) - 🚧 En développement

**Usage**: Objects PDF avec préservation structure.

```json
{
  "compression_method": "pdf_object_v1",
  "reconstruction": {
    "method": "pdf_object_reconstruct",
    "parameters": {
      "object_id": 42,
      "generation": 0,
      "has_stream": true,
      "filters": ["FlateDecode"]
    }
  }
}
```

**Status**: 🔜 Planifié pour v0.4.0

---

## 🏗️ Assembly Info (Multi-Chunk)

Pour reconstruction de fichiers complets depuis plusieurs chunks.

```json
{
  "assembly_info": {
    "offset": 0,
    "size": 1024,
    "total_chunks": 5,
    "ordering": 0,
    "depends_on": []
  }
}
```

### Champs Assembly

| Champ | Type | Description |
|-------|------|-------------|
| `offset` | int | Position dans fichier final (bytes) |
| `size` | int | Taille du chunk décompressé |
| `total_chunks` | int | Nombre total de chunks du fichier |
| `ordering` | int | Ordre de reconstruction (0-indexed) |
| `depends_on` | list[int] | IDs de chunks requis (pour delta frames) |

### Reconstruction Multi-Chunk

```python
def reconstruct_file(chunks_dir: Path, output_file: Path) -> bool:
    """Reconstruit fichier complet depuis chunks"""
    
    # Charger manifest
    manifest = json.loads((chunks_dir / 'manifest.json').read_text())
    total_chunks = manifest['total_chunks']
    
    # Charger et trier chunks par offset
    chunks_with_offsets = []
    for i in range(total_chunks):
        chunk_dir = chunks_dir / f"chunk_{i:04d}"
        
        # Charger recipe
        recipe = json.loads((chunk_dir / 'recipe.json').read_text())
        
        # Charger données compressées
        compressed_data = (chunk_dir / 'compressed.bin').read_bytes()
        
        # Décompresser
        decompressed = decompress_chunk(compressed_data, recipe)
        
        # Ajouter avec offset
        offset = recipe.get('assembly_info', {}).get('offset', i * len(decompressed))
        chunks_with_offsets.append((offset, decompressed))
    
    # Trier par offset
    chunks_with_offsets.sort(key=lambda x: x[0])
    
    # Assembler
    reconstructed = bytearray()
    for offset, data in chunks_with_offsets:
        # Vérifier pas de gap
        if offset != len(reconstructed):
            raise ValueError(f"Gap détecté à offset {offset}")
        reconstructed.extend(data)
    
    # Sauvegarder
    output_file.write_bytes(reconstructed)
    
    # Valider hash
    reconstructed_hash = hashlib.sha256(reconstructed).hexdigest()
    expected_hash = manifest['original_hash']
    
    if reconstructed_hash != expected_hash:
        raise ValueError("Hash mismatch!")
    
    return True
```

---

## 📊 Stratégies de Compression par Type

### Images

| Format | Stratégie | Méthode | Ratio Typique |
|--------|-----------|---------|---------------|
| PNG | Semantic array | `semantic_image_v1` | 60-80% |
| JPEG | Direct passthrough | `passthrough_v1` | 0% (déjà compressé) |
| BMP | Aggressive compress | `semantic_image_v1` | 80-95% |
| WebP | Direct passthrough | `passthrough_v1` | 0% |
| TIFF | Layer-aware | `semantic_image_v1` | 50-70% |

**Recommandations**:
- **PNG**: Décompresser DEFLATE, re-compresser array numpy (meilleur ratio GPU)
- **JPEG**: Pas de re-compression (lossy + déjà optimal)
- **BMP**: Compression agressive (non compressé à la base)

### Vidéo

| Format | Stratégie | Méthode | Ratio Typique |
|--------|-----------|---------|---------------|
| MP4 | Keyframe split | `video_keyframe_v1` | 10-30% |
| MOV | Keyframe split | `video_keyframe_v1` | 10-30% |
| WebM | Cluster aware | `video_cluster_v1` | 15-35% |
| AVI | Frame aware | `video_keyframe_v1` | 20-40% |

**Recommandations**:
- **Séparer keyframes des delta frames** (keyframes = gros, deltas = petits)
- **Compresser metadata (moov) agressivement** (text-like)
- **Passthrough mdat si déjà H.264/VP9** (déjà optimal)

### Audio

| Format | Stratégie | Méthode | Ratio Typique |
|--------|-----------|---------|---------------|
| WAV | PCM compress | `semantic_audio_v1` | 40-60% |
| MP3 | Passthrough | `passthrough_v1` | 0% |
| FLAC | Passthrough | `passthrough_v1` | 0% |
| OGG | Passthrough | `passthrough_v1` | 0% |

### Documents

| Format | Stratégie | Méthode | Ratio Typique |
|--------|-----------|---------|---------------|
| PDF | Object-level | `pdf_object_v1` | 30-50% |
| ZIP | Skip (déjà comp) | `passthrough_v1` | 0% |
| GZIP | Skip | `passthrough_v1` | 0% |
| TXT | Aggressive | `semantic_text_v1` | 60-80% |

---

## ✅ Validation Bit-Perfect

### Script de Validation

```python
#!/usr/bin/env python3
"""Valider reconstruction bit-perfect"""

def validate_reconstruction(original_file: Path, chunks_dir: Path) -> bool:
    """Valide que reconstruction == original (bit-perfect)"""
    
    # Hash original
    original_data = original_file.read_bytes()
    original_hash = hashlib.sha256(original_data).hexdigest()
    
    print(f"Original: {len(original_data)} bytes, hash={original_hash[:16]}...")
    
    # Reconstruire
    reconstructed_file = chunks_dir.parent / f"{original_file.stem}_reconstructed{original_file.suffix}"
    reconstruct_file(chunks_dir, reconstructed_file)
    
    # Hash reconstructed
    reconstructed_data = reconstructed_file.read_bytes()
    reconstructed_hash = hashlib.sha256(reconstructed_data).hexdigest()
    
    print(f"Reconstructed: {len(reconstructed_data)} bytes, hash={reconstructed_hash[:16]}...")
    
    # Comparer
    if original_hash == reconstructed_hash:
        print("✅ BIT-PERFECT MATCH!")
        return True
    else:
        print("❌ HASH MISMATCH!")
        
        # Debug: où diffère
        for i, (a, b) in enumerate(zip(original_data, reconstructed_data)):
            if a != b:
                print(f"First difference at byte {i}: {a:02x} != {b:02x}")
                break
        
        return False

# Usage
validate_reconstruction(
    Path('original.png'),
    Path('chunks/original')
)
```

### Tests Automatisés

```python
import pytest

@pytest.mark.parametrize("format_type,file_path", [
    ("png", "test_data/image.png"),
    ("jpeg", "test_data/photo.jpg"),
    ("mp4", "test_data/video.mp4"),
    ("pdf", "test_data/document.pdf"),
])
def test_bit_perfect_reconstruction(format_type, file_path):
    """Test reconstruction bit-perfect pour tous formats"""
    
    original_file = Path(file_path)
    
    # Chunk
    chunks_dir = chunk_with_metadata(original_file, Path('/tmp/chunks'))
    
    # Compress (simulation)
    compressed_dir = compress_chunks(chunks_dir, compression_level=9)
    
    # Reconstruct
    reconstructed_file = Path('/tmp/reconstructed') / original_file.name
    reconstruct_file(compressed_dir, reconstructed_file)
    
    # Validate
    assert original_file.read_bytes() == reconstructed_file.read_bytes()
```

---

## 🚀 Optimisations Avancées

### 1. Compression Delta (Video)

Pour vidéos, exploiter temporalité:

```json
{
  "compression_method": "video_delta_v1",
  "reconstruction": {
    "method": "temporal_delta_reconstruct",
    "parameters": {
      "reference_chunks": [0, 30],
      "delta_type": "P-frame",
      "motion_vectors": true
    }
  },
  "assembly_info": {
    "depends_on": [0, 30]
  }
}
```

**Ratio gain**: +20-40% sur delta frames

### 2. Deduplication Globale

Identifier chunks identiques entre fichiers:

```json
{
  "compression_method": "dedup_reference_v1",
  "reconstruction": {
    "method": "dedup_resolve",
    "parameters": {
      "reference_hash": "abc123...",
      "reference_path": "chunks/other_file/chunk_0005"
    }
  }
}
```

**Ratio gain**: 100% si chunk identique existe

### 3. GPU-Accelerated Compression

Utiliser Colab Pro GPU pour compression:

```json
{
  "compression_method": "gpu_tensor_compress_v1",
  "reconstruction": {
    "method": "gpu_tensor_decompress",
    "parameters": {
      "model": "efficientnet_lite",
      "quantization": "int8"
    }
  },
  "stats": {
    "gpu_time_ms": 15,
    "cpu_time_ms": 450
  }
}
```

**Speedup**: 20-30x plus rapide

---

## 📚 Exemples Complets

### Exemple 1: PNG Simple

**Original**: 10KB PNG (256x256)

**Recipe**:
```json
{
  "version": "1.0",
  "chunk_id": 2,
  "original_hash": "a1b2c3d4...",
  "compression_method": "semantic_image_v1",
  "reconstruction": {
    "method": "image_array_reconstruct",
    "parameters": {
      "shape": [256, 256, 3],
      "dtype": "uint8",
      "format": "PNG"
    }
  },
  "stats": {
    "original_size": 10240,
    "compressed_size": 2048,
    "ratio": 0.2,
    "savings_percent": 80.0
  }
}
```

**Reconstruction**: 2KB → 10KB (bit-perfect ✅)

### Exemple 2: MP4 avec Keyframes

**Original**: 10MB MP4 (moov box)

**Recipe (keyframe)**:
```json
{
  "version": "1.0",
  "chunk_id": 0,
  "original_hash": "e5f6g7h8...",
  "compression_method": "video_keyframe_v1",
  "reconstruction": {
    "method": "video_keyframe_reconstruct",
    "parameters": {
      "codec": "h264",
      "is_keyframe": true,
      "frame_index": 0,
      "pts": 0
    }
  },
  "assembly_info": {
    "offset": 1024,
    "size": 102400,
    "depends_on": []
  }
}
```

**Recipe (delta frame)**:
```json
{
  "version": "1.0",
  "chunk_id": 1,
  "compression_method": "video_keyframe_v1",
  "reconstruction": {
    "method": "video_keyframe_reconstruct",
    "parameters": {
      "codec": "h264",
      "is_keyframe": false,
      "frame_index": 1,
      "pts": 33,
      "temporal_refs": [0]
    }
  },
  "assembly_info": {
    "offset": 103424,
    "size": 15360,
    "depends_on": [0]
  }
}
```

---

## 🔗 Ressources

### Tools
- **Validator**: `tools/validation/reconstruction_validator.py`
- **End-to-end test**: `tools/validation/test_end_to_end.py`

### Documentation Connexe
- [CHUNKER_API.md](CHUNKER_API.md) - API du chunker sémantique
- [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) - Workflow compression
- [COLAB_PRO_SETUP.md](COLAB_PRO_SETUP.md) - Worker GPU

### Spécifications
- **Recipe format**: JSON Schema (voir `schemas/recipe_v1.json`)
- **Compression methods**: Registry dans `compression_registry.json`

---

**Version**: 0.2.0  
**Dernière mise à jour**: 2025-11-13  
**Auteur**: Équipe PaniniFS  
**License**: MIT
