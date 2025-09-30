#!/usr/bin/env python3
"""
Tests Validation Framework PaniniFS
Tests exhaustifs pour tous les formats supportés
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src' / 'analysis'))

from panini_fs_validator import PaniniFSValidator
from multi_format_ingestion import MultiFormatIngestion
from integrity_checker import IntegrityChecker


class TestMultiFormatIngestion(unittest.TestCase):
    """Tests pour le module d'ingestion multi-format"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.ingestion = MultiFormatIngestion()
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_text_ingestion(self):
        """Test ingestion fichiers texte"""
        # Création fichier texte test
        test_file = self.temp_dir / "test.txt"
        test_content = "Ceci est un test PaniniFS\nAvec plusieurs lignes\nISO 8601 compliant"
        test_file.write_text(test_content, encoding='utf-8')
        
        # Ingestion
        result = self.ingestion.ingest_file(test_file)
        
        # Vérifications
        self.assertEqual(result['format_type'], 'text')
        self.assertEqual(result['extension'], 'txt')
        self.assertEqual(result['encoding'], 'utf-8')
        self.assertEqual(result['content'], test_content)
        self.assertEqual(result['char_count'], len(test_content))
        self.assertEqual(result['line_count'], 3)
    
    def test_markdown_ingestion(self):
        """Test ingestion fichiers Markdown"""
        test_file = self.temp_dir / "README.md"
        test_content = "# PaniniFS\n\n## Validation Framework\n\nTest markdown"
        test_file.write_text(test_content, encoding='utf-8')
        
        result = self.ingestion.ingest_file(test_file)
        
        self.assertEqual(result['format_type'], 'text')
        self.assertEqual(result['extension'], 'md')
        self.assertIn('content', result)
    
    def test_binary_formats(self):
        """Test ingestion formats binaires"""
        # Création fichier binaire test
        test_file = self.temp_dir / "test.bin"
        test_data = b'\x00\x01\x02\x03\x04\x05'
        test_file.write_bytes(test_data)
        
        result = self.ingestion.ingest_file(test_file)
        
        self.assertIn('data', result)
        self.assertEqual(result['data_length'], len(test_data))
    
    def test_png_header_detection(self):
        """Test détection header PNG"""
        test_file = self.temp_dir / "test.png"
        # PNG signature + IHDR minimal
        png_signature = b'\x89PNG\r\n\x1a\n'
        ihdr_chunk = b'\x00\x00\x00\x0dIHDR\x00\x00\x01\x00\x00\x00\x00\x80'
        test_file.write_bytes(png_signature + ihdr_chunk + b'\x00' * 100)
        
        result = self.ingestion.ingest_file(test_file)
        
        self.assertEqual(result['format_type'], 'image')
        self.assertTrue(result.get('header_parsed', False))
        self.assertEqual(result.get('image_format'), 'PNG')
    
    def test_wav_header_detection(self):
        """Test détection header WAV"""
        test_file = self.temp_dir / "test.wav"
        # WAV header minimal (RIFF)
        wav_header = (
            b'RIFF' + 
            b'\x00\x00\x00\x00' +  # File size placeholder
            b'WAVE' +
            b'fmt ' +
            b'\x10\x00\x00\x00' +  # fmt chunk size
            b'\x01\x00' +  # Audio format (PCM)
            b'\x02\x00' +  # Channels (2)
            b'\x44\xac\x00\x00' +  # Sample rate (44100)
            b'\x10\xb1\x02\x00' +  # Byte rate
            b'\x04\x00' +  # Block align
            b'\x10\x00'    # Bits per sample (16)
        )
        test_file.write_bytes(wav_header + b'\x00' * 100)
        
        result = self.ingestion.ingest_file(test_file)
        
        self.assertEqual(result['format_type'], 'audio')
        self.assertTrue(result.get('header_parsed', False))
        self.assertEqual(result.get('audio_format'), 'WAV')
        self.assertEqual(result.get('channels'), 2)
        self.assertEqual(result.get('sample_rate'), 44100)


class TestIntegrityChecker(unittest.TestCase):
    """Tests pour le vérificateur d'intégrité"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.checker = IntegrityChecker()
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_hash_computation(self):
        """Test calcul de hash"""
        test_file = self.temp_dir / "test.txt"
        test_content = b"Test content for hashing"
        test_file.write_bytes(test_content)
        
        # Test SHA256
        hash_result = self.checker.compute_hash(test_file, 'sha256')
        self.assertIsInstance(hash_result, str)
        self.assertEqual(len(hash_result), 64)  # SHA256 = 64 hex chars
        
        # Test MD5
        hash_result = self.checker.compute_hash(test_file, 'md5')
        self.assertEqual(len(hash_result), 32)  # MD5 = 32 hex chars
    
    def test_multiple_hashes(self):
        """Test calcul de plusieurs hashes"""
        test_file = self.temp_dir / "test.txt"
        test_file.write_bytes(b"Test content")
        
        hashes = self.checker.compute_multiple_hashes(test_file)
        
        self.assertIn('md5', hashes)
        self.assertIn('sha256', hashes)
        self.assertIn('sha512', hashes)
    
    def test_integrity_verification_identical(self):
        """Test vérification intégrité - fichiers identiques"""
        # Création de deux fichiers identiques
        test_content = b"Identical content for integrity test"
        file1 = self.temp_dir / "original.txt"
        file2 = self.temp_dir / "copy.txt"
        
        file1.write_bytes(test_content)
        file2.write_bytes(test_content)
        
        result = self.checker.verify_file_integrity(file1, file2, verbose=False)
        
        self.assertTrue(result['success'])
        self.assertTrue(result['hash_match'])
        self.assertTrue(result['size_match'])
        self.assertEqual(result['original_hash'], result['restored_hash'])
    
    def test_integrity_verification_different(self):
        """Test vérification intégrité - fichiers différents"""
        file1 = self.temp_dir / "file1.txt"
        file2 = self.temp_dir / "file2.txt"
        
        file1.write_bytes(b"Content A")
        file2.write_bytes(b"Content B")
        
        result = self.checker.verify_file_integrity(file1, file2, verbose=False)
        
        self.assertFalse(result['success'])
        self.assertFalse(result['hash_match'])
        self.assertNotEqual(result['original_hash'], result['restored_hash'])
    
    def test_bitwise_comparison(self):
        """Test comparaison bit-à-bit"""
        file1 = self.temp_dir / "file1.bin"
        file2 = self.temp_dir / "file2.bin"
        
        # Fichiers identiques
        content = b'\x00\x01\x02\x03\x04\x05'
        file1.write_bytes(content)
        file2.write_bytes(content)
        
        result = self.checker._compare_files_bitwise(file1, file2)
        self.assertTrue(result)
        
        # Fichiers différents
        file2.write_bytes(content + b'\x06')
        result = self.checker._compare_files_bitwise(file1, file2)
        self.assertFalse(result)
    
    def test_manifest_generation(self):
        """Test génération manifeste d'intégrité"""
        # Création fichiers test
        files = []
        for i in range(3):
            test_file = self.temp_dir / f"file{i}.txt"
            test_file.write_bytes(f"Content {i}".encode())
            files.append(test_file)
        
        manifest_path = self.temp_dir / "manifest.json"
        self.checker.generate_integrity_manifest(files, manifest_path)
        
        self.assertTrue(manifest_path.exists())
        
        # Vérification contre manifeste
        result = self.checker.verify_against_manifest(manifest_path, self.temp_dir)
        
        self.assertEqual(result['total_files'], 3)
        self.assertEqual(result['successful'], 3)
        self.assertEqual(result['failed'], 0)


class TestPaniniFSValidator(unittest.TestCase):
    """Tests pour le validateur PaniniFS complet"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.validator = PaniniFSValidator(workspace=self.temp_dir / 'validation')
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_format_detection(self):
        """Test détection de format"""
        test_cases = [
            ('test.txt', 'text', 'txt'),
            ('doc.md', 'text', 'md'),
            ('image.png', 'image', 'png'),
            ('audio.mp3', 'audio', 'mp3'),
            ('video.mp4', 'video', 'mp4'),
            ('unknown.xyz', 'unknown', 'xyz')
        ]
        
        for filename, expected_cat, expected_fmt in test_cases:
            test_file = self.temp_dir / filename
            category, format_type = self.validator.detect_format(test_file)
            
            self.assertEqual(category, expected_cat, f"Failed for {filename}")
            self.assertEqual(format_type, expected_fmt, f"Failed for {filename}")
    
    def test_file_hash_computation(self):
        """Test calcul hash fichier"""
        test_file = self.temp_dir / "test.txt"
        test_file.write_bytes(b"Test content")
        
        hash1 = self.validator.compute_file_hash(test_file)
        hash2 = self.validator.compute_file_hash(test_file)
        
        self.assertEqual(hash1, hash2)  # Hash doit être déterministe
        self.assertIsInstance(hash1, str)
    
    def test_validation_pipeline_simulation(self):
        """Test pipeline validation complet (simulation)"""
        # Création fichier test
        test_file = self.temp_dir / "test.txt"
        test_content = b"Test validation pipeline PaniniFS"
        test_file.write_bytes(test_content)
        
        # Exécution pipeline (sans compression réelle)
        result = self.validator.validate_format_pipeline(test_file)
        
        # Vérifications
        self.assertEqual(result['file_name'], 'test.txt')
        self.assertEqual(result['category'], 'text')
        self.assertEqual(result['format'], 'txt')
        self.assertTrue(result['integrity']['success'])
        self.assertEqual(result['original_size'], len(test_content))
    
    def test_corpus_validation(self):
        """Test validation corpus multi-format"""
        # Création corpus test
        corpus_dir = self.temp_dir / 'corpus'
        corpus_dir.mkdir()
        
        # Fichiers de différents formats
        (corpus_dir / 'doc.txt').write_text('Text document')
        (corpus_dir / 'README.md').write_text('# Markdown')
        (corpus_dir / 'data.bin').write_bytes(b'\x00\x01\x02')
        
        # Validation corpus
        report = self.validator.validate_corpus(corpus_dir)
        
        # Vérifications
        self.assertIn('metrics', report)
        self.assertGreater(report['metrics']['total_files'], 0)
        self.assertEqual(
            report['metrics']['successful_validations'],
            report['metrics']['total_files']
        )
    
    def test_performance_benchmark(self):
        """Test génération benchmark performance"""
        # Création fichiers test
        test_files = []
        for i in range(3):
            test_file = self.temp_dir / f"bench{i}.txt"
            test_file.write_bytes(f"Benchmark test {i}".encode() * 100)
            test_files.append(test_file)
        
        # Génération benchmark
        benchmark = self.validator.generate_performance_benchmark(test_files)
        
        # Vérifications
        self.assertEqual(benchmark['test_files_count'], 3)
        self.assertGreater(benchmark['total_size'], 0)
        self.assertIn('overall_metrics', benchmark)


class TestIntegrationValidation(unittest.TestCase):
    """Tests d'intégration entre tous les modules"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.validator = PaniniFSValidator(workspace=self.temp_dir / 'validation')
        self.ingestion = MultiFormatIngestion()
        self.checker = IntegrityChecker()
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_full_validation_workflow(self):
        """Test workflow complet: ingestion → validation → vérification"""
        # Création fichier test
        test_file = self.temp_dir / "test.txt"
        test_content = "PaniniFS validation workflow test"
        test_file.write_text(test_content, encoding='utf-8')
        
        # 1. Ingestion
        ingestion_result = self.ingestion.ingest_file(test_file)
        self.assertEqual(ingestion_result['format_type'], 'text')
        
        # 2. Validation pipeline
        validation_result = self.validator.validate_format_pipeline(test_file)
        self.assertTrue(validation_result['integrity']['success'])
        
        # 3. Vérification intégrité
        restored_file = self.validator.restitution_dir / test_file.name
        integrity_result = self.checker.verify_file_integrity(
            test_file, 
            restored_file,
            verbose=False
        )
        self.assertTrue(integrity_result['success'])


def run_tests():
    """Exécute tous les tests"""
    print("🧪 TESTS VALIDATION FRAMEWORK PANINI FS")
    print("=" * 60)
    
    # Création suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Ajout des tests
    suite.addTests(loader.loadTestsFromTestCase(TestMultiFormatIngestion))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrityChecker))
    suite.addTests(loader.loadTestsFromTestCase(TestPaniniFSValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationValidation))
    
    # Exécution
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    print(f"Tests exécutés: {result.testsRun}")
    print(f"✅ Réussis: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Échecs: {len(result.failures)}")
    print(f"⚠️  Erreurs: {len(result.errors)}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
