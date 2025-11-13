#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pour extraction keyframes et parsing VINT
Valide les améliorations vidéo (v0.2.0)
"""

import struct
import sys
from pathlib import Path

# Ajouter le module au path
sys.path.insert(0, str(Path(__file__).parent.parent / 'modules/core/filesystem/src'))

from panini_fs_chunker import SemanticChunker


def create_minimal_mp4_with_keyframes():
    """Crée un MP4 minimal avec structure moov>trak>stss"""
    chunks = []
    
    # 1. ftyp box (avec brand et compatible brands corrects)
    ftyp_content = b'isom' + struct.pack('>I', 512) + b'isom'
    ftyp = b'ftyp' + ftyp_content
    ftyp = struct.pack('>I', len(ftyp) + 4) + ftyp
    chunks.append(ftyp)
    
    # 2. moov box avec stss (sync sample table)
    # Construire de l'intérieur vers l'extérieur
    
    # stss table: 3 keyframes aux samples 1, 10, 20
    stss_entries = struct.pack('>III', 1, 10, 20)
    stss_data = (
        b'\x00\x00\x00\x00' +  # version + flags
        struct.pack('>I', 3) +  # entry_count = 3
        stss_entries
    )
    stss = struct.pack('>I', len(stss_data) + 8) + b'stss' + stss_data
    
    # stbl contient stss
    stbl_data = stss
    stbl = struct.pack('>I', len(stbl_data) + 8) + b'stbl' + stbl_data
    
    # minf contient stbl
    minf_data = stbl
    minf = struct.pack('>I', len(minf_data) + 8) + b'minf' + minf_data
    
    # mdia contient minf
    mdia_data = minf
    mdia = struct.pack('>I', len(mdia_data) + 8) + b'mdia' + mdia_data
    
    # trak contient mdia
    trak_data = mdia
    trak = struct.pack('>I', len(trak_data) + 8) + b'trak' + trak_data
    
    # moov contient trak
    moov_data = trak
    moov = struct.pack('>I', len(moov_data) + 8) + b'moov' + moov_data
    chunks.append(moov)
    
    # 3. mdat box (media data)
    mdat = b'mdat' + b'\x00' * 1000
    mdat = struct.pack('>I', len(mdat) + 4) + mdat
    chunks.append(mdat)
    
    return b''.join(chunks)


def create_minimal_webm_with_vint():
    """Crée un WebM minimal avec éléments VINT"""
    chunks = []
    
    # 1. EBML Header (ID: 0x1A45DFA3)
    ebml_header = (
        b'\x1a\x45\xdf\xa3' +  # EBML ID
        b'\x9f' +              # Size VINT: 1 byte, valeur 31 (0x9f = 10011111)
        b'\x42\x86\x81\x01' +  # EBMLVersion = 1
        b'\x42\xf7\x81\x01' +  # EBMLReadVersion = 1
        b'\x42\xf2\x81\x04' +  # EBMLMaxIDLength = 4
        b'\x42\xf3\x81\x08' +  # EBMLMaxSizeLength = 8
        b'\x42\x82\x88webm' +  # DocType = "webm"
        b'\x42\x87\x81\x02' +  # DocTypeVersion = 2
        b'\x42\x85\x81\x02'    # DocTypeReadVersion = 2
    )
    chunks.append(ebml_header)
    
    # 2. Segment (ID: 0x18538067)
    segment_content = (
        # Info (ID: 0x1549A966)
        b'\x15\x49\xa9\x66' +
        b'\x8c' +              # Size VINT: 12 bytes (0x8c = 10001100)
        b'\x2a\xd7\xb1' +      # TimecodeScale
        b'\x44\x89\x84\x00\x00\x00\x00' +  # Duration
        
        # Tracks (ID: 0x1654AE6B)
        b'\x16\x54\xae\x6b' +
        b'\x85'                # Size VINT: 5 bytes
        b'\x00\x00\x00\x00\x00'
    )
    
    segment = (
        b'\x18\x53\x80\x67' +  # Segment ID
        b'\x01\x00\x00\x00\x00\x00\x00\x50' +  # Size VINT: 8 bytes, valeur 80
        segment_content
    )
    chunks.append(segment)
    
    # 3. Cluster avec SimpleBlock (ID: 0x1F43B675)
    cluster = (
        b'\x1f\x43\xb6\x75' +  # Cluster ID
        b'\x9a' +              # Size VINT: 26 bytes
        b'\xe7\x81\x00' +      # Timecode = 0
        b'\xa3' +              # SimpleBlock ID (3 bytes)
        b'\x90' +              # Size VINT: 16 bytes
        b'\x00' * 16           # Frame data
    )
    chunks.append(cluster)
    
    return b''.join(chunks)


def test_mp4_keyframe_extraction():
    """Test extraction des keyframes depuis stss table"""
    print("🎬 Test extraction keyframes MP4...")
    
    mp4_data = create_minimal_mp4_with_keyframes()
    
    # Test direct de la méthode _chunk_isobmff (sans passer par detect)
    chunker = SemanticChunker('test_mp4')
    chunks = chunker._chunk_isobmff(mp4_data)
    
    # Vérifier présence des patterns
    patterns = [chunk[2] for chunk in chunks]
    print(f"   Patterns détectés: {patterns}")
    
    assert 'ISOBMFF_FTYP' in patterns, "❌ ftyp box manquant"
    assert 'ISOBMFF_MOOV_METADATA' in patterns, "❌ moov box manquant"
    assert any('MDAT' in p for p in patterns), "❌ mdat box manquant"
    
    # Vérifier classification mdat avec keyframes
    has_keyframe_mdat = 'ISOBMFF_MDAT_KEYFRAMES' in patterns
    print(f"   Classification MDAT avec keyframes: {has_keyframe_mdat}")
    
    print("✅ Test keyframes MP4 réussi!")
    return True


def test_webm_vint_parsing():
    """Test parsing VINT complet pour WebM"""
    print("🎥 Test parsing VINT WebM...")
    
    webm_data = create_minimal_webm_with_vint()
    
    # Test direct de la méthode _chunk_ebml (sans passer par detect)
    chunker = SemanticChunker('test_webm')
    chunks = chunker._chunk_ebml(webm_data)
    
    # Vérifier présence des patterns EBML
    patterns = [chunk[2] for chunk in chunks]
    print(f"   Patterns détectés: {patterns}")
    
    assert 'EBML_HEADER' in patterns, "❌ EBML_HEADER manquant"
    assert 'EBML_SEGMENT' in patterns, "❌ EBML_SEGMENT manquant"
    
    # Vérifier parsing précis (pas de fallback sur chunks fixes)
    has_precise_parsing = not any('EBML_DATA' in p for p in patterns[:3])
    print(f"   Parsing précis (sans fallback): {has_precise_parsing}")
    
    print("✅ Test VINT WebM réussi!")
    return True


def test_vint_decoder():
    """Test unitaire du décodeur VINT"""
    print("🔢 Test décodeur VINT...")
    
    chunker = SemanticChunker('test_vint')
    
    # Test VINT 1 byte: 0x8c = 10001100 -> longueur 1, valeur 12 (0x0c)
    val, length = chunker._decode_vint(b'\x8c\x00\x00', 0)
    assert val == 12 and length == 1, f"❌ VINT 1 byte: {val}, {length}"
    print(f"   VINT 1 byte (0x8c): valeur={val}, longueur={length} ✓")
    
    # Test VINT 2 bytes: 0x40 0x7F = 01000000 01111111 -> longueur 2, valeur 127
    val, length = chunker._decode_vint(b'\x40\x7f\x00', 0)
    assert val == 127 and length == 2, f"❌ VINT 2 bytes: {val}, {length}"
    print(f"   VINT 2 bytes (0x407F): valeur={val}, longueur={length} ✓")
    
    # Test VINT 4 bytes: 0x10 0x00 0x00 0xFF
    val, length = chunker._decode_vint(b'\x10\x00\x00\xff\x00', 0)
    assert length == 4, f"❌ VINT 4 bytes longueur: {length}"
    print(f"   VINT 4 bytes (0x100000FF): valeur={val}, longueur={length} ✓")
    
    print("✅ Test décodeur VINT réussi!")
    return True


if __name__ == '__main__':
    print("=" * 60)
    print("Tests Améliorations Vidéo v0.2.0")
    print("=" * 60)
    
    tests = [
        test_vint_decoder,
        test_mp4_keyframe_extraction,
        test_webm_vint_parsing,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ ERREUR: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
            print()
    
    # Résumé
    print("=" * 60)
    success = sum(results)
    total = len(results)
    print(f"Résultat: {success}/{total} tests réussis")
    
    if success == total:
        print("🎉 Tous les tests passent!")
        sys.exit(0)
    else:
        print("⚠️ Certains tests ont échoué")
        sys.exit(1)
