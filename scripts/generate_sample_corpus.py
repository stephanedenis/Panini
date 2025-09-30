#!/usr/bin/env python3
"""
Sample Corpus Generator - PaniniFS Research
Generates sample multi-format corpus for testing
"""

import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_sample_book_content():
    """Create sample book content in multiple formats"""
    
    corpus_root = Path("data/multi_format_corpus/books")
    corpus_root.mkdir(parents=True, exist_ok=True)
    
    # Sample book 1: "Introduction to PaniniFS"
    book1_content = """Introduction to PaniniFS

PaniniFS is a revolutionary filesystem that separates container structure from semantic content.
This allows for optimized compression and intelligent content addressing.

Chapter 1: The Problem
Traditional filesystems treat all files as opaque byte sequences.
This approach misses opportunities for semantic optimization and deduplication.

Chapter 2: The Solution
PaniniFS analyzes content at three levels:
1. File structure (container)
2. Presentation envelope (metadata)
3. Pure semantic content (meaning)

By separating these levels, we achieve superior compression and content-based deduplication.

Conclusion
PaniniFS represents a paradigm shift in how we think about file storage.
The future of filesystems is semantic, not just structural."""

    # Save as TXT
    with open(corpus_root / "intro_panini.txt", "w", encoding="utf-8") as f:
        f.write(book1_content)
    
    # Save as MD (with markdown formatting)
    md_content = """# Introduction to PaniniFS

**PaniniFS** is a revolutionary filesystem that separates container structure from semantic content.
This allows for optimized compression and intelligent content addressing.

## Chapter 1: The Problem

Traditional filesystems treat all files as *opaque byte sequences*.
This approach misses opportunities for semantic optimization and deduplication.

## Chapter 2: The Solution

PaniniFS analyzes content at **three levels**:
1. File structure (container)
2. Presentation envelope (metadata)
3. Pure semantic content (meaning)

By separating these levels, we achieve superior compression and content-based deduplication.

## Conclusion

PaniniFS represents a paradigm shift in how we think about file storage.
*The future of filesystems is semantic, not just structural.*"""
    
    with open(corpus_root / "intro_panini.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    
    # Create a fake PDF header (placeholder)
    with open(corpus_root / "intro_panini.pdf", "wb") as f:
        f.write(b'%PDF-1.4\n')
        f.write(b'% Placeholder PDF file\n')
        f.write(book1_content.encode('utf-8'))
    
    logger.info("Created sample book: intro_panini (txt, md, pdf)")
    
    # Sample book 2: "Dhatu Theory"
    book2_content = """Dhatu Theory and Semantic Roots

Dhatu are the fundamental semantic units in Sanskrit grammar.
They represent the irreducible roots of meaning in language.

Origins
The concept of dhatu comes from Panini's Ashtadhyayi.
These roots form the basis of word formation and meaning.

Application to Computing
In PaniniFS, we apply dhatu theory to content analysis.
By identifying semantic roots, we can deduplicate content at the meaning level.

Benefits
- Language-independent content addressing
- Semantic deduplication across translations
- Universal content patterns

Implementation
Modern NLP combined with dhatu theory enables breakthrough compression."""

    with open(corpus_root / "dhatu_theory.txt", "w", encoding="utf-8") as f:
        f.write(book2_content)
    
    with open(corpus_root / "dhatu_theory.md", "w", encoding="utf-8") as f:
        f.write(book2_content.replace('\n\n', '\n\n## '))
    
    logger.info("Created sample book: dhatu_theory (txt, md)")


def create_sample_audio_content():
    """Create sample audio content with transcription"""
    
    corpus_root = Path("data/multi_format_corpus/audio")
    corpus_root.mkdir(parents=True, exist_ok=True)
    
    # Transcription for audio 1
    transcript1 = """Welcome to PaniniFS podcast.

In this episode, we explore how semantic filesystems work.
Traditional filesystems only understand bytes and blocks.
But what if your filesystem understood meaning?

That's where PaniniFS comes in.
By analyzing content at multiple levels, we can achieve compression ratios that seem impossible.

The key insight is separating the container from the content.
The container is how data is stored.
The content is what the data means.

Join us next time as we dive deeper into dhatu theory."""

    with open(corpus_root / "podcast_episode1.txt", "w", encoding="utf-8") as f:
        f.write(transcript1)
    
    # Create placeholder MP3 (with ID3 header)
    with open(corpus_root / "podcast_episode1.mp3", "wb") as f:
        f.write(b'ID3\x03\x00\x00\x00\x00\x00\x00')
        f.write(b'\xff\xfb\x90\x00')  # MP3 frame header
        f.write(b'\x00' * 1000)  # Placeholder audio data
    
    logger.info("Created sample audio: podcast_episode1 (txt transcription, mp3)")
    
    # Transcription for audio 2
    transcript2 = """PaniniFS Technical Deep Dive

This talk covers the architecture of PaniniFS.
We'll examine the three-level separation model.

Level one is the filesystem container.
This includes inodes, blocks, and filesystem metadata.

Level two is the presentation envelope.
For a PDF, this is the PDF structure.
For an EPUB, this is the ZIP container and metadata.

Level three is pure semantic content.
This is the meaning, independent of format.
A book has the same semantic content whether it's PDF, EPUB, or plain text.

By optimizing each level independently, we achieve superior results."""

    with open(corpus_root / "tech_talk.txt", "w", encoding="utf-8") as f:
        f.write(transcript2)
    
    logger.info("Created sample audio: tech_talk (txt transcription)")


def create_sample_video_content():
    """Create sample video content with subtitles"""
    
    corpus_root = Path("data/multi_format_corpus/video")
    corpus_root.mkdir(parents=True, exist_ok=True)
    
    # Subtitles for video 1 (SRT format)
    srt1 = """1
00:00:00,000 --> 00:00:03,000
Welcome to the PaniniFS video tutorial

2
00:00:03,500 --> 00:00:07,000
In this video we'll learn about multi-format analysis

3
00:00:07,500 --> 00:00:11,000
The same content can exist in many formats

4
00:00:11,500 --> 00:00:15,000
Text files, PDFs, EPUBs all contain the same information

5
00:00:15,500 --> 00:00:19,000
PaniniFS extracts the invariant semantic content

6
00:00:19,500 --> 00:00:23,000
This enables cross-format deduplication and compression

7
00:00:23,500 --> 00:00:27,000
Thank you for watching"""

    with open(corpus_root / "tutorial_video.srt", "w", encoding="utf-8") as f:
        f.write(srt1)
    
    # Create placeholder MP4
    with open(corpus_root / "tutorial_video.mp4", "wb") as f:
        # MP4 file type box
        f.write(b'\x00\x00\x00\x20ftypisom\x00\x00\x02\x00')
        f.write(b'isomiso2mp41')
        f.write(b'\x00' * 1000)  # Placeholder video data
    
    logger.info("Created sample video: tutorial_video (srt, mp4)")
    
    # VTT format for video 2
    vtt1 = """WEBVTT

00:00:00.000 --> 00:00:04.000
Container versus content separation explained

00:00:04.500 --> 00:00:08.000
Every file has a container and content

00:00:08.500 --> 00:00:12.000
The container is format-specific structure

00:00:12.500 --> 00:00:16.000
The content is the semantic meaning

00:00:16.500 --> 00:00:20.000
Separating these enables better optimization"""

    with open(corpus_root / "explainer_video.vtt", "w", encoding="utf-8") as f:
        f.write(vtt1)
    
    logger.info("Created sample video: explainer_video (vtt)")


def main():
    """Generate complete sample corpus"""
    logger.info("=" * 60)
    logger.info("Sample Corpus Generator")
    logger.info("=" * 60)
    
    create_sample_book_content()
    create_sample_audio_content()
    create_sample_video_content()
    
    logger.info("\n" + "=" * 60)
    logger.info("Sample corpus generation completed!")
    logger.info("=" * 60)
    logger.info("\nCreated multi-format content:")
    logger.info("  Books: intro_panini (txt, md, pdf), dhatu_theory (txt, md)")
    logger.info("  Audio: podcast_episode1 (txt, mp3), tech_talk (txt)")
    logger.info("  Video: tutorial_video (srt, mp4), explainer_video (vtt)")


if __name__ == "__main__":
    main()
