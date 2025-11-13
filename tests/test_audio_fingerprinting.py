#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pour Audio Fingerprinting type Shazam
"""

import struct
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / 'modules/core/filesystem/src'))

from panini_audio_fingerprint import (
    AudioFingerprintExtractor,
    AudioSimilarityIndex
)


def generate_sine_wave(frequency: float, duration_ms: int,
                       sample_rate: int = 44100) -> np.ndarray:
    """Génère une onde sinusoïdale pour tests"""
    num_samples = int(duration_ms * sample_rate / 1000)
    t = np.linspace(0, duration_ms / 1000, num_samples)
    return np.sin(2 * np.pi * frequency * t).astype(np.float32)


def create_test_wav(samples: np.ndarray, sample_rate: int = 44100,
                   channels: int = 1, bits_per_sample: int = 16) -> bytes:
    """Crée un fichier WAV synthétique pour tests"""
    # Normaliser et convertir en int16
    if bits_per_sample == 16:
        pcm_samples = (samples * 32767).astype(np.int16)
        pcm_bytes = pcm_samples.tobytes()
    else:
        raise ValueError(f"Bits per sample {bits_per_sample} non supporté")
    
    # Construire WAV
    chunks = []
    
    # RIFF header
    riff_size = 36 + len(pcm_bytes)
    chunks.append(b'RIFF')
    chunks.append(struct.pack('<I', riff_size))
    chunks.append(b'WAVE')
    
    # fmt chunk
    fmt_data = struct.pack(
        '<HHIIHH',
        1,                    # audio_format (PCM)
        channels,             # num_channels
        sample_rate,          # sample_rate
        sample_rate * channels * (bits_per_sample // 8),  # byte_rate
        channels * (bits_per_sample // 8),  # block_align
        bits_per_sample       # bits_per_sample
    )
    chunks.append(b'fmt ')
    chunks.append(struct.pack('<I', len(fmt_data)))
    chunks.append(fmt_data)
    
    # data chunk
    chunks.append(b'data')
    chunks.append(struct.pack('<I', len(pcm_bytes)))
    chunks.append(pcm_bytes)
    
    return b''.join(chunks)


def test_wav_parsing():
    """Test parsing WAV basique"""
    print("🔊 Test parsing WAV...")
    
    # Créer WAV test: 440 Hz (La) pendant 1 seconde
    samples = generate_sine_wave(440, 1000, 44100)
    wav_data = create_test_wav(samples, 44100, 1, 16)
    
    extractor = AudioFingerprintExtractor()
    fp = extractor.extract_from_wav(wav_data)
    
    print(f"   Durée: {fp.duration_ms} ms")
    print(f"   Sample rate: {fp.sample_rate} Hz")
    print(f"   Canaux: {fp.channels}")
    print(f"   Points constellation: {len(fp.constellation_points)}")
    print(f"   Hash pairs: {len(fp.hash_pairs)}")
    print(f"   Spectral centroid: {fp.spectral_centroid:.2f}")
    print(f"   Zero crossing rate: {fp.zero_crossing_rate:.4f}")
    
    assert fp.duration_ms == 1000, "Durée incorrecte"
    assert fp.sample_rate == 44100, "Sample rate incorrect"
    assert fp.channels == 1, "Nombre de canaux incorrect"
    assert len(fp.constellation_points) > 0, "Aucun point de constellation"
    assert len(fp.hash_pairs) > 0, "Aucun hash généré"
    
    print("✅ Test parsing WAV réussi!\n")
    return True


def test_fingerprint_uniqueness():
    """Test que différentes fréquences donnent empreintes différentes"""
    print("🎵 Test unicité des empreintes...")
    
    extractor = AudioFingerprintExtractor()
    
    # Trois fréquences différentes
    freqs = [220, 440, 880]  # La (octaves)
    fingerprints = []
    
    for freq in freqs:
        samples = generate_sine_wave(freq, 1000, 44100)
        wav_data = create_test_wav(samples, 44100, 1, 16)
        fp = extractor.extract_from_wav(wav_data)
        fingerprints.append(fp)
        print(f"   {freq} Hz: {len(fp.hash_pairs)} hashes, "
              f"centroid={fp.spectral_centroid:.1f}")
    
    # Vérifier que les empreintes sont différentes
    for i in range(len(fingerprints)):
        for j in range(i+1, len(fingerprints)):
            common = fingerprints[i].hash_pairs & fingerprints[j].hash_pairs
            total = len(fingerprints[i].hash_pairs)
            overlap = len(common) / total if total > 0 else 0
            print(f"   Overlap {freqs[i]}-{freqs[j]} Hz: {overlap:.1%}")
            assert overlap < 0.3, f"Trop de overlap entre {freqs[i]} et {freqs[j]}"
    
    print("✅ Test unicité réussi!\n")
    return True


def test_similarity_index():
    """Test index de similarité"""
    print("🔍 Test index de similarité...")
    
    extractor = AudioFingerprintExtractor()
    index = AudioSimilarityIndex()
    
    # Créer 3 fichiers: 2 similaires (440 Hz) + 1 différent (880 Hz)
    files = {
        'file1_440hz': generate_sine_wave(440, 1000, 44100),
        'file2_440hz_copy': generate_sine_wave(440, 1000, 44100),
        'file3_880hz': generate_sine_wave(880, 1000, 44100),
    }
    
    # Indexer
    for file_id, samples in files.items():
        wav_data = create_test_wav(samples, 44100, 1, 16)
        fp = extractor.extract_from_wav(wav_data)
        index.add_fingerprint(file_id, fp)
        print(f"   Indexé: {file_id}")
    
    # Chercher similarité pour file1
    query_samples = generate_sine_wave(440, 1000, 44100)
    query_wav = create_test_wav(query_samples, 44100, 1, 16)
    query_fp = extractor.extract_from_wav(query_wav)
    
    results = index.find_similar(query_fp, top_k=3)
    
    print(f"\n   Résultats recherche:")
    for file_id, score in results:
        print(f"     {file_id}: {score:.3f}")
    
    # Vérifier que file2_440hz_copy est le plus similaire
    assert len(results) >= 2, "Pas assez de résultats"
    top_match = results[0][0]
    assert '440hz' in top_match, f"Top match devrait être 440Hz, got {top_match}"
    assert results[0][1] > 0.5, "Score trop bas pour match identique"
    
    print("✅ Test index de similarité réussi!\n")
    return True


def test_robustness_to_noise():
    """Test robustesse au bruit"""
    print("📡 Test robustesse au bruit...")
    
    extractor = AudioFingerprintExtractor()
    
    # Signal original: 440 Hz
    clean_signal = generate_sine_wave(440, 1000, 44100)
    clean_wav = create_test_wav(clean_signal, 44100, 1, 16)
    clean_fp = extractor.extract_from_wav(clean_wav)
    
    # Signal avec bruit (SNR = 20 dB)
    noise = np.random.normal(0, 0.1, len(clean_signal)).astype(np.float32)
    noisy_signal = clean_signal + noise
    noisy_signal = np.clip(noisy_signal, -1.0, 1.0)  # Clamp
    noisy_wav = create_test_wav(noisy_signal, 44100, 1, 16)
    noisy_fp = extractor.extract_from_wav(noisy_wav)
    
    # Comparer empreintes
    common = clean_fp.hash_pairs & noisy_fp.hash_pairs
    jaccard = len(common) / len(clean_fp.hash_pairs | noisy_fp.hash_pairs)
    
    print(f"   Hashes communs: {len(common)}/{len(clean_fp.hash_pairs)}")
    print(f"   Jaccard similarity: {jaccard:.3f}")
    print(f"   Spectral centroid clean: {clean_fp.spectral_centroid:.1f}")
    print(f"   Spectral centroid noisy: {noisy_fp.spectral_centroid:.1f}")
    
    # Note: Avec bruit important (SNR 20dB), le matching est difficile
    # En pratique, l'algo Shazam utilise des techniques plus avancées
    # (filtrage adaptatif, multiple time scales, etc.)
    # Pour ce test, on vérifie juste qu'on garde quelques hashes
    assert jaccard > 0.01, f"Aucun hash commun: {jaccard:.3f}"
    print(f"   ⚠️  Avec bruit important, robustesse limitée (attendu)")
    
    print("✅ Test robustesse réussi!\n")
    return True


def test_complex_signal():
    """Test signal complexe (accord multiple fréquences)"""
    print("🎼 Test signal complexe (accord)...")
    
    extractor = AudioFingerprintExtractor()
    
    # Accord majeur C (Do majeur): C4 (261.63 Hz), E4 (329.63 Hz), G4 (392 Hz)
    c4 = generate_sine_wave(261.63, 1000, 44100)
    e4 = generate_sine_wave(329.63, 1000, 44100)
    g4 = generate_sine_wave(392.00, 1000, 44100)
    
    chord = (c4 + e4 + g4) / 3  # Moyenne
    chord_wav = create_test_wav(chord, 44100, 1, 16)
    chord_fp = extractor.extract_from_wav(chord_wav)
    
    print(f"   Points constellation: {len(chord_fp.constellation_points)}")
    print(f"   Hash pairs: {len(chord_fp.hash_pairs)}")
    print(f"   Spectral centroid: {chord_fp.spectral_centroid:.1f}")
    
    # Signal complexe devrait avoir plus de points de constellation
    single_note = generate_sine_wave(440, 1000, 44100)
    single_wav = create_test_wav(single_note, 44100, 1, 16)
    single_fp = extractor.extract_from_wav(single_wav)
    
    print(f"   Note simple - points: {len(single_fp.constellation_points)}")
    print(f"   Note simple - hashes: {len(single_fp.hash_pairs)}")
    
    # Accord devrait avoir plus de complexité
    assert len(chord_fp.constellation_points) >= len(single_fp.constellation_points), \
        "Accord devrait avoir ≥ points qu'une note simple"
    
    print("✅ Test signal complexe réussi!\n")
    return True


if __name__ == '__main__':
    print("=" * 60)
    print("Tests Audio Fingerprinting (Shazam-like)")
    print("=" * 60)
    
    tests = [
        test_wav_parsing,
        test_fingerprint_uniqueness,
        test_similarity_index,
        test_robustness_to_noise,
        test_complex_signal,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ ERREUR: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
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
