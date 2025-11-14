#!/usr/bin/env python3
"""
Benchmark Audio Fingerprinting Performance

Compare CPU vs GPU pour traitement batch de fichiers audio.
Mesure temps, throughput, et utilisation mémoire.

Usage:
    python experiments/benchmark_audio_fingerprinting.py --num-samples 100
"""

import sys
import os
import argparse
import time
import json
from pathlib import Path
from datetime import datetime

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np

# Try importing audio fingerprinting
try:
    from modules.core.filesystem.src.panini_audio_fingerprint import (
        AudioFingerprintExtractor,
        AudioSimilarityIndex
    )
except ImportError as e:
    print(f"❌ Erreur import: {e}")
    print("⚠️  Assurez-vous que le module est dans PYTHONPATH")
    sys.exit(1)

# Try importing GPU mock
try:
    from utils.gpu_mock import setup_device, get_device_info, print_device_info
    HAS_GPU_MOCK = True
except ImportError:
    HAS_GPU_MOCK = False
    print("⚠️  GPU mock non disponible, tests CPU uniquement")


def generate_test_audio(num_samples: int, duration_sec: float = 5.0, 
                        sample_rate: int = 44100) -> list:
    """
    Génère fichiers audio synthétiques pour benchmark
    
    Args:
        num_samples: Nombre de fichiers à générer
        duration_sec: Durée de chaque fichier
        sample_rate: Taux d'échantillonnage
    
    Returns:
        list: Liste de tuples (audio_data, sample_rate, file_id)
    """
    print(f"\n🎵 Génération de {num_samples} fichiers audio synthétiques...")
    
    audio_files = []
    num_samples_per_file = int(duration_sec * sample_rate)
    
    for i in range(num_samples):
        # Créer signal complexe (mélange de fréquences)
        t = np.linspace(0, duration_sec, num_samples_per_file)
        
        # Plusieurs fréquences pour simuler musique
        frequencies = [220, 440, 880, 1760]  # Notes musicales
        audio = np.zeros(num_samples_per_file, dtype=np.float32)
        
        for freq in frequencies:
            amplitude = np.random.uniform(0.1, 0.3)
            audio += amplitude * np.sin(2 * np.pi * freq * t)
        
        # Ajouter bruit léger
        noise = np.random.randn(num_samples_per_file) * 0.01
        audio += noise
        
        # Normaliser
        audio = audio / np.max(np.abs(audio))
        
        audio_files.append((audio, sample_rate, f"test_audio_{i:04d}"))
    
    print(f"✅ {len(audio_files)} fichiers générés")
    return audio_files


def benchmark_fingerprinting(audio_files: list, device_name: str = "CPU") -> dict:
    """
    Benchmark extraction de fingerprints
    
    Args:
        audio_files: Liste de tuples (audio, sr, file_id)
        device_name: Nom du device pour logs
    
    Returns:
        dict: Métriques de performance
    """
    print(f"\n🚀 Benchmark sur {device_name}...")
    print(f"   Fichiers: {len(audio_files)}")
    
    extractor = AudioFingerprintExtractor()
    
    # Warmup (ignore premier run)
    _ = extractor.extract_fingerprint(audio_files[0][0], audio_files[0][1])
    
    # Benchmark extraction
    start_time = time.time()
    fingerprints = []
    
    for i, (audio, sr, file_id) in enumerate(audio_files):
        if (i + 1) % 10 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            print(f"   Progress: {i+1}/{len(audio_files)} ({rate:.1f} files/sec)")
        
        fp = extractor.extract_fingerprint(audio, sr)
        fingerprints.append((file_id, fp))
    
    extraction_time = time.time() - start_time
    
    print(f"✅ Extraction terminée: {extraction_time:.2f}s")
    
    # Benchmark indexing
    print(f"\n📊 Indexation des fingerprints...")
    start_time = time.time()
    
    index = AudioSimilarityIndex()
    for file_id, fp in fingerprints:
        index.add_fingerprint(file_id, fp)
    
    indexing_time = time.time() - start_time
    print(f"✅ Indexation terminée: {indexing_time:.2f}s")
    
    # Benchmark search
    print(f"\n🔍 Benchmark recherche...")
    num_queries = min(10, len(fingerprints))
    query_fingerprints = [fp for _, fp in fingerprints[:num_queries]]
    
    start_time = time.time()
    for fp in query_fingerprints:
        matches = index.search_similar(fp, top_k=5)
    
    search_time = time.time() - start_time
    avg_search_time = search_time / num_queries
    
    print(f"✅ {num_queries} recherches: {search_time:.3f}s (avg: {avg_search_time*1000:.1f}ms)")
    
    # Métriques
    total_time = extraction_time + indexing_time
    throughput = len(audio_files) / extraction_time
    
    # Statistiques fingerprints
    num_hashes = [len(fp.hash_pairs) for _, fp in fingerprints]
    avg_hashes = np.mean(num_hashes)
    
    metrics = {
        'device': device_name,
        'num_files': len(audio_files),
        'extraction_time': extraction_time,
        'indexing_time': indexing_time,
        'total_time': total_time,
        'throughput_files_per_sec': throughput,
        'avg_hashes_per_file': avg_hashes,
        'search_time_ms': avg_search_time * 1000,
        'timestamp': datetime.now().isoformat()
    }
    
    return metrics


def compare_performance(metrics_cpu: dict, metrics_gpu: dict) -> None:
    """Affiche comparaison CPU vs GPU"""
    print("\n" + "="*60)
    print("📊 COMPARAISON PERFORMANCE CPU vs GPU")
    print("="*60)
    
    speedup_extraction = metrics_cpu['extraction_time'] / metrics_gpu['extraction_time']
    speedup_total = metrics_cpu['total_time'] / metrics_gpu['total_time']
    
    print(f"\nExtraction:")
    print(f"  CPU:  {metrics_cpu['extraction_time']:.2f}s")
    print(f"  GPU:  {metrics_gpu['extraction_time']:.2f}s")
    print(f"  Speedup: {speedup_extraction:.2f}x")
    
    print(f"\nIndexation:")
    print(f"  CPU:  {metrics_cpu['indexing_time']:.2f}s")
    print(f"  GPU:  {metrics_gpu['indexing_time']:.2f}s")
    
    print(f"\nTotal:")
    print(f"  CPU:  {metrics_cpu['total_time']:.2f}s")
    print(f"  GPU:  {metrics_gpu['total_time']:.2f}s")
    print(f"  Speedup: {speedup_total:.2f}x")
    
    print(f"\nThroughput:")
    print(f"  CPU:  {metrics_cpu['throughput_files_per_sec']:.1f} files/sec")
    print(f"  GPU:  {metrics_gpu['throughput_files_per_sec']:.1f} files/sec")
    
    print(f"\nRecherche (moyenne):")
    print(f"  CPU:  {metrics_cpu['search_time_ms']:.1f}ms")
    print(f"  GPU:  {metrics_gpu['search_time_ms']:.1f}ms")
    
    print("\n" + "="*60)


def save_results(metrics: dict, output_dir: Path) -> None:
    """Sauvegarde résultats en JSON"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"benchmark_{metrics['device'].lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\n💾 Résultats sauvegardés: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Benchmark audio fingerprinting')
    parser.add_argument('--num-samples', type=int, default=100,
                        help='Nombre de fichiers audio à générer (default: 100)')
    parser.add_argument('--duration', type=float, default=5.0,
                        help='Durée de chaque fichier en secondes (default: 5.0)')
    parser.add_argument('--output-dir', type=str, default=None,
                        help='Dossier pour résultats (default: $EXPERIMENT_OUTPUT_DIR ou outputs/)')
    
    args = parser.parse_args()
    
    # Output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    elif 'EXPERIMENT_OUTPUT_DIR' in os.environ:
        output_dir = Path(os.environ['EXPERIMENT_OUTPUT_DIR'])
    else:
        output_dir = Path('outputs/benchmark_audio_fingerprinting')
    
    print("="*60)
    print("🎵 AUDIO FINGERPRINTING BENCHMARK")
    print("="*60)
    print(f"Samples: {args.num_samples}")
    print(f"Duration: {args.duration}s")
    print(f"Output: {output_dir}")
    
    # Afficher infos device
    if HAS_GPU_MOCK:
        print("\n" + "="*60)
        print_device_info()
        print("="*60)
    
    # Générer audio
    audio_files = generate_test_audio(args.num_samples, args.duration)
    
    # Benchmark (CPU uniquement pour l'instant - audio fingerprinting utilise NumPy)
    metrics = benchmark_fingerprinting(audio_files, device_name="CPU")
    
    # Afficher résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    print(f"Device: {metrics['device']}")
    print(f"Fichiers traités: {metrics['num_files']}")
    print(f"Temps extraction: {metrics['extraction_time']:.2f}s")
    print(f"Temps indexation: {metrics['indexing_time']:.2f}s")
    print(f"Temps total: {metrics['total_time']:.2f}s")
    print(f"Throughput: {metrics['throughput_files_per_sec']:.1f} files/sec")
    print(f"Hashes moyen/file: {metrics['avg_hashes_per_file']:.0f}")
    print(f"Temps recherche: {metrics['search_time_ms']:.1f}ms")
    print("="*60)
    
    # Sauvegarder
    save_results(metrics, output_dir)
    
    print("\n✅ Benchmark terminé!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
