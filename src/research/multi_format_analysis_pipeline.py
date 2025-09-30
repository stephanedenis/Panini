#!/usr/bin/env python3
"""
Multi-Format Analysis Pipeline - PaniniFS Research
Intégration complète des 3 modules d'analyse

Pipeline complet:
1. MultiFormatAnalyzer - Scan et catalogue du corpus multi-format
2. ContentInvariantExtractor - Extraction des invariants cross-format
3. ContainerContentSeparator - Séparation 3 niveaux contenant/contenu

Métriques Success:
- Corpus 100+ contenus en 3+ formats chacun
- Extraction automatique invariants cross-format
- Séparation container vs contenu validée
- Compression optimisée par niveau
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent
sys.path.insert(0, str(parent_dir))

# Now import from src.research
from src.research.multi_format_analyzer import MultiFormatAnalyzer, ContentItem
from src.research.content_invariant_extractor import ContentInvariantExtractor, SemanticInvariant
from src.research.container_vs_content_separator import ContainerContentSeparator, ThreeLevelSeparation

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MultiFormatAnalysisPipeline:
    """Complete pipeline for multi-format corpus analysis"""
    
    def __init__(self, corpus_root: Optional[Path] = None):
        """
        Initialize the complete analysis pipeline
        
        Args:
            corpus_root: Root directory of multi-format corpus
        """
        self.corpus_root = corpus_root or Path("./data/multi_format_corpus")
        
        # Initialize components
        self.analyzer = MultiFormatAnalyzer(self.corpus_root)
        self.extractor = ContentInvariantExtractor()
        self.separator = ContainerContentSeparator()
        
        # Results storage
        self.content_items: List[ContentItem] = []
        self.invariants: List[SemanticInvariant] = []
        self.separations: List[ThreeLevelSeparation] = []
        
        logger.info(f"Pipeline initialized with corpus root: {self.corpus_root}")
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """
        Run complete multi-format analysis pipeline
        
        Returns:
            Comprehensive analysis results
        """
        logger.info("=" * 70)
        logger.info("MULTI-FORMAT ANALYSIS PIPELINE - STARTING")
        logger.info("=" * 70)
        
        # Step 1: Scan and catalog corpus
        logger.info("\n📂 STEP 1: Scanning multi-format corpus...")
        self._scan_corpus()
        
        # Step 2: Extract cross-format invariants
        logger.info("\n🔍 STEP 2: Extracting cross-format invariants...")
        self._extract_invariants()
        
        # Step 3: Perform 3-level separation
        logger.info("\n⚙️  STEP 3: Performing 3-level container/content separation...")
        self._perform_separations()
        
        # Step 4: Generate comprehensive report
        logger.info("\n📊 STEP 4: Generating comprehensive analysis report...")
        report = self._generate_report()
        
        # Step 5: Export results
        logger.info("\n💾 STEP 5: Exporting results...")
        self._export_results()
        
        logger.info("\n" + "=" * 70)
        logger.info("MULTI-FORMAT ANALYSIS PIPELINE - COMPLETED")
        logger.info("=" * 70)
        
        return report
    
    def _scan_corpus(self) -> None:
        """Scan corpus and identify multi-format content"""
        
        # Scan each content type directory
        content_types = {
            'books': self.corpus_root / 'books',
            'audio': self.corpus_root / 'audio',
            'video': self.corpus_root / 'video'
        }
        
        for content_type, directory in content_types.items():
            if directory.exists():
                items = self.analyzer.scan_directory(directory, content_type)
                self.content_items.extend(items)
        
        # Log statistics
        stats = self.analyzer.get_format_coverage_stats()
        logger.info(f"  ✓ Scanned {stats['total_items']} multi-format items")
        logger.info(f"  ✓ Total files: {stats['total_files']}")
        
        for content_type, count in stats['by_content_type'].items():
            logger.info(f"    - {content_type}: {count} items")
    
    def _extract_invariants(self) -> None:
        """Extract invariants from all multi-format content"""
        
        total_items = len(self.content_items)
        
        for idx, item in enumerate(self.content_items, 1):
            logger.info(f"  [{idx}/{total_items}] Processing: {item.title}")
            
            try:
                invariant = self.extractor.extract_invariants_from_content(
                    content_id=item.content_id,
                    title=item.title,
                    formats=item.formats
                )
                self.invariants.append(invariant)
                
                logger.info(f"      Similarity score: {invariant.similarity_score:.2%}")
                logger.info(f"      Common words: {len(invariant.invariants.get('common_top_words', []))}")
                
            except Exception as e:
                logger.error(f"      Error extracting invariants: {e}")
        
        logger.info(f"  ✓ Extracted invariants from {len(self.invariants)} items")
    
    def _perform_separations(self) -> None:
        """Perform 3-level separation on all formats"""
        
        total_files = sum(len(item.formats) for item in self.content_items)
        processed = 0
        
        for item in self.content_items:
            for format_type, file_path in item.formats.items():
                processed += 1
                logger.info(f"  [{processed}/{total_files}] Separating: {file_path.name}")
                
                try:
                    # Extract text for level 3
                    text_content = self.extractor.extract_text_from_format(file_path, format_type)
                    
                    # Perform 3-level separation
                    separation = self.separator.separate_three_levels(
                        file_path=file_path,
                        content_id=item.content_id,
                        text_content=text_content
                    )
                    self.separations.append(separation)
                    
                    # Log compression metrics
                    l3_ratio = separation.compression_by_level['level3_compression_ratio']
                    logger.info(f"      Level 3 compression: {l3_ratio:.2%}")
                    
                except Exception as e:
                    logger.error(f"      Error in separation: {e}")
        
        logger.info(f"  ✓ Completed {len(self.separations)} separations")
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        
        # Basic statistics
        report = {
            'timestamp': datetime.now().isoformat(),
            'corpus_root': str(self.corpus_root),
            'summary': {
                'total_content_items': len(self.content_items),
                'total_files_analyzed': len(self.separations),
                'total_invariants_extracted': len(self.invariants)
            }
        }
        
        # Content type distribution
        content_type_dist = {}
        for item in self.content_items:
            ctype = item.content_type
            content_type_dist[ctype] = content_type_dist.get(ctype, 0) + 1
        report['content_type_distribution'] = content_type_dist
        
        # Format distribution
        format_dist = {}
        for sep in self.separations:
            fmt = sep.format_type
            format_dist[fmt] = format_dist.get(fmt, 0) + 1
        report['format_distribution'] = format_dist
        
        # Invariant analysis
        if self.invariants:
            avg_similarity = sum(inv.similarity_score for inv in self.invariants) / len(self.invariants)
            report['invariant_analysis'] = {
                'average_cross_format_similarity': avg_similarity,
                'high_similarity_count': sum(1 for inv in self.invariants if inv.similarity_score > 0.8),
                'medium_similarity_count': sum(1 for inv in self.invariants if 0.5 < inv.similarity_score <= 0.8),
                'low_similarity_count': sum(1 for inv in self.invariants if inv.similarity_score <= 0.5)
            }
        
        # Separation analysis
        separation_report = self.separator.generate_separation_report(self.separations)
        report['separation_analysis'] = separation_report
        
        # Success metrics validation
        report['success_metrics'] = self._validate_success_metrics()
        
        # Print summary
        self._print_report_summary(report)
        
        return report
    
    def _validate_success_metrics(self) -> Dict[str, Any]:
        """
        Validate against success metrics from issue
        
        Success Metrics:
        - Corpus 100+ contenus en 3+ formats chacun
        - Extraction automatique invariants cross-format
        - Séparation container vs contenu validée
        - Compression optimisée par niveau
        """
        metrics = {
            'corpus_size_target': 100,
            'formats_per_item_target': 3,
            'current_corpus_size': len(self.content_items),
            'current_avg_formats_per_item': 0,
            'invariant_extraction_working': len(self.invariants) > 0,
            'separation_working': len(self.separations) > 0,
            'compression_optimization_working': False
        }
        
        # Calculate average formats per item
        if self.content_items:
            total_formats = sum(len(item.formats) for item in self.content_items)
            metrics['current_avg_formats_per_item'] = total_formats / len(self.content_items)
        
        # Check if compression is working
        if self.separations:
            avg_l3_compression = sum(
                s.compression_by_level['level3_compression_ratio'] 
                for s in self.separations
            ) / len(self.separations)
            metrics['avg_level3_compression_ratio'] = avg_l3_compression
            metrics['compression_optimization_working'] = avg_l3_compression < 1.0
        
        # Overall validation
        metrics['meets_corpus_size_target'] = metrics['current_corpus_size'] >= 100
        metrics['meets_format_target'] = metrics['current_avg_formats_per_item'] >= 3
        metrics['all_systems_working'] = (
            metrics['invariant_extraction_working'] and
            metrics['separation_working'] and
            metrics['compression_optimization_working']
        )
        
        return metrics
    
    def _print_report_summary(self, report: Dict[str, Any]) -> None:
        """Print human-readable report summary"""
        
        logger.info("\n" + "=" * 70)
        logger.info("ANALYSIS REPORT SUMMARY")
        logger.info("=" * 70)
        
        # Summary
        summary = report['summary']
        logger.info(f"\n📊 Summary:")
        logger.info(f"  Content items: {summary['total_content_items']}")
        logger.info(f"  Files analyzed: {summary['total_files_analyzed']}")
        logger.info(f"  Invariants extracted: {summary['total_invariants_extracted']}")
        
        # Content types
        logger.info(f"\n📚 Content Type Distribution:")
        for ctype, count in report['content_type_distribution'].items():
            logger.info(f"  {ctype}: {count}")
        
        # Formats
        logger.info(f"\n📄 Format Distribution:")
        for fmt, count in report['format_distribution'].items():
            logger.info(f"  {fmt}: {count}")
        
        # Invariants
        if 'invariant_analysis' in report:
            inv_analysis = report['invariant_analysis']
            logger.info(f"\n🔍 Invariant Analysis:")
            logger.info(f"  Average similarity: {inv_analysis['average_cross_format_similarity']:.2%}")
            logger.info(f"  High similarity (>80%): {inv_analysis['high_similarity_count']}")
            logger.info(f"  Medium similarity (50-80%): {inv_analysis['medium_similarity_count']}")
            logger.info(f"  Low similarity (<50%): {inv_analysis['low_similarity_count']}")
        
        # Separation
        if 'separation_analysis' in report:
            sep_analysis = report['separation_analysis']
            if 'compression_metrics' in sep_analysis:
                comp = sep_analysis['compression_metrics']
                logger.info(f"\n⚙️  Separation & Compression:")
                logger.info(f"  Avg Level 2 compression: {comp['avg_level2_ratio']:.2%}")
                logger.info(f"  Avg Level 3 compression: {comp['avg_level3_ratio']:.2%}")
                logger.info(f"  Compression potential: {comp['avg_compression_potential']:.2%}")
        
        # Success metrics
        metrics = report['success_metrics']
        logger.info(f"\n✅ Success Metrics Validation:")
        logger.info(f"  Corpus size: {metrics['current_corpus_size']}/{metrics['corpus_size_target']} "
                   f"({'✓' if metrics['meets_corpus_size_target'] else '✗'})")
        logger.info(f"  Avg formats/item: {metrics['current_avg_formats_per_item']:.1f}/{metrics['formats_per_item_target']} "
                   f"({'✓' if metrics['meets_format_target'] else '✗'})")
        logger.info(f"  Invariant extraction: {'✓' if metrics['invariant_extraction_working'] else '✗'}")
        logger.info(f"  Container/content separation: {'✓' if metrics['separation_working'] else '✗'}")
        logger.info(f"  Compression optimization: {'✓' if metrics['compression_optimization_working'] else '✗'}")
    
    def _export_results(self) -> None:
        """Export all results to files"""
        
        output_dir = self.corpus_root / 'analysis_results'
        output_dir.mkdir(exist_ok=True)
        
        # Export content registry
        registry_path = self.analyzer.export_registry(output_dir / 'content_registry.json')
        logger.info(f"  ✓ Content registry: {registry_path}")
        
        # Export invariants
        if self.invariants:
            invariants_path = output_dir / 'invariants.json'
            self.extractor.export_invariants(self.invariants, invariants_path)
            logger.info(f"  ✓ Invariants: {invariants_path}")
        
        # Export separations
        if self.separations:
            separations_path = output_dir / 'separations.json'
            self.separator.export_separation_results(self.separations, separations_path)
            logger.info(f"  ✓ Separations: {separations_path}")
        
        # Export comprehensive report
        report_path = output_dir / 'analysis_report.json'
        report = self._generate_report()
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        logger.info(f"  ✓ Analysis report: {report_path}")


def main():
    """Main entry point"""
    logger.info("Starting Multi-Format Analysis Pipeline")
    
    # Initialize pipeline
    pipeline = MultiFormatAnalysisPipeline()
    
    # Run complete analysis
    report = pipeline.run_complete_analysis()
    
    # Check if we need more corpus data
    metrics = report['success_metrics']
    if not metrics['meets_corpus_size_target']:
        logger.info("\n⚠️  NOTE: Current corpus size is below target (100+ items)")
        logger.info("   To meet success metrics, expand corpus with more multi-format content")
    
    if not metrics['meets_format_target']:
        logger.info("\n⚠️  NOTE: Average formats per item is below target (3+ formats)")
        logger.info("   Add more format variants for existing content")
    
    logger.info("\n✨ Analysis pipeline completed successfully!")
    
    return pipeline


if __name__ == '__main__':
    main()
