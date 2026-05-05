#!/usr/bin/env python3
"""
§236-fetch: Chinese Classics from sacred-texts.com (SBE27 + SBE28).

NIPADA v0.4.0-α — Panini Research
Date: 2026-05-01
Author: §236

Goal: Sign 4 graph nodes from the Chinese Axial tradition:
  - liji      : Li Ji / Book of Rites (SBE27 vol.I + SBE28 vol.II)
  - daxue     : Da Xue / Great Learning (SBE28 Book XXXIX)
  - zhongyong : Zhong Yong / Doctrine of the Mean (SBE28 Book XXVIII)
  - yueji     : Yue Ji / Record of Music (SBE28 Book XVII)

Source:
  SBE27 Part I : https://www.sacred-texts.com/cfu/liki/   (liki01.htm..liki10.htm)
  SBE28 Part II: https://www.sacred-texts.com/cfu/liki2/  (liki211.htm..liki246.htm)

Translator: James Legge (1885), Sacred Books of the East vol. 27-28.
License: Public domain (pre-1928).

Output:
  nipada/corpus/signed_corpus_v236_chinese_classics.json
  nipada/falsification/nipada_v236_fetch_report.json

Usage:
  python3 nipada_fetch_corpus_v236_chinese_classics.py [--dry-run]
"""

import argparse
import json
import re
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

SCRIPT_VERSION = "v236"
GRAPH_FILE = FALSI_DIR / "nipada_v219_graph_v13.json"

BASE_LIKI1 = "https://www.sacred-texts.com/cfu/liki/"   # SBE27 (Books I-X)
BASE_LIKI2 = "https://www.sacred-texts.com/cfu/liki2/"  # SBE28 (Books XI-XLVI)

# Chapter files for SBE27 (liki/) — liki00 is front-matter/index, skip it
LIKI1_CHAPTERS = [f"liki{i:02d}.htm" for i in range(1, 11)]  # liki01..liki10

# Chapter files for SBE28 (liki2/) — liki200 is table of contents, skip it
LIKI2_CHAPTERS = [f"liki2{i:02d}.htm" for i in range(11, 47)]  # liki211..liki246

# Specific chapters for sub-works
DAXUE_CHAPTERS     = ["liki239.htm"]   # Book XXXIX
ZHONGYONG_CHAPTERS = ["liki228.htm"]   # Book XXVIII
YUEJI_CHAPTERS     = ["liki217.htm"]   # Book XVII

# Catalog of works to sign
WORKS_CATALOG = [
    {
        "graph_node_id": "liji",
        "title_en": "Li Ji – Book of Rites",
        "title_original": "禮記",
        "source_volumes": "SBE27+SBE28",
        "tradition_label": "CHINESE_AXIAL",
        "tradition_micro": "CONFUCIAN_RITUAL",
        "language_original": "zho",
        "author": "James Legge (tr.)",
        "year": 1885,
        "base_urls": [BASE_LIKI1, BASE_LIKI2],
        "chapter_files": {
            BASE_LIKI1: LIKI1_CHAPTERS,
            BASE_LIKI2: LIKI2_CHAPTERS,
        },
        "tags": ["confucianism", "ritual", "rites", "li", "sbe27", "sbe28", "legge"],
    },
    {
        "graph_node_id": "daxue",
        "title_en": "Da Xue – The Great Learning",
        "title_original": "大學",
        "source_volumes": "SBE28",
        "tradition_label": "CHINESE_AXIAL",
        "tradition_micro": "CONFUCIAN_FOUR_BOOKS",
        "language_original": "zho",
        "author": "James Legge (tr.)",
        "year": 1885,
        "base_urls": [BASE_LIKI2],
        "chapter_files": {
            BASE_LIKI2: DAXUE_CHAPTERS,
        },
        "tags": ["confucianism", "four_books", "learning", "sbe28", "legge"],
    },
    {
        "graph_node_id": "zhongyong",
        "title_en": "Zhong Yong – Doctrine of the Mean",
        "title_original": "中庸",
        "source_volumes": "SBE28",
        "tradition_label": "CHINESE_AXIAL",
        "tradition_micro": "CONFUCIAN_FOUR_BOOKS",
        "language_original": "zho",
        "author": "James Legge (tr.)",
        "year": 1885,
        "base_urls": [BASE_LIKI2],
        "chapter_files": {
            BASE_LIKI2: ZHONGYONG_CHAPTERS,
        },
        "tags": ["confucianism", "four_books", "equilibrium", "sbe28", "legge"],
    },
    {
        "graph_node_id": "yueji",
        "title_en": "Yue Ji – Record of Music",
        "title_original": "樂記",
        "source_volumes": "SBE28",
        "tradition_label": "CHINESE_AXIAL",
        "tradition_micro": "CONFUCIAN_RITUAL",
        "language_original": "zho",
        "author": "James Legge (tr.)",
        "year": 1885,
        "base_urls": [BASE_LIKI2],
        "chapter_files": {
            BASE_LIKI2: YUEJI_CHAPTERS,
        },
        "tags": ["confucianism", "ritual", "music", "sbe28", "legge"],
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
    Fetch all chapters for a work and concatenate their text.
    Chapters are cached in CACHE_SACRED_TEXTS / <work_id>_<chapter>.txt

    Returns full concatenated text, or None on failure.
    """
    work_id = work["graph_node_id"]
    cache_key = f"v236_{work_id}"
    full_cache = CACHE_SACRED_TEXTS / f"{cache_key}.txt"

    if full_cache.exists():
        print(f"  [cache] {work_id}: {full_cache.stat().st_size} bytes")
        return full_cache.read_text(encoding="utf-8")

    all_parts = []
    total_fetched = 0

    for base_url, chapter_files in work["chapter_files"].items():
        target_chapters = chapter_files[:1] if dry_run else chapter_files
        for chap_file in target_chapters:
            url = base_url + chap_file
            chap_cache = CACHE_SACRED_TEXTS / f"v236_{work_id}_{chap_file}"

            if chap_cache.exists():
                chap_text = chap_cache.read_text(encoding="utf-8")
                print(f"    [cache] {chap_file}: {len(chap_text)} chars")
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
                print(f"    [ok] {chap_file}: {len(chap_text)} chars")

            all_parts.append(chap_text)
            total_fetched += len(chap_text)

    if not all_parts:
        print(f"  [ERROR] No text extracted for {work_id}")
        return None

    full_text = " ".join(all_parts)
    if not dry_run:
        full_cache.write_text(full_text, encoding="utf-8")
        print(f"  [saved] {work_id}: {len(full_text)} chars total")
    else:
        print(f"  [dry-run] {work_id}: {len(full_text)} chars (from {len(all_parts)} chapters, not saved)")

    return full_text


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="§236 Chinese Classics corpus fetcher")
    parser.add_argument("--dry-run", action="store_true", help="Fetch 1 chapter per work only")
    args = parser.parse_args()

    nodes = _load_graph_nodes()
    print(f"Graph v13: {len(nodes)} nodes loaded")

    signed_works = []
    report_entries = []

    for work in WORKS_CATALOG:
        work_id = work["graph_node_id"]
        print(f"\n=== {work_id} ({work['title_en']}) ===")

        # Verify node in graph
        if work_id not in nodes:
            print(f"  [WARNING] {work_id} not found in graph v13 — will sign anyway")
        else:
            node = nodes[work_id]
            print(f"  Graph node: {node.get('title_en', '?')} [{node.get('ingestion_status', '?')}]")

        # Fetch text
        full_text = _fetch_chapters(work, dry_run=args.dry_run)
        if full_text is None:
            report_entries.append({
                "work_id": work_id,
                "status": "FAILED",
                "reason": "no_text_extracted",
            })
            continue

        # Compute V14 signature
        sig = freq_signature(full_text, lang="eng")
        signed_n_chars = len(full_text)

        # Build signed record
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
            "source_url": [b + c
                           for b, chaps in work["chapter_files"].items()
                           for c in chaps],
            "tags": work["tags"],
            "v14_signature": sig,
            "signed_n_chars": signed_n_chars,
            "ingestion_status": "dry_run" if args.dry_run else "signed",
            "script_version": SCRIPT_VERSION,
            "signed_at": datetime.now(timezone.utc).isoformat(),
        }
        signed_works.append(record)

        # Signature summary
        top3 = sorted(sig.items(), key=lambda x: -x[1])[:3]
        print(f"  V14 top-3: {', '.join(f'{a}={v:.3f}' for a, v in top3)}")
        print(f"  Signed: {signed_n_chars:,} chars")

        report_entries.append({
            "work_id": work_id,
            "status": "signed",
            "signed_n_chars": signed_n_chars,
            "top3_atoms": {a: round(v, 4) for a, v in top3},
        })

    # Write outputs (skip if dry-run)
    if not args.dry_run:
        out_corpus = CORPUS_DIR / "signed_corpus_v236_chinese_classics.json"
        corpus_envelope = {
            "version": SCRIPT_VERSION,
            "description": "§236 Chinese Classics: liji, daxue, zhongyong, yueji (SBE27+SBE28, Legge tr.)",
            "lexicon_version": "v212f_lexicon",
            "n_signed": len(signed_works),
            "v14_atoms": V14_ATOMS,
            "signed": signed_works,
        }
        with open(out_corpus, "w", encoding="utf-8") as f:
            json.dump(corpus_envelope, f, ensure_ascii=False, indent=2)
        print(f"\nCorpus saved: {out_corpus} ({len(signed_works)} works)")

        out_report = FALSI_DIR / "nipada_v236_fetch_report.json"
        report = {
            "script": "nipada_fetch_corpus_v236_chinese_classics.py",
            "version": SCRIPT_VERSION,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "n_signed": len(signed_works),
            "entries": report_entries,
        }
        with open(out_report, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"Report saved: {out_report}")
    else:
        print(f"\n[dry-run] {len(signed_works)} works would be signed (outputs not written)")
        for r in report_entries:
            print(f"  {r}")


if __name__ == "__main__":
    main()
