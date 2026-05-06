#!/usr/bin/env python3
"""
§263-patch: Deduplicate 27 corpus entries with identical v14_signatures.

NIPADA v0.4.0-α — Panini Research
Date: 2026-05-07

Problem (§212f volume-collision bug, 10 groups):
  The v212f fetcher used volume-level index URLs, causing multiple distinct
  texts within the same SBE volume to receive identical concatenated text
  → identical V14 signatures.

  Groups fixed here:
  1. SBE08: bhagavad_gita / anugita
  2. SBE02: apastamba_dharmasutra / gautama_dharmasutra
  3. SBE14: baudhayana_dharmasutra / vasistha_dharmasutra
  4. SBE22: acaranga_sutra / kalpa_sutra_jaina
  5. SBE45: uttaradhyayana_sutra / sutrakrtanga
  6. SBE30: hiranyakesi_grhya_sutra / apastamba_grhya_sutra
  7. SBE29: paraskara_grhya_sutra / sankhayana_grhya_sutra / asvalayana_grhya_sutra
  8. ICH:   yijing / daxiang_zhuan / xugua_zhuan / xicizhuan / zaguazhuan
  9. SBE03: shujing / shijing / xiaojing
 10. SBE39: daodejing / zhuangzi / yangsheng_zhu / qiwulun

Fix: per-text chapter file lists, fetched from correct SBE section pages.

Input:  nipada/corpus/signed_corpus_v260_fusion.json
Output: nipada/corpus/signed_corpus_v263_clean.json
        nipada/falsification/nipada_v263_deduplicate_report.json

Usage:
  python3 nipada_patch_v263_deduplicate.py [--dry-run]
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

SCRIPT_VERSION = "v263"
INPUT_CORPUS = CORPUS_DIR / "signed_corpus_v260_fusion.json"
OUTPUT_CORPUS = CORPUS_DIR / "signed_corpus_v263_clean.json"
OUTPUT_REPORT = FALSI_DIR / "nipada_v263_deduplicate_report.json"

# ---------------------------------------------------------------------------
# Chapter-range mappings (determined from volume index pages)
# ---------------------------------------------------------------------------

# == SBE08: Bhagavad Gita + Sanatsugâtîya + Anugita =======================
BASE_SBE08 = "https://www.sacred-texts.com/hin/sbe08/"
# Bhagavad Gita: intro (sbe0802) + 18 chapters (sbe0803–sbe0820)
BHAGAVAD_GITA_CHAPTERS = [f"sbe08{i:02d}.htm" for i in range(2, 21)]
# Anugita: intro (sbe0827) + 36 chapters (sbe0828–sbe0863)
ANUGITA_CHAPTERS = [f"sbe08{i:02d}.htm" for i in range(27, 64)]

# == SBE02: Apastamba + Gautama Dharmasutras ================================
BASE_SBE02 = "https://www.sacred-texts.com/hin/sbe02/"
# Apastamba: intro (sbe0202) + Prasnas I-II khandas (sbe0204–sbe0264)
APASTAMBA_DHARMASUTRA_CHAPTERS = (
    ["sbe0202.htm"]
    + [f"sbe02{i:02d}.htm" for i in range(4, 65)]
)
# Gautama: intro (sbe0203) + Chapters I-XXVIII (sbe0265–sbe0292)
GAUTAMA_DHARMASUTRA_CHAPTERS = (
    ["sbe0203.htm"]
    + [f"sbe02{i:02d}.htm" for i in range(65, 93)]
)

# == SBE14: Vasistha + Baudhayana Dharmasutras ==============================
BASE_SBE14 = "https://www.sacred-texts.com/hin/sbe14/"
# Vasistha: intro (sbe1402) + Chapters I-XXX (sbe1404–sbe1433)
VASISTHA_DHARMASUTRA_CHAPTERS = (
    ["sbe1402.htm"]
    + [f"sbe14{i:02d}.htm" for i in range(4, 34)]
)
# Baudhayana: intro (sbe1403) + Prasnas I-IV (sbe1434–sbe1491)
BAUDHAYANA_DHARMASUTRA_CHAPTERS = (
    ["sbe1403.htm"]
    + [f"sbe14{i:02d}.htm" for i in range(34, 92)]
)

# == SBE22: Acaranga Sutra + Kalpa Sutra ====================================
BASE_SBE22 = "https://www.sacred-texts.com/jai/sbe22/"
# Acaranga: intro (sbe2202) + Books I-II (sbe2203–sbe2280)
ACARANGA_SUTRA_CHAPTERS = (
    ["sbe2202.htm"]
    + [f"sbe22{i:02d}.htm" for i in range(3, 81)]
)
# Kalpa Sutra: Life of Mahavira + Lives of Parsva/Arishtanemi/Rishabha
#              + Sthaviravali + Rules for Yatis (sbe2281–sbe2291)
KALPA_SUTRA_CHAPTERS = [f"sbe22{i:02d}.htm" for i in range(81, 92)]

# == SBE45: Uttaradhyayana Sutra + Sutrakrtanga ============================
BASE_SBE45 = "https://www.sacred-texts.com/jai/sbe45/"
# Uttaradhyayana: intro (sbe4502) + 36 Lectures (sbe4503–sbe4538)
UTTARADHYAYANA_CHAPTERS = (
    ["sbe4502.htm"]
    + [f"sbe45{i:02d}.htm" for i in range(3, 39)]
)
# Sutrakrtanga: Books 1-2 (sbe4539–sbe4571)
SUTRAKRTANGA_CHAPTERS = [f"sbe45{i:02d}.htm" for i in range(39, 72)]

# == SBE30: Hiranyakesi + Apastamba Grihyasutras ===========================
BASE_SBE30 = "https://www.sacred-texts.com/hin/sbe30/"
# Hiranyakesi: intro (sbe30002, sbe30003) + Sections I-IV (sbe30004–sbe30042)
HIRANYAKESI_CHAPTERS = (
    ["sbe30002.htm", "sbe30003.htm"]
    + [f"sbe30{i:03d}.htm" for i in range(4, 43)]
)
# Apastamba: intro (sbe30043) + Sections I-II (sbe30044–sbe30116)
APASTAMBA_GRHYA_CHAPTERS = (
    ["sbe30043.htm"]
    + [f"sbe30{i:03d}.htm" for i in range(44, 117)]
)

# == SBE29: Sankhayana + Asvalayana + Paraskara Grihyasutras ===============
BASE_SBE29 = "https://www.sacred-texts.com/hin/sbe29/"
# Sankhayana: intro (sbe29002) + Sections I-VI (sbe29003–sbe29098)
SANKHAYANA_CHAPTERS = (
    ["sbe29002.htm"]
    + [f"sbe29{i:03d}.htm" for i in range(3, 99)]
)
# Asvalayana: intro (sbe29099) + Sections I-IV (sbe29100–sbe29153)
ASVALAYANA_CHAPTERS = (
    ["sbe29099.htm"]
    + [f"sbe29{i:03d}.htm" for i in range(100, 154)]
)
# Paraskara: intro (sbe29154) + Sections I-III (sbe29155–sbe29206)
PARASKARA_CHAPTERS = (
    ["sbe29154.htm"]
    + [f"sbe29{i:03d}.htm" for i in range(155, 207)]
)

# == ICH: I Ching + Ten Wings (Appendices) ==================================
BASE_ICH = "https://www.sacred-texts.com/ich/"
# Yijing: 64 hexagrams (ic01–ic64)
YIJING_CHAPTERS = [f"ic{i:02d}.htm" for i in range(1, 65)]
# Daxiang Zhuan (Commentary on the Images, Appendix II)
DAXIANG_ZHUAN_CHAPTERS = ["icap2-1.htm", "icap2-2.htm"]
# Xugua Zhuan (Sequence of Hexagrams, Appendix VI)
XUGUA_ZHUAN_CHAPTERS = ["icap6.htm"]
# Xicizhuan (Great Appendix / Xi Ci Zhuan, Appendix III)
XICIZHUAN_CHAPTERS = ["icap3-1.htm", "icap3-2.htm"]
# Zaguazhuan (Miscellaneous Hexagrams, Appendix VII)
ZAGUAZHUAN_CHAPTERS = ["icap7.htm"]

# == SBE03: Shujing + Shijing + Xiaojing ===================================
BASE_SBE03 = "https://www.sacred-texts.com/cfu/sbe03/"
# Shujing (Shu King / Book of History): Canon of Yao through Speech of Qin
SHUJING_CHAPTERS = (
    ["sbe03004.htm", "sbe03005.htm", "sbe03006.htm", "sbe03007.htm"]  # intro
    + [f"sbe03{i:03d}.htm" for i in range(8, 58)]                     # content
)
# Shijing (She King / Book of Songs): title + intro chapters + odes
SHIJING_CHAPTERS = (
    ["shih00.htm"]
    + [f"sbe03{i:03d}.htm" for i in range(59, 176)]
)
# Xiaojing (Hsiao King / Classic of Filial Piety): title + chapters
XIAOJING_CHAPTERS = (
    ["hsiao.htm"]
    + [f"sbe03{i:03d}.htm" for i in range(177, 199)]
)

# == SBE39: Daodejing + Zhuangzi (Books I-XXXIII) ==========================
BASE_SBE39 = "https://www.sacred-texts.com/tao/sbe39/"
# Daodejing (Tao Te Ching): 81 chapters
DAODEJING_CHAPTERS = [f"sbe39{i:03d}.htm" for i in range(8, 89)]
# Zhuangzi: Books I-XXXIII (concise + detailed translation pages)
ZHUANGZI_CHAPTERS = (
    [f"sbe39{i:03d}.htm" for i in range(89, 122)]   # Books I-XXXIII (concise)
    + [f"sbe39{i:03d}.htm" for i in range(122, 139)]  # Books I-XVII (detailed)
)
# Qiwulun (Book II: Khî Wû Lun — On the Adjustment of Controversies)
QIWULUN_CHAPTERS = ["sbe39090.htm", "sbe39123.htm"]
# Yangsheng Zhu (Book III: Yang Shang Kû — Nourishing the Lord of Life)
YANGSHENG_ZHU_CHAPTERS = ["sbe39091.htm", "sbe39124.htm"]

# ---------------------------------------------------------------------------
# Works catalog: per-text fetch specification for all 27 duplicate entries
# ---------------------------------------------------------------------------

WORKS_CATALOG = [
    # ---- SBE08 group -------------------------------------------------------
    {
        "local_id": "bhagavad_gita",
        "base_url": BASE_SBE08,
        "chapters": BHAGAVAD_GITA_CHAPTERS,
        "source_label": f"sacred-texts.com SBE08 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE08,
    },
    {
        "local_id": "anugita",
        "base_url": BASE_SBE08,
        "chapters": ANUGITA_CHAPTERS,
        "source_label": f"sacred-texts.com SBE08 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE08,
    },
    # ---- SBE02 group -------------------------------------------------------
    {
        "local_id": "apastamba_dharmasutra",
        "base_url": BASE_SBE02,
        "chapters": APASTAMBA_DHARMASUTRA_CHAPTERS,
        "source_label": f"sacred-texts.com SBE02 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE02,
    },
    {
        "local_id": "gautama_dharmasutra",
        "base_url": BASE_SBE02,
        "chapters": GAUTAMA_DHARMASUTRA_CHAPTERS,
        "source_label": f"sacred-texts.com SBE02 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE02,
    },
    # ---- SBE14 group -------------------------------------------------------
    {
        "local_id": "vasistha_dharmasutra",
        "base_url": BASE_SBE14,
        "chapters": VASISTHA_DHARMASUTRA_CHAPTERS,
        "source_label": f"sacred-texts.com SBE14 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE14,
    },
    {
        "local_id": "baudhayana_dharmasutra",
        "base_url": BASE_SBE14,
        "chapters": BAUDHAYANA_DHARMASUTRA_CHAPTERS,
        "source_label": f"sacred-texts.com SBE14 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE14,
    },
    # ---- SBE22 group -------------------------------------------------------
    {
        "local_id": "acaranga_sutra",
        "base_url": BASE_SBE22,
        "chapters": ACARANGA_SUTRA_CHAPTERS,
        "source_label": f"sacred-texts.com SBE22 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE22,
    },
    {
        "local_id": "kalpa_sutra_jaina",
        "base_url": BASE_SBE22,
        "chapters": KALPA_SUTRA_CHAPTERS,
        "source_label": f"sacred-texts.com SBE22 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE22,
    },
    # ---- SBE45 group -------------------------------------------------------
    {
        "local_id": "uttaradhyayana_sutra",
        "base_url": BASE_SBE45,
        "chapters": UTTARADHYAYANA_CHAPTERS,
        "source_label": f"sacred-texts.com SBE45 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE45,
    },
    {
        "local_id": "sutrakrtanga",
        "base_url": BASE_SBE45,
        "chapters": SUTRAKRTANGA_CHAPTERS,
        "source_label": f"sacred-texts.com SBE45 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE45,
    },
    # ---- SBE30 group -------------------------------------------------------
    {
        "local_id": "hiranyakesi_grhya_sutra",
        "base_url": BASE_SBE30,
        "chapters": HIRANYAKESI_CHAPTERS,
        "source_label": f"sacred-texts.com SBE30 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE30,
    },
    {
        "local_id": "apastamba_grhya_sutra",
        "base_url": BASE_SBE30,
        "chapters": APASTAMBA_GRHYA_CHAPTERS,
        "source_label": f"sacred-texts.com SBE30 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE30,
    },
    # ---- SBE29 group -------------------------------------------------------
    {
        "local_id": "sankhayana_grhya_sutra",
        "base_url": BASE_SBE29,
        "chapters": SANKHAYANA_CHAPTERS,
        "source_label": f"sacred-texts.com SBE29 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE29,
    },
    {
        "local_id": "asvalayana_grhya_sutra",
        "base_url": BASE_SBE29,
        "chapters": ASVALAYANA_CHAPTERS,
        "source_label": f"sacred-texts.com SBE29 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE29,
    },
    {
        "local_id": "paraskara_grhya_sutra",
        "base_url": BASE_SBE29,
        "chapters": PARASKARA_CHAPTERS,
        "source_label": f"sacred-texts.com SBE29 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE29,
    },
    # ---- ICH group ---------------------------------------------------------
    {
        "local_id": "yijing",
        "base_url": BASE_ICH,
        "chapters": YIJING_CHAPTERS,
        "source_label": f"sacred-texts.com ICH (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_ICH,
    },
    {
        "local_id": "daxiang_zhuan",
        "base_url": BASE_ICH,
        "chapters": DAXIANG_ZHUAN_CHAPTERS,
        "source_label": f"sacred-texts.com ICH (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_ICH,
    },
    {
        "local_id": "xugua_zhuan",
        "base_url": BASE_ICH,
        "chapters": XUGUA_ZHUAN_CHAPTERS,
        "source_label": f"sacred-texts.com ICH (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_ICH,
    },
    {
        "local_id": "xicizhuan",
        "base_url": BASE_ICH,
        "chapters": XICIZHUAN_CHAPTERS,
        "source_label": f"sacred-texts.com ICH (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_ICH,
    },
    {
        "local_id": "zaguazhuan",
        "base_url": BASE_ICH,
        "chapters": ZAGUAZHUAN_CHAPTERS,
        "source_label": f"sacred-texts.com ICH (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_ICH,
    },
    # ---- SBE03 group -------------------------------------------------------
    {
        "local_id": "shujing",
        "base_url": BASE_SBE03,
        "chapters": SHUJING_CHAPTERS,
        "source_label": f"sacred-texts.com SBE03 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE03,
    },
    {
        "local_id": "shijing",
        "base_url": BASE_SBE03,
        "chapters": SHIJING_CHAPTERS,
        "source_label": f"sacred-texts.com SBE03 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE03,
    },
    {
        "local_id": "xiaojing",
        "base_url": BASE_SBE03,
        "chapters": XIAOJING_CHAPTERS,
        "source_label": f"sacred-texts.com SBE03 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE03,
    },
    # ---- SBE39 group -------------------------------------------------------
    {
        "local_id": "daodejing",
        "base_url": BASE_SBE39,
        "chapters": DAODEJING_CHAPTERS,
        "source_label": f"sacred-texts.com SBE39 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE39,
    },
    {
        "local_id": "zhuangzi",
        "base_url": BASE_SBE39,
        "chapters": ZHUANGZI_CHAPTERS,
        "source_label": f"sacred-texts.com SBE39 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE39,
    },
    {
        "local_id": "qiwulun",
        "base_url": BASE_SBE39,
        "chapters": QIWULUN_CHAPTERS,
        "source_label": f"sacred-texts.com SBE39 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE39,
    },
    {
        "local_id": "yangsheng_zhu",
        "base_url": BASE_SBE39,
        "chapters": YANGSHENG_ZHU_CHAPTERS,
        "source_label": f"sacred-texts.com SBE39 (§{SCRIPT_VERSION} per-text fix)",
        "url_canonical": BASE_SBE39,
    },
]


# ---------------------------------------------------------------------------
# Fetch helpers
# ---------------------------------------------------------------------------

def fetch_chapters(local_id: str, base_url: str, chapters: list[str],
                   dry_run: bool = False) -> Optional[str]:
    """Fetch and concatenate text from a list of chapter files.

    Caches the entire concatenated result for each local_id at:
      CACHE_SACRED_TEXTS / f'v263_{local_id}.txt'

    Returns the concatenated text or None if all chapters failed.
    """
    cache_file = CACHE_SACRED_TEXTS / f"v263_{local_id}.txt"

    # Return cached result if available
    if cache_file.exists() and not dry_run:
        text = cache_file.read_text(encoding="utf-8")
        print(f"  [cache] {local_id}: loaded {len(text)} chars from cache")
        return text

    all_parts = []
    fetched = 0
    skipped = 0

    for chapter_file in chapters:
        if dry_run:
            print(f"  [dry-run] would fetch {base_url}{chapter_file}")
            continue

        chapter_url = base_url + chapter_file

        try:
            r = _get(chapter_url)
        except Exception as exc:
            print(f"  [warn] failed to fetch {chapter_url}: {exc}")
            skipped += 1
            continue

        if r is None:
            print(f"  [warn] no response for {chapter_url}")
            skipped += 1
            continue

        if r.status_code != 200:
            print(f"  [warn] HTTP {r.status_code} for {chapter_url}")
            skipped += 1
            continue

        chapter_text = _extract_text_from_html(r.text)
        if len(chapter_text) > 50:
            all_parts.append(chapter_text)
            fetched += 1
        else:
            print(f"  [warn] very short text ({len(chapter_text)} chars) for {chapter_url}")
            skipped += 1

        time.sleep(REQUEST_DELAY)

    if not all_parts:
        return None

    combined = "\n\n".join(all_parts)
    # Save to cache
    cache_file.write_text(combined, encoding="utf-8")
    print(f"  [fetch] {local_id}: {fetched} chapters, {skipped} skipped, "
          f"{len(combined)} chars total → cached")
    return combined


def compute_v14_signature(text: str) -> dict:
    """Compute V14 signature from text using freq_signature()."""
    sig = freq_signature(text)
    # freq_signature returns a dict {atom: frequency_ratio}
    return sig


def top3(sig: dict) -> list:
    """Return top-3 atoms by frequency."""
    return sorted(sig.items(), key=lambda x: x[1], reverse=True)[:3]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="§263: Fix 27 duplicate signatures in signed_corpus_v260_fusion.json"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Fetch nothing, only list what would be fetched")
    args = parser.parse_args()

    # ---- Load input corpus -------------------------------------------------
    if not INPUT_CORPUS.exists():
        print(f"ERROR: input corpus not found: {INPUT_CORPUS}", file=sys.stderr)
        return 1

    with open(INPUT_CORPUS, encoding="utf-8") as f:
        corpus_data = json.load(f)

    signed = corpus_data["signed"]
    print(f"Loaded {len(signed)} entries from {INPUT_CORPUS.name}")

    # Build index by local_id (fallback to graph_node_id)
    entry_index = {}
    for e in signed:
        lid = e.get("local_id") or e.get("graph_node_id")
        if lid:
            entry_index[lid] = e

    # ---- Process each work -------------------------------------------------
    results = []
    patched = 0
    failed = 0

    for spec in WORKS_CATALOG:
        local_id = spec["local_id"]
        base_url = spec["base_url"]
        chapters = spec["chapters"]
        source_label = spec["source_label"]

        print(f"\n[{local_id}] fetching {len(chapters)} chapter(s) ...")

        if args.dry_run:
            for ch in chapters[:3]:
                print(f"  [dry-run] {base_url}{ch}")
            if len(chapters) > 3:
                print(f"  [dry-run] ... and {len(chapters)-3} more")
            results.append({"local_id": local_id, "status": "dry-run", "n_chapters": len(chapters)})
            continue

        text = fetch_chapters(local_id, base_url, chapters, dry_run=False)

        if not text:
            print(f"  [ERROR] no text fetched for {local_id}")
            results.append({"local_id": local_id, "status": "error", "reason": "no text"})
            failed += 1
            continue

        n_chars = len(text)
        n_words = len(text.split())

        # Compute new V14 signature
        sig = compute_v14_signature(text)
        t3 = [[atom, val] for atom, val in top3(sig)]

        print(f"  [sign] {local_id}: {n_chars} chars, top3={[x[0] for x in t3]}")

        # Update the corpus entry
        entry = entry_index.get(local_id)
        if entry is None:
            print(f"  [warn] entry '{local_id}' not found in corpus, skipping")
            results.append({"local_id": local_id, "status": "not_found"})
            failed += 1
            continue

        entry["n_chars"] = n_chars
        entry["n_words"] = n_words
        entry["v14_signature"] = sig
        entry["v14_top3"] = t3
        entry["matched"] = True
        entry["lexicon_version"] = "v14"
        entry["source"] = source_label
        entry["url"] = spec["url_canonical"]
        entry["url_original"] = spec["url_canonical"]

        results.append({
            "local_id": local_id,
            "status": "ok",
            "n_chars": n_chars,
            "n_words": n_words,
            "n_chapters": len(chapters),
            "top3": t3,
            "source": source_label,
        })
        patched += 1

    # ---- Verify deduplication ---------------------------------------------
    if not args.dry_run:
        from collections import defaultdict
        import hashlib

        def make_sig_hash(e):
            v14 = e.get("v14_signature")
            if not v14:
                return None
            vals = tuple(round(v14[k], 6) for k in sorted(v14.keys()))
            return hashlib.md5(str(vals).encode()).hexdigest()[:12]

        sig_groups = defaultdict(list)
        for e in signed:
            h = make_sig_hash(e)
            lid = e.get("local_id") or e.get("graph_node_id", "?")
            if h:
                sig_groups[h].append(lid)

        remaining_dups = {h: ids for h, ids in sig_groups.items() if len(ids) > 1}
        print(f"\nDeduplication check: {len(remaining_dups)} duplicate groups remain")
        for h, ids in remaining_dups.items():
            print(f"  STILL DUP: {ids}")

    # ---- Save output corpus -----------------------------------------------
    if not args.dry_run:
        corpus_data["metadata"] = corpus_data.get("metadata", {})
        corpus_data["metadata"]["version"] = "v263"
        corpus_data["metadata"]["generated_at"] = datetime.now(timezone.utc).isoformat()
        corpus_data["metadata"]["patch"] = (
            f"§{SCRIPT_VERSION}: fixed {patched}/27 duplicate v14_signatures"
        )

        with open(OUTPUT_CORPUS, "w", encoding="utf-8") as f:
            json.dump(corpus_data, f, ensure_ascii=False, indent=2)
        print(f"\nSaved patched corpus → {OUTPUT_CORPUS}")

    # ---- Save report -------------------------------------------------------
    report = {
        "script": f"nipada_patch_{SCRIPT_VERSION}_deduplicate.py",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "input_corpus": str(INPUT_CORPUS),
        "output_corpus": str(OUTPUT_CORPUS),
        "n_patched": patched,
        "n_failed": failed,
        "results": results,
    }

    FALSI_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Saved report → {OUTPUT_REPORT}")

    print(f"\nDone: {patched} patched, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
