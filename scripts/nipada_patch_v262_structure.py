#!/usr/bin/env python3
"""
nipada_patch_v262_structure.py
Chantier #6 — Hierarchical structure for corpus fragments.

For each corpus entry, adds two things:

1. A 'structure' field describing the detected text hierarchy:
   - Gutenberg (pg_*.txt cache): format='gutenberg_paragraphs', with
     chapter and paragraph index tables.
   - SC / Sacred-Texts / others (flat cache): format='flat'.
   - No cache: structure=null.

2. Three new optional fields per fragment in 'fragments':
   - chapter_id  : id of the chapter this window starts in (str or null)
   - para_start  : first paragraph index (0-based) spanned by the window
   - para_end    : last paragraph index (0-based) spanned by the window

The 'fragments' list keys 'seq', 'n_words', 'hash' are left unchanged
(backward-compatible with nipada_restitution_score.py).

Output: corpus version upgraded; top-level key 'patch_v262_structure' added.

Usage:
  python3 nipada_patch_v262_structure.py [--dry-run]
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_RESEARCH = Path(__file__).resolve().parent.parent.parent / "Panini-Research"
CORPUS_JSON   = REPO_RESEARCH / "nipada/corpus/signed_corpus_v260_fusion.json"
CACHE_ROOT    = REPO_RESEARCH / "nipada/corpus/_cache"

FRAGMENT_WORDS = 500

# ---------------------------------------------------------------------------
# Same MANUAL_CACHE as the patch script — only Gutenberg entries matter here
# (pg_*.txt have real paragraph structure; others are flat)
# ---------------------------------------------------------------------------

MANUAL_CACHE = {
    # Gutenberg – Plato
    "plato_protagoras":              ["pg_1591.txt"],
    "plato_parmenides":              ["pg_1687.txt"],   # Burnet vol.II PG#1687

    # Gutenberg – Burnet (Early Greek Philosophy, separate file)
    "burnet_early_greek_philosophy": ["pg_31649.txt"],

    # Gutenberg – Epicurus (Diogenes Laertius X, Bailey)
    "epicurus_letters":              ["pg_32.txt"],

    # Gutenberg – Lucretius
    "lucretius_drn":                 ["pg_785.txt"],

    # Gutenberg – Sextus Empiricus (Against the Professors)
    "sextus_pyrrho":                 ["pg_sextus_pyrrho.txt"],

    # Gutenberg – Democritus (Presocratic anthology)
    "democritus_fragments":          ["pg_democritus.txt"],

    # Gutenberg – Spinoza
    "spinoza_ethica_complete":       ["pg_3800.txt"],
    "spinoza_ttp":                   ["pg_989.txt"],

    # Gutenberg – Hume
    "hume_enquiry":                  ["pg_9662.txt"],
    "hume_dialogues_nhr":            ["pg_4583.txt"],

    # Gutenberg – d'Holbach
    "holbach_systeme_en":            ["pg_8909.txt"],

    # Gutenberg – Paine
    "paine_age_of_reason":           ["pg_3743.txt"],

    # Gutenberg – Marx
    "marx_critique":                 ["pg_46423.txt"],

    # Gutenberg – Voltaire
    "voltaire_candide":              ["pg_4650.txt"],

    # Gutenberg – Ingersoll, Volney, Koran
    "ingersoll_works":               ["pg_38802.txt"],
    "volney_ruines":                 ["pg_27931.txt"],
    "koran_rodwell_en":              ["pg_16955.txt"],
}

# ---------------------------------------------------------------------------
# Chapter detection patterns (ordered by specificity, first match wins)
# ---------------------------------------------------------------------------

CHAPTER_PATTERNS = [
    # "CHAPTER I.", "CHAPTER 1.", "Chapter One"
    re.compile(
        r'^(CHAPTER|Chapter|BOOK|Book|PART|Part|SECTION|Section)'
        r'\s+([IVXLCDM]+\.?|\d+\.?|[A-Za-z]+)',
        re.MULTILINE,
    ),
    # Standalone roman numerals: "I.", "II.", "III."
    re.compile(r'^\s*(I{1,3}V?|V?I{0,3}|IX|XI|XII|XIII|XIV|XV|XVI|XVII|XVIII|XIX|XX)\.\s*$', re.MULTILINE),
    # "1. TITLE" at line start
    re.compile(r'^\s*\d+\.\s+[A-Z][A-Z\s]{3,}$', re.MULTILINE),
]

GUTENBERG_HEADER_END = re.compile(
    r'\*{3}\s*START OF THE PROJECT GUTENBERG[^\n]*\n', re.IGNORECASE
)
GUTENBERG_FOOTER_START = re.compile(
    r'\*{3}\s*END OF THE PROJECT GUTENBERG[^\n]*', re.IGNORECASE
)


def strip_gutenberg_boilerplate(text: str) -> str:
    """Remove PG header/footer boilerplate."""
    m = GUTENBERG_HEADER_END.search(text)
    if m:
        text = text[m.end():]
    m = GUTENBERG_FOOTER_START.search(text)
    if m:
        text = text[: m.start()]
    return text.lstrip("\ufeff").strip()


# ---------------------------------------------------------------------------
# Core: parse paragraph / chapter structure from plain text
# ---------------------------------------------------------------------------

def parse_structure(text: str, local_id: str) -> dict:
    """
    Parse paragraph and chapter structure from a Gutenberg plain-text file.

    Returns:
      {
        "format": "gutenberg_paragraphs",
        "n_paragraphs": <int>,
        "n_chapters": <int>,
        "chapters": [{"id": str, "title": str, "para_start": int, "para_end": int}, ...],
        "paragraphs": [{"id": int, "chapter_id": str|null, "n_words": int, "hash": str}, ...]
      }
    """
    text = strip_gutenberg_boilerplate(text)
    raw_paras = [p.strip() for p in text.split("\n\n")]
    paragraphs = [p for p in raw_paras if p]  # discard empty

    if not paragraphs:
        return {"format": "flat", "n_paragraphs": 0, "n_chapters": 0,
                "chapters": [], "paragraphs": []}

    # Detect chapter headings: paragraph that matches a chapter pattern
    # and is short (< 20 words) — avoids false positives in body text.
    def is_chapter_heading(para: str) -> bool:
        if len(para.split()) > 20:
            return False
        for pat in CHAPTER_PATTERNS:
            if pat.match(para):
                return True
        return False

    chapters = []
    para_chapter = {}      # para_index → chapter_id
    current_chapter = None
    chapter_seq = 0

    for i, para in enumerate(paragraphs):
        if is_chapter_heading(para):
            chapter_seq += 1
            cid = str(chapter_seq)
            chapters.append({
                "id": cid,
                "title": para.replace("\n", " ")[:120],
                "para_start": i,
                "para_end": None,   # filled below
            })
            current_chapter = cid

        para_chapter[i] = current_chapter

    # Fill para_end for each chapter
    for j, ch in enumerate(chapters):
        next_start = chapters[j + 1]["para_start"] if j + 1 < len(chapters) else len(paragraphs)
        ch["para_end"] = next_start - 1

    # Build paragraph records
    para_records = []
    for i, para in enumerate(paragraphs):
        words = para.split()
        h = hashlib.sha256(para.encode("utf-8")).hexdigest()
        para_records.append({
            "id": i,
            "chapter_id": para_chapter.get(i),
            "n_words": len(words),
            "hash": h,
        })

    return {
        "format": "gutenberg_paragraphs",
        "n_paragraphs": len(paragraphs),
        "n_chapters": len(chapters),
        "chapters": chapters,
        "paragraphs": para_records,
    }


# ---------------------------------------------------------------------------
# Fragment annotation: find which paragraphs each 500-word window spans
# ---------------------------------------------------------------------------

def annotate_fragments(fragments: list[dict], structure: dict) -> list[dict]:
    """
    Add chapter_id / para_start / para_end to each fragment.

    The mapping: accumulate word counts paragraph by paragraph and find
    which paragraphs fall within [window_start, window_end) word offsets.
    """
    if not fragments:
        return fragments

    fmt = structure.get("format", "flat")
    if fmt != "gutenberg_paragraphs":
        # Flat source — just add null fields
        return [
            {**frag, "chapter_id": None, "para_start": None, "para_end": None}
            for frag in fragments
        ]

    para_records = structure["paragraphs"]

    # Build cumulative word-offset table for paragraphs
    offsets = []   # (para_id, word_start, word_end)
    acc = 0
    for pr in para_records:
        offsets.append((pr["id"], acc, acc + pr["n_words"]))
        acc += pr["n_words"]
    total_words = acc

    annotated = []
    for frag in fragments:
        seq = frag["seq"]
        w_start = seq * FRAGMENT_WORDS
        w_end = min(w_start + frag["n_words"], total_words)

        # Find overlapping paragraphs
        overlapping = [
            (pid, pw0, pw1)
            for pid, pw0, pw1 in offsets
            if pw0 < w_end and pw1 > w_start
        ]

        if overlapping:
            first_pid = overlapping[0][0]
            last_pid  = overlapping[-1][0]
            chapter_id = para_records[first_pid]["chapter_id"]
        else:
            first_pid = last_pid = None
            chapter_id = None

        annotated.append({
            **frag,
            "chapter_id": chapter_id,
            "para_start":  first_pid,
            "para_end":    last_pid,
        })

    return annotated


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(dry_run: bool = False) -> None:
    print(f"Loading corpus: {CORPUS_JSON}")
    with open(CORPUS_JSON, encoding="utf-8") as fh:
        data = json.load(fh)

    corpus = data["signed"]
    print(f"  {len(corpus)} entries")

    # Build local_id → cache file list from MANUAL_CACHE
    pg_cache_map: dict[str, list[Path]] = {}
    for local_id, files in MANUAL_CACHE.items():
        paths = []
        for fname in files:
            p = CACHE_ROOT / fname
            if p.exists():
                paths.append(p)
        if paths:
            pg_cache_map[local_id] = paths

    stats = {"gutenberg": 0, "flat": 0, "null": 0, "frags_annotated": 0}

    for entry in corpus:
        local_id = entry.get("local_id") or entry.get("graph_node_id") or ""

        if local_id in pg_cache_map:
            # Gutenberg: read and concatenate cache files
            texts = []
            for p in pg_cache_map[local_id]:
                texts.append(p.read_text(encoding="utf-8", errors="replace"))
            full_text = "\n\n".join(texts)

            structure = parse_structure(full_text, local_id)
            entry["structure"] = structure

            if entry.get("fragments"):
                entry["fragments"] = annotate_fragments(entry["fragments"], structure)
                stats["frags_annotated"] += len(entry["fragments"])

            stats["gutenberg"] += 1
            print(
                f"  [gutenberg] {local_id:45} "
                f"{structure['n_paragraphs']:5} paras, "
                f"{structure['n_chapters']:3} chapitres"
            )

        elif entry.get("fragments") is not None:
            # Has fragments but not Gutenberg → flat source (SC, sacred-texts, MIT)
            entry["structure"] = {"format": "flat"}
            if entry.get("fragments"):
                entry["fragments"] = annotate_fragments(entry["fragments"], {"format": "flat"})
                stats["frags_annotated"] += len(entry["fragments"])
            stats["flat"] += 1

        else:
            # No fragments (the one null-fragment text)
            entry["structure"] = None
            stats["null"] += 1

    # Mark corpus version
    data["patch_v262_structure"] = {
        "applied": True,
        "gutenberg_texts": stats["gutenberg"],
        "flat_texts": stats["flat"],
        "fragments_annotated": stats["frags_annotated"],
        "description": (
            "Chantier #6: added 'structure' per entry (paragraph/chapter hierarchy "
            "for Gutenberg texts) and chapter_id/para_start/para_end per fragment."
        ),
    }

    if dry_run:
        print("\n[dry-run] No file written.")
        print(f"Stats: {stats}")
        # Spot-check: show first annotated Gutenberg entry
        for entry in corpus:
            if entry.get("structure", {}).get("format") == "gutenberg_paragraphs":
                frags = entry.get("fragments") or []
                print(f"\nSpot-check: {entry.get('local_id')}")
                print(f"  Structure chapters: {entry['structure']['n_chapters']}")
                print(f"  First 3 fragments:")
                for frag in frags[:3]:
                    print(f"    {frag}")
                break
        return

    out_path = CORPUS_JSON
    tmp_path = CORPUS_JSON.with_suffix(".tmp.json")
    with open(tmp_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    tmp_path.replace(out_path)

    print(f"\nWritten: {out_path}")
    print(f"Stats: {stats}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="Parse and annotate but do not write")
    args = parser.parse_args()
    main(dry_run=args.dry_run)
