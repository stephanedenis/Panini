#!/usr/bin/env python3
"""
Benchmark PaniniFS vs ext4/NTFS
Comparaison performance validation multi-format
"""

import sys
import time
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'analysis'))
from panini_fs_validator import PaniniFSValidator


def create_benchmark_corpus(corpus_dir: Path, size_category: str):
    """
    Crée un corpus de benchmark de différentes tailles
    
    Args:
        corpus_dir: Répertoire du corpus
        size_category: 'small', 'medium', 'large'
    """
    corpus_dir.mkdir(exist_ok=True, parents=True)
    
    sizes = {
        'small': {
            'num_files': 10,
            'file_size': 1024,  # 1 KB
            'description': '10 fichiers, 1 KB chacun'
        },
        'medium': {
            'num_files': 100,
            'file_size': 10240,  # 10 KB
            'description': '100 fichiers, 10 KB chacun'
        },
        'large': {
            'num_files': 1000,
            'file_size': 102400,  # 100 KB
            'description': '1000 fichiers, 100 KB chacun'
        }
    }
    
    config = sizes[size_category]
    print(f"📁 Création corpus {size_category}: {config['description']}")
    
    formats = ['txt', 'md', 'pdf', 'png', 'wav', 'mp4']
    
    for i in range(config['num_files']):
        format_idx = i % len(formats)
        ext = formats[format_idx]
        
        file_path = corpus_dir / f"file_{i:04d}.{ext}"
        
        # Création contenu selon format
        if ext in ['txt', 'md']:
            content = f"Test file {i}\n" * (config['file_size'] // 20)
            file_path.write_text(content, encoding='utf-8')
        else:
            # Données binaires pseudo-aléatoires
            data = bytes([(i + j) % 256 for j in range(config['file_size'])])
            file_path.write_bytes(data)
    
    total_size = sum(f.stat().st_size for f in corpus_dir.glob('*'))
    print(f"✅ Corpus créé: {config['num_files']} fichiers, {total_size:,} bytes")
    
    return config['num_files'], total_size


def benchmark_panini_fs(corpus_dir: Path, num_files: int, total_size: int):
    """Benchmark PaniniFS"""
    print("\n" + "=" * 70)
    print("🔷 BENCHMARK PANINI FS")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as temp_workspace:
        validator = PaniniFSValidator(workspace=Path(temp_workspace))
        
        # Benchmark validation complète
        start_time = time.time()
        
        report = validator.validate_corpus(corpus_dir)
        
        elapsed_time = time.time() - start_time
        
        # Calcul métriques
        metrics = report['metrics']
        throughput = total_size / elapsed_time / (1024 * 1024)  # MB/s
        files_per_second = num_files / elapsed_time
        
        results = {
            'system': 'PaniniFS',
            'total_files': num_files,
            'total_size_mb': total_size / (1024 * 1024),
            'elapsed_time': elapsed_time,
            'throughput_mbps': throughput,
            'files_per_second': files_per_second,
            'integrity_score': metrics['integrity_score'] * 100,
            'successful_validations': metrics['successful_validations'],
            'failed_validations': metrics['failed_validations']
        }
        
        print(f"\n📊 RÉSULTATS PANINI FS:")
        print(f"   Fichiers traités: {results['total_files']}")
        print(f"   Taille totale: {results['total_size_mb']:.2f} MB")
        print(f"   Temps total: {results['elapsed_time']:.3f}s")
        print(f"   Débit: {results['throughput_mbps']:.2f} MB/s")
        print(f"   Fichiers/s: {results['files_per_second']:.1f}")
        print(f"   Score intégrité: {results['integrity_score']:.2f}%")
        
        return results


def benchmark_filesystem_baseline(corpus_dir: Path, num_files: int, total_size: int):
    """
    Benchmark baseline système de fichiers (ext4/NTFS)
    Simule opérations équivalentes: lecture + hash + copie
    """
    print("\n" + "=" * 70)
    print("🔷 BENCHMARK BASELINE FILESYSTEM")
    print("=" * 70)
    
    import hashlib
    
    with tempfile.TemporaryDirectory() as temp_dir:
        copy_dir = Path(temp_dir) / 'copy'
        copy_dir.mkdir()
        
        start_time = time.time()
        
        files_processed = 0
        for file_path in corpus_dir.glob('*'):
            if file_path.is_file():
                # Lecture + hash (équivalent validation)
                with open(file_path, 'rb') as f:
                    data = f.read()
                    hashlib.sha256(data).hexdigest()
                
                # Copie (équivalent compression/décompression)
                shutil.copy2(file_path, copy_dir / file_path.name)
                
                files_processed += 1
        
        elapsed_time = time.time() - start_time
        
        # Calcul métriques
        throughput = total_size / elapsed_time / (1024 * 1024)  # MB/s
        files_per_second = num_files / elapsed_time
        
        results = {
            'system': 'Filesystem Baseline',
            'total_files': num_files,
            'total_size_mb': total_size / (1024 * 1024),
            'elapsed_time': elapsed_time,
            'throughput_mbps': throughput,
            'files_per_second': files_per_second,
            'operations': 'read + hash + copy'
        }
        
        print(f"\n📊 RÉSULTATS FILESYSTEM BASELINE:")
        print(f"   Fichiers traités: {results['total_files']}")
        print(f"   Taille totale: {results['total_size_mb']:.2f} MB")
        print(f"   Temps total: {results['elapsed_time']:.3f}s")
        print(f"   Débit: {results['throughput_mbps']:.2f} MB/s")
        print(f"   Fichiers/s: {results['files_per_second']:.1f}")
        print(f"   Opérations: {results['operations']}")
        
        return results


def compare_results(panini_results, baseline_results):
    """Compare les résultats PaniniFS vs baseline"""
    print("\n" + "=" * 70)
    print("🔷 COMPARAISON PANINI FS vs FILESYSTEM BASELINE")
    print("=" * 70)
    
    # Calcul ratios
    speed_ratio = panini_results['throughput_mbps'] / baseline_results['throughput_mbps']
    files_ratio = panini_results['files_per_second'] / baseline_results['files_per_second']
    
    print(f"\n📈 Débit (MB/s):")
    print(f"   PaniniFS:  {panini_results['throughput_mbps']:.2f} MB/s")
    print(f"   Baseline:  {baseline_results['throughput_mbps']:.2f} MB/s")
    print(f"   Ratio:     {speed_ratio:.2f}x")
    
    print(f"\n📊 Fichiers/seconde:")
    print(f"   PaniniFS:  {panini_results['files_per_second']:.1f} fichiers/s")
    print(f"   Baseline:  {baseline_results['files_per_second']:.1f} fichiers/s")
    print(f"   Ratio:     {files_ratio:.2f}x")
    
    print(f"\n🎯 Avantages PaniniFS:")
    print(f"   ✅ Intégrité garantie: {panini_results['integrity_score']:.2f}%")
    print(f"   ✅ Validation multi-format native")
    print(f"   ✅ Rapports JSON détaillés")
    print(f"   ✅ Métriques par format")
    print(f"   ✅ Support 17 formats")
    
    if speed_ratio >= 0.8:
        print(f"\n✅ Performance comparable au baseline ({speed_ratio:.2f}x)")
    elif speed_ratio >= 0.5:
        print(f"\n⚠️  Performance acceptable ({speed_ratio:.2f}x du baseline)")
    else:
        print(f"\n⚠️  Performance à optimiser ({speed_ratio:.2f}x du baseline)")
    
    return {
        'speed_ratio': speed_ratio,
        'files_ratio': files_ratio,
        'panini_results': panini_results,
        'baseline_results': baseline_results
    }


def generate_benchmark_report(comparisons: dict, output_path: Path):
    """Génère un rapport de benchmark JSON"""
    import json
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'framework': 'PaniniFS Multi-Format Validation',
        'version': '1.0',
        'benchmarks': comparisons
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Rapport sauvegardé: {output_path}")


def main():
    """Fonction principale benchmark"""
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  🏁 BENCHMARK PANINI FS vs ext4/NTFS".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    print("\n📊 Comparaison performance validation multi-format")
    print("   PaniniFS vs Filesystem Baseline (ext4/NTFS)")
    
    all_comparisons = {}
    
    # Benchmarks pour différentes tailles
    for size_category in ['small', 'medium', 'large']:
        print("\n" + "=" * 70)
        print(f"🔷 BENCHMARK CATÉGORIE: {size_category.upper()}")
        print("=" * 70)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            corpus_dir = Path(temp_dir) / 'corpus'
            
            # Création corpus
            num_files, total_size = create_benchmark_corpus(corpus_dir, size_category)
            
            # Benchmark PaniniFS
            panini_results = benchmark_panini_fs(corpus_dir, num_files, total_size)
            
            # Benchmark baseline
            baseline_results = benchmark_filesystem_baseline(corpus_dir, num_files, total_size)
            
            # Comparaison
            comparison = compare_results(panini_results, baseline_results)
            all_comparisons[size_category] = comparison
    
    # Génération rapport
    report_path = Path('panini_fs_benchmark_report.json')
    generate_benchmark_report(all_comparisons, report_path)
    
    print("\n" + "=" * 70)
    print("✅ BENCHMARK TERMINÉ")
    print("=" * 70)
    print("\n📊 Résumé global:")
    
    for category, comparison in all_comparisons.items():
        print(f"\n   {category.upper()}:")
        print(f"      Performance: {comparison['speed_ratio']:.2f}x baseline")
        print(f"      Intégrité: {comparison['panini_results']['integrity_score']:.2f}%")


if __name__ == '__main__':
    main()
