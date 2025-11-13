#!/usr/bin/env python3
"""
PaniniFS Reconstruction Validator

Validates bit-perfect reconstruction from compressed chunks.

Pipeline:
1. Load compressed chunk from Google One
2. Read reconstruction recipe
3. Decompress using recipe instructions
4. Reconstruct original file from chunks
5. Validate SHA-256 hash matches original

Usage:
    python reconstruction_validator.py <chunk_dir> <original_file>
    python reconstruction_validator.py --batch <chunks_parent_dir>
"""

import json
import hashlib
import gzip
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import argparse


@dataclass
class ValidationResult:
    """Result of validation"""
    chunk_id: int
    original_hash: str
    reconstructed_hash: str
    is_valid: bool
    error: Optional[str] = None
    stats: Optional[Dict] = None


class ReconstructionValidator:
    """Validates bit-perfect reconstruction from compressed chunks"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.results: List[ValidationResult] = []
    
    def log(self, message: str):
        """Log message if verbose"""
        if self.verbose:
            print(message)
    
    def load_compressed_chunk(self, chunk_dir: Path) -> Tuple[bytes, Dict]:
        """Load compressed data and recipe from chunk directory"""
        self.log(f"📦 Loading chunk: {chunk_dir}")
        
        # Load compressed data
        compressed_file = chunk_dir / 'compressed.bin'
        if not compressed_file.exists():
            raise FileNotFoundError(f"Compressed file not found: {compressed_file}")
        
        compressed_data = compressed_file.read_bytes()
        self.log(f"  ✅ Loaded compressed data: {len(compressed_data)} bytes")
        
        # Load recipe
        recipe_file = chunk_dir / 'recipe.json'
        if not recipe_file.exists():
            raise FileNotFoundError(f"Recipe file not found: {recipe_file}")
        
        with open(recipe_file) as f:
            recipe = json.load(f)
        
        self.log(f"  ✅ Loaded recipe: {recipe['compression_method']}")
        
        return compressed_data, recipe
    
    def decompress_chunk(self, compressed_data: bytes, recipe: Dict) -> bytes:
        """Decompress chunk using recipe instructions"""
        self.log(f"🔧 Decompressing chunk...")
        
        compression_method = recipe['compression_method']
        reconstruction = recipe['reconstruction']
        
        # Handle different compression methods
        if 'gzip' in reconstruction.get('method', ''):
            decompressed = gzip.decompress(compressed_data)
            self.log(f"  ✅ Decompressed: {len(decompressed)} bytes (gzip)")
            return decompressed
        
        elif reconstruction.get('method') == 'semantic_image_v1':
            # Image reconstruction
            import numpy as np
            from PIL import Image
            import io
            
            decompressed = gzip.decompress(compressed_data)
            shape = tuple(reconstruction['shape'])
            dtype = reconstruction['dtype']
            
            # Reconstruct array
            img_array = np.frombuffer(decompressed, dtype=dtype).reshape(shape)
            
            # Convert back to image bytes
            img = Image.fromarray(img_array.astype('uint8'))
            img_bytes = io.BytesIO()
            img.save(img_bytes, format=reconstruction.get('format', 'PNG'))
            
            result = img_bytes.getvalue()
            self.log(f"  ✅ Reconstructed image: {len(result)} bytes")
            return result
        
        else:
            raise ValueError(f"Unknown reconstruction method: {reconstruction.get('method')}")
    
    def validate_hash(self, data: bytes, expected_hash: str) -> bool:
        """Validate SHA-256 hash"""
        actual_hash = hashlib.sha256(data).hexdigest()
        is_valid = actual_hash == expected_hash
        
        if is_valid:
            self.log(f"  ✅ Hash validation: PASSED")
            self.log(f"     Expected: {expected_hash[:16]}...")
            self.log(f"     Actual:   {actual_hash[:16]}...")
        else:
            self.log(f"  ❌ Hash validation: FAILED")
            self.log(f"     Expected: {expected_hash}")
            self.log(f"     Actual:   {actual_hash}")
        
        return is_valid
    
    def validate_chunk(self, chunk_dir: Path) -> ValidationResult:
        """Validate single chunk reconstruction"""
        try:
            self.log(f"\n{'='*60}")
            self.log(f"🔍 Validating chunk: {chunk_dir.name}")
            self.log(f"{'='*60}")
            
            # Load compressed chunk and recipe
            compressed_data, recipe = self.load_compressed_chunk(chunk_dir)
            
            chunk_id = recipe.get('chunk_id', -1)
            expected_hash = recipe.get('original_hash', '')
            
            # Decompress
            decompressed_data = self.decompress_chunk(compressed_data, recipe)
            
            # Validate hash
            is_valid = self.validate_hash(decompressed_data, expected_hash)
            
            # Calculate stats
            stats = {
                'compressed_size': len(compressed_data),
                'decompressed_size': len(decompressed_data),
                'compression_ratio': len(compressed_data) / len(decompressed_data),
                'savings_percent': (1 - len(compressed_data) / len(decompressed_data)) * 100
            }
            
            if 'stats' in recipe:
                stats.update(recipe['stats'])
            
            result = ValidationResult(
                chunk_id=chunk_id,
                original_hash=expected_hash,
                reconstructed_hash=hashlib.sha256(decompressed_data).hexdigest(),
                is_valid=is_valid,
                stats=stats
            )
            
            self.results.append(result)
            
            if is_valid:
                self.log(f"\n✅ Chunk {chunk_id}: VALIDATION PASSED")
            else:
                self.log(f"\n❌ Chunk {chunk_id}: VALIDATION FAILED")
            
            return result
            
        except Exception as e:
            self.log(f"\n❌ Error validating chunk: {e}")
            import traceback
            if self.verbose:
                traceback.print_exc()
            
            result = ValidationResult(
                chunk_id=-1,
                original_hash='',
                reconstructed_hash='',
                is_valid=False,
                error=str(e)
            )
            self.results.append(result)
            return result
    
    def validate_batch(self, parent_dir: Path) -> List[ValidationResult]:
        """Validate all chunks in directory"""
        self.log(f"\n{'='*60}")
        self.log(f"📂 Batch validation: {parent_dir}")
        self.log(f"{'='*60}\n")
        
        # Find all chunk directories
        chunk_dirs = sorted([d for d in parent_dir.iterdir() if d.is_dir() and d.name.startswith('chunk_')])
        
        if not chunk_dirs:
            self.log(f"⚠️ No chunk directories found in {parent_dir}")
            return []
        
        self.log(f"Found {len(chunk_dirs)} chunks to validate\n")
        
        # Validate each chunk
        results = []
        for chunk_dir in chunk_dirs:
            result = self.validate_chunk(chunk_dir)
            results.append(result)
        
        return results
    
    def reconstruct_from_chunks(self, chunks_dir: Path, output_file: Path) -> bool:
        """Reconstruct complete file from multiple chunks"""
        self.log(f"\n{'='*60}")
        self.log(f"🔨 Reconstructing file from chunks")
        self.log(f"{'='*60}")
        
        # Find all chunks
        chunk_dirs = sorted([d for d in chunks_dir.iterdir() if d.is_dir() and d.name.startswith('chunk_')])
        
        if not chunk_dirs:
            self.log(f"❌ No chunks found in {chunks_dir}")
            return False
        
        self.log(f"Found {len(chunk_dirs)} chunks")
        
        # Load chunks with their offsets from recipes
        chunks_with_offsets = []
        for chunk_dir in chunk_dirs:
            compressed_data, recipe = self.load_compressed_chunk(chunk_dir)
            decompressed = self.decompress_chunk(compressed_data, recipe)
            
            # Get offset from recipe
            offset = recipe.get('reconstruction', {}).get('offset')
            if offset is None:
                # Fallback to assembly_info
                offset = recipe.get('assembly_info', {}).get('offset', 0)
            
            chunks_with_offsets.append((offset, decompressed))
        
        # Sort by offset
        chunks_with_offsets.sort(key=lambda x: x[0])
        
        # Reconstruct in order
        reconstructed_data = bytearray()
        for offset, decompressed in chunks_with_offsets:
            reconstructed_data.extend(decompressed)
        
        # Write reconstructed file
        output_file.write_bytes(reconstructed_data)
        self.log(f"\n✅ Reconstructed file: {output_file}")
        self.log(f"   Total size: {len(reconstructed_data)} bytes")
        
        # Calculate final hash
        final_hash = hashlib.sha256(reconstructed_data).hexdigest()
        self.log(f"   SHA-256: {final_hash}")
        
        return True
    
    def print_summary(self):
        """Print validation summary"""
        if not self.results:
            print("\nℹ️ No validation results")
            return
        
        print(f"\n{'='*60}")
        print("📊 VALIDATION SUMMARY")
        print(f"{'='*60}\n")
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.is_valid)
        failed = total - passed
        
        print(f"Total chunks:  {total}")
        print(f"✅ Passed:     {passed}")
        print(f"❌ Failed:     {failed}")
        print(f"Success rate:  {passed/total*100:.1f}%\n")
        
        if failed > 0:
            print("Failed chunks:")
            for result in self.results:
                if not result.is_valid:
                    error_msg = result.error or "Hash mismatch"
                    print(f"  - Chunk {result.chunk_id}: {error_msg}")
            print()
        
        # Compression stats
        total_compressed = sum(r.stats.get('compressed_size', 0) for r in self.results if r.stats)
        total_original = sum(r.stats.get('decompressed_size', 0) for r in self.results if r.stats)
        
        if total_original > 0:
            overall_ratio = total_compressed / total_original
            overall_savings = (1 - overall_ratio) * 100
            
            print("Compression Statistics:")
            print(f"  Original size:    {self._format_size(total_original)}")
            print(f"  Compressed size:  {self._format_size(total_compressed)}")
            print(f"  Compression ratio: {overall_ratio:.3f}")
            print(f"  Space savings:    {overall_savings:.1f}%")
            print()
        
        print(f"{'='*60}\n")
    
    def _format_size(self, size_bytes: int) -> str:
        """Format size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
    
    def export_results(self, output_file: Path):
        """Export validation results to JSON"""
        results_data = []
        for result in self.results:
            results_data.append({
                'chunk_id': result.chunk_id,
                'original_hash': result.original_hash,
                'reconstructed_hash': result.reconstructed_hash,
                'is_valid': result.is_valid,
                'error': result.error,
                'stats': result.stats
            })
        
        with open(output_file, 'w') as f:
            json.dump({
                'validation_timestamp': __import__('datetime').datetime.utcnow().isoformat() + 'Z',
                'total_chunks': len(self.results),
                'passed': sum(1 for r in self.results if r.is_valid),
                'failed': sum(1 for r in self.results if not r.is_valid),
                'results': results_data
            }, f, indent=2)
        
        print(f"✅ Results exported to: {output_file}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Validate bit-perfect reconstruction from compressed chunks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate single chunk
  python reconstruction_validator.py /path/to/chunk_0000
  
  # Validate all chunks in directory
  python reconstruction_validator.py --batch /path/to/compressed_chunks
  
  # Reconstruct complete file
  python reconstruction_validator.py --reconstruct /path/to/chunks --output original.bin
  
  # Export results to JSON
  python reconstruction_validator.py --batch /path/to/chunks --export results.json
        """
    )
    
    parser.add_argument('chunk_dir', nargs='?', type=Path,
                        help='Path to chunk directory or parent directory')
    parser.add_argument('--batch', type=Path,
                        help='Validate all chunks in directory')
    parser.add_argument('--reconstruct', type=Path,
                        help='Reconstruct file from chunks directory')
    parser.add_argument('--output', type=Path,
                        help='Output file for reconstruction')
    parser.add_argument('--export', type=Path,
                        help='Export validation results to JSON')
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress verbose output')
    
    args = parser.parse_args()
    
    # Create validator
    validator = ReconstructionValidator(verbose=not args.quiet)
    
    try:
        # Batch validation
        if args.batch:
            validator.validate_batch(args.batch)
        
        # Single chunk validation
        elif args.chunk_dir:
            validator.validate_chunk(args.chunk_dir)
        
        # Reconstruction
        elif args.reconstruct:
            if not args.output:
                print("❌ Error: --output required for reconstruction")
                sys.exit(1)
            
            validator.reconstruct_from_chunks(args.reconstruct, args.output)
        
        else:
            parser.print_help()
            sys.exit(1)
        
        # Print summary
        validator.print_summary()
        
        # Export results
        if args.export:
            validator.export_results(args.export)
        
        # Exit code based on validation results
        if validator.results and not all(r.is_valid for r in validator.results):
            sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
