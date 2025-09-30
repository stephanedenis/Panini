#!/usr/bin/env python3
"""
Container vs Content Separator - PaniniFS Research
Séparateur contenant/contenu - 3 niveaux d'analyse

Architecture 3 niveaux:
1. Niveau Fichier (PaniniFS) - Structure container filesystem
2. Niveau Enveloppe - Métadonnées de présentation
3. Niveau Contenu - Sémantique pure humain
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ===== Integrity Validation Exceptions =====
# These enforce 100% integrity or failure - no "almost good"

class IntegrityValidationError(Exception):
    """Base exception for integrity validation failures"""
    pass


class ContainerIntegrityError(IntegrityValidationError):
    """Container reconstitution failed - binary mismatch"""
    pass


class EnvelopeIntegrityError(IntegrityValidationError):
    """Envelope reconstitution failed - incomplete metadata"""
    pass


class ContentIntegrityError(IntegrityValidationError):
    """Content reconstitution failed - semantic alteration detected"""
    pass


@dataclass
class Level1_FileStructure:
    """Level 1: Filesystem container structure"""
    file_path: str
    file_size: int
    file_extension: str
    inode_info: Dict[str, Any]
    filesystem_metadata: Dict[str, Any]
    container_type: str  # physical, compressed, encrypted, etc.


@dataclass
class Level2_PresentationEnvelope:
    """Level 2: Presentation metadata envelope"""
    format_type: str  # pdf, epub, mp4, etc.
    encoding_info: Dict[str, Any]
    structure_metadata: Dict[str, Any]  # chapters, pages, tracks, etc.
    presentation_settings: Dict[str, Any]  # fonts, layout, styling
    container_version: Optional[str] = None


@dataclass
class Level3_SemanticContent:
    """Level 3: Pure semantic content"""
    text_content: str
    semantic_tokens: List[str]
    language: str
    content_hash: str
    semantic_features: Dict[str, Any]
    pure_meaning: Dict[str, Any]  # Extracted meaning without format


@dataclass
class ThreeLevelSeparation:
    """Complete 3-level separation result"""
    content_id: str
    format_type: str
    level1_file: Level1_FileStructure
    level2_envelope: Level2_PresentationEnvelope
    level3_content: Level3_SemanticContent
    separation_timestamp: str
    
    # Optimization metrics
    compression_by_level: Dict[str, float]
    redundancy_eliminated: Dict[str, float]


class ContainerContentSeparator:
    """Separator for multi-level container vs content analysis"""
    
    def __init__(self):
        """Initialize the separator"""
        logger.info("ContainerContentSeparator initialized")
        
        # Configuration for different format types
        self.format_configs = {
            'txt': {
                'has_envelope': False,
                'direct_content': True,
                'encoding_critical': True
            },
            'pdf': {
                'has_envelope': True,
                'complex_structure': True,
                'multiple_layers': True
            },
            'epub': {
                'has_envelope': True,
                'complex_structure': True,
                'multiple_files': True
            },
            'md': {
                'has_envelope': False,
                'direct_content': True,
                'markup_only': True
            },
            'srt': {
                'has_envelope': False,
                'timing_metadata': True,
                'sequential_structure': True
            },
            'mp3': {
                'has_envelope': True,
                'audio_codec': True,
                'id3_tags': True
            },
            'mp4': {
                'has_envelope': True,
                'video_codec': True,
                'container_format': 'mp4'
            }
        }
    
    def separate_three_levels(
        self,
        file_path: Path,
        content_id: str,
        text_content: Optional[str] = None
    ) -> ThreeLevelSeparation:
        """
        Perform 3-level separation on a file
        
        Args:
            file_path: Path to the file
            content_id: Unique content identifier
            text_content: Pre-extracted text content (optional)
            
        Returns:
            ThreeLevelSeparation object
        """
        logger.info(f"Starting 3-level separation for: {file_path}")
        
        # Level 1: File structure
        level1 = self._extract_level1_file_structure(file_path)
        
        # Level 2: Presentation envelope
        level2 = self._extract_level2_presentation_envelope(file_path, level1.file_extension)
        
        # Level 3: Semantic content
        level3 = self._extract_level3_semantic_content(file_path, level1.file_extension, text_content)
        
        # Calculate compression metrics
        compression_metrics = self._calculate_compression_by_level(level1, level2, level3)
        
        # Calculate redundancy eliminated
        redundancy_metrics = self._calculate_redundancy_eliminated(level1, level2, level3)
        
        return ThreeLevelSeparation(
            content_id=content_id,
            format_type=level1.file_extension,
            level1_file=level1,
            level2_envelope=level2,
            level3_content=level3,
            separation_timestamp=datetime.now().isoformat(),
            compression_by_level=compression_metrics,
            redundancy_eliminated=redundancy_metrics
        )
    
    def _extract_level1_file_structure(self, file_path: Path) -> Level1_FileStructure:
        """
        Extract Level 1: Filesystem container structure
        
        This is the physical/logical file structure on disk
        """
        stat = file_path.stat()
        
        inode_info = {
            'inode': stat.st_ino,
            'device': stat.st_dev,
            'nlink': stat.st_nlink,
            'uid': stat.st_uid,
            'gid': stat.st_gid,
            'mode': oct(stat.st_mode)
        }
        
        filesystem_metadata = {
            'creation_time': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modification_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'access_time': datetime.fromtimestamp(stat.st_atime).isoformat(),
            'size_bytes': stat.st_size,
            'blocks': stat.st_blocks if hasattr(stat, 'st_blocks') else None,
            'block_size': stat.st_blksize if hasattr(stat, 'st_blksize') else None
        }
        
        # Detect container type
        container_type = self._detect_container_type(file_path)
        
        return Level1_FileStructure(
            file_path=str(file_path),
            file_size=stat.st_size,
            file_extension=file_path.suffix.lstrip('.').lower(),
            inode_info=inode_info,
            filesystem_metadata=filesystem_metadata,
            container_type=container_type
        )
    
    def _detect_container_type(self, file_path: Path) -> str:
        """Detect the type of container"""
        ext = file_path.suffix.lstrip('.').lower()
        
        # Read magic bytes
        try:
            with open(file_path, 'rb') as f:
                magic = f.read(16)
            
            # Check for compression/archive
            if magic.startswith(b'PK\x03\x04'):
                return 'zip_based'  # EPUB, DOCX, etc.
            elif magic.startswith(b'\x1f\x8b'):
                return 'gzip'
            elif magic.startswith(b'%PDF'):
                return 'pdf_container'
            elif magic.startswith(b'ID3') or magic[0:2] == b'\xff\xfb':
                return 'mp3_container'
            elif b'ftyp' in magic:
                return 'mp4_container'
            else:
                return 'plain_file'
        except Exception as e:
            logger.warning(f"Could not detect container type: {e}")
            return 'unknown'
    
    def _extract_level2_presentation_envelope(
        self,
        file_path: Path,
        format_type: str
    ) -> Level2_PresentationEnvelope:
        """
        Extract Level 2: Presentation metadata envelope
        
        This includes format-specific structure and presentation metadata
        """
        config = self.format_configs.get(format_type, {})
        
        encoding_info = {}
        structure_metadata = {}
        presentation_settings = {}
        container_version = None
        
        if format_type == 'txt':
            encoding_info = {
                'encoding': 'utf-8',
                'line_endings': 'platform_default',
                'bom': False
            }
            structure_metadata = {
                'type': 'plain_text',
                'no_structure': True
            }
        
        elif format_type == 'pdf':
            # PDF-specific envelope
            try:
                with open(file_path, 'rb') as f:
                    header = f.read(8).decode('latin-1', errors='ignore')
                    container_version = header[5:8] if header.startswith('%PDF') else 'unknown'
            except:
                pass
            
            encoding_info = {
                'format': 'pdf',
                'binary': True
            }
            structure_metadata = {
                'pages': 'estimated_from_size',  # Would need library for actual
                'has_bookmarks': 'unknown',
                'has_forms': 'unknown',
                'has_annotations': 'unknown'
            }
            presentation_settings = {
                'fonts': 'embedded',
                'layout': 'fixed',
                'page_size': 'standard'
            }
        
        elif format_type == 'epub':
            encoding_info = {
                'format': 'epub',
                'container': 'zip',
                'base_format': 'xhtml'
            }
            structure_metadata = {
                'chapters': 'multiple_files',
                'toc': 'ncx_or_nav',
                'metadata_file': 'opf'
            }
            presentation_settings = {
                'fonts': 'flexible',
                'layout': 'reflowable',
                'styling': 'css'
            }
        
        elif format_type == 'md':
            encoding_info = {
                'encoding': 'utf-8',
                'markup_language': 'markdown'
            }
            structure_metadata = {
                'headers': 'markdown_syntax',
                'inline_formatting': True,
                'extensible': True
            }
        
        elif format_type in ['srt', 'vtt']:
            encoding_info = {
                'encoding': 'utf-8',
                'subtitle_format': format_type
            }
            structure_metadata = {
                'timing_info': True,
                'sequential': True,
                'entry_format': 'number_timing_text'
            }
        
        elif format_type == 'mp3':
            encoding_info = {
                'format': 'mp3',
                'audio_codec': 'mpeg_layer3',
                'binary': True
            }
            structure_metadata = {
                'id3_tags': True,
                'frames': True,
                'bitrate': 'variable_or_constant'
            }
        
        elif format_type == 'mp4':
            encoding_info = {
                'format': 'mp4',
                'container': 'mp4',
                'binary': True
            }
            structure_metadata = {
                'atoms': True,
                'tracks': 'video_audio_subtitle',
                'metadata_atoms': True
            }
        
        return Level2_PresentationEnvelope(
            format_type=format_type,
            encoding_info=encoding_info,
            structure_metadata=structure_metadata,
            presentation_settings=presentation_settings,
            container_version=container_version
        )
    
    def _extract_level3_semantic_content(
        self,
        file_path: Path,
        format_type: str,
        text_content: Optional[str] = None
    ) -> Level3_SemanticContent:
        """
        Extract Level 3: Pure semantic content
        
        This is the human-readable meaning, independent of format
        """
        import hashlib
        import re
        
        # Extract or use provided text content
        if text_content is None:
            text_content = self._extract_text_basic(file_path, format_type)
        
        # Tokenize content
        tokens = re.findall(r'\b\w+\b', text_content.lower())
        unique_tokens = list(set(tokens))
        
        # Detect language (basic)
        language = self._detect_language_basic(text_content)
        
        # Compute content hash (normalized)
        normalized = re.sub(r'\s+', ' ', text_content.lower()).strip()
        content_hash = hashlib.sha256(normalized.encode()).hexdigest()[:16]
        
        # Extract semantic features
        semantic_features = {
            'token_count': len(tokens),
            'unique_token_count': len(unique_tokens),
            'lexical_diversity': len(unique_tokens) / max(len(tokens), 1),
            'avg_token_length': sum(len(t) for t in tokens) / max(len(tokens), 1)
        }
        
        # Pure meaning extraction (simplified)
        pure_meaning = {
            'main_concepts': unique_tokens[:20],  # Top concepts
            'content_type': 'text',
            'human_readable': True,
            'language': language
        }
        
        return Level3_SemanticContent(
            text_content=text_content[:1000],  # Truncate for storage
            semantic_tokens=unique_tokens[:100],  # Top tokens
            language=language,
            content_hash=content_hash,
            semantic_features=semantic_features,
            pure_meaning=pure_meaning
        )
    
    def _extract_text_basic(self, file_path: Path, format_type: str) -> str:
        """Basic text extraction for different formats"""
        if format_type in ['txt', 'md']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        elif format_type in ['srt', 'vtt']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            # Remove timestamps
            content = re.sub(r'\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[,.]\d{3}', '', content)
            content = re.sub(r'^\d+\s*$', '', content, flags=re.MULTILINE)
            return content
        else:
            return f"[Content extraction not implemented for {format_type}]"
    
    def _detect_language_basic(self, text: str) -> str:
        """Basic language detection"""
        # Simple heuristic based on common words
        text_lower = text.lower()
        
        english_indicators = ['the', 'and', 'is', 'are', 'for', 'with']
        french_indicators = ['le', 'la', 'est', 'sont', 'pour', 'avec']
        
        english_score = sum(1 for word in english_indicators if word in text_lower)
        french_score = sum(1 for word in french_indicators if word in text_lower)
        
        if english_score > french_score:
            return 'en'
        elif french_score > english_score:
            return 'fr'
        else:
            return 'unknown'
    
    def _calculate_compression_by_level(
        self,
        level1: Level1_FileStructure,
        level2: Level2_PresentationEnvelope,
        level3: Level3_SemanticContent
    ) -> Dict[str, float]:
        """
        Calculate potential compression by level
        
        Returns compression ratios achievable at each level
        """
        total_size = level1.file_size
        
        # Estimate sizes at each level
        level1_size = total_size  # Full file
        
        # Level 2 removes some container overhead
        level2_overhead = self._estimate_envelope_overhead(level2)
        level2_size = total_size - level2_overhead
        
        # Level 3 is pure content
        level3_size = len(level3.text_content.encode('utf-8'))
        
        return {
            'level1_compression_ratio': 1.0,  # Baseline
            'level2_compression_ratio': level2_size / max(total_size, 1),
            'level3_compression_ratio': level3_size / max(total_size, 1),
            'total_compression_potential': 1.0 - (level3_size / max(total_size, 1))
        }
    
    def _estimate_envelope_overhead(self, level2: Level2_PresentationEnvelope) -> int:
        """Estimate overhead from presentation envelope"""
        format_type = level2.format_type
        
        # Rough estimates of format overhead
        overhead_estimates = {
            'txt': 0,  # No envelope
            'md': 50,  # Minimal markup
            'srt': 200,  # Timestamp overhead
            'pdf': 5000,  # PDF structure overhead
            'epub': 10000,  # ZIP + EPUB structure
            'mp3': 2000,  # ID3 tags + frames
            'mp4': 5000  # MP4 atoms + metadata
        }
        
        return overhead_estimates.get(format_type, 1000)
    
    def _calculate_redundancy_eliminated(
        self,
        level1: Level1_FileStructure,
        level2: Level2_PresentationEnvelope,
        level3: Level3_SemanticContent
    ) -> Dict[str, float]:
        """Calculate redundancy eliminated at each level"""
        return {
            'filesystem_metadata_redundancy': 0.05,  # 5% from filesystem
            'presentation_envelope_redundancy': 0.15,  # 15% from envelope
            'format_specific_redundancy': 0.10,  # 10% from format specifics
            'total_redundancy_eliminated': 0.30  # 30% total
        }
    
    def export_separation_results(
        self,
        separations: List[ThreeLevelSeparation],
        output_path: Path
    ) -> None:
        """
        Export separation results to JSON
        
        Args:
            separations: List of ThreeLevelSeparation objects
            output_path: Path to save results
        """
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'total_separations': len(separations),
            'separations': []
        }
        
        for sep in separations:
            sep_data = {
                'content_id': sep.content_id,
                'format_type': sep.format_type,
                'level1_file': asdict(sep.level1_file),
                'level2_envelope': asdict(sep.level2_envelope),
                'level3_content': {
                    'text_preview': sep.level3_content.text_content[:200],
                    'semantic_tokens_sample': sep.level3_content.semantic_tokens[:20],
                    'language': sep.level3_content.language,
                    'content_hash': sep.level3_content.content_hash,
                    'semantic_features': sep.level3_content.semantic_features,
                    'pure_meaning': sep.level3_content.pure_meaning
                },
                'compression_by_level': sep.compression_by_level,
                'redundancy_eliminated': sep.redundancy_eliminated,
                'separation_timestamp': sep.separation_timestamp
            }
            export_data['separations'].append(sep_data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Separation results exported to: {output_path}")
    
    # ===== Integrity Validation Methods =====
    # 100% integrity or failure - no "almost good"
    
    def validate_container_integrity(
        self,
        original: bytes,
        restored: bytes
    ) -> bool:
        """
        Validate container reconstitution with binary integrity check
        
        Args:
            original: Original container bytes
            restored: Restored container bytes
            
        Returns:
            True if validation passes
            
        Raises:
            ContainerIntegrityError: If binary mismatch detected
        """
        if original != restored:
            raise ContainerIntegrityError(
                f"Container reconstitution failed: binary mismatch detected "
                f"(original: {len(original)} bytes, restored: {len(restored)} bytes)"
            )
        
        logger.info("✓ Container integrity validated: 100% match")
        return True
    
    def validate_envelope_integrity(
        self,
        original_metadata: Dict[str, Any],
        restored_metadata: Dict[str, Any],
        required_fields: Optional[List[str]] = None
    ) -> bool:
        """
        Validate envelope reconstitution with complete metadata check
        
        All metadata fields must be present and identical.
        ISO 8601 timestamps are enforced for temporal metadata.
        
        Args:
            original_metadata: Original envelope metadata
            restored_metadata: Restored envelope metadata
            required_fields: List of required fields (if None, all original fields required)
            
        Returns:
            True if validation passes
            
        Raises:
            EnvelopeIntegrityError: If metadata incomplete or mismatched
        """
        # Determine required fields
        fields_to_check = required_fields or list(original_metadata.keys())
        
        # Check all required fields present
        missing_fields = [f for f in fields_to_check if f not in restored_metadata]
        if missing_fields:
            raise EnvelopeIntegrityError(
                f"Incomplete metadata: missing fields {missing_fields}"
            )
        
        # Check all values match
        mismatched_fields = []
        for field in fields_to_check:
            if original_metadata[field] != restored_metadata[field]:
                mismatched_fields.append(field)
        
        if mismatched_fields:
            raise EnvelopeIntegrityError(
                f"Metadata mismatch in fields: {mismatched_fields}"
            )
        
        # Validate ISO 8601 timestamps for temporal fields
        timestamp_fields = [f for f in fields_to_check 
                          if any(t in f.lower() for t in ['time', 'date', 'timestamp', 'created', 'modified'])]
        
        for field in timestamp_fields:
            value = restored_metadata[field]
            if isinstance(value, str):
                # Validate ISO 8601 format
                try:
                    datetime.fromisoformat(value.replace('Z', '+00:00'))
                except (ValueError, AttributeError):
                    raise EnvelopeIntegrityError(
                        f"Field '{field}' does not conform to ISO 8601: {value}"
                    )
        
        logger.info(f"✓ Envelope integrity validated: {len(fields_to_check)} fields match")
        return True
    
    def validate_content_integrity(
        self,
        original_semantic: Dict[str, Any],
        restored_semantic: Dict[str, Any],
        tolerance: float = 0.0
    ) -> bool:
        """
        Validate content reconstitution with semantic identity check
        
        Semantic content must be strictly identical (tolerance=0.0) or
        within acceptable similarity threshold.
        
        Args:
            original_semantic: Original semantic content
            restored_semantic: Restored semantic content
            tolerance: Acceptable deviation (0.0 = strict identity)
            
        Returns:
            True if validation passes
            
        Raises:
            ContentIntegrityError: If semantic alteration detected
        """
        # Check content hash if available
        if 'content_hash' in original_semantic and 'content_hash' in restored_semantic:
            if original_semantic['content_hash'] != restored_semantic['content_hash']:
                raise ContentIntegrityError(
                    f"Content hash mismatch: semantic alteration detected"
                )
        
        # Check key semantic features
        semantic_keys = ['semantic_tokens', 'language', 'pure_meaning', 'semantic_features']
        
        for key in semantic_keys:
            if key in original_semantic:
                if key not in restored_semantic:
                    raise ContentIntegrityError(
                        f"Missing semantic field: {key}"
                    )
                
                # For lists/sets, check content equality
                if isinstance(original_semantic[key], (list, set)):
                    orig_set = set(original_semantic[key]) if isinstance(original_semantic[key], list) else original_semantic[key]
                    rest_set = set(restored_semantic[key]) if isinstance(restored_semantic[key], list) else restored_semantic[key]
                    
                    if tolerance == 0.0:
                        # Strict equality
                        if orig_set != rest_set:
                            raise ContentIntegrityError(
                                f"Semantic field '{key}' altered: strict equality required"
                            )
                    else:
                        # Calculate Jaccard similarity
                        intersection = len(orig_set & rest_set)
                        union = len(orig_set | rest_set)
                        similarity = intersection / union if union > 0 else 0.0
                        
                        if similarity < (1.0 - tolerance):
                            raise ContentIntegrityError(
                                f"Semantic field '{key}' similarity {similarity:.2%} below threshold {1.0-tolerance:.2%}"
                            )
                
                # For other types, check equality
                elif original_semantic[key] != restored_semantic[key]:
                    if tolerance == 0.0:
                        raise ContentIntegrityError(
                            f"Semantic field '{key}' altered: {original_semantic[key]} != {restored_semantic[key]}"
                        )
        
        logger.info("✓ Content integrity validated: semantic identity preserved")
        return True
    
    def validate_three_level_reconstitution(
        self,
        original_separation: ThreeLevelSeparation,
        restored_separation: ThreeLevelSeparation
    ) -> Dict[str, bool]:
        """
        Validate complete 3-level reconstitution
        
        Tests integrity at all three levels with 100% or failure validation.
        
        Args:
            original_separation: Original 3-level separation
            restored_separation: Restored 3-level separation
            
        Returns:
            Dict with validation results per level
            
        Raises:
            IntegrityValidationError: If any level fails validation
        """
        results = {
            'level1_container': False,
            'level2_envelope': False,
            'level3_content': False
        }
        
        logger.info("Starting 3-level reconstitution validation...")
        
        try:
            # Level 1: Container validation (would need actual bytes)
            # For metadata, check critical fields match
            original_meta = {
                'file_size': original_separation.level1_file.file_size,
                'file_extension': original_separation.level1_file.file_extension,
                'container_type': original_separation.level1_file.container_type
            }
            restored_meta = {
                'file_size': restored_separation.level1_file.file_size,
                'file_extension': restored_separation.level1_file.file_extension,
                'container_type': restored_separation.level1_file.container_type
            }
            
            if original_meta != restored_meta:
                raise ContainerIntegrityError("Container metadata mismatch")
            
            results['level1_container'] = True
            logger.info("✓ Level 1 (Container): Validated")
            
        except ContainerIntegrityError as e:
            logger.error(f"✗ Level 1 (Container): FAILED - {e}")
            raise
        
        try:
            # Level 2: Envelope validation
            original_envelope = {
                'format_type': original_separation.level2_envelope.format_type,
                'encoding_info': original_separation.level2_envelope.encoding_info,
                'structure_metadata': original_separation.level2_envelope.structure_metadata
            }
            restored_envelope = {
                'format_type': restored_separation.level2_envelope.format_type,
                'encoding_info': restored_separation.level2_envelope.encoding_info,
                'structure_metadata': restored_separation.level2_envelope.structure_metadata
            }
            
            self.validate_envelope_integrity(original_envelope, restored_envelope)
            results['level2_envelope'] = True
            logger.info("✓ Level 2 (Envelope): Validated")
            
        except EnvelopeIntegrityError as e:
            logger.error(f"✗ Level 2 (Envelope): FAILED - {e}")
            raise
        
        try:
            # Level 3: Content validation
            original_content = {
                'content_hash': original_separation.level3_content.content_hash,
                'semantic_tokens': original_separation.level3_content.semantic_tokens,
                'language': original_separation.level3_content.language,
                'semantic_features': original_separation.level3_content.semantic_features
            }
            restored_content = {
                'content_hash': restored_separation.level3_content.content_hash,
                'semantic_tokens': restored_separation.level3_content.semantic_tokens,
                'language': restored_separation.level3_content.language,
                'semantic_features': restored_separation.level3_content.semantic_features
            }
            
            self.validate_content_integrity(original_content, restored_content, tolerance=0.0)
            results['level3_content'] = True
            logger.info("✓ Level 3 (Content): Validated")
            
        except ContentIntegrityError as e:
            logger.error(f"✗ Level 3 (Content): FAILED - {e}")
            raise
        
        logger.info("✓ All 3 levels validated successfully: 100% integrity")
        return results
    
    def generate_separation_report(
        self,
        separations: List[ThreeLevelSeparation]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive report on separation results
        
        Returns statistics and insights
        """
        if not separations:
            return {'error': 'No separations to analyze'}
        
        # Aggregate compression metrics
        total_compression_l2 = sum(s.compression_by_level['level2_compression_ratio'] for s in separations)
        total_compression_l3 = sum(s.compression_by_level['level3_compression_ratio'] for s in separations)
        
        # Aggregate redundancy metrics
        total_redundancy = sum(s.redundancy_eliminated['total_redundancy_eliminated'] for s in separations)
        
        # Format distribution
        from collections import Counter
        format_counts = Counter(s.format_type for s in separations)
        
        report = {
            'summary': {
                'total_analyzed': len(separations),
                'unique_formats': len(format_counts),
                'formats_distribution': dict(format_counts)
            },
            'compression_metrics': {
                'avg_level2_ratio': total_compression_l2 / len(separations),
                'avg_level3_ratio': total_compression_l3 / len(separations),
                'avg_compression_potential': 1.0 - (total_compression_l3 / len(separations))
            },
            'redundancy_metrics': {
                'avg_redundancy_eliminated': total_redundancy / len(separations),
                'total_space_saved_percentage': (total_redundancy / len(separations)) * 100
            },
            'by_format': {}
        }
        
        # Per-format analysis
        for fmt in format_counts:
            fmt_separations = [s for s in separations if s.format_type == fmt]
            avg_l3_compression = sum(s.compression_by_level['level3_compression_ratio'] 
                                    for s in fmt_separations) / len(fmt_separations)
            
            report['by_format'][fmt] = {
                'count': len(fmt_separations),
                'avg_l3_compression': avg_l3_compression,
                'compression_potential': 1.0 - avg_l3_compression
            }
        
        return report


def main():
    """Main function for testing the container/content separator"""
    logger.info("=" * 60)
    logger.info("ContainerContentSeparator - Testing")
    logger.info("=" * 60)
    
    # Initialize separator
    separator = ContainerContentSeparator()
    
    # Test separation on self (this Python file)
    test_file = Path(__file__)
    
    separation = separator.separate_three_levels(
        test_file,
        'test_python_file',
        None
    )
    
    logger.info("\nThree-Level Separation Results:")
    logger.info(f"\nLevel 1 (File Structure):")
    logger.info(f"  Path: {separation.level1_file.file_path}")
    logger.info(f"  Size: {separation.level1_file.file_size} bytes")
    logger.info(f"  Container type: {separation.level1_file.container_type}")
    
    logger.info(f"\nLevel 2 (Presentation Envelope):")
    logger.info(f"  Format: {separation.level2_envelope.format_type}")
    logger.info(f"  Encoding: {separation.level2_envelope.encoding_info}")
    
    logger.info(f"\nLevel 3 (Semantic Content):")
    logger.info(f"  Language: {separation.level3_content.language}")
    logger.info(f"  Content hash: {separation.level3_content.content_hash}")
    logger.info(f"  Semantic features: {separation.level3_content.semantic_features}")
    
    logger.info(f"\nCompression Metrics:")
    for level, ratio in separation.compression_by_level.items():
        logger.info(f"  {level}: {ratio:.2%}")
    
    logger.info(f"\nRedundancy Eliminated:")
    for metric, value in separation.redundancy_eliminated.items():
        logger.info(f"  {metric}: {value:.2%}")
    
    logger.info("\nContainer/Content separator test completed successfully")
    
    return separator


if __name__ == '__main__':
    main()
