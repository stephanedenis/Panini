#!/usr/bin/env python3
"""
§237-fetch: Indian Upanishads from SBE01 + SBE15, per-chapter fix.

NIPADA v0.4.0-α — Panini Research
Date: 2026-05-01

Problem (§212f collision bug):
  In signed_corpus_v212f.json, all upanishads were mapped to volume-level URLs:
    - 5 works → sbe/sbe1/ → ALL got same 194 293-char text (first 30 chapters of SBE01)
      · chandogya, aitareya, kausitaki, kena, isa
    - 8 works → sbe/sbe15/ → ALL got same 158 398-char text (first 30 chapters of SBE15)
      · brihadaranyaka, katha, svetasvatara, mundaka, mandukya, prashna, taittiriya, maitri

  Root cause: fetch_sacred_texts() fetched the volume index then took the first 30 chapters,
  giving every work in the same volume identical text and V14 signature.

Fix:
  Per-upanishad chapter file lists, determined from the SBE volume table of contents:

  SBE01 (Müller 1879) — https://www.sacred-texts.com/hin/sbe01/
    sbe01017.htm = "I. The Khândogya-Upanishad"   → chapters sbe01022–sbe01175 (154 files)
    sbe01018.htm = "II. The Talavakâra-Upanishad"  → chapters sbe01176–sbe01179 (Kena, 4 files)
    sbe01019.htm = "III. The Aitareya-Âranyaka"    → chapters sbe01180–sbe01238 (59 files)
    sbe01020.htm = "IV. The Kaushîtaki-Upanishad"  → chapters sbe01239–sbe01242 (4 files)
    sbe01021.htm = "V. The Vâgasaneyi-Upanishad"   → chapter  sbe01243         (Isa, 1 file)

  SBE15 (Müller 1884) — https://www.sacred-texts.com/hin/sbe15/
    sbe15003.htm = "I: The Katha-Upanishad"        → chapters sbe15010–sbe15015 (6 files)
    sbe15004.htm = "II: The Mundaka-Upanishad"     → chapters sbe15016–sbe15021 (6 files)
    sbe15005.htm = "III: The Taittirîyaka-Upanishad" → chapters sbe15022–sbe15052 (31 files)
    sbe15006.htm = "IV: The Brihadâranyaka-Upanishad" → chapters sbe15053–sbe15099 (47 files)
    sbe15007.htm = "V: The Svetâsvatara-Upanishad" → chapters sbe15100–sbe15105 (6 files)
    sbe15008.htm = "VI: Prasña-Upanishad"          → chapters sbe15106–sbe15111 (6 files)
    sbe15009.htm = "VII: Maitrâyana-Upanishad"     → chapters sbe15112–sbe15118 (7 files)

  Mandukya (12 mantras, very short):
    NOT in SBE15 — use sacred-texts.com hin/upan/ collection (Hume tr.)

Output:
  nipada/corpus/signed_corpus_v237_upanishads.json
  nipada/falsification/nipada_v237_fetch_report.json

Usage:
  python3 nipada_fetch_corpus_v237_upanishads.py [--dry-run]
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Import shared infrastructure from v212f
# ---------------------------------------------------------------------------

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from nipada_fetch_corpus_v212f import (  # noqa: E402
    freq_signature,
    _get,
    _extract_text_from_html,
    CACHE_SACRED_TEXTS,
    CORPUS_DIR,
    FALSI_DIR,
    HTTP_HEADERS,
    REQUEST_DELAY,
    V14_ATOMS,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_VERSION = "v237"
GRAPH_FILE = FALSI_DIR / "nipada_v219_graph_v13.json"

BASE_SBE01 = "https://www.sacred-texts.com/hin/sbe01/"
BASE_SBE15 = "https://www.sacred-texts.com/hin/sbe15/"

# ---------------------------------------------------------------------------
# Per-upanishad chapter file lists (corrects the §212f volume-collision bug)
# ---------------------------------------------------------------------------

# SBE01: Chandogya Upanishad — Prapāthakas I–VIII (154 chapter pages)
CHANDOGYA_CHAPTERS = [f"sbe01{i:03d}.htm" for i in range(22, 176)]

# SBE01: Kena (Talavakara) Upanishad — 4 Khandas
KENA_CHAPTERS = [f"sbe01{i:03d}.htm" for i in range(176, 180)]

# SBE01: Aitareya Aranyaka (contains Aitareya Upanishad) — Adhyāyas I–III
AITAREYA_CHAPTERS = [f"sbe01{i:03d}.htm" for i in range(180, 239)]

# SBE01: Kausitaki Brahmana Upanishad — Adhyāyas I–IV
KAUSITAKI_CHAPTERS = [f"sbe01{i:03d}.htm" for i in range(239, 243)]

# SBE01: Isa (Vagasaneyi-Samhita) Upanishad — single page
ISA_CHAPTERS = ["sbe01243.htm"]

# SBE15: Katha Upanishad — 2 Adhyāyas × 3 Vallis (I,1–I,3 / II,4–II,6)
KATHA_CHAPTERS = [f"sbe15{i:03d}.htm" for i in range(10, 16)]

# SBE15: Mundaka Upanishad — 3 Mundakas × 2 Khandas
MUNDAKA_CHAPTERS = [f"sbe15{i:03d}.htm" for i in range(16, 22)]

# SBE15: Taittiriya Upanishad — 3 Vallīs × many Anuvākas
TAITTIRIYA_CHAPTERS = [f"sbe15{i:03d}.htm" for i in range(22, 53)]

# SBE15: Brihadaranyaka Upanishad — 6 Adhyāyas (longest upanishad in the volume)
BRIHADARANYAKA_CHAPTERS = [f"sbe15{i:03d}.htm" for i in range(53, 100)]

# SBE15: Svetasvatara Upanishad — 6 Adhyāyas
SVETASVATARA_CHAPTERS = [f"sbe15{i:03d}.htm" for i in range(100, 106)]

# SBE15: Prashna Upanishad — 6 Questions
PRASHNA_CHAPTERS = [f"sbe15{i:03d}.htm" for i in range(106, 112)]

# SBE15: Maitri (Maitrayaniya) Upanishad — 7 Prapāthakas
MAITRI_CHAPTERS = [f"sbe15{i:03d}.htm" for i in range(112, 119)]

# Mandukya Upanishad — NOT in SBE01/SBE15.
# Use sacred-texts.com hin/upan/ (Hume 1921 translation), single page.
# The Mandukya is only 12 mantras (~600 words). We use the Hume translation
# from "Thirteen Principal Upanishads" (Oxford 1921), which is public domain.
MANDUKYA_URL = "https://www.sacred-texts.com/hin/upan/upan09.htm"

# ---------------------------------------------------------------------------
# Works catalog
# ---------------------------------------------------------------------------

WORKS_CATALOG = [
    # ---- SBE01 group -------------------------------------------------------
    {
        "graph_node_id": "chandogya_upanishad",
        "title_en": "Chandogya Upanishad",
        "title_original": "छान्दोग्योपनिषद्",
        "source_volumes": "SBE01",
        "tradition_label": "INDIAN_AXIAL",
        "tradition_micro": "VEDANTA",
        "language_original": "san",
        "author": "F. Max Müller (tr.)",
        "year": 1879,
        "base_urls": [BASE_SBE01],
        "chapter_files": {BASE_SBE01: CHANDOGYA_CHAPTERS},
        "tags": ["upanishad", "vedanta", "atman", "brahman", "sbe01", "muller"],
    },
    {
        "graph_node_id": "kena_upanishad",
        "title_en": "Kena Upanishad",
        "title_original": "केनोपनिषद्",
        "source_volumes": "SBE01",
        "tradition_label": "INDIAN_AXIAL",
        "tradition_micro": "VEDANTA",
        "language_original": "san",
        "author": "F. Max Müller (tr.)",
        "year": 1879,
        "base_urls": [BASE_SBE01],
        "chapter_files": {BASE_SBE01: KENA_CHAPTERS},
        "tags": ["upanishad", "vedanta", "kena", "sbe01", "muller"],
    },
    {
        "graph_node_id": "aitareya_upanishad",
        "title_en": "Aitareya Upanishad",
        "title_original": "ऐतरेयोपनिषद्",
        "source_volumes": "SBE01",
        "tradition_label": "INDIAN_AXIAL",
        "tradition_micro": "VEDANTA",
        "language_original": "san",
        "author": "F. Max Müller (tr.)",
        "year": 1879,
        "base_urls": [BASE_SBE01],
        "chapter_files": {BASE_SBE01: AITAREYA_CHAPTERS},
        "tags": ["upanishad", "vedanta", "atman", "sbe01", "muller"],
    },
    {
        "graph_node_id": "kausitaki_upanishad",
        "title_en": "Kausitaki Upanishad",
        "title_original": "कौषीतकि-उपनिषद्",
        "source_volumes": "SBE01",
        "tradition_label": "INDIAN_AXIAL",
        "tradition_micro": "VEDANTA",
        "language_original": "san",
        "author": "F. Max Müller (tr.)",
        "year": 1879,
        "base_urls": [BASE_SBE01],
        "chapter_files": {BASE_SBE01: KAUSITAKI_CHAPTERS},
        "tags": ["upanishad", "vedanta", "brahman", "sbe01", "muller"],
    },
    {
        "graph_node_id": "isa_upanishad",
        "title_en": "Isa Upanishad",
        "title_original": "ईशोपनिषद्",
        "source_volumes": "SBE01",
        "tradition_label": "INDIAN_AXIAL",
        "tradition_micro": "VEDANTA",
        "language_original": "san",
        "author": "F. Max Müller (tr.)",
        "year": 1879,
        "base_urls": [BASE_SBE01],
        "chapter_files": {BASE_SBE01: ISA_CHAPTERS},
        "tags": ["upanishad", "vedanta", "ishvara", "sbe01", "muller"],
    },
    # ---- SBE15 group -------------------------------------------------------
    {
        "graph_node_id": "katha_upanishad",
        "title_en": "Katha Upanishad",
        "title_original": "कठोपनिषद्",
        "source_volumes": "SBE15",
        "tradition_label": "INDIAN_AXIAL",
        "tradition_micro": "VEDANTA",
        "language_original": "san",
        "author": "F. Max Müller (tr.)",
        "year": 1884,
        "base_urls": [BASE_SBE15],
        "chapter_files": {BASE_SBE15: KATHA_CHAPTERS},
        "tags": ["upanishad", "vedanta", "death", "atman", "sbe15", "muller"],
    },
    {
        "graph_node_id": "mundaka_upanishad",
        "title_en": "Mundaka Upanishad",
        "title_original": "मुण्डकोपनिषद्",
        "source_volumes": "SBE15",
        "tradition_label": "INDIAN_AXIAL",
        "tradition_micro": "VEDANTA",
        "language_original": "san",
        "author": "F. Max Müller (tr.)",
        "year": 1884,
        "base_urls": [BASE_SBE15],
        "chapter_files": {BASE_SBE15: MUNDAKA_CHAPTERS},
        "tags": ["upanishad", "vedanta", "brahman", "sbe15", "muller"],
    },
    {
        "graph_node_id": "taittiriya_upanishad",
        "title_en": "Taittiriya Upanishad",
        "title_original": "तैत्तिरीयोपनिषद्",
        "source_volumes": "SBE15",
        "tradition_label": "INDIAN_AXIAL",
        "tradition_micro": "VEDANTA",
        "language_original": "san",
        "author": "F. Max Müller (tr.)",
        "year": 1884,
        "base_urls": [BASE_SBE15],
        "chapter_files": {BASE_SBE15: TAITTIRIYA_CHAPTERS},
        "tags": ["upanishad", "vedanta", "ananda", "sbe15", "muller"],
    },
    {
        "graph_node_id": "brihadaranyaka_upanishad",
        "title_en": "Brihadaranyaka Upanishad",
        "title_original": "बृहदारण्यकोपनिषद्",
        "source_volumes": "SBE15",
        "tradition_label": "INDIAN_AXIAL",
        "tradition_micro": "VEDANTA",
        "language_original": "san",
        "author": "F. Max Müller (tr.)",
        "year": 1884,
        "base_urls": [BASE_SBE15],
        "chapter_files": {BASE_SBE15: BRIHADARANYAKA_CHAPTERS},
        "tags": ["upanishad", "vedanta", "atman", "brahman", "sbe15", "muller"],
    },
    {
        "graph_node_id": "svetasvatara_upanishad",
        "title_en": "Svetasvatara Upanishad",
        "title_original": "श्वेताश्वतरोपनिषद्",
        "source_volumes": "SBE15",
        "tradition_label": "INDIAN_AXIAL",
        "tradition_micro": "VEDANTA",
        "language_original": "san",
        "author": "F. Max Müller (tr.)",
        "year": 1884,
        "base_urls": [BASE_SBE15],
        "chapter_files": {BASE_SBE15: SVETASVATARA_CHAPTERS},
        "tags": ["upanishad", "vedanta", "shiva", "sbe15", "muller"],
    },
    {
        "graph_node_id": "prashna_upanishad",
        "title_en": "Prashna Upanishad",
        "title_original": "प्रश्नोपनिषद्",
        "source_volumes": "SBE15",
        "tradition_label": "INDIAN_AXIAL",
        "tradition_micro": "VEDANTA",
        "language_original": "san",
        "author": "F. Max Müller (tr.)",
        "year": 1884,
        "base_urls": [BASE_SBE15],
        "chapter_files": {BASE_SBE15: PRASHNA_CHAPTERS},
        "tags": ["upanishad", "vedanta", "prana", "sbe15", "muller"],
    },
    {
        "graph_node_id": "maitri_upanishad",
        "title_en": "Maitri Upanishad",
        "title_original": "मैत्री उपनिषद्",
        "source_volumes": "SBE15",
        "tradition_label": "INDIAN_AXIAL",
        "tradition_micro": "VEDANTA",
        "language_original": "san",
        "author": "F. Max Müller (tr.)",
        "year": 1884,
        "base_urls": [BASE_SBE15],
        "chapter_files": {BASE_SBE15: MAITRI_CHAPTERS},
        "tags": ["upanishad", "vedanta", "moksha", "sbe15", "muller"],
    },
    # ---- Mandukya: separate source (not in SBE01/SBE15) -------------------
    {
        "graph_node_id": "mandukya_upanishad",
        "title_en": "Mandukya Upanishad",
        "title_original": "माण्डूक्योपनिषद्",
        "source_volumes": "HUME1921",
        "tradition_label": "INDIAN_AXIAL",
        "tradition_micro": "VEDANTA",
        "language_original": "san",
        "author": "R.E. Hume (tr.)",
        "year": 1921,
        "base_urls": [MANDUKYA_URL],
        "chapter_files": {MANDUKYA_URL: [""]},  # direct page (no sub-files)
        "tags": ["upanishad", "vedanta", "om", "turiya", "hume"],
        "_direct_url": MANDUKYA_URL,  # single-page override
    },
]

# ---------------------------------------------------------------------------
# Graph loader
# ---------------------------------------------------------------------------

def _load_graph_nodes() -> dict:
    if not GRAPH_FILE.exists():
        print(f"WARNING: graph file not found at {GRAPH_FILE}")
        return {}
    with open(GRAPH_FILE, encoding="utf-8") as f:
        g = json.load(f)
    return g.get("nodes", {})


# ---------------------------------------------------------------------------
# Chapter fetcher
# ---------------------------------------------------------------------------

def _fetch_chapters(work: dict, dry_run: bool = False) -> Optional[str]:
    """
    Fetch all chapter pages for a work and concatenate their text.
    Each chapter is individually cached in CACHE_SACRED_TEXTS.

    Returns full concatenated text, or None on failure.
    """
    work_id = work["graph_node_id"]
    full_cache = CACHE_SACRED_TEXTS / f"v237_{work_id}.txt"

    if full_cache.exists():
        text = full_cache.read_text(encoding="utf-8")
        print(f"  [cache] {work_id}: {len(text):,} bytes from {full_cache.name}")
        return text

    # Special case: Mandukya is a direct single-URL page
    if "_direct_url" in work:
        direct_url = work["_direct_url"]
        chap_cache = CACHE_SACRED_TEXTS / f"v237_{work_id}_direct.txt"
        if chap_cache.exists():
            text = chap_cache.read_text(encoding="utf-8")
        else:
            print(f"  [fetch] {direct_url}")
            r = _get(direct_url)
            time.sleep(REQUEST_DELAY)
            if r is None or r.status_code != 200:
                print(f"  [FAIL] {direct_url} → {r.status_code if r else 'None'}")
                return None
            text = _extract_text_from_html(r.text)
            if len(text) < 50:
                print(f"  [FAIL] {work_id}: page too short ({len(text)} chars)")
                return None
            chap_cache.write_text(text, encoding="utf-8")
            print(f"  [ok] {work_id}: {len(text)} chars")
        if not dry_run:
            full_cache.write_text(text, encoding="utf-8")
        return text

    # Normal case: iterate over chapter files
    all_parts = []

    for base_url, chapter_files in work["chapter_files"].items():
        target_chapters = chapter_files[:2] if dry_run else chapter_files
        for chap_file in target_chapters:
            url = base_url + chap_file
            chap_cache = CACHE_SACRED_TEXTS / f"v237_{work_id}_{chap_file}"

            if chap_cache.exists():
                chap_text = chap_cache.read_text(encoding="utf-8")
            else:
                print(f"    [fetch] {url}")
                r = _get(url)
                time.sleep(REQUEST_DELAY)
                if r is None or r.status_code != 200:
                    print(f"    [FAIL] {url} → {r.status_code if r else 'None'}")
                    continue
                chap_text = _extract_text_from_html(r.text)
                if len(chap_text) < 50:
                    print(f"    [skip] {chap_file}: too short ({len(chap_text)} chars)")
                    continue
                chap_cache.write_text(chap_text, encoding="utf-8")

            all_parts.append(chap_text)

    if not all_parts:
        print(f"  [ERROR] No text extracted for {work_id}")
        return None

    full_text = " ".join(all_parts)
    if not dry_run:
        full_cache.write_text(full_text, encoding="utf-8")
        print(f"  [saved] {work_id}: {len(full_text):,} chars ({len(all_parts)} chapters)")
    else:
        print(f"  [dry-run] {work_id}: {len(full_text):,} chars ({len(all_parts)} chapters, not saved)")

    return full_text


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="§237 Upanishads corpus fetcher (SBE01+SBE15, collision fix)")
    parser.add_argument("--dry-run", action="store_true", help="Fetch 2 chapters per work only, no writes")
    args = parser.parse_args()

    nodes = _load_graph_nodes()
    print(f"Graph v13: {len(nodes)} nodes loaded")

    signed_works = []
    report_entries = []

    for work in WORKS_CATALOG:
        work_id = work["graph_node_id"]
        print(f"\n=== {work_id} ({work['title_en']}) ===")

        if work_id not in nodes:
            print(f"  [WARNING] {work_id} not found in graph v13 — signing anyway")
        else:
            node = nodes[work_id]
            print(f"  Graph node: {node.get('title_en', '?')} [{node.get('ingestion_status', '?')}]")

        n_chapters = sum(len(v) for v in work["chapter_files"].values())
        print(f"  Chapters to fetch: {n_chapters}")

        full_text = _fetch_chapters(work, dry_run=args.dry_run)
        if full_text is None:
            report_entries.append({
                "work_id": work_id,
                "status": "FAILED",
                "reason": "no_text_extracted",
            })
            continue

        sig = freq_signature(full_text, lang="eng")
        top3 = sorted(sig.items(), key=lambda x: -x[1])[:3]

        record = {
            "graph_node_id": work_id,
            "title_en": work["title_en"],
            "title_original": work["title_original"],
            "tradition_label": work["tradition_label"],
            "tradition_micro": work["tradition_micro"],
            "language_original": work["language_original"],
            "author": work["author"],
            "year": work["year"],
            "source_volumes": work["source_volumes"],
            "tags": work["tags"],
            "v14_signature": sig,
            "signed_n_chars": len(full_text),
            "n_chapters_fetched": n_chapters,
            "ingestion_status": "dry_run" if args.dry_run else "signed",
            "script_version": SCRIPT_VERSION,
            "signed_at": datetime.now(timezone.utc).isoformat(),
        }
        signed_works.append(record)

        print(f"  V14 top-3: {', '.join(f'{a}={v:.3f}' for a, v in top3)}")
        print(f"  Signed: {len(full_text):,} chars")

        report_entries.append({
            "work_id": work_id,
            "status": "signed",
            "signed_n_chars": len(full_text),
            "top3_atoms": {a: round(v, 4) for a, v in top3},
        })

    # ---- Output ------------------------------------------------------------
    if not args.dry_run:
        out_corpus = CORPUS_DIR / "signed_corpus_v237_upanishads.json"
        corpus_envelope = {
            "version": SCRIPT_VERSION,
            "description": (
                "§237 Indian Upanishads — per-chapter fix for §212f volume-collision bug. "
                "SBE01 (Müller 1879): chandogya, kena, aitareya, kausitaki, isa. "
                "SBE15 (Müller 1884): katha, mundaka, taittiriya, brihadaranyaka, "
                "svetasvatara, prashna, maitri. Mandukya: Hume 1921."
            ),
            "lexicon_version": "v212f_lexicon",
            "fixes": "§212f_sbe01_sbe15_volume_collision",
            "n_signed": len(signed_works),
            "v14_atoms": V14_ATOMS,
            "signed": signed_works,
        }
        with open(out_corpus, "w", encoding="utf-8") as f:
            json.dump(corpus_envelope, f, ensure_ascii=False, indent=2)
        print(f"\nCorpus saved: {out_corpus} ({len(signed_works)} works)")

        out_report = FALSI_DIR / "nipada_v237_fetch_report.json"
        with open(out_report, "w", encoding="utf-8") as f:
            json.dump({
                "script": "nipada_fetch_corpus_v237_upanishads.py",
                "version": SCRIPT_VERSION,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "n_signed": len(signed_works),
                "bug_fixed": "§212f volume-collision: 13 upanishads reduced from 2 to 13 distinct V14 points",
                "entries": report_entries,
            }, f, ensure_ascii=False, indent=2)
        print(f"Report saved: {out_report}")
    else:
        print(f"\n[dry-run] {len(signed_works)} works would be signed (outputs not written)")
        for r in report_entries:
            status = r.get("status", "?")
            chars = r.get("signed_n_chars", 0)
            top3 = r.get("top3_atoms", {})
            print(f"  {r['work_id']:45s} {status}  {chars:8,} chars  {top3}")


if __name__ == "__main__":
    main()
