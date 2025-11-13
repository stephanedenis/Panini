#!/usr/bin/env python3
"""Test semantic chunking for multiple video formats"""

import sys
from pathlib import Path
import struct

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "modules" /
                        "core" / "filesystem" / "src"))

from panini_fs_chunker import FormatDetector, SemanticChunker


def create_minimal_mp4() -> bytes:
    """Créer MP4 minimal (ISO BMFF)"""
    data = bytearray()
    
    # ftyp box
    ftyp_content = b'mp42' + struct.pack('>I', 0) + b'mp42isom'
    ftyp_size = 8 + len(ftyp_content)
    data.extend(struct.pack('>I', ftyp_size) + b'ftyp' + ftyp_content)
    
    # moov with mvhd
    mvhd_content = b'\x00' * 100
    mvhd_size = 8 + len(mvhd_content)
    mvhd_box = struct.pack('>I', mvhd_size) + b'mvhd' + mvhd_content
    moov_size = 8 + len(mvhd_box)
    data.extend(struct.pack('>I', moov_size) + b'moov' + mvhd_box)
    
    # mdat box
    mdat_content = b'\x00' * 256
    mdat_size = 8 + len(mdat_content)
    data.extend(struct.pack('>I', mdat_size) + b'mdat' + mdat_content)
    
    return bytes(data)


def create_minimal_mov() -> bytes:
    """Créer MOV minimal (QuickTime ISO BMFF)"""
    data = bytearray()
    
    # ftyp box with 'qt  ' brand
    ftyp_content = b'qt  ' + struct.pack('>I', 0) + b'qt  '
    ftyp_size = 8 + len(ftyp_content)
    data.extend(struct.pack('>I', ftyp_size) + b'ftyp' + ftyp_content)
    
    # moov
    mvhd_content = b'\x00' * 80
    mvhd_size = 8 + len(mvhd_content)
    mvhd_box = struct.pack('>I', mvhd_size) + b'mvhd' + mvhd_content
    moov_size = 8 + len(mvhd_box)
    data.extend(struct.pack('>I', moov_size) + b'moov' + mvhd_box)
    
    # mdat
    mdat_content = b'\x00' * 200
    mdat_size = 8 + len(mdat_content)
    data.extend(struct.pack('>I', mdat_size) + b'mdat' + mdat_content)
    
    return bytes(data)


def create_minimal_webm() -> bytes:
    """Créer WebM minimal (EBML)"""
    data = bytearray()
    
    # EBML Header (0x1A45DFA3)
    data.extend(b'\x1a\x45\xdf\xa3')
    # Size (VINT approximatif)
    data.extend(b'\x9f')  # Size ~31 bytes
    # DocType: 'webm'
    data.extend(b'\x42\x82\x84webm')  # DocType element
    data.extend(b'\x42\x87\x81\x02')  # Version 2
    data.extend(b'\x42\x85\x81\x02')  # ReadVersion 2
    data.extend(b'\x00' * 10)  # Padding
    
    # Segment (0x18538067) - simplified
    data.extend(b'\x18\x53\x80\x67')
    data.extend(b'\x01\x00\x00\x00\x00\x00\x01\x00')  # Size ~256
    data.extend(b'\x00' * 256)  # Data
    
    return bytes(data)


def create_minimal_avi() -> bytes:
    """Créer AVI minimal (RIFF)"""
    data = bytearray()
    
    # RIFF header
    total_size = 300  # Approximate
    data.extend(b'RIFF')
    data.extend(struct.pack('<I', total_size - 8))
    data.extend(b'AVI ')
    
    # LIST hdrl (headers)
    hdrl_data = b'avih' + struct.pack('<I', 56) + b'\x00' * 56
    data.extend(b'LIST')
    data.extend(struct.pack('<I', len(hdrl_data) + 4))
    data.extend(b'hdrl')
    data.extend(hdrl_data)
    
    # LIST movi (movie data)
    movi_data = b'00dc' + struct.pack('<I', 100) + b'\x00' * 100
    data.extend(b'LIST')
    data.extend(struct.pack('<I', len(movi_data) + 4))
    data.extend(b'movi')
    data.extend(movi_data)
    
    # idx1 (index)
    data.extend(b'idx1')
    data.extend(struct.pack('<I', 16))
    data.extend(b'\x00' * 16)
    
    return bytes(data)


def test_video_format(name: str, video_data: bytes,
                      expected_format: str, expected_patterns: list):
    """Test un format vidéo"""
    print(f"\n{'='*60}")
    print(f"🎬 Test {name}")
    print(f"{'='*60}")
    
    # Detect format
    format_info = FormatDetector.detect(video_data)
    if not format_info or len(format_info) < 3:
        print(f"❌ Format non détecté!")
        return False
    
    format_name, media_type, grammar_id = format_info
    print(f"✓ Format: {format_name} ({media_type})")
    print(f"✓ Grammar: {grammar_id}")
    print(f"✓ Taille: {len(video_data)} bytes")
    
    if format_name != expected_format:
        print(f"❌ Format attendu: {expected_format}, "
              f"obtenu: {format_name}")
        return False
    
    # Chunk
    chunker = SemanticChunker(grammar_id=grammar_id)
    chunks = chunker.chunk(video_data)
    
    print(f"\n📦 Chunks: {len(chunks)}")
    for i, (offset, size, pattern) in enumerate(chunks, 1):
        print(f"  {i}. offset={offset:5d}, size={size:5d}, "
              f"pattern={pattern}")
    
    # Verify
    success = True
    
    if len(chunks) < 2:
        print(f"\n❌ Trop peu de chunks ({len(chunks)} < 2)")
        success = False
    else:
        print(f"\n✓ Chunks créés: {len(chunks)}")
    
    # Check coverage
    total_size = sum(size for _, size, _ in chunks)
    if total_size == len(video_data):
        print(f"✓ Coverage complet: {total_size} bytes")
    else:
        print(f"❌ Coverage incomplet: {total_size}/{len(video_data)}")
        success = False
    
    # Check expected patterns
    found_patterns = [pattern for _, _, pattern in chunks]
    for pattern in expected_patterns:
        if any(pattern in p for p in found_patterns):
            print(f"✓ Pattern {pattern} trouvé")
        else:
            print(f"⚠️  Pattern {pattern} non trouvé")
    
    # Check semantic vs fixed-size
    if len(chunks) <= 10:
        print(f"✓ Découpage sémantique (pas taille fixe)")
    else:
        print(f"⚠️  Beaucoup de chunks ({len(chunks)}), "
              f"vérifier découpage")
    
    return success


def main():
    """Test tous les formats vidéo"""
    print("🎥 TEST FORMATS VIDÉO - DÉCOUPAGE SÉMANTIQUE")
    print("=" * 60)
    
    tests = [
        ("MP4 (ISO BMFF)", create_minimal_mp4(), "MP4",
         ["ISOBMFF_FTYP", "ISOBMFF_MOOV", "ISOBMFF_MDAT"]),
        
        ("MOV (QuickTime)", create_minimal_mov(), "MOV",
         ["ISOBMFF_FTYP", "ISOBMFF_MOOV", "ISOBMFF_MDAT"]),
        
        ("WebM (EBML)", create_minimal_webm(), "WebM",
         ["EBML_HEADER", "EBML_SEGMENT"]),
        
        ("AVI (RIFF)", create_minimal_avi(), "AVI",
         ["AVI_RIFF_HEADER", "AVI_LIST_HEADERS", "AVI_LIST_MOVIE"]),
    ]
    
    results = {}
    for test_args in tests:
        name = test_args[0]
        results[name] = test_video_format(*test_args)
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 RÉSUMÉ")
    print(f"{'='*60}")
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    
    for name, success in results.items():
        status = "✅ SUCCÈS" if success else "❌ ÉCHEC"
        print(f"{status}: {name}")
    
    print(f"\n{passed}/{total} tests réussis ({passed*100//total}%)")
    
    if passed == total:
        print("\n🎉 TOUS LES FORMATS VIDÉO SUPPORTÉS!")
        return 0
    else:
        print(f"\n⚠️  {total-passed} format(s) à corriger")
        return 1


if __name__ == '__main__':
    sys.exit(main())
