#!/usr/bin/env python3
"""
Content Invariant Extractor - PaniniFS Research
Extracteur d'invariants cross-format

Identifies semantic content that remains consistent across different formats
of the same content (e.g., TXT vs PDF vs EPUB for the same book)
"""

import hashlib
import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from collections import Counter
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class TextInvariant:
    """Represents invariant content extracted from text"""
    word_count: int
    unique_words: int
    sentence_count: int
    paragraph_count: int
    top_words: List[Tuple[str, int]]  # (word, count)
    character_count: int
    avg_word_length: float
    avg_sentence_length: float
    content_hash: str  # Normalized content hash


@dataclass
class SemanticInvariant:
    """Represents semantic invariants across formats"""
    content_id: str
    title: str
    invariants: Dict[str, Any]  # Common invariants across all formats
    variants: Dict[str, Dict[str, Any]]  # Format-specific variations
    similarity_score: float  # Cross-format similarity (0-1)
    extraction_timestamp: str


class ContentInvariantExtractor:
    """Extract invariants from multi-format content"""
    
    def __init__(self):
        """Initialize the invariant extractor"""
        # Stop words for filtering (basic set)
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'le', 'la', 'les', 'un', 'une', 'des', 'et', 'ou', 'de', 'du',
            'en', 'dans', 'sur', 'pour', 'avec', 'est', 'sont', 'était'
        }
        
        logger.info("ContentInvariantExtractor initialized")
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text for comparison
        
        Removes formatting, extra whitespace, etc.
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:\-\']', '', text)
        
        return text.strip()
    
    def extract_text_from_format(self, file_path: Path, format_type: str) -> str:
        """
        Extract text content from different formats
        
        Args:
            file_path: Path to the file
            format_type: Format type (txt, md, srt, etc.)
            
        Returns:
            Extracted text content
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        text = ""
        
        try:
            if format_type in ['txt', 'md']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            
            elif format_type in ['srt', 'vtt']:
                text = self._extract_from_subtitles(file_path)
            
            elif format_type == 'pdf':
                text = self._extract_from_pdf_basic(file_path)
            
            elif format_type == 'epub':
                text = self._extract_from_epub_basic(file_path)
            
            else:
                logger.warning(f"Format {format_type} not supported for text extraction")
        
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
        
        return text
    
    def _extract_from_subtitles(self, file_path: Path) -> str:
        """Extract text content from subtitle files"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Remove timestamps
        content = re.sub(r'\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[,.]\d{3}', '', content)
        
        # Remove subtitle numbers
        content = re.sub(r'^\d+\s*$', '', content, flags=re.MULTILINE)
        
        # Remove WEBVTT header
        content = re.sub(r'WEBVTT.*?\n\n', '', content, flags=re.DOTALL)
        
        # Clean up extra whitespace
        content = re.sub(r'\n\n+', '\n', content)
        
        return content.strip()
    
    def _extract_from_pdf_basic(self, file_path: Path) -> str:
        """Basic text extraction from PDF (without library)"""
        # Note: This is a placeholder. In production, use PyPDF2 or pdfplumber
        logger.warning("PDF text extraction requires library. Using filename as placeholder.")
        return f"PDF content placeholder for {file_path.stem}"
    
    def _extract_from_epub_basic(self, file_path: Path) -> str:
        """Basic text extraction from EPUB (without library)"""
        # Note: This is a placeholder. In production, use ebooklib
        logger.warning("EPUB text extraction requires library. Using filename as placeholder.")
        return f"EPUB content placeholder for {file_path.stem}"
    
    def compute_text_invariants(self, text: str) -> TextInvariant:
        """
        Compute invariant features from text
        
        Args:
            text: Text content to analyze
            
        Returns:
            TextInvariant object with extracted features
        """
        # Normalize text
        normalized = self.normalize_text(text)
        
        # Count characters
        char_count = len(normalized)
        
        # Split into sentences (basic splitting)
        sentences = re.split(r'[.!?]+', normalized)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)
        
        # Split into paragraphs (basic splitting)
        paragraphs = text.split('\n\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        paragraph_count = len(paragraphs)
        
        # Tokenize into words
        words = re.findall(r'\b\w+\b', normalized)
        word_count = len(words)
        
        # Filter stop words and get unique words
        filtered_words = [w for w in words if w not in self.stop_words and len(w) > 2]
        unique_words = len(set(filtered_words))
        
        # Get top words
        word_freq = Counter(filtered_words)
        top_words = word_freq.most_common(20)
        
        # Calculate averages
        avg_word_length = sum(len(w) for w in words) / max(word_count, 1)
        avg_sentence_length = word_count / max(sentence_count, 1)
        
        # Compute content hash (normalized)
        content_hash = hashlib.sha256(normalized.encode()).hexdigest()[:16]
        
        return TextInvariant(
            word_count=word_count,
            unique_words=unique_words,
            sentence_count=sentence_count,
            paragraph_count=paragraph_count,
            top_words=top_words,
            character_count=char_count,
            avg_word_length=avg_word_length,
            avg_sentence_length=avg_sentence_length,
            content_hash=content_hash
        )
    
    def extract_invariants_from_content(
        self,
        content_id: str,
        title: str,
        formats: Dict[str, Path]
    ) -> SemanticInvariant:
        """
        Extract invariants across all formats of content
        
        Args:
            content_id: Unique content identifier
            title: Content title
            formats: Dict of format -> file path
            
        Returns:
            SemanticInvariant object
        """
        logger.info(f"Extracting invariants for: {title} ({content_id})")
        
        # Extract text from each format
        format_texts: Dict[str, str] = {}
        format_invariants: Dict[str, TextInvariant] = {}
        
        for fmt, path in formats.items():
            try:
                text = self.extract_text_from_format(path, fmt)
                if text:
                    format_texts[fmt] = text
                    invariants = self.compute_text_invariants(text)
                    format_invariants[fmt] = invariants
                    logger.info(f"  {fmt}: {invariants.word_count} words, {invariants.sentence_count} sentences")
            except Exception as e:
                logger.error(f"  Error processing {fmt}: {e}")
        
        # Compute common invariants
        common_invariants = self._compute_common_invariants(format_invariants)
        
        # Compute format-specific variants
        variants = self._compute_variants(format_invariants, common_invariants)
        
        # Calculate similarity score
        similarity = self._calculate_cross_format_similarity(format_invariants)
        
        return SemanticInvariant(
            content_id=content_id,
            title=title,
            invariants=common_invariants,
            variants=variants,
            similarity_score=similarity,
            extraction_timestamp=datetime.now().isoformat()
        )
    
    def _compute_common_invariants(
        self,
        format_invariants: Dict[str, TextInvariant]
    ) -> Dict[str, Any]:
        """
        Compute invariants common across all formats
        
        Uses median/average values and shared top words
        """
        if not format_invariants:
            return {}
        
        # Collect metrics from all formats
        word_counts = [inv.word_count for inv in format_invariants.values()]
        unique_words = [inv.unique_words for inv in format_invariants.values()]
        sentence_counts = [inv.sentence_count for inv in format_invariants.values()]
        paragraph_counts = [inv.paragraph_count for inv in format_invariants.values()]
        avg_word_lengths = [inv.avg_word_length for inv in format_invariants.values()]
        avg_sentence_lengths = [inv.avg_sentence_length for inv in format_invariants.values()]
        
        # Find common top words across formats
        all_top_words = []
        for inv in format_invariants.values():
            all_top_words.extend([word for word, count in inv.top_words])
        
        common_words_counter = Counter(all_top_words)
        num_formats = len(format_invariants)
        # Words that appear in at least half of the formats
        threshold = max(1, num_formats // 2)
        common_words = [word for word, count in common_words_counter.items() if count >= threshold]
        
        return {
            'avg_word_count': sum(word_counts) / len(word_counts),
            'avg_unique_words': sum(unique_words) / len(unique_words),
            'avg_sentence_count': sum(sentence_counts) / len(sentence_counts),
            'avg_paragraph_count': sum(paragraph_counts) / len(paragraph_counts),
            'avg_word_length': sum(avg_word_lengths) / len(avg_word_lengths),
            'avg_sentence_length': sum(avg_sentence_lengths) / len(avg_sentence_lengths),
            'common_top_words': common_words[:10],
            'num_formats': num_formats
        }
    
    def _compute_variants(
        self,
        format_invariants: Dict[str, TextInvariant],
        common_invariants: Dict[str, Any]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Compute format-specific variations from common invariants
        """
        variants = {}
        
        for fmt, inv in format_invariants.items():
            # Calculate deviations from common values
            variants[fmt] = {
                'word_count_delta': inv.word_count - common_invariants['avg_word_count'],
                'unique_words_delta': inv.unique_words - common_invariants['avg_unique_words'],
                'sentence_count_delta': inv.sentence_count - common_invariants['avg_sentence_count'],
                'paragraph_count_delta': inv.paragraph_count - common_invariants['avg_paragraph_count'],
                'format_specific_words': [w for w, c in inv.top_words[:10] 
                                         if w not in common_invariants['common_top_words']],
                'content_hash': inv.content_hash
            }
        
        return variants
    
    def _calculate_cross_format_similarity(
        self,
        format_invariants: Dict[str, TextInvariant]
    ) -> float:
        """
        Calculate similarity score across formats (0-1)
        
        Based on overlap in top words and consistency of metrics
        """
        if len(format_invariants) < 2:
            return 1.0
        
        # Calculate word overlap similarity
        word_sets = []
        for inv in format_invariants.values():
            word_set = set(word for word, count in inv.top_words)
            word_sets.append(word_set)
        
        # Average pairwise Jaccard similarity
        similarities = []
        for i in range(len(word_sets)):
            for j in range(i + 1, len(word_sets)):
                intersection = len(word_sets[i] & word_sets[j])
                union = len(word_sets[i] | word_sets[j])
                if union > 0:
                    similarities.append(intersection / union)
        
        if not similarities:
            return 0.0
        
        return sum(similarities) / len(similarities)
    
    def export_invariants(
        self,
        invariants: List[SemanticInvariant],
        output_path: Path
    ) -> None:
        """
        Export extracted invariants to JSON
        
        Args:
            invariants: List of SemanticInvariant objects
            output_path: Path to save the invariants
        """
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'total_contents': len(invariants),
            'invariants': []
        }
        
        for inv in invariants:
            inv_data = {
                'content_id': inv.content_id,
                'title': inv.title,
                'invariants': inv.invariants,
                'variants': inv.variants,
                'similarity_score': inv.similarity_score,
                'extraction_timestamp': inv.extraction_timestamp
            }
            export_data['invariants'].append(inv_data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Invariants exported to: {output_path}")
    
    def analyze_corpus_invariants(
        self,
        content_registry: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze invariants across entire corpus
        
        Returns statistics about cross-format invariants
        """
        stats = {
            'total_analyzed': 0,
            'avg_similarity': 0.0,
            'high_similarity_count': 0,  # similarity > 0.8
            'medium_similarity_count': 0,  # 0.5 < similarity <= 0.8
            'low_similarity_count': 0,  # similarity <= 0.5
            'format_combinations': Counter()
        }
        
        similarities = []
        
        for content_id, item in content_registry.items():
            # Track format combinations
            formats_tuple = tuple(sorted(item.get('formats', {}).keys()))
            stats['format_combinations'][formats_tuple] += 1
        
        return stats


def main():
    """Main function for testing the invariant extractor"""
    logger.info("=" * 60)
    logger.info("ContentInvariantExtractor - Testing")
    logger.info("=" * 60)
    
    # Initialize extractor
    extractor = ContentInvariantExtractor()
    
    # Test with sample text
    sample_text = """
    This is a sample text for testing the invariant extractor.
    It contains multiple sentences across several paragraphs.
    
    The extractor should identify common patterns and features
    that remain consistent across different formats of the same content.
    
    This helps separate the semantic content from the container format.
    """
    
    # Compute invariants
    invariants = extractor.compute_text_invariants(sample_text)
    
    logger.info("\nSample Text Invariants:")
    logger.info(f"  Word count: {invariants.word_count}")
    logger.info(f"  Unique words: {invariants.unique_words}")
    logger.info(f"  Sentence count: {invariants.sentence_count}")
    logger.info(f"  Paragraph count: {invariants.paragraph_count}")
    logger.info(f"  Avg word length: {invariants.avg_word_length:.2f}")
    logger.info(f"  Avg sentence length: {invariants.avg_sentence_length:.2f}")
    logger.info(f"  Top words: {invariants.top_words[:5]}")
    logger.info(f"  Content hash: {invariants.content_hash}")
    
    logger.info("\nInvariant extractor test completed successfully")
    
    return extractor


if __name__ == '__main__':
    main()
