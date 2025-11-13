#!/usr/bin/env python3
"""Test semantic MP4 chunking with box structure detection"""

import sys
from pathlib import Path
import struct

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "modules" / "core" / "filesystem" / "src"))

from panini_fs_chunker import FormatDetector, SemanticChunker


def create_minimal_mp4() -> bytes:
    """
    Crée un fichier MP4 minimal valide avec:
    - ftyp box (file type)
    - moov box (metadata minimal)
    - mdat box (media data vide)
    """
    data = bytearray()
    
    # ftyp box (file type: MP4 version 2)
    # Format: size(4) + type(4) + brand(4) + minorversion(4) + brands...
    ftyp_content = b'mp42' + struct.pack('>I', 0) + b'mp42isom'
    ftyp_size = 8 + len(ftyp_content)
    data.extend(struct.pack('>I', ftyp_size) + b'ftyp' + ftyp_content)
    
    # moov box (minimal movie header)
    # mvhd (movie header box inside moov)
    mvhd_content = b'\x00' * 100  # Version/flags + timescale/duration/etc
    mvhd_size = 8 + len(mvhd_content)
    mvhd_box = struct.pack('>I', mvhd_size) + b'mvhd' + mvhd_content
    
    # moov container with mvhd inside
    moov_size = 8 + len(mvhd_box)
    data.extend(struct.pack('>I', moov_size) + b'moov' + mvhd_box)
    
    # mdat box (media data - vide pour ce test)
    mdat_content = b'\x00' * 256  # 256 bytes de données fictives
    mdat_size = 8 + len(mdat_content)
    data.extend(struct.pack('>I', mdat_size) + b'mdat' + mdat_content)
    
    return bytes(data)


def test_mp4_semantic_chunking():
    """Test que MP4 est découpé en boxes sémantiques, pas taille fixe"""
    
    print("🎬 Test MP4 Semantic Chunking")
    print("=" * 60)
    
    # Créer fichier MP4 minimal
    mp4_data = create_minimal_mp4()
    print(f"✓ Fichier MP4 minimal créé: {len(mp4_data)} bytes")
    
    # Détecter format (méthode classmethod)
    format_info = FormatDetector.detect(mp4_data)
    
    if not format_info or len(format_info) < 3:
        print("❌ Format MP4 non détecté!")
        return False
    
    format_name, media_type, grammar_id = format_info
    print(f"✓ Format détecté: {format_name} ({media_type})")
    print(f"✓ Grammar: {grammar_id}")
    
    if grammar_id != 'mp4_v1':
        print(f"❌ Grammar attendue: mp4_v1, obtenue: {grammar_id}")
        return False
    
    # Chunker (utilise la classe SemanticChunker interne)
    semantic_chunker = SemanticChunker(grammar_id=grammar_id)
    chunks = semantic_chunker.chunk(mp4_data)
    
    print(f"\n📦 Chunks créés: {len(chunks)}")
    print("-" * 60)
    
    # Analyser chunks
    expected_patterns = ['MP4_FTYP', 'MP4_MOOV_METADATA', 'MP4_MDAT_MEDIA']
    found_patterns = []
    
    for i, (offset, size, pattern) in enumerate(chunks):
        print(f"  Chunk {i+1}: offset={offset}, size={size}, pattern={pattern}")
        found_patterns.append(pattern)
    
    # Vérifications
    print("\n🔍 Vérifications:")
    print("-" * 60)
    
    success = True
    
    # 1. Doit avoir au moins 3 chunks (ftyp, moov, mdat)
    if len(chunks) < 3:
        print(f"❌ Attendu ≥3 chunks, obtenu {len(chunks)}")
        success = False
    else:
        print(f"✓ Nombre de chunks correct: {len(chunks)}")
    
    # 2. Patterns attendus
    for pattern in expected_patterns:
        if pattern in found_patterns:
            print(f"✓ Pattern {pattern} trouvé")
        else:
            print(f"❌ Pattern {pattern} manquant")
            success = False
    
    # 3. Vérifier que ce n'est PAS du découpage taille fixe
    # Si c'était taille fixe, on aurait des chunks de ~64KB
    # Notre fichier fait ~400 bytes, donc découpage sémantique = peu de chunks
    if len(chunks) <= 5:  # Sémantique: ~3 boxes
        print(f"✓ Découpage sémantique (pas taille fixe)")
    else:
        print(f"❌ Trop de chunks ({len(chunks)}), semble être taille fixe")
        success = False
    
    # 4. Coverage complet
    total_size = sum(size for _, size, _ in chunks)
    if total_size == len(mp4_data):
        print(f"✓ Coverage complet: {total_size} bytes")
    else:
        print(f"❌ Coverage incomplet: {total_size}/{len(mp4_data)} bytes")
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✅ TEST MP4 SEMANTIC CHUNKING: SUCCÈS")
        print("\n💡 Les keyframes (I-frames) sont dans mdat.")
        print("   Pour extraction complète, il faudrait parser:")
        print("   moov > trak > mdia > minf > stbl > stss")
        print("   (stss = sync sample table = indices keyframes)")
    else:
        print("❌ TEST MP4 SEMANTIC CHUNKING: ÉCHEC")
    
    return success


if __name__ == '__main__':
    success = test_mp4_semantic_chunking()
    sys.exit(0 if success else 1)
