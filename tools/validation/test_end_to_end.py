#!/usr/bin/env python3
"""
PaniniFS End-to-End Pipeline Test

Tests complete pipeline:
1. Create test file
2. Chunk file with panini_fs_chunker
3. Simulate GitHub Actions dispatch (or actually push to GitHub)
4. Wait for Colab processing (manual or automated)
5. Download compressed chunks from Google One
6. Validate reconstruction
7. Verify bit-perfect match

Usage:
    python test_end_to_end.py --mode local     # Local simulation (no GitHub/Colab)
    python test_end_to_end.py --mode full      # Full pipeline with GitHub/Colab
    python test_end_to_end.py --quick          # Quick test with small file
"""

import sys
import json
import hashlib
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Optional
import argparse
import time
from datetime import datetime


class EndToEndTester:
    """End-to-end pipeline tester"""
    
    def __init__(self, work_dir: Path, mode: str = 'local', verbose: bool = True):
        self.work_dir = Path(work_dir)
        self.mode = mode
        self.verbose = verbose
        self.test_results = {}
        
        # Create work directory
        self.work_dir.mkdir(parents=True, exist_ok=True)
        
        self.log(f"🧪 End-to-End Test Initialized")
        self.log(f"   Mode: {mode}")
        self.log(f"   Work dir: {work_dir}\n")
    
    def log(self, message: str):
        """Log message if verbose"""
        if self.verbose:
            print(message)
    
    def create_test_file(self, file_type: str = 'text', size: str = 'small') -> Path:
        """Create test file"""
        self.log(f"📝 Creating test file ({file_type}, {size})...")
        
        test_file = self.work_dir / f'test_{file_type}_{size}.dat'
        
        if file_type == 'text':
            # Create text file
            content = []
            content.append("PaniniFS End-to-End Test File\n")
            content.append("=" * 50 + "\n\n")
            content.append(f"Generated: {datetime.utcnow().isoformat()}Z\n")
            content.append(f"Size: {size}\n\n")
            
            # Add repeated content based on size
            if size == 'small':
                lines = 100
            elif size == 'medium':
                lines = 1000
            else:  # large
                lines = 10000
            
            for i in range(lines):
                content.append(f"Line {i:06d}: Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n")
            
            test_file.write_text(''.join(content))
        
        elif file_type == 'binary':
            # Create binary file with patterns
            import numpy as np
            
            if size == 'small':
                data_size = 1024 * 10  # 10KB
            elif size == 'medium':
                data_size = 1024 * 100  # 100KB
            else:  # large
                data_size = 1024 * 1024  # 1MB
            
            # Create pattern (easier to compress)
            data = np.arange(data_size // 8, dtype=np.uint8)
            data = np.tile(data, 8)[:data_size]
            
            test_file.write_bytes(data.tobytes())
        
        elif file_type == 'image':
            # Create test image
            from PIL import Image
            import numpy as np
            
            if size == 'small':
                img_size = (64, 64)
            elif size == 'medium':
                img_size = (256, 256)
            else:  # large
                img_size = (512, 512)
            
            # Create gradient image
            x = np.linspace(0, 255, img_size[0])
            y = np.linspace(0, 255, img_size[1])
            xx, yy = np.meshgrid(x, y)
            img_array = ((xx + yy) / 2).astype(np.uint8)
            
            img = Image.fromarray(img_array, mode='L')
            img.save(test_file, 'PNG')
        
        # Calculate hash
        file_hash = hashlib.sha256(test_file.read_bytes()).hexdigest()
        file_size = test_file.stat().st_size
        
        self.log(f"  ✅ Created: {test_file.name}")
        self.log(f"     Size: {file_size} bytes")
        self.log(f"     SHA-256: {file_hash[:16]}...\n")
        
        self.test_results['original_file'] = {
            'path': str(test_file),
            'size': file_size,
            'hash': file_hash,
            'type': file_type
        }
        
        return test_file
    
    def chunk_file(self, test_file: Path) -> Path:
        """Chunk file using panini_fs_chunker"""
        self.log(f"✂️ Chunking file: {test_file.name}...")
        
        # Find chunker script
        chunker_script = Path(__file__).parent.parent.parent / 'modules/core/filesystem/src/panini_fs_chunker.py'
        
        if not chunker_script.exists():
            raise FileNotFoundError(f"Chunker script not found: {chunker_script}")
        
        # Create output directory
        output_dir = self.work_dir / 'pending_compression'
        output_dir.mkdir(exist_ok=True)
        
        # Run chunker
        cmd = [
            sys.executable,
            str(chunker_script),
            str(test_file),
            '--output', str(output_dir),
            '--chunk-size', '1024'  # Small chunks for testing
        ]
        
        self.log(f"  Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            self.log(f"  ❌ Chunker failed:")
            self.log(result.stderr)
            raise RuntimeError("Chunking failed")
        
        # Find created chunks
        chunk_dirs = list(output_dir.glob('*/chunk_*'))
        
        self.log(f"  ✅ Created {len(chunk_dirs)} chunks")
        
        self.test_results['chunks'] = {
            'count': len(chunk_dirs),
            'directory': str(output_dir),
            'chunks': [str(c) for c in chunk_dirs]
        }
        
        return output_dir
    
    def simulate_compression(self, chunks_dir: Path) -> Path:
        """Simulate compression (local mode)"""
        self.log(f"\n🔧 Simulating compression...")
        
        import gzip
        
        # Create compressed output directory
        compressed_dir = self.work_dir / 'compressed_chunks'
        compressed_dir.mkdir(exist_ok=True)
        
        # Process each chunk
        chunk_dirs = sorted(chunks_dir.glob('*/chunk_*'))
        
        for i, chunk_dir in enumerate(chunk_dirs):
            self.log(f"  Processing chunk {i}...")
            
            # Load metadata
            metadata_file = chunk_dir / 'metadata.json'
            if not metadata_file.exists():
                self.log(f"    ⚠️ No metadata found, skipping")
                continue
            
            with open(metadata_file) as f:
                metadata = json.load(f)
            
            # Find content file (try both names)
            content_file = chunk_dir / 'data.bin'
            if not content_file.exists():
                content_file = chunk_dir / 'content'
            if not content_file.exists():
                self.log(f"    ⚠️ No content file found, skipping")
                continue
            
            # Compress
            content_data = content_file.read_bytes()
            compressed_data = gzip.compress(content_data, compresslevel=9)
            
            # Create output directory
            output_chunk_dir = compressed_dir / f"chunk_{i:04d}"
            output_chunk_dir.mkdir(exist_ok=True)
            
            # Save compressed data
            (output_chunk_dir / 'compressed.bin').write_bytes(compressed_data)
            
            # Create recipe
            recipe = {
                'chunk_id': i,
                'original_hash': metadata.get('original_hash', ''),
                'compression_method': 'generic_gzip_v1',
                'reconstruction': {
                    'method': 'gzip_decompress'
                },
                'stats': {
                    'original_size': len(content_data),
                    'compressed_size': len(compressed_data),
                    'ratio': len(compressed_data) / len(content_data),
                    'savings_percent': (1 - len(compressed_data) / len(content_data)) * 100
                },
                'uploaded_at': datetime.utcnow().isoformat() + 'Z',
                'worker': 'local_simulation'
            }
            
            (output_chunk_dir / 'recipe.json').write_text(json.dumps(recipe, indent=2))
            
            self.log(f"    ✅ Compressed: {len(content_data)} → {len(compressed_data)} bytes")
        
        self.log(f"\n  ✅ All chunks compressed: {compressed_dir}\n")
        
        self.test_results['compression'] = {
            'directory': str(compressed_dir),
            'chunks_compressed': len(list(compressed_dir.glob('chunk_*')))
        }
        
        return compressed_dir
    
    def validate_reconstruction(self, compressed_dir: Path) -> bool:
        """Validate reconstruction using validator"""
        self.log(f"✅ Validating reconstruction...")
        
        # Find validator script
        validator_script = Path(__file__).parent / 'reconstruction_validator.py'
        
        if not validator_script.exists():
            raise FileNotFoundError(f"Validator script not found: {validator_script}")
        
        # Run validator
        cmd = [
            sys.executable,
            str(validator_script),
            '--batch', str(compressed_dir),
            '--export', str(self.work_dir / 'validation_results.json')
        ]
        
        self.log(f"  Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Print validator output
        if result.stdout:
            self.log(result.stdout)
        
        if result.returncode != 0:
            self.log(f"  ❌ Validation failed")
            if result.stderr:
                self.log(result.stderr)
            return False
        
        # Load validation results
        results_file = self.work_dir / 'validation_results.json'
        if results_file.exists():
            with open(results_file) as f:
                validation_data = json.load(f)
            
            self.test_results['validation'] = validation_data
            
            all_passed = validation_data['passed'] == validation_data['total_chunks']
            return all_passed
        
        return False
    
    def reconstruct_and_compare(self, compressed_dir: Path) -> bool:
        """Reconstruct file and compare with original"""
        self.log(f"\n🔨 Reconstructing file and comparing...")
        
        # Reconstruct file
        reconstructed_file = self.work_dir / 'reconstructed.dat'
        
        validator_script = Path(__file__).parent / 'reconstruction_validator.py'
        
        cmd = [
            sys.executable,
            str(validator_script),
            '--reconstruct', str(compressed_dir),
            '--output', str(reconstructed_file),
            '--quiet'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            self.log(f"  ❌ Reconstruction failed")
            return False
        
        # Compare with original
        original_file = Path(self.test_results['original_file']['path'])
        original_hash = self.test_results['original_file']['hash']
        
        reconstructed_hash = hashlib.sha256(reconstructed_file.read_bytes()).hexdigest()
        
        match = original_hash == reconstructed_hash
        
        if match:
            self.log(f"  ✅ Bit-perfect match!")
            self.log(f"     Original:      {original_hash[:16]}...")
            self.log(f"     Reconstructed: {reconstructed_hash[:16]}...")
        else:
            self.log(f"  ❌ Hash mismatch!")
            self.log(f"     Original:      {original_hash}")
            self.log(f"     Reconstructed: {reconstructed_hash}")
        
        self.test_results['reconstruction_match'] = match
        
        return match
    
    def print_summary(self):
        """Print test summary"""
        print(f"\n{'='*60}")
        print("🎯 END-TO-END TEST SUMMARY")
        print(f"{'='*60}\n")
        
        print(f"Original file:")
        print(f"  Path: {self.test_results['original_file']['path']}")
        print(f"  Size: {self.test_results['original_file']['size']} bytes")
        print(f"  Hash: {self.test_results['original_file']['hash'][:16]}...")
        print()
        
        if 'chunks' in self.test_results:
            print(f"Chunking:")
            print(f"  Chunks created: {self.test_results['chunks']['count']}")
            print()
        
        if 'compression' in self.test_results:
            print(f"Compression:")
            print(f"  Chunks compressed: {self.test_results['compression']['chunks_compressed']}")
            print()
        
        if 'validation' in self.test_results:
            val = self.test_results['validation']
            print(f"Validation:")
            print(f"  Total chunks: {val['total_chunks']}")
            print(f"  ✅ Passed: {val['passed']}")
            print(f"  ❌ Failed: {val['failed']}")
            print()
        
        if 'reconstruction_match' in self.test_results:
            match = self.test_results['reconstruction_match']
            print(f"Final Reconstruction:")
            if match:
                print(f"  ✅ BIT-PERFECT MATCH VERIFIED!")
            else:
                print(f"  ❌ MISMATCH DETECTED")
            print()
        
        # Overall result
        all_passed = (
            self.test_results.get('reconstruction_match', False) and
            (self.test_results.get('validation', {}).get('failed', 1) == 0)
        )
        
        print(f"{'='*60}")
        if all_passed:
            print("✅ ALL TESTS PASSED - Pipeline working correctly!")
        else:
            print("❌ TESTS FAILED - Issues detected in pipeline")
        print(f"{'='*60}\n")
        
        return all_passed
    
    def run_full_test(self, file_type: str = 'text', size: str = 'small') -> bool:
        """Run complete end-to-end test"""
        try:
            start_time = time.time()
            
            # 1. Create test file
            test_file = self.create_test_file(file_type, size)
            
            # 2. Chunk file
            chunks_dir = self.chunk_file(test_file)
            
            if self.mode == 'local':
                # 3. Simulate compression locally
                compressed_dir = self.simulate_compression(chunks_dir)
            else:
                # 3. Full pipeline (GitHub + Colab)
                self.log("\n⚠️ Full pipeline mode not yet implemented")
                self.log("   This would:")
                self.log("   - Push chunks to GitHub")
                self.log("   - Trigger GitHub Actions")
                self.log("   - Wait for Colab processing")
                self.log("   - Download from Google One")
                self.log("\n   For now, using local simulation...\n")
                compressed_dir = self.simulate_compression(chunks_dir)
            
            # 4. Validate reconstruction
            validation_passed = self.validate_reconstruction(compressed_dir)
            
            # 5. Reconstruct and compare
            reconstruction_passed = self.reconstruct_and_compare(compressed_dir)
            
            elapsed_time = time.time() - start_time
            self.test_results['elapsed_time'] = elapsed_time
            
            # 6. Print summary
            all_passed = self.print_summary()
            
            print(f"Test completed in {elapsed_time:.2f} seconds\n")
            
            return all_passed
        
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="End-to-end pipeline test for PaniniFS",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--mode', choices=['local', 'full'], default='local',
                        help='Test mode: local (simulation) or full (GitHub+Colab)')
    parser.add_argument('--type', choices=['text', 'binary', 'image'], default='text',
                        help='Test file type')
    parser.add_argument('--size', choices=['small', 'medium', 'large'], default='small',
                        help='Test file size')
    parser.add_argument('--work-dir', type=Path, default=Path('/tmp/panini_e2e_test'),
                        help='Working directory for test')
    parser.add_argument('--quick', action='store_true',
                        help='Quick test (small text file)')
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress verbose output')
    
    args = parser.parse_args()
    
    # Quick test shortcut
    if args.quick:
        args.type = 'text'
        args.size = 'small'
        args.mode = 'local'
    
    # Create tester
    tester = EndToEndTester(
        work_dir=args.work_dir,
        mode=args.mode,
        verbose=not args.quiet
    )
    
    # Run test
    print(f"\n{'='*60}")
    print("🚀 PaniniFS End-to-End Pipeline Test")
    print(f"{'='*60}\n")
    
    success = tester.run_full_test(file_type=args.type, size=args.size)
    
    # Export results
    results_file = args.work_dir / 'test_results.json'
    with open(results_file, 'w') as f:
        json.dump(tester.test_results, f, indent=2)
    print(f"📄 Test results exported to: {results_file}\n")
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
