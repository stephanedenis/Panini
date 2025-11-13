# 🔄 Pipeline Asynchrone - Intégration avec Décomposeur Existant

**Date**: 2025-11-12  
**Statut**: Adaptation pour utiliser infrastructure existante

## 🎯 Approche Révisée

Au lieu de réinventer le chunker, nous **intégrons** le décomposeur sémantique existant dans le pipeline asynchrone.

## 📚 Composants Existants à Utiliser

### 1. **Generic Decomposer** (Python)
- **Localisation**: `research/panini-fs/prototypes/decomposers/generic_decomposer.py`
- **Capacités**: 
  - Décomposition basée sur grammaires JSON
  - Support ~44 formats (PNG, JPEG, GIF, WebP, WAV, MP4, PDF, ZIP, etc.)
  - Patterns universels réutilisables
  - Décomposition récursive et hiérarchique

### 2. **Grammaires de Formats**
- **Localisation**: `research/panini-fs/format_grammars/*.json`
- **Formats supportés**: PNG, JPEG, GIF, WebP, TIFF, WAV, MP3, MP4, PDF, ZIP, GZIP, BMP, etc.
- **Patterns universels**: MAGIC_NUMBER, LENGTH_PREFIXED_DATA, TYPED_CHUNK, CRC_CHECKSUM, etc.

### 3. **PaniniFS Rust** (Production)
- **Localisation**: `research/archives/.../CORE/panini-fs/src/`
- **Modules**:
  - `semantic/decomposer.rs`: Décomposeur production
  - `semantic/analyzer.rs`: Analyseur sémantique
  - Core types: Atom, Context, Relationship

## 🔧 Adaptation du Pipeline

### Étape 1: Wrapper pour Décomposeur Existant

```python
# modules/core/filesystem/src/panini_fs_async_chunker.py

from pathlib import Path
import json
import hashlib
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / 'research' / 'panini-fs' / 'prototypes' / 'decomposers'))

from generic_decomposer import GenericDecomposer


class AsyncChunkAdapter:
    """
    Adapte le GenericDecomposer pour pipeline asynchrone
    """
    
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.grammar_dir = Path(__file__).parent.parent.parent.parent.parent / 'research' / 'panini-fs' / 'format_grammars'
    
    def chunk_file_semantic(self, file_path: Path) -> dict:
        """
        Utilise GenericDecomposer pour obtenir chunks sémantiques
        """
        # Détection automatique du format
        grammar_file = self._detect_grammar(file_path)
        
        if not grammar_file:
            raise ValueError(f"Format non supporté ou grammaire introuvable pour: {file_path}")
        
        print(f"📂 Décomposition sémantique: {file_path}")
        print(f"   Grammaire: {grammar_file.name}")
        
        # Décomposition via GenericDecomposer
        decomposer = GenericDecomposer(file_path, grammar_file)
        result = decomposer.decompose()
        
        # Conversion en chunks pour pipeline async
        chunks = self._convert_to_async_chunks(result, file_path)
        
        return {
            'file': str(file_path),
            'grammar': str(grammar_file),
            'total_chunks': len(chunks),
            'chunks': chunks,
            'decomposition_result': result
        }
    
    def _detect_grammar(self, file_path: Path) -> Optional[Path]:
        """Détecte grammaire appropriée"""
        data = file_path.read_bytes()
        
        # Magic number detection
        magic_map = {
            b'\x89PNG': 'png.json',
            b'\xff\xd8\xff': 'jpeg.json',
            b'GIF87a': 'gif.json',
            b'GIF89a': 'gif.json',
            b'RIFF': self._detect_riff_subtype(data),
            b'%PDF': 'pdf.json',
            b'PK\x03\x04': 'zip.json',
            b'\x1f\x8b': 'gzip.json',
        }
        
        for magic, grammar_name in magic_map.items():
            if data.startswith(magic):
                if callable(grammar_name):
                    grammar_name = grammar_name()
                grammar_file = self.grammar_dir / grammar_name
                if grammar_file.exists():
                    return grammar_file
        
        return None
    
    def _detect_riff_subtype(self, data: bytes) -> str:
        """Détecte sous-type RIFF"""
        if len(data) >= 12:
            riff_type = data[8:12]
            if riff_type == b'WAVE':
                return 'wav.json'
            elif riff_type == b'WEBP':
                return 'webp.json'
            elif riff_type == b'AVI ':
                return 'avi.json'
        return 'riff.json'
    
    def _convert_to_async_chunks(self, decomposition: dict, file_path: Path) -> list:
        """
        Convertit résultat décomposition en chunks pour async processing
        """
        chunks = []
        data = file_path.read_bytes()
        
        # Extraire éléments décomposés
        elements = decomposition.get('elements', [])
        
        for i, element in enumerate(elements):
            offset = element.get('offset', 0)
            size = element.get('size', 0)
            pattern = element.get('pattern', 'UNKNOWN')
            
            # Extraire données chunk
            chunk_data = data[offset:offset+size]
            chunk_hash = hashlib.sha256(chunk_data).hexdigest()
            
            chunks.append({
                'chunk_id': i,
                'offset': offset,
                'size': size,
                'hash': chunk_hash,
                'pattern_type': pattern,
                'element': element,  # Métadonnées complètes du décomposeur
                'status': 'pending'
            })
        
        return chunks
    
    def save_for_async_processing(self, decomposition_result: dict, base_name: str):
        """
        Sauvegarde chunks pour traitement asynchrone Colab
        """
        chunks_dir = self.output_dir / base_name
        chunks_dir.mkdir(parents=True, exist_ok=True)
        
        data = Path(decomposition_result['file']).read_bytes()
        
        for chunk_info in decomposition_result['chunks']:
            chunk_dir = chunks_dir / f"chunk_{chunk_info['chunk_id']:04d}"
            chunk_dir.mkdir(parents=True, exist_ok=True)
            
            # Données binaires
            offset = chunk_info['offset']
            size = chunk_info['size']
            chunk_data = data[offset:offset+size]
            (chunk_dir / 'data.bin').write_bytes(chunk_data)
            
            # Métadonnées enrichies avec info décomposeur
            metadata = {
                'chunk_id': chunk_info['chunk_id'],
                'offset': offset,
                'size': size,
                'original_hash': chunk_info['hash'],
                'pattern_type': chunk_info['pattern_type'],
                'grammar_id': Path(decomposition_result['grammar']).stem,
                'status': 'pending',
                'element_details': chunk_info['element']  # Inclut structure complète
            }
            (chunk_dir / 'metadata.json').write_text(json.dumps(metadata, indent=2))
            
            # Recipe utilisant structure décomposeur
            recipe = self._generate_recipe_from_element(
                chunk_info['element'],
                chunk_info['chunk_id'],
                decomposition_result['total_chunks']
            )
            (chunk_dir / 'reconstruction.recipe').write_text(json.dumps(recipe, indent=2))
        
        # Manifest incluant résultat décomposition complet
        manifest = {
            'base_name': base_name,
            'source_file': decomposition_result['file'],
            'grammar': decomposition_result['grammar'],
            'total_chunks': decomposition_result['total_chunks'],
            'decomposition_summary': {
                'valid': decomposition_result['decomposition_result'].get('valid', False),
                'format': decomposition_result['decomposition_result'].get('format', 'unknown'),
                'patterns_found': len(decomposition_result['decomposition_result'].get('elements', []))
            }
        }
        (chunks_dir / 'manifest.json').write_text(json.dumps(manifest, indent=2))
        
        return chunks_dir
    
    def _generate_recipe_from_element(self, element: dict, chunk_id: int, total_chunks: int) -> dict:
        """Génère recipe en utilisant structure du décomposeur"""
        return {
            'version': '1.0',
            'chunk_id': chunk_id,
            'pattern': element.get('pattern'),
            'reconstruction_steps': [
                {
                    'step': 1,
                    'operation': 'LOAD_FROM_DECOMPOSER',
                    'element': element
                },
                {
                    'step': 2,
                    'operation': 'VALIDATE_STRUCTURE',
                    'description': 'Validate using grammar rules'
                },
                {
                    'step': 3,
                    'operation': 'SEMANTIC_COMPRESS',
                    'description': 'Extract dhātu patterns'
                },
                {
                    'step': 4,
                    'operation': 'ASSEMBLE',
                    'offset': element.get('offset'),
                    'size': element.get('size')
                }
            ],
            'assembly_info': {
                'offset': element.get('offset'),
                'size': element.get('size'),
                'total_chunks': total_chunks,
                'ordering': chunk_id
            }
        }


def main():
    """CLI adapté pour décomposeur existant"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='PaniniFS Async Chunker - Utilise décomposeur sémantique existant'
    )
    parser.add_argument('file', type=Path, help='File to decompose')
    parser.add_argument('--output', type=Path, default=Path('pending_compression'),
                       help='Output directory')
    
    args = parser.parse_args()
    
    adapter = AsyncChunkAdapter(args.output)
    
    try:
        result = adapter.chunk_file_semantic(args.file)
        
        print(f"\n✅ Décomposition réussie!")
        print(f"   Format: {result['decomposition_result'].get('format')}")
        print(f"   Chunks: {result['total_chunks']}")
        
        # Sauvegarder pour async processing
        chunks_dir = adapter.save_for_async_processing(result, args.file.stem)
        print(f"   Répertoire: {chunks_dir}")
        print(f"\n🚀 Prêt pour: git add {chunks_dir} && git commit && git push")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

## 🎯 Avantages de l'Approche

1. **Réutilisation Code Existant**: Pas de réinvention, utilise décomposeur mature
2. **44 Formats Supportés**: Immédiatement disponible
3. **Grammaires Extensibles**: Ajouter formats via JSON
4. **Structure Riche**: Décomposeur fournit métadonnées détaillées
5. **Migration Rust Future**: Interface compatible avec version Rust production

## 📝 Prochaines Étapes

1. ✅ Adapter chunker pour utiliser `generic_decomposer.py`
2. Tester avec formats variés (PNG, JPEG, PDF, WebP)
3. Valider compatibilité avec GitHub Actions workflow
4. Intégrer avec Colab worker
5. Plan migration vers version Rust quand prête

---

**Note**: Cette approche respecte le travail existant et permet une évolution progressive vers la version Rust de production.
