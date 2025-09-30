#!/usr/bin/env python3
"""
Multi-Format Analyzer - PaniniFS Research
Analyseur multi-format pour séparation contenant/contenu

Supports:
- Books: TXT/PDF/EPUB (same content)
- Audio: Transcription/MP3 (same content)
- Video: Subtitles/MP4 (same content)
"""

import hashlib
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class FormatMetadata:
    """Metadata specific to a file format"""
    format_type: str  # txt, pdf, epub, mp3, mp4, srt
    file_size: int
    encoding: Optional[str] = None
    mime_type: Optional[str] = None
    creation_date: Optional[str] = None
    container_structure: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.container_structure is None:
            self.container_structure = {}


@dataclass
class ContentItem:
    """Represents content available in multiple formats"""
    content_id: str
    title: str
    content_type: str  # book, audio, video
    formats: Dict[str, Path]  # format -> file path
    metadata_by_format: Dict[str, FormatMetadata]
    
    def __post_init__(self):
        if not self.formats:
            self.formats = {}
        if not self.metadata_by_format:
            self.metadata_by_format = {}


class MultiFormatAnalyzer:
    """Analyzer for multi-format content corpus"""
    
    def __init__(self, corpus_root: Optional[Path] = None):
        """
        Initialize the multi-format analyzer
        
        Args:
            corpus_root: Root directory for multi-format corpus
        """
        self.corpus_root = corpus_root or Path("./data/multi_format_corpus")
        self.corpus_root.mkdir(parents=True, exist_ok=True)
        
        # Content registry: content_id -> ContentItem
        self.content_registry: Dict[str, ContentItem] = {}
        
        # Format groups for content types
        self.format_groups = {
            'book': ['txt', 'pdf', 'epub', 'html', 'md'],
            'audio': ['txt', 'mp3', 'wav', 'flac', 'srt'],  # txt = transcription
            'video': ['srt', 'vtt', 'mp4', 'webm', 'mkv']
        }
        
        logger.info(f"MultiFormatAnalyzer initialized with corpus root: {self.corpus_root}")
    
    def generate_content_id(self, title: str, content_type: str) -> str:
        """Generate unique content ID from title and type"""
        content_hash = hashlib.md5(f"{title}:{content_type}".encode()).hexdigest()[:8]
        return f"{content_type}_{content_hash}"
    
    def detect_format(self, file_path: Path) -> str:
        """Detect file format from extension"""
        return file_path.suffix.lstrip('.').lower()
    
    def extract_format_metadata(self, file_path: Path) -> FormatMetadata:
        """
        Extract metadata specific to the file format
        
        Args:
            file_path: Path to the file
            
        Returns:
            FormatMetadata object with container-specific information
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        format_type = self.detect_format(file_path)
        file_size = file_path.stat().st_size
        
        # Basic metadata
        metadata = FormatMetadata(
            format_type=format_type,
            file_size=file_size,
            creation_date=datetime.fromtimestamp(file_path.stat().st_ctime).isoformat()
        )
        
        # Format-specific container structure
        if format_type == 'txt':
            metadata.encoding = 'utf-8'
            metadata.mime_type = 'text/plain'
            metadata.container_structure = self._analyze_txt_structure(file_path)
        
        elif format_type == 'pdf':
            metadata.mime_type = 'application/pdf'
            metadata.container_structure = self._analyze_pdf_structure(file_path)
        
        elif format_type == 'epub':
            metadata.mime_type = 'application/epub+zip'
            metadata.container_structure = self._analyze_epub_structure(file_path)
        
        elif format_type == 'md':
            metadata.encoding = 'utf-8'
            metadata.mime_type = 'text/markdown'
            metadata.container_structure = self._analyze_markdown_structure(file_path)
        
        elif format_type in ['mp3', 'wav', 'flac']:
            metadata.mime_type = f'audio/{format_type}'
            metadata.container_structure = self._analyze_audio_structure(file_path)
        
        elif format_type in ['mp4', 'webm', 'mkv']:
            metadata.mime_type = f'video/{format_type}'
            metadata.container_structure = self._analyze_video_structure(file_path)
        
        elif format_type in ['srt', 'vtt']:
            metadata.encoding = 'utf-8'
            metadata.mime_type = 'text/plain'
            metadata.container_structure = self._analyze_subtitle_structure(file_path)
        
        return metadata
    
    def _analyze_txt_structure(self, file_path: Path) -> Dict[str, Any]:
        """Analyze plain text file structure"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        lines = content.split('\n')
        return {
            'line_count': len(lines),
            'char_count': len(content),
            'has_bom': content.startswith('\ufeff'),
            'line_endings': 'CRLF' if '\r\n' in content else 'LF',
            'encoding_confidence': 'high'
        }
    
    def _analyze_pdf_structure(self, file_path: Path) -> Dict[str, Any]:
        """Analyze PDF container structure (basic, without PDF library)"""
        with open(file_path, 'rb') as f:
            header = f.read(8)
            f.seek(0, 2)  # End of file
            file_size = f.tell()
        
        # Basic PDF structure analysis
        is_pdf = header.startswith(b'%PDF')
        version = header.decode('latin-1', errors='ignore')[5:8] if is_pdf else 'unknown'
        
        return {
            'is_valid_pdf': is_pdf,
            'pdf_version': version,
            'file_size': file_size,
            'has_encryption': False,  # Would need PDF library for full analysis
            'container_type': 'pdf'
        }
    
    def _analyze_epub_structure(self, file_path: Path) -> Dict[str, Any]:
        """Analyze EPUB container structure (basic, without ZIP library)"""
        with open(file_path, 'rb') as f:
            header = f.read(4)
        
        is_zip = header.startswith(b'PK\x03\x04')
        
        return {
            'is_valid_zip': is_zip,
            'container_type': 'epub',
            'expected_structure': ['META-INF', 'OEBPS', 'mimetype'],
            'file_size': file_path.stat().st_size
        }
    
    def _analyze_markdown_structure(self, file_path: Path) -> Dict[str, Any]:
        """Analyze Markdown file structure"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Count markdown elements
        headers = len(re.findall(r'^#+\s', content, re.MULTILINE))
        links = len(re.findall(r'\[.*?\]\(.*?\)', content))
        code_blocks = len(re.findall(r'```', content)) // 2
        
        return {
            'header_count': headers,
            'link_count': links,
            'code_block_count': code_blocks,
            'char_count': len(content),
            'line_count': len(content.split('\n'))
        }
    
    def _analyze_audio_structure(self, file_path: Path) -> Dict[str, Any]:
        """Analyze audio file structure (basic, without audio library)"""
        with open(file_path, 'rb') as f:
            header = f.read(12)
        
        # Detect audio format by magic bytes
        is_mp3 = header.startswith(b'ID3') or header[0:2] == b'\xff\xfb'
        is_wav = header.startswith(b'RIFF')
        is_flac = header.startswith(b'fLaC')
        
        return {
            'is_valid_audio': is_mp3 or is_wav or is_flac,
            'detected_format': 'mp3' if is_mp3 else ('wav' if is_wav else ('flac' if is_flac else 'unknown')),
            'file_size': file_path.stat().st_size,
            'container_type': 'audio'
        }
    
    def _analyze_video_structure(self, file_path: Path) -> Dict[str, Any]:
        """Analyze video file structure (basic)"""
        with open(file_path, 'rb') as f:
            header = f.read(12)
        
        is_mp4 = b'ftyp' in header
        is_webm = header.startswith(b'\x1a\x45\xdf\xa3')
        
        return {
            'is_valid_video': is_mp4 or is_webm,
            'detected_format': 'mp4' if is_mp4 else ('webm' if is_webm else 'unknown'),
            'file_size': file_path.stat().st_size,
            'container_type': 'video'
        }
    
    def _analyze_subtitle_structure(self, file_path: Path) -> Dict[str, Any]:
        """Analyze subtitle file structure"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Detect subtitle format
        is_srt = bool(re.search(r'^\d+\s*$', content, re.MULTILINE))
        is_vtt = content.strip().startswith('WEBVTT')
        
        # Count subtitle entries
        if is_srt:
            entries = len(re.findall(r'^\d+\s*$', content, re.MULTILINE))
        else:
            entries = len(re.findall(r'\d{2}:\d{2}:\d{2}', content))
        
        return {
            'subtitle_format': 'srt' if is_srt else ('vtt' if is_vtt else 'unknown'),
            'entry_count': entries,
            'char_count': len(content),
            'line_count': len(content.split('\n'))
        }
    
    def register_content(self, content_item: ContentItem) -> None:
        """Register a content item in the registry"""
        self.content_registry[content_item.content_id] = content_item
        logger.info(f"Registered content: {content_item.content_id} ({content_item.title})")
    
    def scan_directory(self, directory: Path, content_type: str) -> List[ContentItem]:
        """
        Scan directory for multi-format content
        
        Groups files by base name and creates ContentItem for each group
        
        Args:
            directory: Directory to scan
            content_type: Type of content (book, audio, video)
            
        Returns:
            List of discovered ContentItem objects
        """
        if not directory.exists():
            logger.warning(f"Directory not found: {directory}")
            return []
        
        # Group files by base name
        file_groups: Dict[str, List[Path]] = {}
        
        for file_path in directory.iterdir():
            if file_path.is_file():
                base_name = file_path.stem
                if base_name not in file_groups:
                    file_groups[base_name] = []
                file_groups[base_name].append(file_path)
        
        # Create ContentItem for each group with multiple formats
        discovered_items = []
        
        for base_name, files in file_groups.items():
            if len(files) < 2:  # Skip single-format items
                continue
            
            content_id = self.generate_content_id(base_name, content_type)
            
            formats = {}
            metadata_by_format = {}
            
            for file_path in files:
                format_type = self.detect_format(file_path)
                formats[format_type] = file_path
                
                try:
                    metadata = self.extract_format_metadata(file_path)
                    metadata_by_format[format_type] = metadata
                except Exception as e:
                    logger.error(f"Error extracting metadata from {file_path}: {e}")
            
            if len(formats) >= 2:  # Only include if we have at least 2 formats
                content_item = ContentItem(
                    content_id=content_id,
                    title=base_name,
                    content_type=content_type,
                    formats=formats,
                    metadata_by_format=metadata_by_format
                )
                
                self.register_content(content_item)
                discovered_items.append(content_item)
        
        logger.info(f"Scanned {directory}: found {len(discovered_items)} multi-format items")
        return discovered_items
    
    def get_format_coverage_stats(self) -> Dict[str, Any]:
        """Calculate coverage statistics for the corpus"""
        stats = {
            'total_items': len(self.content_registry),
            'by_content_type': {},
            'formats_per_item': {},
            'total_files': 0
        }
        
        for content_id, item in self.content_registry.items():
            # Count by content type
            if item.content_type not in stats['by_content_type']:
                stats['by_content_type'][item.content_type] = 0
            stats['by_content_type'][item.content_type] += 1
            
            # Track formats per item
            num_formats = len(item.formats)
            if num_formats not in stats['formats_per_item']:
                stats['formats_per_item'][num_formats] = 0
            stats['formats_per_item'][num_formats] += 1
            
            stats['total_files'] += num_formats
        
        return stats
    
    def export_registry(self, output_path: Optional[Path] = None) -> Path:
        """
        Export content registry to JSON
        
        Args:
            output_path: Path to save the registry
            
        Returns:
            Path where registry was saved
        """
        if output_path is None:
            output_path = self.corpus_root / 'content_registry.json'
        
        registry_data = {
            'timestamp': datetime.now().isoformat(),
            'corpus_root': str(self.corpus_root),
            'content_items': []
        }
        
        for content_id, item in self.content_registry.items():
            item_data = {
                'content_id': item.content_id,
                'title': item.title,
                'content_type': item.content_type,
                'formats': {fmt: str(path) for fmt, path in item.formats.items()},
                'metadata_by_format': {
                    fmt: asdict(meta) for fmt, meta in item.metadata_by_format.items()
                }
            }
            registry_data['content_items'].append(item_data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(registry_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Registry exported to: {output_path}")
        return output_path
    
    def get_content_by_id(self, content_id: str) -> Optional[ContentItem]:
        """Retrieve content item by ID"""
        return self.content_registry.get(content_id)
    
    def get_all_formats_for_content(self, content_id: str) -> List[str]:
        """Get list of all available formats for a content item"""
        item = self.get_content_by_id(content_id)
        if item:
            return list(item.formats.keys())
        return []


def main():
    """Main function for testing the multi-format analyzer"""
    logger.info("=" * 60)
    logger.info("MultiFormatAnalyzer - Testing")
    logger.info("=" * 60)
    
    # Initialize analyzer
    analyzer = MultiFormatAnalyzer()
    
    # Create test corpus structure
    test_dirs = {
        'books': analyzer.corpus_root / 'books',
        'audio': analyzer.corpus_root / 'audio',
        'video': analyzer.corpus_root / 'video'
    }
    
    for dir_path in test_dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Scan for multi-format content
    for content_type, dir_path in test_dirs.items():
        analyzer.scan_directory(dir_path, content_type)
    
    # Generate statistics
    stats = analyzer.get_format_coverage_stats()
    
    logger.info("\n" + "=" * 60)
    logger.info("CORPUS STATISTICS")
    logger.info("=" * 60)
    logger.info(f"Total multi-format items: {stats['total_items']}")
    logger.info(f"Total files: {stats['total_files']}")
    logger.info(f"\nBy content type:")
    for ctype, count in stats['by_content_type'].items():
        logger.info(f"  {ctype}: {count}")
    logger.info(f"\nFormats per item distribution:")
    for num_formats, count in sorted(stats['formats_per_item'].items()):
        logger.info(f"  {num_formats} formats: {count} items")
    
    # Export registry
    registry_path = analyzer.export_registry()
    logger.info(f"\nRegistry saved to: {registry_path}")
    
    return analyzer


if __name__ == '__main__':
    main()
