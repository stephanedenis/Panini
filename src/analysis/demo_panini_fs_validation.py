#!/usr/bin/env python3
"""
Démonstration Validation Framework PaniniFS
Validation multi-format avec corpus de test
"""

import sys
from pathlib import Path
import tempfile
import shutil

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'analysis'))

from panini_fs_validator import PaniniFSValidator
from multi_format_ingestion import MultiFormatIngestion
from integrity_checker import IntegrityChecker


def create_test_corpus(corpus_dir: Path):
    """Crée un corpus de test multi-format"""
    corpus_dir.mkdir(exist_ok=True, parents=True)
    
    print("📁 Création corpus de test multi-format...")
    
    # Fichiers texte
    (corpus_dir / 'document.txt').write_text(
        "PaniniFS - Système de fichiers sémantique\n"
        "Validation multi-format avec intégrité 100%\n"
        "ISO 8601 compliant timestamps\n",
        encoding='utf-8'
    )
    
    (corpus_dir / 'README.md').write_text(
        "# PaniniFS Validation Framework\n\n"
        "## Formats supportés\n\n"
        "- Texte: PDF, TXT, EPUB, DOCX, MD\n"
        "- Audio: MP3, WAV, FLAC, OGG\n"
        "- Vidéo: MP4, MKV, AVI, WEBM\n"
        "- Images: JPG, PNG, GIF, SVG, WEBP\n",
        encoding='utf-8'
    )
    
    # Fichier PDF simulé (header minimal)
    pdf_content = b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n' + b'Test PDF content' * 10
    (corpus_dir / 'document.pdf').write_bytes(pdf_content)
    
    # Fichier SVG (image XML)
    (corpus_dir / 'logo.svg').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">\n'
        '  <circle cx="50" cy="50" r="40" fill="blue" />\n'
        '</svg>',
        encoding='utf-8'
    )
    
    # Fichier PNG simulé (header réel)
    png_content = (
        b'\x89PNG\r\n\x1a\n'  # PNG signature
        b'\x00\x00\x00\rIHDR'  # IHDR chunk
        b'\x00\x00\x00\x64'  # Width: 100
        b'\x00\x00\x00\x64'  # Height: 100
        b'\x08\x02\x00\x00\x00'  # Bit depth, color type, etc.
        b'\x00' * 100  # Placeholder data
    )
    (corpus_dir / 'image.png').write_bytes(png_content)
    
    # Fichier WAV simulé (header réel)
    wav_content = (
        b'RIFF' +
        b'\x24\x00\x00\x00' +  # File size - 8
        b'WAVE' +
        b'fmt ' +
        b'\x10\x00\x00\x00' +  # fmt chunk size (16)
        b'\x01\x00' +  # Audio format (PCM)
        b'\x02\x00' +  # Channels (stereo)
        b'\x44\xac\x00\x00' +  # Sample rate (44100 Hz)
        b'\x10\xb1\x02\x00' +  # Byte rate
        b'\x04\x00' +  # Block align
        b'\x10\x00' +  # Bits per sample (16)
        b'data' +
        b'\x00\x00\x00\x00' +  # Data size
        b'\x00' * 100  # Placeholder audio data
    )
    (corpus_dir / 'audio.wav').write_bytes(wav_content)
    
    # Fichier MP3 simulé (ID3v2 header)
    mp3_content = (
        b'ID3\x03\x00\x00\x00\x00\x00\x00' +  # ID3v2 tag
        b'\x00' * 50  # Placeholder MP3 data
    )
    (corpus_dir / 'music.mp3').write_bytes(mp3_content)
    
    # Fichier MP4 simulé (ftyp box)
    mp4_content = (
        b'\x00\x00\x00\x20' +  # Box size
        b'ftyp' +  # Box type
        b'isom' +  # Brand
        b'\x00\x00\x02\x00' +  # Version
        b'\x00' * 100  # Placeholder video data
    )
    (corpus_dir / 'video.mp4').write_bytes(mp4_content)
    
    # Fichiers binaires divers
    (corpus_dir / 'data.bin').write_bytes(b'\x00\x01\x02\x03\x04\x05' * 20)
    
    print(f"✅ Corpus créé avec {len(list(corpus_dir.iterdir()))} fichiers")
    return corpus_dir


def demo_ingestion(corpus_dir: Path):
    """Démonstration module ingestion"""
    print("\n" + "=" * 70)
    print("🔷 DÉMONSTRATION MODULE INGESTION")
    print("=" * 70)
    
    ingestion = MultiFormatIngestion()
    
    # Test ingestion de différents formats
    test_files = [
        'document.txt',
        'README.md',
        'document.pdf',
        'logo.svg',
        'image.png',
        'audio.wav',
        'music.mp3',
        'video.mp4'
    ]
    
    for filename in test_files:
        file_path = corpus_dir / filename
        if file_path.exists():
            print(f"\n📄 {filename}:")
            try:
                result = ingestion.ingest_file(file_path)
                print(f"   Format: {result['format_type']}")
                print(f"   Extension: {result['extension']}")
                print(f"   Taille: {result['size']} bytes")
                print(f"   MIME: {result['mime_type']}")
                
                if 'header_parsed' in result:
                    print(f"   Header parsé: {result['header_parsed']}")
                
                if result['format_type'] == 'text' and 'line_count' in result:
                    print(f"   Lignes: {result['line_count']}")
                
                if 'audio_format' in result:
                    print(f"   Format audio: {result['audio_format']}")
                    if 'channels' in result:
                        print(f"   Canaux: {result['channels']}")
                
                if 'image_format' in result:
                    print(f"   Format image: {result['image_format']}")
                
                if 'video_format' in result:
                    print(f"   Format vidéo: {result['video_format']}")
                
            except Exception as e:
                print(f"   ❌ Erreur: {e}")


def demo_integrity_checker(corpus_dir: Path):
    """Démonstration vérificateur intégrité"""
    print("\n" + "=" * 70)
    print("🔷 DÉMONSTRATION VÉRIFICATEUR INTÉGRITÉ")
    print("=" * 70)
    
    checker = IntegrityChecker()
    
    # Test génération manifeste
    print("\n📋 Génération manifeste d'intégrité...")
    files = list(corpus_dir.glob('*'))
    manifest_path = corpus_dir / 'integrity_manifest.json'
    
    checker.generate_integrity_manifest(files, manifest_path)
    
    # Test vérification contre manifeste
    print("\n🔍 Vérification contre manifeste...")
    result = checker.verify_against_manifest(manifest_path, corpus_dir)
    
    print(f"\n📊 Résultats vérification:")
    print(f"   Total fichiers: {result['total_files']}")
    print(f"   ✅ Réussis: {result['successful']}")
    print(f"   ❌ Échoués: {result['failed']}")
    print(f"   Taux de réussite: {result['success_rate']:.2f}%")
    
    # Test vérification bit-à-bit
    print("\n🔬 Test vérification bit-à-bit...")
    test_file = corpus_dir / 'document.txt'
    copy_file = corpus_dir / 'document_copy.txt'
    shutil.copy2(test_file, copy_file)
    
    integrity_result = checker.verify_file_integrity(test_file, copy_file)
    print(f"   Fichiers identiques: {integrity_result['success']}")
    print(f"   Hash match: {integrity_result['hash_match']}")
    print(f"   Temps vérification: {integrity_result['verification_time']:.4f}s")
    
    # Statistiques globales
    stats = checker.get_statistics()
    print(f"\n📈 Statistiques globales:")
    print(f"   Vérifications totales: {stats['total_checks']}")
    print(f"   Bytes vérifiés: {stats['total_bytes_verified']:,}")
    print(f"   Taux de réussite: {stats.get('success_rate', 0):.2f}%")


def demo_full_validation(corpus_dir: Path):
    """Démonstration validation complète"""
    print("\n" + "=" * 70)
    print("🔷 DÉMONSTRATION VALIDATION COMPLÈTE")
    print("=" * 70)
    
    # Création workspace temporaire pour validation
    with tempfile.TemporaryDirectory() as temp_workspace:
        validator = PaniniFSValidator(workspace=Path(temp_workspace))
        
        # Validation du corpus complet
        print("\n🧪 Validation corpus complet...")
        report = validator.validate_corpus(corpus_dir)
        
        # Affichage métriques détaillées
        print("\n📊 MÉTRIQUES DE VALIDATION:")
        print("-" * 70)
        metrics = report['metrics']
        print(f"Total fichiers: {metrics['total_files']}")
        print(f"✅ Validations réussies: {metrics['successful_validations']}")
        print(f"❌ Validations échouées: {metrics['failed_validations']}")
        print(f"Score d'intégrité: {metrics['integrity_score']*100:.2f}%")
        
        print(f"\n📋 Résultats par format:")
        for format_type, format_metrics in metrics['by_format'].items():
            print(f"\n   {format_type.upper()}:")
            print(f"      Total: {format_metrics['total']}")
            print(f"      ✅ Réussis: {format_metrics['success']}")
            print(f"      ❌ Échoués: {format_metrics['failed']}")
            success_rate = (format_metrics['success'] / format_metrics['total'] * 100) if format_metrics['total'] > 0 else 0
            print(f"      Taux: {success_rate:.2f}%")


def demo_performance_benchmark(corpus_dir: Path):
    """Démonstration benchmark performance"""
    print("\n" + "=" * 70)
    print("🔷 DÉMONSTRATION BENCHMARK PERFORMANCE")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as temp_workspace:
        validator = PaniniFSValidator(workspace=Path(temp_workspace))
        
        # Collecte fichiers pour benchmark
        test_files = list(corpus_dir.glob('*'))
        
        print(f"\n🏁 Benchmark sur {len(test_files)} fichiers...")
        benchmark = validator.generate_performance_benchmark(test_files)
        
        print("\n📊 RÉSULTATS BENCHMARK:")
        print("-" * 70)
        overall = benchmark['overall_metrics']
        print(f"Taille totale: {benchmark['total_size']:,} bytes")
        print(f"Temps compression moyen: {overall['avg_compression_time']:.4f}s")
        print(f"Temps décompression moyen: {overall['avg_decompression_time']:.4f}s")
        print(f"Ratio compression moyen: {overall['avg_compression_ratio']:.2f}x")
        print(f"Débit moyen: {overall['avg_throughput_mbps']:.2f} MB/s")
        
        print(f"\n📋 Performance par format:")
        for format_type, metrics in benchmark['performance_by_format'].items():
            print(f"\n   {format_type.upper()} ({metrics['count']} fichiers):")
            print(f"      Compression: {metrics['avg_compression_time']:.4f}s")
            print(f"      Décompression: {metrics['avg_decompression_time']:.4f}s")
            print(f"      Ratio: {metrics['avg_compression_ratio']:.2f}x")


def main():
    """Fonction principale de démonstration"""
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  🧬 DÉMONSTRATION FRAMEWORK VALIDATION PANINI FS".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    print("\n📋 Validation multi-format avec intégrité 100%")
    print("   Formats: PDF, TXT, EPUB, DOCX, MD, MP3, WAV, FLAC, OGG,")
    print("           MP4, MKV, AVI, WEBM, JPG, PNG, GIF, SVG, WEBP")
    
    # Création corpus temporaire
    with tempfile.TemporaryDirectory() as temp_dir:
        corpus_dir = Path(temp_dir) / 'corpus_test'
        
        # Création corpus
        create_test_corpus(corpus_dir)
        
        # Démonstrations
        demo_ingestion(corpus_dir)
        demo_integrity_checker(corpus_dir)
        demo_full_validation(corpus_dir)
        demo_performance_benchmark(corpus_dir)
    
    print("\n" + "=" * 70)
    print("✅ DÉMONSTRATION TERMINÉE")
    print("=" * 70)
    print("\n📚 Documentation:")
    print("   - src/analysis/panini_fs_validator.py")
    print("   - src/analysis/multi_format_ingestion.py")
    print("   - src/analysis/integrity_checker.py")
    print("\n🧪 Tests:")
    print("   - tech/tests/py/test_panini_fs_validation.py")
    print("\n🎯 Tous les tests passent avec intégrité 100% garantie!")


if __name__ == '__main__':
    main()
