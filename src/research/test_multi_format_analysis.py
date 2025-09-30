#!/usr/bin/env python3
"""
Tests for Multi-Format Analysis System
Validation des modules d'analyse multi-format
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.research.multi_format_analyzer import MultiFormatAnalyzer, ContentItem, FormatMetadata
from src.research.content_invariant_extractor import ContentInvariantExtractor, TextInvariant
from src.research.container_vs_content_separator import ContainerContentSeparator


class MultiFormatAnalysisTests:
    """Test suite for multi-format analysis system"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "summary": {}
        }
        self.passed = 0
        self.failed = 0
    
    def log(self, message, level="INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def run_test(self, test_name, test_func):
        """Run a single test and record result"""
        self.log(f"Running: {test_name}")
        try:
            test_func()
            self.log(f"✓ PASSED: {test_name}", "PASS")
            self.results["tests"].append({
                "name": test_name,
                "status": "PASSED",
                "timestamp": datetime.now().isoformat()
            })
            self.passed += 1
            return True
        except AssertionError as e:
            self.log(f"✗ FAILED: {test_name} - {e}", "FAIL")
            self.results["tests"].append({
                "name": test_name,
                "status": "FAILED",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            self.failed += 1
            return False
        except Exception as e:
            self.log(f"✗ ERROR: {test_name} - {e}", "ERROR")
            self.results["tests"].append({
                "name": test_name,
                "status": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            self.failed += 1
            return False
    
    # ===== MultiFormatAnalyzer Tests =====
    
    def test_analyzer_initialization(self):
        """Test MultiFormatAnalyzer initialization"""
        analyzer = MultiFormatAnalyzer()
        assert analyzer is not None, "Analyzer should be initialized"
        assert analyzer.corpus_root.name == "multi_format_corpus", "Default corpus root should be set"
    
    def test_format_detection(self):
        """Test file format detection"""
        analyzer = MultiFormatAnalyzer()
        
        # Test various formats
        assert analyzer.detect_format(Path("test.txt")) == "txt"
        assert analyzer.detect_format(Path("test.pdf")) == "pdf"
        assert analyzer.detect_format(Path("test.epub")) == "epub"
        assert analyzer.detect_format(Path("test.md")) == "md"
        assert analyzer.detect_format(Path("test.mp3")) == "mp3"
        assert analyzer.detect_format(Path("test.mp4")) == "mp4"
    
    def test_content_id_generation(self):
        """Test content ID generation"""
        analyzer = MultiFormatAnalyzer()
        
        id1 = analyzer.generate_content_id("Test Book", "book")
        id2 = analyzer.generate_content_id("Test Book", "book")
        id3 = analyzer.generate_content_id("Different Book", "book")
        
        assert id1 == id2, "Same title/type should generate same ID"
        assert id1 != id3, "Different title should generate different ID"
        assert id1.startswith("book_"), "ID should start with content type"
    
    def test_format_metadata_extraction(self):
        """Test format metadata extraction on self"""
        analyzer = MultiFormatAnalyzer()
        
        # Test on this Python file
        test_file = Path(__file__)
        metadata = analyzer.extract_format_metadata(test_file)
        
        assert metadata.format_type == "py", "Should detect .py format"
        assert metadata.file_size > 0, "Should have file size"
        assert metadata.container_structure is not None, "Should have container structure"
    
    # ===== ContentInvariantExtractor Tests =====
    
    def test_extractor_initialization(self):
        """Test ContentInvariantExtractor initialization"""
        extractor = ContentInvariantExtractor()
        assert extractor is not None, "Extractor should be initialized"
        assert len(extractor.stop_words) > 0, "Should have stop words loaded"
    
    def test_text_normalization(self):
        """Test text normalization"""
        extractor = ContentInvariantExtractor()
        
        text = "  This is    a TEST!  "
        normalized = extractor.normalize_text(text)
        
        assert normalized == "this is a test!", "Should normalize text"
        assert "  " not in normalized, "Should remove extra spaces"
    
    def test_text_invariants_computation(self):
        """Test computation of text invariants"""
        extractor = ContentInvariantExtractor()
        
        sample_text = """
        This is a test document.
        It has multiple sentences.
        We will analyze its features.
        """
        
        invariants = extractor.compute_text_invariants(sample_text)
        
        assert isinstance(invariants, TextInvariant), "Should return TextInvariant object"
        assert invariants.word_count > 0, "Should count words"
        assert invariants.sentence_count > 0, "Should count sentences"
        assert invariants.unique_words > 0, "Should count unique words"
        assert len(invariants.top_words) > 0, "Should identify top words"
        assert len(invariants.content_hash) > 0, "Should compute content hash"
    
    def test_cross_format_similarity(self):
        """Test cross-format similarity calculation"""
        extractor = ContentInvariantExtractor()
        
        # Create two text invariants with similar content
        from src.research.content_invariant_extractor import TextInvariant
        
        inv1 = TextInvariant(
            word_count=100,
            unique_words=50,
            sentence_count=10,
            paragraph_count=3,
            top_words=[("test", 5), ("data", 4), ("format", 3)],
            character_count=500,
            avg_word_length=5.0,
            avg_sentence_length=10.0,
            content_hash="abc123"
        )
        
        inv2 = TextInvariant(
            word_count=105,
            unique_words=52,
            sentence_count=11,
            paragraph_count=3,
            top_words=[("test", 5), ("data", 4), ("format", 3), ("extra", 2)],
            character_count=525,
            avg_word_length=5.0,
            avg_sentence_length=10.5,
            content_hash="def456"
        )
        
        format_invariants = {"txt": inv1, "md": inv2}
        similarity = extractor._calculate_cross_format_similarity(format_invariants)
        
        assert 0.0 <= similarity <= 1.0, "Similarity should be between 0 and 1"
        assert similarity > 0.5, "Similar content should have high similarity"
    
    # ===== ContainerContentSeparator Tests =====
    
    def test_separator_initialization(self):
        """Test ContainerContentSeparator initialization"""
        separator = ContainerContentSeparator()
        assert separator is not None, "Separator should be initialized"
        assert len(separator.format_configs) > 0, "Should have format configs"
    
    def test_container_type_detection(self):
        """Test container type detection"""
        separator = ContainerContentSeparator()
        
        # Test on this Python file
        test_file = Path(__file__)
        container_type = separator._detect_container_type(test_file)
        
        assert container_type in ["plain_file", "unknown"], "Should detect container type"
    
    def test_three_level_separation(self):
        """Test 3-level separation on actual file"""
        separator = ContainerContentSeparator()
        
        # Test on this Python file
        test_file = Path(__file__)
        separation = separator.separate_three_levels(test_file, "test_file")
        
        # Verify Level 1 (File structure)
        assert separation.level1_file is not None, "Should have level 1 data"
        assert separation.level1_file.file_size > 0, "Should have file size"
        assert separation.level1_file.file_extension == "py", "Should detect .py extension"
        
        # Verify Level 2 (Presentation envelope)
        assert separation.level2_envelope is not None, "Should have level 2 data"
        assert separation.level2_envelope.format_type == "py", "Should identify format"
        
        # Verify Level 3 (Semantic content)
        assert separation.level3_content is not None, "Should have level 3 data"
        assert len(separation.level3_content.content_hash) > 0, "Should have content hash"
        
        # Verify compression metrics
        assert "level3_compression_ratio" in separation.compression_by_level
        assert 0.0 <= separation.compression_by_level["level3_compression_ratio"] <= 1.0
    
    def test_compression_metrics(self):
        """Test compression metrics calculation"""
        separator = ContainerContentSeparator()
        
        test_file = Path(__file__)
        separation = separator.separate_three_levels(test_file, "test_file")
        
        metrics = separation.compression_by_level
        
        assert "level1_compression_ratio" in metrics, "Should have L1 compression"
        assert "level2_compression_ratio" in metrics, "Should have L2 compression"
        assert "level3_compression_ratio" in metrics, "Should have L3 compression"
        assert "total_compression_potential" in metrics, "Should have total potential"
        
        # Level 1 should always be 1.0 (baseline)
        assert metrics["level1_compression_ratio"] == 1.0, "L1 should be baseline"
    
    # ===== Integration Tests =====
    
    def test_end_to_end_single_file(self):
        """Test end-to-end processing of a single file"""
        analyzer = MultiFormatAnalyzer()
        extractor = ContentInvariantExtractor()
        separator = ContainerContentSeparator()
        
        # Use this test file
        test_file = Path(__file__)
        
        # Step 1: Extract metadata
        metadata = analyzer.extract_format_metadata(test_file)
        assert metadata is not None, "Should extract metadata"
        
        # Step 2: Extract text content
        text = extractor.extract_text_from_format(test_file, "py")
        assert len(text) > 0, "Should extract text"
        
        # Step 3: Compute invariants
        invariants = extractor.compute_text_invariants(text)
        assert invariants.word_count > 0, "Should compute invariants"
        
        # Step 4: Perform 3-level separation
        separation = separator.separate_three_levels(test_file, "test_001", text)
        assert separation is not None, "Should complete separation"
    
    def run_all_tests(self):
        """Run all tests"""
        self.log("=" * 70)
        self.log("Multi-Format Analysis System - Test Suite")
        self.log("=" * 70)
        
        # MultiFormatAnalyzer tests
        self.log("\n📂 Testing MultiFormatAnalyzer...")
        self.run_test("Analyzer Initialization", self.test_analyzer_initialization)
        self.run_test("Format Detection", self.test_format_detection)
        self.run_test("Content ID Generation", self.test_content_id_generation)
        self.run_test("Format Metadata Extraction", self.test_format_metadata_extraction)
        
        # ContentInvariantExtractor tests
        self.log("\n🔍 Testing ContentInvariantExtractor...")
        self.run_test("Extractor Initialization", self.test_extractor_initialization)
        self.run_test("Text Normalization", self.test_text_normalization)
        self.run_test("Text Invariants Computation", self.test_text_invariants_computation)
        self.run_test("Cross-Format Similarity", self.test_cross_format_similarity)
        
        # ContainerContentSeparator tests
        self.log("\n⚙️  Testing ContainerContentSeparator...")
        self.run_test("Separator Initialization", self.test_separator_initialization)
        self.run_test("Container Type Detection", self.test_container_type_detection)
        self.run_test("Three-Level Separation", self.test_three_level_separation)
        self.run_test("Compression Metrics", self.test_compression_metrics)
        
        # Integration tests
        self.log("\n🔗 Testing Integration...")
        self.run_test("End-to-End Single File", self.test_end_to_end_single_file)
        
        # Summary
        self.log("\n" + "=" * 70)
        self.log("TEST SUMMARY")
        self.log("=" * 70)
        total = self.passed + self.failed
        self.log(f"Total Tests: {total}")
        self.log(f"Passed: {self.passed} ✓", "PASS" if self.passed > 0 else "INFO")
        self.log(f"Failed: {self.failed} ✗", "FAIL" if self.failed > 0 else "INFO")
        
        if self.failed == 0:
            self.log("\n✨ All tests passed!", "PASS")
        else:
            self.log(f"\n⚠️  {self.failed} test(s) failed", "FAIL")
        
        self.results["summary"] = {
            "total": total,
            "passed": self.passed,
            "failed": self.failed,
            "success_rate": (self.passed / total * 100) if total > 0 else 0
        }
        
        return self.failed == 0


def main():
    """Main test runner"""
    tester = MultiFormatAnalysisTests()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
